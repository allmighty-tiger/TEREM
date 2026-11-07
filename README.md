![TEREM operations chamber with eight agent emblems](.squad/assets/terem-operations-chamber.svg)

# TEREM — White-Box Security Agent Team

**White-Box Security Agent Team** · Built on **Squad v0.0.0-source** · Sink-first static analysis.

For quick team reference, see [TEAM.md](TEAM.md).

---

## What TEREM Provides

TEREM is an eight-agent team for **static white-box security analysis**. It inventories output sinks first, traces data flows back to their sources, and applies relevant vulnerability classes to each sink. It does not execute a target, access an environment, or turn unverified observations into findings.

TEREM's project-specific contribution is the security-team configuration layered on GitHub Squad: eight role-specific charters, sink-first routing and ceremonies, explicit producer/consumer handoffs, skill ownership, Five-Gates validation, report templates, structural validators, and session documentation rules. The underlying Squad framework and third-party checklist sources remain separately attributed.

Its mysterious fairy-tale identities are light presentation elements only. They never replace evidence, weaken validation gates, expand scope, or authorize fictional findings.

### Eight-agent team

| Agent | Responsibility |
|---|---|
| Vasilisa | Leads the assessment, enforces Phase 0, routes work, and assembles the final report. |
| Volk | Reviews web application attack surfaces and overlooked paths. |
| Yaga | Reviews authentication, authorization, sessions, and identity boundaries. |
| Gorynych | Reviews infrastructure, cloud, containers, proxies, and CI/CD. |
| Leshy | Maps the codebase, dependencies, and hidden connections. |
| Koschei | Investigates root causes and connects triaged candidates across agents into multi-step attack chains, with source evidence for each hop. |
| Mirror | Independently validates evidence through the Five-Gates workflow. |
| Kot | Preserves decisions, coverage, handoffs, and session records. |

The normal handoff order is Phase 0 inventory, parallel discovery, Vasilisa triage, Koschei chain analysis, Mirror validation, final report assembly, and Kot documentation. Only evidence that passes validation is eligible for the final findings report.

