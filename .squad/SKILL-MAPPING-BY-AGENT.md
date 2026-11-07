# TEREM — Skill Mapping by Agent

## Configured Local Skill Set (51 Active Skill Files)

The entries below map agents to the checklist files expected in the local workspace. Checklist contents under `.squad/skills/` and `.squad/skills-archive-binary/` are excluded from this repository. Supply the required active `SKILL.md` files separately before running the full workflow. Archived checklists are outside the active white-box workflow. See [local checklist setup](../README.md#local-checklist-files).

Some local checklists are derived from [SnailSploit/offensive-checklist](https://github.com/SnailSploit/offensive-checklist). The [Third-Party Notices](../THIRD_PARTY_NOTICES.md#snailsploitoffensive-checklist) identify the corresponding local paths, original source links, and unresolved redistribution status. Source links provide attribution and do not themselves grant permission to copy, adapt, or redistribute checklist text.

---

## 🔧 Volk — Web Application Pentester (25 Skills)

**Core Skills:**
1. `offensive-xss` — Cross-Site Scripting (stored, reflected, DOM, mutation)
2. `offensive-idor` — Insecure Direct Object References (enumeration, business logic)
3. `offensive-ssrf` — Server-Side Request Forgery (cloud metadata, filter bypass)
4. `offensive-sqli` — SQL Injection (UNION, blind, cloud-native, ORM)
5. `offensive-ssti` — Server-Side Template Injection (Jinja2, EJS, Twig, Freemarker)
6. `offensive-rce` — Remote Code Execution (command injection, eval, deserialization chains)
7. `offensive-file-upload` — File Upload Vulnerabilities (extension bypass, polyglots, webshells)
8. `offensive-race-condition` — Race Conditions (TOCTOU, limit bypass, concurrent requests)
9. `offensive-request-smuggling` — HTTP Request Smuggling (CL.TE, TE.CL, pipeline desync)
10. `offensive-open-redirect` — Open Redirect (OAuth abuse, phishing chains)
11. `offensive-parameter-pollution` — HTTP Parameter Pollution (WAF bypass, logic confusion)
12. `offensive-graphql` — GraphQL Security (introspection, batching, aliasing)
13. `offensive-deserialization` — Insecure Deserialization (Java, Python, .NET gadget chains)
14. `offensive-xxe` — XML External Entity (XXE, blind XXE, OOB extraction)
15. `query-param-fuzzing` — Query Parameter Injection (path traversal, SQLi, LDAP, SSTI, SSRF via query params)
16. `input-validation-fuzzing` — Input Validation Patterns (OpenResty/Lua, API gateways)
17. `offensive-waf-bypass` — WAF Evasion Techniques (encoding, protocol variance, HTTP/2 smuggling)
18. `offensive-business-logic` — Business Logic Flaws (workflow bypass, state machines, approval manipulation)
19. `offensive-mass-assignment` — Mass Assignment (JSON over-posting, prototype pollution, auto-binding)
20. `offensive-rest-api-security` — REST API Security (version bypass, method override, content-type confusion, BFLA)
21. `offensive-clickjacking` — Clickjacking / UI Redressing (iframe stacking, frame-ancestors, multi-level)
22. `offensive-csrf` — Cross-Site Request Forgery (token validation, SameSite, WebSocket CSRF, OAuth state)
23. `offensive-prototype-pollution` — Prototype Pollution (__proto__, constructor.prototype, deep merge)
24. `offensive-cors` — CORS Misconfiguration (origin reflection, wildcard, regex bypass, credentials)
25. `offensive-fast-checking` — Fast Testing Checklist (rapid triage, quick wins) **[SHARED]**

**Removed (archived as binary exploitation content):** `offensive-fuzzing`, `offensive-vuln-classes`, `offensive-bug-identification`

---

## 🔐 Yaga — Authentication & Identity Specialist (9 Skills)

**Core Skills:**
1. `offensive-jwt` — JWT Security (alg:none, key confusion, secret cracking)
2. `offensive-oauth` — OAuth Security Testing (redirects, token leakage, PKCE bypass)
3. `openresty-lua-auth-patterns` — OpenResty/Lua Auth Patterns (decode-before-verify, SameSite, cache revocation)
4. `idor-access-control-discovery` — IDOR Access Control Discovery (authorization-as-code, OPA/Cedar, BOLA patterns)
5. `offensive-session` — Session Management Security (fixation, prediction, invalidation, cookie flags, timeout)
6. `offensive-saml` — SAML 2.0 Security (signature stripping, XSW, certificate confusion, replay attacks)
7. `offensive-debug-disclosure` — Debug & Info Disclosure (stack traces, user enumeration, verbose auth errors, debug endpoints)
8. `offensive-password-handling` — Password Handling (hashing algorithm, reset token security, brute force protection, session fixation)
9. `offensive-fast-checking` — Fast Testing Checklist (rapid triage) **[SHARED]**

---

## 🔧 Gorynych — Infrastructure & Cloud Security Specialist (10 Skills)

**Core Skills:**
1. `infrastructure-secret-detection` — Hardcoded credentials, API keys, JWT secrets, TLS keys in source
2. `infrastructure-cloud-misconfig` — IAM over-permission, public storage, open security groups, IMDSv1
3. `infrastructure-container-k8s` — Dockerfile, docker-compose, K8s RBAC, pod security, volume mounts
4. `infrastructure-proxy-config` — nginx/OpenResty/HAProxy/Traefik misconfigurations, header forwarding, TLS
5. `infrastructure-ci-cd` — GitHub Actions, GitLab CI, Jenkins credential exposure, supply chain, template includes
6. `kubernetes-security` — K8s-specific security patterns (SA token abuse, label selector injection, secrets in git)
7. `infrastructure-tls-cipher-patterns` — TLS protocol downgrade, weak cipher suites, HSTS, EOL base images, Lua package path hijack
8. `offensive-supply-chain` — Supply Chain Security (CI template includes, dependency confusion, SBOM, post-install scripts)
9. `offensive-ai-security` — AI/ML Security (LLM injection, RAG poisoning, model supply chain)
10. `offensive-fast-checking` — Fast Testing Checklist (rapid triage) **[SHARED]**

**Renamed:** `binary-exploit-patterns` → `infrastructure-tls-cipher-patterns` (content was TLS/Docker patterns, not binary exploitation)
**Removed (archived as binary exploitation content):** `offensive-bug-identification`

---

## 🔍 Leshy — Codebase Reconnaissance Specialist (3 Skills)

**Core Skills:**
1. `osint-recon-patterns` — Recon Patterns (codebase-focused recon: dependency analysis, leaked credentials, metadata extraction, internal service topology)
2. `offensive-supply-chain` — Supply Chain Security (shared with Gorynych for cross-reference on dependency analysis, SBOM)
3. `offensive-fast-checking` — Fast Testing Checklist (rapid triage) **[SHARED]**

**Removed (archived as black-box content):** `offensive-osint`, `offensive-osint-methodology`, `offensive-fuzzing-course`

---

## 🧬 Koschei — Vulnerability Research & Attack-Chain Analysis (5 Skills)

**Core Skills:**
1. `vulnerability-chaining` — Multi-Hop Attack Chains (cross-stack patterns, 3+ hop chains)
2. `root-cause-analysis` — Root Cause Methodology (5 Whys, fishbone, architecture-level tracing)
3. `offensive-ai-security` — AI/ML Security (shared with Gorynych for cross-reference)
4. `output-encoding-verification` — Output Encoding Checks (HTML, JSON, URL, JS, CSS context verification)
5. `offensive-fast-checking` — Fast Testing Checklist (rapid triage) **[SHARED]**

**Removed (archived as binary exploitation content):** `offensive-bug-identification`

---

## ✅ Mirror — Validator / Verifier (1 Skill)

**Required local skills:**
1. `five-gates-validation` — Five-Gates Framework (source verification, attack flow, severity calibration, false positive review, reproducibility)

**Custom verification logic:**
1. Gate 1: Source Code Verification
2. Gate 2: Attack Flow Validation
3. Gate 3: Severity Calibration
4. Gate 4: False Positive Likelihood
5. Gate 5: Reproducibility & PoC Sufficiency

**Total:** 1 skill + custom framework

---

## 🏗️ Vasilisa — Pentest Lead & Orchestrator (2 Skills)

**Required local skills:**
1. `sink-inventory` — Phase 0 Output Sink Enumeration (routes, sinks, encoding, context matrix)
2. `discovery-spawn-completeness` — Spawn Completeness Checks (verify all 7 gates before agent spawn)

**Orchestration-only role:**
- Routes work to appropriate discovery agents
- Triages candidate findings
- Prioritizes work phases
- Coordinates with Mirror for validation
- Assembles final report

**Total:** 2 skills

---

## 📋 Kot — Session Memory & Documentation (2 Skills)

**Required local skills:**
1. `coverage-tracking` — Endpoint/sink/file/pattern coverage metrics and Coverage Report
2. `project-conventions` — Project-Specific Conventions (OpenResty/nginx/Kubernetes patterns, anti-patterns)

**Mechanical operations:**
- Logs orchestration events
- Merges decision inbox
- Updates agent history
- Creates session archives
- Produces Coverage Report from agent orchestration logs
- Record staging manifests (Kot writes manifest; humans/CI perform commits)

**Total:** 2 skills

---

## Summary by Category

### Vulnerability Discovery Coverage

| Category | Primary Agent | Total Skills | Coverage |
|----------|---------------|-------------|----------|
| **Web App Security** | Volk | 25 | XSS, IDOR, SSRF, SQLi, SSTI, RCE, file upload, race conditions, request smuggling, open redirect, parameter pollution, GraphQL, deserialization, XXE, WAF bypass, business logic, mass assignment, REST API, clickjacking, CSRF, prototype pollution, CORS, fast-checking |
| **Authentication** | Yaga | 7 | JWT, OAuth, OpenResty auth patterns, access control, IDOR discovery, session management, SAML, fast-checking |
| **Infrastructure & Cloud** | Gorynych | 10 | Secret detection, cloud misconfig, K8s RBAC, proxy configs, CI/CD, TLS/cipher patterns, supply chain, AI security, fast-checking |
| **Reconnaissance** | Leshy | 3 | Codebase-focused recon patterns, supply chain (shared), fast-checking |
| **Synthesis & Analysis** | Koschei | 5 | Vulnerability chaining, root cause, output encoding, AI security, fast-checking |
| **Validation** | Mirror | 1 | Five-Gates framework, severity calibration |
| **Phase 0** | Vasilisa | 2 | Sink inventory, spawn completeness |
| **Session** | Kot | 2 | Coverage tracking, project conventions |

### Skill Reuse (Shared Utilities)

The following skills are used by multiple agents:

- **`offensive-fast-checking`** → Volk, Yaga, Gorynych, Leshy, Koschei (rapid triage, quick wins)
- **`offensive-ai-security`** → Gorynych, Koschei (cross-reference AI/ML attack surfaces)
- **`offensive-supply-chain`** → Gorynych, Leshy (cross-reference: CI/CD templates vs dependency analysis)

---

## Changes Log

This log describes changes to the local skill set. The referenced checklist contents are excluded from this repository.

### Skill Gap Closure

#### New Skills Created (4)
- `offensive-session` — Session Management Security (assigned to Yaga)
- `offensive-prototype-pollution` — Prototype Pollution (assigned to Volk)
- `offensive-cors` — CORS Misconfiguration (assigned to Volk)
- `offensive-saml` — SAML 2.0 Security (assigned to Yaga)

#### Skills Archived (2)
- `offensive-osint` → `.squad/skills-archive-binary/` (black-box OSINT tool directory — not applicable to white-box code review)
- `offensive-osint-methodology` → `.squad/skills-archive-binary/` (threat-intelligence OSINT methodology — not applicable to white-box code review)

#### Skills Updated (1)
- `offensive-fast-checking` — Added new skills to deferral table (session, prototype-pollution, cors, saml)

#### Skills Reassigned (2)
- `input-validation-fuzzing` → moved from Kot to Volk (discovery skill, not audit trail)
- `output-encoding-verification` → stays with Koschei (discovery skill, removed from Kot)

#### Skill Count
- Before: 47 active + 18 archived = 65
- After: 51 active + 18 archived = 69

---

### Previous Changes (Archived/Consolidated)

#### New Skills Created (6)
- `offensive-csrf` — Cross-Site Request Forgery (assigned to Volk)
- `offensive-business-logic` — Business Logic Flaws (assigned to Volk)
- `offensive-mass-assignment` — Mass Assignment / BOPLA (assigned to Volk)
- `offensive-rest-api-security` — REST API Security (assigned to Volk)
- `offensive-clickjacking` — Clickjacking / UI Redressing (assigned to Volk)
- `offensive-supply-chain` — Supply Chain Security (shared by Gorynych and Leshy)

#### Skills Archived (6)
- `offensive-fuzzing` → `.squad/skills-archive-binary/` (binary fuzzing: AFL++, syzkaller)
- `offensive-vuln-classes` → `.squad/skills-archive-binary/` (binary exploit dev curriculum)
- `offensive-fuzzing-course` → `.squad/skills-archive-binary/` (binary fuzzing curriculum)
- `offensive-bug-identification` → `.squad/skills-archive-binary/` (reverse engineering, DBI, symbolic execution)
- `offensive-osint` → `.squad/skills-archive-binary/` (black-box OSINT tool directory)
- `offensive-osint-methodology` → `.squad/skills-archive-binary/` (threat-intelligence OSINT methodology)

#### Skills Renamed (1)
- `binary-exploit-patterns` → `infrastructure-tls-cipher-patterns` (content was TLS/Docker patterns, not binary exploitation)

#### Skills Generalized (4)
- `root-cause-analysis` — Removed engagement-specific file paths and finding references
- `osint-recon-patterns` — Removed engagement-specific domain names and attribution
- `input-validation-fuzzing` — Removed engagement-specific metadata
- `project-conventions` — Populated with OpenResty/nginx/K8s conventions (was empty template)

#### Skills Deduplicated (2)
- `offensive-fast-checking` — Replaced 486-line catch-all with concise rapid-triage checklist + cross-reference table to dedicated skills
- `infrastructure-cloud-misconfig` — Removed K8s grep duplication, added cross-reference to `infrastructure-container-k8s` and `kubernetes-security`

#### Skills Enhanced (1)
- `infrastructure-ci-cd` — Added GitLab template include supply chain risk detection patterns

---

## Parallel Execution

```
User: "Run a pentest"
       ↓
   Vasilisa: Phase 0 (sink inventory + spawn gates)
       ↓
   Spawn 5 discovery agents (parallel):
   • Volk (Web App)          → 25 skills, broad surface discovery
   • Yaga (Auth)           → 7 skills, identity & trust boundaries
   • Gorynych (Infrastructure) → 10 skills, cloud misconfig, secrets, K8s, proxy
   • Leshy (Recon)           → 3 skills, codebase recon & dependency analysis
   • Koschei (Synthesis)        → 5 skills, chain analysis & root cause
       ↓
   All report to Vasilisa (Lead)
       ↓
   Vasilisa routes to Mirror (Validator)
       ↓
   Mirror applies Five-Gates framework
       ↓
   Vasilisa assembles final report
       ↓
   Kot produces Coverage Report + Execution Summary
```

---

## Getting Started

After completing the [local checklist setup](../README.md#local-checklist-files), invoke TEREM with:

```
"Vasilisa, run a comprehensive pentest on [target-codebase]"
```

This triggers the full 8-member team:
- Parallel discovery across web, auth, infrastructure, reconnaissance, and synthesis
- Cross-verification and chaining analysis
- Five-Gates validation
- Evidence-first reporting with coverage metrics

---

**Squad v0.0.0-source — Expanded Pentest Team**
Total Members: 8 | Active Skill Files: 51 | Archived Skills: 18 | Parallel Discovery Agents: 5
