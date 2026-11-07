# Work Routing — TEREM

How to decide who handles pentest work.

## Pentest Routing Table

| Work Type | Route To | Examples |
|-----------|----------|----------|
| Pentest scoping & orchestration | **Vasilisa** (Pentest Lead & Orchestrator) | "Run a pentest on the codebase", "What's the pentest status?", prioritize findings |
| Sink-first web discovery — assigned per output sink, tests ALL web vuln classes per sink (XSS, IDOR, SSRF, SQLi, RCE, etc.) | **Volk** (Web Application Pentester) | Given the email HTML sink, test for stored XSS, template injection, encoding gaps, HTML injection; given the HTTP response sink, test for reflected XSS, redirect injection, response splitting |
| Sink-first auth & identity — assigned per auth sink (login flows, token handling, session stores, SSO callbacks), tests ALL auth classes per sink | **Yaga** (Authentication & Identity Specialist) | Auth bypass, token handling, trust boundaries, privilege escalation paths at each auth-related sink |
| Sink-first infrastructure — assigned per infra sink (proxy configs, container manifests, CI/CD pipelines, cloud configs), tests ALL infra classes per sink | **Gorynych** (Infrastructure & Cloud Security Specialist) | Hardcoded credentials, cloud misconfig, K8s RBAC, proxy header forwarding, CI/CD supply chain at each infrastructure sink |
| Codebase reconnaissance — assigned per sink, traces data flows across sinks to find topology and supply chain risks | **Leshy** (Codebase Reconnaissance Specialist) | Hardcoded credentials, dependency ecosystem, internal service topology, supply chain risks |
| Vulnerability synthesis & attack-chain analysis — assigned per sink cluster, chains findings across sinks | **Koschei** (Vulnerability Research & Attack-Chain Analysis) | Cross-reference findings, trace root causes, identify chaining opportunities, output encoding verification |
| Validator gate & false-positive reduction | **Mirror** (Validator / Verifier) | Five-Gates review of all findings, severity calibration, PoC validation |
| Session logging & decision consolidation | **Kot** (Session Memory & Documentation) | Automatic after work — orchestration logs, decision merging, history updates |

## Pentest Workflow

1. **User says: "Run a pentest on {codebase}"**
   - Coordinator spawns **Vasilisa** (sync) to plan scope and run Phase 0 (Output Sink Inventory)
   - **BLOCKING GATE:** Discovery agents (Volk, Yaga, Gorynych, Leshy, Koschei) MUST NOT be spawned until Vasilisa marks Phase 0 complete by updating `.squad/decisions/inbox/vasilisa-phase0-complete.md` with a "Phase 0 complete: <summary>" line and timestamp
   - Once Phase 0 is marked complete, the Coordinator spawns **ALL FIVE discovery agents in a single batch**: **Volk** + **Yaga** + **Gorynych** + **Leshy** + **Koschei** (all background, parallel)
   - Each agent reads relevant skills before starting: Volk (web app), Yaga (auth), Gorynych (infrastructure/cloud), Leshy (OSINT/recon), Koschei (synthesis/research)
   - **Koschei in the discovery batch does per-sink deep analysis only** (root cause, output-encoding verification, CVE context). It does NOT attempt cross-agent chaining while the other agents are still running in parallel — chaining is the dedicated Phase 2.5 after triage
   - All discovery agents report candidates to Vasilisa (not directly to user)

2. **Discovery agents complete & report candidates to Vasilisa**
   - Vasilisa triages candidates: deduplicates, groups by category, severity, confidence
   - Vasilisa writes EXACTLY ONE triage file: `.squad/decisions/inbox/vasilisa-triaged-candidates.md` — every surviving candidate as a `TRC-xx` entry (id, root cause, attack flow, severity guess, merged `file:line` evidence, source agents)
   - **BLOCKING GATE: neither Koschei Phase 2.5 nor Mirror may spawn until this file exists on disk.** The coordinator MUST verify the file on disk, not trust a completion notification.