**Attack-chain analysis:** After triage, Koschei examines how candidates from different agents can combine into a multi-step attack path. It traces the data flow and state transitions between hops in source code, checks for controls that break the chain, and documents the resulting impact and manual verification steps. Mirror then independently validates both standalone candidates and complete chains through the Five-Gates workflow. This is static, source-based analysis; runtime verification is performed manually by the user. See [Koschei's charter](.squad/agents/koschei/charter.md) and [Mirror's chain-validation rules](.squad/agents/mirror/charter.md#chain-specific-gate-rules).

**Key difference from traditional testing:**
- **Class-first approach** (traditional): Find all XSS vulnerabilities, then all SQLi, then all IDOR... *Risk:* Vulnerabilities missed because focus shifts between classes
- **Sink-first approach** (TEREM): Find all sinks (HTTP responses, emails, logs, PDFs, etc.), then test **every vulnerability class for each sink** *Benefit:* Comprehensive per-sink coverage, fewer missed vulnerabilities

---


## Pentest Coverage

The team provides comprehensive static security analysis across:

- **MANDATORY PHASE 0 — Query Parameter Inventory:** A required Phase 0 artifact. See `.squad/skills/query-param-fuzzing/SKILL.md` for inventory and test guidance; inventory all query params (sort/filter/search/path/pagination) and classify HIGH/MED priority before discovery.

- **Output Sinks** — HTTP, email, logs, PDFs, files, APIs, redirects
- **Query Parameter Injection** — Path traversal, SQLi, LDAP, SSTI, SSRF via query params (sort, filter, search, path, pagination)
- **IDOR / BOLA** — Insecure direct object references, business logic attacks
- **XSS Surfaces** — Stored, reflected, DOM, mutation (tested per sink)
- **HTML Injection** — Email templates, PDF generators, user-facing output

- **Mass Assignment** — Bulk update vectors, field binding abuse
- **Prototype Pollution** — Object mutation, chain traversal
- **SSRF** — Server-side request forgery, cloud metadata, filter bypass
- **SQLi** — Union-based, blind, OOB, bypass chains
- **Auth / Identity / Session** — JWT, OAuth, SSO, access control, trust boundaries
- **Open Redirects** — OAuth abuse, phishing chains
- **Parameter Pollution** — WAF bypass, logic confusion
- **File Upload** — Extension bypass, polyglots, webshells
- **Race Conditions** — TOCTOU, limit bypass, concurrent access
- **Request Smuggling** — CL.TE, TE.CL, pipeline desync
- **Dangerous Sinks & Input Flows** — Unvalidated data paths
- **Route Inventory & Protection Matrix** — Endpoint coverage analysis
- **Infrastructure & Cloud Security** — Hardcoded secrets, cloud misconfiguration, K8s RBAC, reverse proxy configs, CI/CD pipeline security
- **Reconnaissance** — Codebase-focused recon, dependency analysis, credential leak detection, supply chain

---

## Setup & Usage

### 1. Prepare Your Codebase

Obtain an approved local copy of this repository, then place the source code to be reviewed inside the `codebase/` folder. This project does not define a canonical public clone URL.

```bash
cd TEREM
# Copy your source code into the codebase folder
cp -r /path/to/your/source/code/* codebase/
```

**Example structure:**
```
terem/
├── .squad/              # Agent team infrastructure (committed)
├── README.md            # This file
├── TEAM.md              # Team reference
├── codebase/            # YOUR SOURCE CODE (not committed, user-specific)
│   ├── src/
│   ├── app/
│   ├── handlers/
│   └── ...
└── reports/             # Pentest findings organized by date
```

The `codebase/` folder is in `.gitignore` — each user brings their own source code to analyze.

### Local checklist files

TEREM's agent configurations reference security checklists stored in the local workspace. Checklist content under `.squad/skills/` and `.squad/skills-archive-binary/` is excluded from the publication snapshot and must be obtained separately from its original or authorized sources. Place each required `SKILL.md` at the path referenced by the agent configuration; both directories are ignored by Git so the local files remain outside the publication index.

The active workflow expects this structure:

```text
.squad/
├── SKILL-MAPPING-BY-AGENT.md
└── skills/
    ├── <skill-id>/
    │   └── SKILL.md
    ├── offensive-rce/
    │   └── SKILL.md
    └── offensive-sqli/
        └── SKILL.md
```

The publication snapshot contains no checklist files. To run the documented full-team workflow, supply all 51 active `SKILL.md` files enumerated in [SKILL-MAPPING-BY-AGENT.md](.squad/SKILL-MAPPING-BY-AGENT.md), including `.squad/skills/offensive-rce/SKILL.md` and `.squad/skills/offensive-sqli/SKILL.md` for Volk. Skills under `.squad/skills-archive-binary/` are archived and are not required by the active white-box workflow.

Original source references for third-party-derived skills are listed in [THIRD_PARTY_NOTICES.md](THIRD_PARTY_NOTICES.md). TEREM does not include a checklist bundle, downloader, or vendoring script. The repository also does not document a separate distribution source for TEREM-specific local skills, so maintainers must provide an authorized local skill set before the full workflow can run.

### 2. Install Squad

TEREM requires a compatible [GitHub Squad](https://github.com/github/squad) host and the local `.squad/` configuration. Follow Squad's upstream installation documentation for the host you use. This repository does not pin a supported Squad CLI version or provide an automated bootstrap. The report-validation scripts also require Python 3, but no Python installer or pinned Python version is supplied here.

### 3. Kick Off a Pentest

Before starting, confirm that the source code is in `codebase/` and that every active skill required by [SKILL-MAPPING-BY-AGENT.md](.squad/SKILL-MAPPING-BY-AGENT.md) has a local `SKILL.md`. Once those prerequisites are satisfied, use a relative path to the `codebase` folder:

```bash
# In Copilot CLI:
"Team, run a fresh pentest on ./codebase"

# Or be specific:
"Team, pentest the authentication module in ./codebase/src/auth"
```

The squad will:
1. **Inventory all output sinks** (Phase 0: Vasilisa's ceremony)
2. **Parallel discovery** (Volk, Yaga, Gorynych, Leshy, Koschei all working simultaneously)
3. **Attack-chain analysis** (after Vasilisa triage, Koschei builds candidate chains and checks each hop against source code)
4. **Five-Gates validation** (Mirror approves findings)
5. **Final report** (findings + manual PoC steps in `/reports/{date}/`)

---

## Key Constraints ✅

- **White-box static only** — No runtime execution, no environment access (INT/QA/STAGE/PROD forbidden)
- **No git commands should run at any phase** — Do not invoke git operations during the entire process. Version control is handled manually and described in this README.
- **Manual PoC required** — Every finding includes step-by-step instructions YOU verify (not automated)
- **Evidence-driven** — All findings tied to exact file:line location in source code
- **Source-proven findings only** — No speculation, no false positives
- **Codebase folder user-specific** — Each user adds their own source code to `./codebase/`

---

## Example Workflow

```
You:      "Team, pentest the authentication module"

Vasilisa: "Starting parallel discovery using sink-first methodology..."
  🔧 Volk scanning HTTP response sinks...
  🔧 Yaga reviewing JWT/OAuth sinks...
  ⚙️ Gorynych analyzing infrastructure sinks...
  🔍 Leshy performing reconnaissance...
  🔍 Koschei cross-referencing attack chains...
  📋 Kot logging session...

[agents work in parallel, analyzing sinks systematically]

You: [wait for results]

Vasilisa: "Discovery complete. Routing to validator..."
  ✅ Mirror verifying 12 candidates...

[validation complete]

Vasilisa: "✅ Report ready with 7 confirmed findings + manual PoC steps"
  [You can now manually verify each finding against source]
```

---

## How Sink-First Works

### Example: Email Notifications Sink

```
SINK: Email notifications (sendNotification endpoint)

1. Identify the sink: Email sent via /api/notifications
2. Trace input sources: userId, clientId, account details
3. Test ALL vulnerability classes on THIS sink:
   - IDOR: Can I send notifications for other users?
   - HTML Injection: Can I inject HTML in email body?
   - XSS: Can I break out of email template?
   - Mass Assignment: Can I override fields?
   - Privilege Escalation: Can I escalate via notification content?
   - ...
4. Document findings with exact file:line evidence
5. Move to next sink
```

**Result:** Every sink gets exhaustive testing. Vulnerabilities hidden in multi-layer call chains are discovered because the email builder layer is explicitly tested, not glossed over as "internal communication."

---

## Validation Framework — Five-Gates

Every finding is verified through five gates before confirmation:

1. **Source Code Verification** — Exact file:line location in source
2. **Attack Flow Validation** — Realistic exploitation path documented
3. **Severity Calibration** — Impact matches severity claim
4. **False Positive Review** — No existing mitigations hiding finding
5. **Reproducibility & PoC** — Manual steps for user verification

**Result:** Only confirmed findings reach the final report. Observations and gaps are separated and clearly marked.

---

## Reports and Deliverables

After pentest execution, findings are organized in `/reports/`:

```
/reports/
├── README.md                                  (manifest + archive guide)
├── {YYYY-MM-DD}/                              (clean date-only structure)
│   ├── PENTEST_REPORT_FINAL.md                (all findings + PoC steps)
│   ├── TEAM_EXECUTION_SUMMARY.md              (team orchestration log)
│   └── reference/                             (supporting analysis)
└── {YYYY-MM-DD-THH-MM-SS}/                    (timestamped archive)
    ├── PENTEST_REPORT_FINAL.md                (original findings)
    ├── TEAM_EXECUTION_SUMMARY.md              (original execution log)
    └── reference/                             (original supporting files)
```

Pentest reports and findings are generated dynamically and stored in dated folders within `/reports/` — based on the current state of the report generation process directed to agents.

---

## Quick Start Commands

**Run a full pentest:**
```bash
"Team, run a pentest on ./codebase"
```

**Analyze a specific sink:**
```bash
"Volk, find all vulnerabilities in the email notification sink (src/service/email-builder.js)"
```

**Deep-dive on auth:**
```bash
"Yaga, deep-dive on the authentication flows in src/auth/"
```

**Review last pentest:**
```bash
"What were the findings from the last pentest?"
```

**See what's been done:**
```bash
"Catch me up — what happened in the last session?"
```

See [TEAM.md](TEAM.md) for the full team roster and more command examples.

---

## Directives in Effect

- ✅ **White-box static analysis only** — No runtime execution, no environment access
- ✅ **Sink-first methodology** — All output channels tested exhaustively for all vulnerability classes
- ✅ **No git operations** — Do not invoke git operations at any phase; version control is managed manually as described in this README.
- ✅ **Manual PoC for user verification** — Every finding includes step-by-step user-executable PoC steps
- ✅ **Source-proven findings only** — All findings tied to exact file:line evidence

---

## Learn More

- **[Routing Rules](.squad/routing.md)** — How work is routed to each agent during pentests
- **[Ceremonies](.squad/ceremonies.md)** — Pre-discovery sink inventory and team synchronization
- **[TEAM.md](TEAM.md)** — Full team roster with skills, expertise, and command examples
- **[SKILL-MAPPING-BY-AGENT.md](.squad/SKILL-MAPPING-BY-AGENT.md)** — Complete skill coverage per agent

---

## Project Structure

```
.squad/
├── team.md                        # Roster & project context
├── routing.md                     # Work assignment rules (who handles what)
├── ceremonies.md                  # Pre-pentesting ceremonies (sink inventory, sync)
├── decisions.md                   # Shared decision ledger (authoritative; NOT committed by default)
├── decisions/inbox/               # Decision drop-box (agents write proposals here)
├── agents/
│   ├── {name}/charter.md          # Agent charter & role definition
│   └── {name}/history.md          # Individual learnings (all agents)
├── orchestration-log/             # Agent work audit trail
├── log/                           # Session logs
└── skills/                        # Reusable security skills
```

Decision workflow (brief):
- Agents submit proposals to .squad/decisions/inbox/{agent}-{slug}.md (append-only).
- Kot merges inbox into .squad/decisions.md using dedupe and Five-Gates annotations.
- .squad/decisions.md is authoritative for confirmed findings; agents read it at spawn.
- decisions.md is session-specific and should be excluded from shared commits (.gitignore).

---

## Acknowledgments

TEREM is built on [GitHub Squad](https://github.com/github/squad). Squad is © 2026 Brady Gaster and contributors and is used under the MIT License. See [SQUAD-MIT.txt](LICENSES/SQUAD-MIT.txt).

See [THIRD_PARTY_NOTICES.md](THIRD_PARTY_NOTICES.md) for detailed upstream attribution and checklist-source information.

---

**Setup status:** The full documented workflow is incomplete until all mapped local checklist files are present and a compatible Python 3 runtime is available for report validation.
**Coordinator Version:** 0.0.0-source  
**Methodology:** Sink-First White-Box Analysis
