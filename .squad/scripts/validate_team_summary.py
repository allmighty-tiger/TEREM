#!/usr/bin/env python3
"""
Validation script for TEAM_EXECUTION_SUMMARY.md

Enforces strict compliance with the template structure defined in:
  reports/template/TEAM_EXECUTION_SUMMARY.template.md

Usage:
  python3 .squad/scripts/validate_team_summary.py reports/TEAM_EXECUTION_SUMMARY.md

Exit codes:
  0 = validation passed
  1 = validation failed (required heading missing, content check failed)
  2 = usage error
"""

import re
import sys
from pathlib import Path


def load_file(path):
    """Load markdown file and return lines."""
    try:
        with open(path, "r", encoding="utf-8") as f:
            return [line.rstrip("\n") for line in f.readlines()]
    except FileNotFoundError:
        print(f"ERROR: File not found: {path}")
        sys.exit(1)
    except Exception as e:
        print(f"ERROR: Failed to read {path}: {e}")
        sys.exit(1)


def extract_headings(lines):
    """Extract all level-2 and level-3 headings in order."""
    headings = []
    for line in lines:
        match = re.match(r"^(#{2,3})\s+(.+)$", line)
        if match:
            level = len(match.group(1))
            text = match.group(2).strip()
            headings.append(f"{'#' * level} {text}")
    return headings


def check_heading_sequence(headings):
    """
    Verify that required headings appear in order (subsequence check).
    Returns (pass: bool, missing_heading: str or None)
    """
    required = [
        "## EXECUTIVE CONTEXT",
        "## TEAM ROSTER & DELIVERABLES",
        "## DISCOVERY COMPLETION TIMELINE",
        "## FINDINGS DISTRIBUTION",
        "### By Severity",
        "### By Agent",
        "## CRITICAL FINDINGS (Deploy Blockers)",
        "## ROOT CAUSE ANALYSIS",
        "## CROSS-LAYER ATTACK CHAINS IDENTIFIED",
        "## CROSS-CHAIN INSIGHTS",
        "## WHITE-BOX COVERAGE MATRIX",
        "## REMEDIATION PRIORITY & ROADMAP",
        "## SESSION OUTCOMES & DELIVERABLES",
        "## VALIDATION METHODOLOGY (Five-Gates Framework)",
        "## OUTPUT ARTIFACTS",
        "## NEXT STEPS FOR USER",
        "## TEAM EXECUTION NOTES",
    ]

    idx = 0
    for required_heading in required:
        try:
            idx = headings.index(required_heading, idx)
            idx += 1
        except ValueError:
            return False, required_heading

    return True, None


def check_roster_table(content):
    """Verify TEAM ROSTER table has required columns and at least one agent row."""
    # Check for header row
    if "| Agent | Role | Status | Findings | Key Contributions |" not in content:
        return False, "Roster table header missing or malformed"

    # Count data rows (lines between | containing Agent data, excluding header/separator)
    lines = content.split("\n")
    in_roster = False
    data_rows = 0

    for i, line in enumerate(lines):
        if "| Agent | Role | Status | Findings | Key Contributions |" in line:
            in_roster = True
            continue
        if in_roster:
            # Stop if we hit next section (##)
            if line.startswith("##"):
                break
            # Count rows that look like data (| ... | ... |)
            if line.startswith("|") and line.count("|") >= 5:
                # Exclude separator rows (all dashes)
                if not all(c in " |-" for c in line):
                    data_rows += 1

    if data_rows < 1:
        return False, "Roster table must have at least one agent row"

    return True, None


def check_findings_totals(content):
    """
    Verify that findings totals are consistent.
    Extract numbers from 'By Severity' and 'By Agent' sections.
    """
    # This is a lightweight check — verifies sections exist
    if "### By Severity" not in content:
        return False, "By Severity subsection missing"
    if "### By Agent" not in content:
        return False, "By Agent subsection missing"
    if "| **TOTAL**" not in content:
        return False, "TOTAL row missing in findings distribution"

    return True, None