3. **Koschei Phase 2.5 — Chain & Cross-Verification (dedicated, gated)**
   - **BLOCKING GATE: Koschei Phase 2.5 must NOT spawn until `.squad/decisions/inbox/vasilisa-triaged-candidates.md` exists on disk.** Triage complete unblocks Phase 2.5, not Mirror.
   - Coordinator spawns Koschei once with the Phase 2.5 mission:
     1. **Cross-verify the TRC set** — flag where agents' claims conflict (same sink, same claim, different conclusion)
     2. **Build the chain matrix** — every candidate whose output an attacker controls (or whose state an attacker changes) × every candidate whose input or state it could feed. Include cross-sink pairs and auth-state transitions (session change, stored object, redirect target, cache) — the worst chains are cross-sink by construction
     3. **Verify each candidate chain hop-by-hop in code** — `file:line` evidence per hop, and confirm no control (auth check, encoding, ownership check) breaks the flow between hops. A chain that cannot be traced end-to-end in code is marked **unverified** — it is never a finding
   - Koschei writes `.squad/decisions/inbox/koschei-chains.md`: `CHN-xx` entries, each referencing its `TRC-xx` components, with per-hop evidence, one manual end-to-end PoC a human can execute across the hops, and severity by **END STATE** (not component severities). If no chains survive verification, the file must still exist and say "no verified chains" with the near-misses marked unverified.

4. **Mirror verifies & returns verdicts**
   - **BLOCKING GATE: Mirror must NOT spawn until BOTH `.squad/decisions/inbox/vasilisa-triaged-candidates.md` AND `.squad/decisions/inbox/koschei-chains.md` exist on disk.** Verify on disk before spawning. Mirror validates the TRC-xx set and the CHN-xx chains — never raw discovery candidates.
   - CONFIRMED: ready for user presentation
   - OBSERVATION: interesting but not a vulnerability
   - REJECTED: false positive or insufficient evidence

5. **Vasilisa assembles final report**
   - CONFIRMED findings ranked by severity
   - OBSERVATIONS listed separately
   - RECON findings (from Leshy) contextualized for remediation
   - Gaps and unreviewed surfaces called out
   - Report delivered to user

6. **Kot consolidates memory and produces TEAM_EXECUTION_SUMMARY.md**
   - **BLOCKING GATE: Coordinator MUST spawn Kot after Vasilisa final report is complete.** Do not skip this step.
   - Kot task: orchestration logs, decision inbox merge, session log, cross-agent history updates, coverage report
   - **Kot MUST also generate `reports/TEAM_EXECUTION_SUMMARY.md`** per charter (mandatory deliverable after validation complete)
   - Session is NOT considered "pentest complete" until both `PENTEST_REPORT_FINAL.md` AND `TEAM_EXECUTION_SUMMARY.md` exist

## Key Rules for Pentest Work

1. **Discovery agents run in parallel.** Volk does NOT wait on Yaga; Yaga does NOT wait on Volk.
2. **Static analysis only** by default. No runtime execution, no live probing, no external calls unless explicitly approved.
3. **Findings route through the validator.** Never present unvalidated findings to the user.
4. **Vasilisa orchestrates and does NOT do discovery.** Vasilisa owns coordination, triage, and final prioritization.
5. **Exact file:line evidence required.** Every candidate must cite the exact source code location.
6. **Conservative posture.** When uncertain, demote or reject. False positives damage credibility.
7. **Gap reporting.** Unread surfaces or uncertain areas must be called out — no silent gaps.
8. **Mirror MUST NOT spawn until Vasilisa triage is complete AND Koschei Phase 2.5 has produced `koschei-chains.md`.** The order is fixed: Vasilisa triages (writes `vasilisa-triaged-candidates.md`) → Koschei Phase 2.5 chains on the TRC set (writes `koschei-chains.md`) → Mirror validates both. Never spawn Vasilisa and Mirror in parallel. Never spawn Mirror from raw discovery output or from the triage file alone.
9. **Kot MUST spawn after Vasilisa's final report.** The coordinator MUST spawn Kot for memory consolidation AND `TEAM_EXECUTION_SUMMARY.md` generation. A pentest is not "complete" until both report files exist. Never skip Kot.
10. **Cross-agent chaining happens ONLY in Koschei's Phase 2.5.** In the discovery batch Koschei does per-sink deep analysis (root cause, encoding, CVE context) — no chaining while the other agents are still running. Phase 2.5 runs after triage and before Mirror, and is the single point where chains are built and verified hop-by-hop.

## Mandatory Routing Gates

**These gates are AUTHORITATIVE routing rules. The Coordinator MUST apply them before every spawn decision.**

### Gate 1: Charter Mandatory Deliverables — ENFORCED

| Agent | Mandatory Deliverables | Ownership Check |
|-------|------------------------|-----------------|
| **Vasilisa** | `PENTEST_REPORT_FINAL.md` (comprehensive technical report with enforced template) | If task is "generate TEAM_EXECUTION_SUMMARY.md" → **REJECT** and route to **Kot** |
| **Kot** | `TEAM_EXECUTION_SUMMARY.md` (team execution summary) | If task is "generate PENTEST_REPORT_FINAL.md" → **REJECT** and route to **Vasilisa** |
| **Leshy** | Infrastructure findings integration into final reports | If findings are deferred/marked "pending" without user authorization → **REJECT** and escalate |

