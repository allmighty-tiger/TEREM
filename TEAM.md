# TEREM — Team Overview

**Squad v0.0.0-source**

**Description:** White-Box Security Agent Team

Quick reference for the 8-member pentesting team. The fairy-tale motifs are presentation cues only; evidence and the established security methodology govern every conclusion.

---

## Your Team

| Avatar | Name | Role | Focus |
|--------|------|------|-------|
| ![Vasilisa](./.squad/agents/vasilisa/avatar.svg) | **Vasilisa** | Pentest Lead & Orchestrator | Orchestrates parallel discovery, triages findings, prioritizes final report |
| ![Volk](./.squad/agents/volk/avatar.svg) | **Volk** | Web Application Pentester | XSS, IDOR/BOLA, mass assignment, SSRF/SQLi, race conditions, file upload, prototype pollution, CORS |
| ![Yaga](./.squad/agents/yaga/avatar.svg) | **Yaga** | Authentication & Identity Specialist | JWT (alg:none, key confusion), OAuth (redirects, token leakage), session management, SAML, privilege escalation |
| ![Gorynych](./.squad/agents/gorynych/avatar.svg) | **Gorynych** | Infrastructure & Cloud Security | Secret detection, cloud misconfiguration, K8s RBAC, reverse proxy configs, CI/CD pipeline security |
| ![Leshy](./.squad/agents/leshy/avatar.svg) | **Leshy** | Codebase Reconnaissance Specialist | Codebase-focused recon, dependency ecosystem, credentials in source, supply chain analysis |
| ![Koschei](./.squad/agents/koschei/avatar.svg) | **Koschei** | Vulnerability Research & Attack-Chain Analysis | Cross-reference findings, exploitation chains, root cause analysis, threat modeling |
| ![Mirror](./.squad/agents/mirror/avatar.svg) | **Mirror** | Validator / Verifier | Five-Gates (source, flow, severity, reproducibility), conservative verdicts, false-positive reduction |
| ![Kot](./.squad/agents/kot/avatar.svg) | **Kot** | Session Memory & Documentation | Session memory, decision consolidation, orchestration logs, history archival |

---

## Skills by Agent

**Complete Coverage: 51 Active Skills (+ 18 Archived) Across 5 Discovery Agents**

For the authoritative skill reference, see **[SKILL-MAPPING-BY-AGENT.md](./.squad/SKILL-MAPPING-BY-AGENT.md)**.

| Agent | Role | Core Skills | Total |
|-------|------|-------------|-------|
| **Volk** | Web Application Pentester | `offensive-xss`, `offensive-idor`, `offensive-ssrf`, `offensive-sqli`, `offensive-ssti`, `offensive-rce`, `offensive-file-upload`, `offensive-race-condition`, `offensive-request-smuggling`, `offensive-open-redirect`, `offensive-parameter-pollution`, `offensive-graphql`, `offensive-deserialization`, `offensive-xxe`, `query-param-fuzzing`, `input-validation-fuzzing`, `offensive-waf-bypass`, `offensive-business-logic`, `offensive-mass-assignment`, `offensive-rest-api-security`, `offensive-clickjacking`, `offensive-csrf`, `offensive-prototype-pollution`, `offensive-cors` + shared | 25 |
| **Yaga** | Authentication & Identity Specialist | `offensive-jwt`, `offensive-oauth`, `openresty-lua-auth-patterns`, `idor-access-control-discovery`, `offensive-session`, `offensive-saml`, `offensive-debug-disclosure`, `offensive-password-handling` + shared | 9 |
| **Gorynych** | Infrastructure & Cloud Security Specialist | `infrastructure-secret-detection`, `infrastructure-cloud-misconfig`, `infrastructure-container-k8s`, `infrastructure-proxy-config`, `infrastructure-ci-cd`, `kubernetes-security`, `infrastructure-tls-cipher-patterns`, `offensive-ai-security`, `offensive-supply-chain` + shared | 10 |
| **Leshy** | Codebase Reconnaissance Specialist | `osint-recon-patterns`, `offensive-supply-chain` + shared | 3 |
| **Koschei** | Vulnerability Research & Attack-Chain Analysis | `vulnerability-chaining`, `root-cause-analysis`, `offensive-ai-security`, `output-encoding-verification` + shared | 5 |
| **Mirror** | Validator / Verifier | `five-gates-validation` + custom framework | 1 |
| **Vasilisa** | Pentest Lead & Orchestrator | `sink-inventory`, `discovery-spawn-completeness` | 2 |
| **Kot** | Session Memory & Documentation | `coverage-tracking`, `project-conventions` | 2 |

**Shared skills:** `offensive-fast-checking` is used by Volk, Yaga, Gorynych, Leshy, Koschei. `offensive-ai-security` is shared by Gorynych and Koschei. `offensive-supply-chain` is shared by Gorynych and Leshy. 18 binary/exploit and black-box OSINT skills are archived in `.squad/skills-archive-binary/` (available for future engagements outside white-box scope).

---

## Quick Commands

**Run a full pentest:**
```bash
"Team, run a pentest on ./codebase"
```

**Focus on a single sink or domain:**
```bash
"Volk, find all vulnerabilities in the email notification sink"
"Yaga, deep-dive on authentication flows in src/auth/"
```

**Check status:**
```bash
"What did the team do?" / "Catch me up"
"What have we decided?"
```

---

## Key Constraints ✅

- **White-box static only** — No runtime execution, no environment access
- **No git commands should run** — Do not invoke git operations during analysis; you handle version control manually
- **Manual PoC required** — Every finding includes user-executable steps for verification
- **Evidence-driven** — All findings tied to exact file:line in source code

---

## Directives in Effect

- ✅ **Sink-first methodology** — Test all vulnerability classes on each output sink exhaustively
- ✅ **Source-proven findings only** — No speculation, no false positives
- ✅ **Five-Gates validation** — Every finding verified before reaching final report

---

## Team State Files

- **`.squad/decisions.md`** — Shared team decisions and methodology directives
- **`.squad/agents/{name}/history.md`** — Individual agent learnings and patterns
- **`.squad/orchestration-log/`** — Audit trail of completed work
- **`.squad/log/`** — Session logs and diagnostics

---

**Status:** Fully deployed  
**For:** Quick team reference — see [README.md](README.md) for project guide
