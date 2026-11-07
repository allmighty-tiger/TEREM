#!/usr/bin/env python3
import os,sys,re,shutil
from datetime import datetime,timezone,timedelta
ROOT=os.getcwd()
cutoff_days=30
cutoff=datetime.now(timezone.utc)-timedelta(days=cutoff_days)
iso_ts=os.environ.get('ISO_TS') or datetime.now(timezone.utc).isoformat()
short_ts=os.environ.get('SHORT_TS') or datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%SZ')
agents_dir=os.path.join(ROOT,'.squad','agents')
report_lines=[]
processed=[]
skipped=[]
archived_files=[]
errors=[]
# helper parse date
date_re=re.compile(r'(\d{4}-\d{2}-\d{2}(?:[T ]\d{2}:\d{2}:\d{2}(?:Z|[+\-]\d{2}:?\d{2})?)?)')
header_re=re.compile(r'^(#{1,6})\s')
decision_marker_re=re.compile(r'^###')

def parse_date(s):
    s=s.strip()
    m=date_re.search(s)
    if not m:
        return None
    ds=m.group(1)
    try:
        if ds.endswith('Z'):
            ds=ds.replace('Z','+00:00')
        # handle date-only
        if re.fullmatch(r'\d{4}-\d{2}-\d{2}',ds):
            return datetime.fromisoformat(ds).replace(tzinfo=timezone.utc)
        return datetime.fromisoformat(ds)
    except Exception:
        return None


def process_agent(agent_path,agent_name):
    history_path=os.path.join(agent_path,'history.md')
    if not os.path.isfile(history_path):
        return None
    st=os.path.getsize(history_path)
    with open(history_path,'r',encoding='utf-8') as f:
        lines=f.readlines()
    # split into blocks starting at header lines or lines with date at start
    blocks=[]
    cur=[]
    cur_raw=''
    def start_new():
        nonlocal cur
        if cur:
            blocks.append(cur)
        cur=[]
    for line in lines:
        if header_re.match(line) or date_re.match(line):
            # start new block
            start_new()
            cur=[line]
        else:
            if not cur:
                cur=[line]
            else:
                cur.append(line)
    start_new()
    # determine which blocks are older than cutoff
    blocks_info=[]
    for b in blocks:
        text=''.join(b)
        # detect if block contains decision references
        has_decision_any = any(('decisions.md' in l or '.squad/decisions.md' in l or decision_marker_re.match(l)) for l in b)
        # find first date in block
        date=None
        for l in b:
            d=parse_date(l)
            if d:
                date=d
                break
        blocks_info.append({'lines':b,'date':date,'has_decision':has_decision_any})
    # find blocks older than cutoff
    old_blocks_idx=[i for i,bi in enumerate(blocks_info) if bi['date'] and bi['date']<cutoff]
    if not old_blocks_idx:
        # nothing to archive
        return {'skipped_reason':'no entries older than 30 days','size':st}
    # prepare archive path
    archive_path=os.path.join(agent_path,'history-archive.md')
    os.makedirs(os.path.dirname(archive_path),exist_ok=True)
    archived_count=0
    archived_blocks=[]
    # build new blocks for history.md
    new_blocks=[]
    placeholder_added_positions=[]
    for idx,bi in enumerate(blocks_info):
        if idx in old_blocks_idx:
            # split decision lines out
            decision_lines=[l for l in bi['lines'] if ('decisions.md' in l or '.squad/decisions.md' in l or decision_marker_re.match(l))]
            other_lines=[l for l in bi['lines'] if l not in decision_lines]
            if other_lines:
                # append to archive file
                with open(archive_path,'a',encoding='utf-8') as af:
                    af.write('\n')
                    af.write(''.join(other_lines))
                archived_count+=1
                archived_blocks.append(''.join(other_lines))
                # insert placeholder in place of moved section
                new_blocks.append([f"[Archived entries moved to history-archive.md on {iso_ts}]\n"])
                # keep decision lines in history
                if decision_lines:
                    new_blocks.append(decision_lines)
            else:
                # nothing to move, keep original block
                new_blocks.append(bi['lines'])
        else:
            new_blocks.append(bi['lines'])
    # write back history.md
    # condense consecutive placeholders into single placeholder
    out_lines=[]
    i=0
    while i < len(new_blocks):
        block=new_blocks[i]
        if len(block)==1 and block[0].startswith('[Archived entries moved'):
            # collapse subsequent placeholders
            j=i+1
            while j<len(new_blocks) and len(new_blocks[j])==1 and new_blocks[j][0].startswith('[Archived entries moved'):
                j+=1
            out_lines.append(new_blocks[i][0])
            i=j
        else:
            out_lines.extend(block)
            i+=1
    # summary section
    summary_lines=['\n## Summary of Archived Entries\n','\n']
    summary_lines.append(f"- Number of archived blocks: {archived_count}\n")
    # extract themes: first header or first non-empty line of each archived block
    themes=[]
    for b in archived_blocks[:10]:
        # find first header or line
        m=re.search(r'^#{1,6}\s*(.*)',b,flags=re.M)
        if m:
            themes.append(m.group(1).strip())
        else:
            # first non-empty
            for l in b.splitlines():
                if l.strip():
                    themes.append(l.strip()[:80])
                    break
    if themes:
        summary_lines.append('\n- Main themes/titles archived:\n')
        for t in themes:
            summary_lines.append(f"  - {t}\n")
    # now write history.md safely by backup
    backup_path=history_path+'.bak'
    shutil.copy2(history_path,backup_path)
    try:
        with open(history_path,'w',encoding='utf-8') as hf:
            hf.writelines(out_lines)
            hf.writelines(summary_lines)
    except Exception as e:
        # restore
        shutil.move(backup_path,history_path)
        raise
    # record processed
    return {'archived_count':archived_count,'archive_path':archive_path,'skipped_reason':None,'size':st}