**Coordinator Enforcement:** Before spawning any agent for report work, read their charter's "Mandatory Deliverables" section. If the spawn assignment doesn't match the charter, **BLOCK THE SPAWN** and clarify with the user.

**Agent Enforcement:** Each agent's charter contains a "## Verification Gate" section. If an agent receives a spawn that violates the gate, the agent MUST reject it explicitly.

### Gate 2: Scope Authorization — NO UNAUTHORIZED DEFERRALS

**Rule:** Scope is "as wide as possible per skill" unless the user explicitly authorizes a limitation in `.squad/decisions.md`.

| Scenario | Action |
|----------|--------|
| User says "run a pentest on the codebase" | Scope = ALL agent skills apply (Web, Auth, Infrastructure, OSINT, Synthesis) |
| User says "defer Leshy to Phase 2" | **ALLOWED** — explicitly authorized |
| User says "focus on web first, do auth later" | **ALLOWED** — explicitly authorized |
| Coordinator marks "Leshy pending / separate engagement" without user approval | **NOT ALLOWED** — unauthorized deferral |
| Coordinator defers findings without documenting in `.squad/decisions.md` | **NOT ALLOWED** — undocumented scope change |

**Coordinator Check:** Before marking any agent's findings as "deferred" or "pending," verify that this deferral is:
1. Explicitly documented in `.squad/decisions.md` as a user-authorized scope limitation, OR
2. Explicitly approved by the user in the current session

### Gate 3: Spawn Completeness — ALL AGENTS IN ONE BATCH

**Rule:** Discovery agents (Volk, Yaga, Gorynych, Leshy, Koschei) MUST spawn together in a single parallel batch. Never stagger. Never omit.

| Failure Mode | Consequence |
|--------------|------------|
| Coordinator announces agent spawn but doesn't call `task` tool | Agent was NOT spawned. Work didn't happen. |
| Coordinator spawns Volk but defers Leshy/Koschei to later | Synthesis phase is crippled. Cross-domain patterns missed. |
| Coordinator skips any discovery agent | Entire vulnerability classes may be missed (e.g., IDOR if Volk is skipped) |

**Coordinator Enforcement:**
- Before spawning discovery agents, read `.squad/routing.md` § Pentest Workflow step 1
- Verify Vasilisa Phase 0 is complete (blocking gate applies)
- Call `task` tool for **ALL FIVE agents in one batch**: Volk + Yaga + Gorynych + Leshy + Koschei
- If you announce a spawn without calling `task`, the work did NOT happen

### Gate 4: Phase 2.5 & Mirror Gate — CHAINING BEFORE VALIDATION

**Rule:** The pipeline order `triage → Koschei Phase 2.5 → Mirror` is fixed. Mirror never sees raw discovery candidates, and Koschei never chains during the discovery batch.

| Checkpoint | Blocking Condition | Verified By |
|------------|--------------------|-------------|
| Koschei Phase 2.5 spawn | `.squad/decisions/inbox/vasilisa-triaged-candidates.md` exists **on disk** | Coordinator lists the file before spawning Koschei |
| Mirror spawn | BOTH `vasilisa-triaged-candidates.md` AND `koschei-chains.md` exist **on disk** | Coordinator lists both files before spawning Mirror |

| Failure Mode | Consequence |
|--------------|------------|
| Koschei spawned before triage completes | No TRC set to chain against — Phase 2.5 is a no-op or guesses |
| Mirror spawned without `koschei-chains.md` | Chains never validated; or Mirror re-derives candidates from raw discovery files, defeating triage |
| Coordinator skips Phase 2.5 because "no obvious chains" | Chaining never happened — `koschei-chains.md` must still exist ("no verified chains") for the gate to pass |
| Mirror spawns when only one of the two input files exists | Mirror MUST stop and report the missing input — do not guess |

**Coordinator Enforcement:**
- Before spawning Koschei Phase 2.5: verify `vasilisa-triaged-candidates.md` exists on disk
- Before spawning Mirror: verify BOTH files exist on disk (a completion notification is NOT evidence — check the filesystem)
- If Koschei reports "no chains," confirm `koschei-chains.md` exists with "no verified chains" content before spawning Mirror