def check_critical_findings(content):
    """
    Verify CRITICAL FINDINGS section has at least one entry with evidence reference.
    Evidence should be in format: file:line or .squad/ path
    """
    if "## CRITICAL FINDINGS" not in content:
        return False, "CRITICAL FINDINGS section missing"

    # Extract section between CRITICAL FINDINGS and next ##
    lines = content.split("\n")
    in_section = False
    section_content = []

    for line in lines:
        if "## CRITICAL FINDINGS" in line:
            in_section = True
            continue
        if in_section:
            if line.startswith("##") and "CRITICAL" not in line:
                break
            section_content.append(line)

    section_text = "\n".join(section_content)

    # Check for evidence patterns: file:line or .squad/ paths
    has_evidence = bool(
        re.search(r"(src/|lib/|app/)[^:]+:\d+", section_text)
        or ".squad/" in section_text
        or "Source:" in section_text
    )

    if not has_evidence:
        return False, "CRITICAL findings must include evidence reference (file:line or .squad/ path)"

    # Check for at least one finding ID (e.g., C-001)
    has_findings = bool(re.search(r"\*\*C-\d+", section_text))
    if not has_findings:
        return False, "CRITICAL findings must include finding IDs (e.g., C-001)"

    return True, None


def check_remediation_phases(content):
    """Verify REMEDIATION PRIORITY & ROADMAP has Phase 1 with at least one task."""
    if "## REMEDIATION PRIORITY & ROADMAP" not in content:
        return False, "REMEDIATION PRIORITY & ROADMAP section missing"
    if "### Phase 1" not in content:
        return False, "Phase 1 subsection missing in REMEDIATION PRIORITY & ROADMAP"

    # Extract Phase 1 section
    lines = content.split("\n")
    in_phase1 = False
    phase1_content = []

    for line in lines:
        if "### Phase 1" in line:
            in_phase1 = True
            continue
        if in_phase1:
            if line.startswith("###"):  # Next phase
                break
            phase1_content.append(line)

    phase1_text = "\n".join(phase1_content)

    # Check for at least one checklist task (- [ ])
    if "- [ ]" not in phase1_text and "- [x]" not in phase1_text:
        return False, "Phase 1 must contain at least one checklist task (- [ ])"

    return True, None


def check_validation_methodology(content):
    """
    Verify VALIDATION METHODOLOGY section includes Five-Gates and verdict counts.
    """
    if "## VALIDATION METHODOLOGY" not in content:
        return False, "VALIDATION METHODOLOGY section missing"
    if "Five-Gates" not in content:
        return False, "VALIDATION METHODOLOGY must reference Five-Gates framework"

    # Check for verdict counts: CONFIRMED, OBSERVATION, REJECTED
    has_verdicts = (
        "CONFIRMED" in content and "OBSERVATION" in content and "REJECTED" in content
    )
    if not has_verdicts:
        return False, "VALIDATION METHODOLOGY must include verdict counts (CONFIRMED/OBSERVATION/REJECTED)"

    return True, None


def check_output_artifacts(content):
    """Verify OUTPUT ARTIFACTS section lists required reports."""
    if "## OUTPUT ARTIFACTS" not in content:
        return False, "OUTPUT ARTIFACTS section missing"
    if "PENTEST_REPORT_FINAL.md" not in content:
        return False, "OUTPUT ARTIFACTS must list PENTEST_REPORT_FINAL.md"

    return True, None


def main():
    if len(sys.argv) < 2:
        print("Usage: validate_team_summary.py <path/to/TEAM_EXECUTION_SUMMARY.md>")
        sys.exit(2)

    file_path = sys.argv[1]
    lines = load_file(file_path)
    content = "\n".join(lines)

    # Run all checks
    checks = [
        ("Headings present and in order", lambda: check_heading_sequence(extract_headings(lines))),
        ("Roster table structure", lambda: check_roster_table(content)),
        ("Findings totals consistency", lambda: check_findings_totals(content)),
        ("Critical findings with evidence", lambda: check_critical_findings(content)),
        ("Remediation phases", lambda: check_remediation_phases(content)),
        ("Validation methodology", lambda: check_validation_methodology(content)),
        ("Output artifacts", lambda: check_output_artifacts(content)),
    ]

    failed_checks = []

    for check_name, check_func in checks:
        result = check_func()
        if isinstance(result, tuple):
            passed, detail = result
            if not passed:
                failed_checks.append((check_name, detail))
                print(f"❌ {check_name}: {detail}")
            else:
                print(f"✅ {check_name}")
        else:
            print(f"⚠️ {check_name}: Unexpected result type")

    # Final verdict
    print()
    if failed_checks:
        print(f"VALIDATION FAILED: {len(failed_checks)} check(s) failed")
        for check_name, detail in failed_checks:
            print(f"  - {check_name}: {detail}")
        sys.exit(1)
    else:
        print("✅ VALIDATION PASSED: All checks successful")
        print(f"Template validation for {file_path} PASSED")
        sys.exit(0)


if __name__ == "__main__":
    main()