# main loop
if not os.path.isdir(agents_dir):
    print('No .squad/agents directory; nothing to do')
    sys.exit(0)
for name in sorted(os.listdir(agents_dir)):
    ap=os.path.join(agents_dir,name)
    if not os.path.isdir(ap):
        continue
    try:
        res=process_agent(ap,name)
        if res is None:
            skipped.append((name,'no history.md'))
        elif res.get('skipped_reason'):
            skipped.append((name,res.get('skipped_reason')))
        else:
            processed.append((name,res.get('archive_path'),res.get('archived_count')))
    except Exception as e:
        errors.append((name,str(e)))
# create inbox report
inbox_dir=os.path.join(ROOT,'.squad','decisions','inbox')
os.makedirs(inbox_dir,exist_ok=True)
inbox_path=os.path.join(inbox_dir,f'kot-history-cleanup-{short_ts}.md')
with open(inbox_path,'w',encoding='utf-8') as inf:
    inf.write(f"ISO timestamp: {iso_ts}\n\n")
    inf.write('Agents processed:\n')
    for p in processed:
        inf.write(f"- {p[0]}: archived {p[2]} blocks -> {p[1]}\n")
    if skipped:
        inf.write('\nFiles skipped:\n')
        for s in skipped:
            inf.write(f"- {s[0]}: {s[1]}\n")
    if errors:
        inf.write('\nErrors:\n')
        for e in errors:
            inf.write(f"- {e[0]}: {e[1]}\n")
# create archive copy dir
cleanup_dir=os.path.join(ROOT,'.squad','archive','history-cleanups',iso_ts)
os.makedirs(cleanup_dir,exist_ok=True)
# copy archived history files and inbox into cleanup_dir preserving relative paths
for p in processed:
    rel=os.path.relpath(p[1],ROOT)
    dest=os.path.join(cleanup_dir,rel)
    os.makedirs(os.path.dirname(dest),exist_ok=True)
    shutil.copy2(p[1],dest)
# copy inbox
sh_inbox=os.path.join(cleanup_dir,'.squad','decisions','inbox')
os.makedirs(sh_inbox,exist_ok=True)
shutil.copy2(inbox_path,os.path.join(sh_inbox,os.path.basename(inbox_path)))
# print summary for caller
print('PROCESSED:'+str(len(processed)))
print('ARCHIVE_DIR:'+cleanup_dir)
print('INBOX:'+inbox_path)
if errors:
    print('ERRORS_PRESENT')
sys.exit(0)