## Discovery Spawn Gate (MANDATORY VERIFICATION)

**COORDINATOR ENFORCEMENT:** The coordinator MUST verify ALL seven conditions BEFORE spawning any discovery agent. If ANY condition fails, BLOCK spawn and report to user which condition failed.

**Gate Conditions (hardcoded routing rule — not optional):**

1. **Vasilisa Phase 0 COMPLETE** — Both Output Sinks AND Logic Sinks inventoried
   - *Check:* `.squad/agents/vasilisa/history.md` contains entry "## Phase 0 Complete" with timestamp
   - *Failure mode:* Discovery agents spawn without knowing auth entry points or authorization gates → repeat critical auth-bypass misses
   
2. **Output Context Matrix provided** — All endpoints mapped to their output sinks
   - *Check:* Vasilisa's Phase 0 report lists endpoints and response sinks
   - *Failure mode:* Agents miss data exfiltration vectors (logs, emails, error responses)

3. **Query Parameter Inventory provided** — All query params classified by injection risk
   - *Check:* Vasilisa's Phase 0 report lists query params per endpoint, classified by HIGH/MEDIUM priority (sort, filter, search, path, pagination, etc.)
   - *Failure mode:* Query parameter injection vectors (path traversal, SQLi, LDAP, SSTI, SSRF) missed during discovery
   - *Reference:* `.squad/skills/query-param-fuzzing/SKILL.md` for classification and test protocol

4. **Auth/Authz Gate Inventory provided** — All authentication and authorization code paths identified
   - *Check:* Vasilisa's Phase 0 report lists auth entry points, privilege checks, access control boundaries
   - *Failure mode:* Agents miss auth bypass, identity spoofing (critical), IDOR (high)

5. **Volk scope verified** — Assigned to: IDOR, mass assignment, SSRF, SQLi, RCE, query parameter injection, logic flaws (never JUST XSS)
   - *Check:* Coordinator confirms Volk's charter or spawn prompt includes IDOR and query parameter testing as priority
   - *Failure mode:* IDOR vulnerabilities skipped (missed in previous run); query params not tested

6. **Yaga scope verified** — Assigned to: JWT, OAuth, session management, auth bypass, access control, privilege escalation (never email)
   - *Check:* Coordinator confirms Yaga's charter or spawn prompt assigns Auth & Identity (not other domains)
   - *Failure mode:* Authentication/authorization review skipped, critical auth-bypass misses repeated

7. **All 5 agents spawn together** (Volk, Yaga, Gorynych, Leshy, Koschei) — Never stagger spawn or omit agents
   - *Check:* Coordinator spawns all 5 as one batch in a single turn
   - *Failure mode:* Agents miss cross-domain patterns; Phase 2.5 chaining (step 3) works from an incomplete candidate set

**BLOCKING RULE:** If the coordinator detects that Vasilisa Phase 0 did not complete, the coordinator MUST refuse to spawn Volk/Yaga/Gorynych/Koschei. Report: `"⚠️ Phase 0 incomplete. Vasilisa must finish Output + Logic Sink inventory before discovery agents spawn."`

**Violation consequence:** Repeat of current pentest: agents spawn without complete sink inventory → Auth & Identity, IDOR, and Authorization vulnerabilities remain undiscovered.

## Escalation & Disputes

- If Volk and Yaga claim the same finding, Vasilisa resolves and deduplicates.
- If Mirror rejects a finding, Vasilisa records it and explains the reasoning (for team learning).
- If user wants to override a validation verdict, user tells Vasilisa → Vasilisa reconsiders with Mirror.

## Multi-Phase Pentest

For large codebases, pentests may split into phases:

| Phase | Scope | Lead | Contributors |
|-------|-------|------|--------------|
| Phase 0 | Sink Inventory & Spawn Gates | Vasilisa | (blocks Phase 1–4) |
| Phase 1 | Web app sinks — all output sinks assigned to Volk, each tested for all web vuln classes | Volk | Koschei (synthesis), Mirror (validation) |
| Phase 2 | Auth sinks — all auth-related sinks assigned to Yaga, each tested for all auth classes | Yaga | Koschei (synthesis), Mirror (validation) |
| Phase 3 | Infrastructure sinks — all infra sinks assigned to Gorynych, each tested for all infra classes | Gorynych | Koschei (synthesis), Mirror (validation) |
| Phase 4 | Deep analysis & chaining across sink clusters | Koschei | Mirror (final validation) |

Vasilisa prioritizes phases and manages discovery order. Leshy runs continuously in parallel with all discovery phases.
