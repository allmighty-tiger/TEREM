# Team Decisions

## Discovery Spawn Gate (Permanent Rule)

**COORDINATOR ENFORCEMENT:** Before spawning Volk, Yaga, Gorynych, Leshy, Koschei on any pentest:

1. Vasilisa Phase 0 COMPLETE — Output + Logic Sinks inventoried
2. Output Context Matrix provided
3. Auth/Authz Gate Inventory provided
4. Volk assigned to IDOR, mass assignment, SSRF, SQLi, RCE, logic flaws
5. Yaga assigned to JWT, OAuth, session mgmt, auth bypass, access control, privilege escalation
6. All 5 agents spawned together with inventory as input

See .squad/routing.md for enforcement details.

## Agent Read Permissions (Standing Directive)

**Effective:** All sessions, all pentests, going forward.

**Decision:** All agents (Vasilisa, Volk, Yaga, Gorynych, Leshy, Koschei, Mirror, Kot) have unrestricted read/find/grep access to ALL files within the project root directory.

**Scope:**
- Unrestricted FIND operations (glob, ls, locate, recursive directory scanning)
- Unrestricted READ operations (cat, view, file contents)
- Unrestricted SEARCH operations (grep, ripgrep, text pattern matching)
- Entire project root and all subdirectories

**No coordinator approval needed.** Agents discover and read project files autonomously.

**Note on .gitignore:** `.squad/decisions/inbox/` is ignored, but `.squad/decisions.md` is committed, ensuring this directive persists across sessions and remote clones.


---

## Findings Consolidation — Reusable Format

**Template guidance:** The following structure is reusable across engagements. Populate it only with evidence collected from the currently authorized codebase; it does not describe a completed session.

### Template Structure for Findings Consolidation

When consolidating pentest findings:

1. **Session Header:** Document span, agents involved, validation framework (Five-Gates)
2. **Findings by Severity:** CRITICAL → HIGH → MEDIUM, with evidence trails
3. **Attack Chains:** Document multi-step exploitation flows combining findings
4. **Validation Metrics:** Pass rate, confirmation accuracy, rejection rate
5. **Agent Performance Summary:** Who found what, accuracy rating
6. **Remediation Priority:** Timeline (24h critical → 2 weeks medium)

### Findings Table Format

**Key columns per finding:**
- **ID:** Unique identifier (F-C01, F-H05, F-M03, etc.)
- **Title:** Vulnerability name (don't include app-specific context)
- **File:Line:** Code location (replace with your codebase)
- **Source:** Which agents discovered it (Volk, Yaga, Gorynych, Leshy, Koschei)
- **Status:** ✅ CONFIRMED or 🔍 OBSERVATION

### Attack Chains Format

**Key columns per chain:**
- **Chain ID:** Sequential identifier (AC-01, AC-02, etc.)
- **Severity:** Inherited from component findings
- **Title:** Multi-step exploitation narrative (generic)
- **Components:** Findings that combine (F-C01 + F-C03 + F-C02)

### Validation Metrics to Track

- **Findings Reviewed:** Raw candidates from discovery phase
- **CONFIRMED:** Survived Five-Gates validation
- **OBSERVATION:** Valid patterns but not exploitable in scope
- **REJECTED:** False positives (%)
- **Five-Gates Pass Rate:** Accuracy of validation gating
- **Estimated Exploitation Time:** Time-to-compromise for critical chains

### Agent Performance Reference

**Standard roles:**
- **Vasilisa:** Orchestration + Phase 0 scope definition
- **Volk:** Web application discovery (IDOR, injection, logic flaws)
- **Yaga:** Auth & identity (JWT, OAuth, privilege escalation)
- **Gorynych:** Infrastructure & Cloud Security (secrets, cloud misconfig, K8s, proxy, CI/CD)
- **Leshy:** Codebase Reconnaissance (credentials in source, dependency analysis, supply chain)
- **Koschei:** Synthesis & root cause analysis
- **Mirror:** Validation gate (Five-Gates framework)

Track: spawn time (wall clock), candidate count, confirmed count, accuracy rating.

### Remediation Priority Framework

1. **24 HOURS:** CRITICAL findings with immediate business impact
2. **BEFORE DEPLOYMENT:** Architectural fixes (auth, identity control)
3. **1 WEEK:** HIGH findings (enables lateral movement, data access)
4. **2 WEEKS:** MEDIUM findings (degrades defense-in-depth)
5. **SPRINT BACKLOG:** LOW/OBSERVATION items

---

*The completed report is generated in `reports/PENTEST_REPORT_FINAL.md` during a pentest run; this path is not a record of an earlier engagement.*

---

## NEEDS_MORE_INFO Resolution Policy (Standing Directive)

**Scenario:** Mirror may return NEEDS_MORE_INFO when static analysis cannot establish runtime-dependent facts. The coordinator must resolve outstanding evidence requirements without waiting for agents whose assigned phases are complete.

**Policy — do not block on completed agent phases.** Resolve NEEDS_MORE_INFO findings using the available evidence and the following decision tree:

1. **Evidence exists on disk** at referenced file:lines → resolve as **CONFIRMED** — the codebase is sufficient proof.
2. **Finding depends on runtime configuration** (env vars, feature flags, external service state) → resolve as **CONFIRMED** with an `Observation` note in the report calling out the runtime dependency.
3. **Finding requires external data** (DNS, public endpoint responses, OSINT, network topology) → resolve as **OBSERVATION** — static analysis can't derive this.
4. **Finding references secrets/credentials** → verify with `grep` on disk. Found on disk → **CONFIRMED**. Only in git history → **OBSERVATION**.

**Do not send evidence requests to agents that have already completed.** Record unresolved dependencies explicitly.

