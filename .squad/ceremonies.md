# Ceremonies

> Team meetings that happen before or after work. Each squad configures their own.

## Pre-Discovery Sink Inventory

| Field | Value |
|-------|-------|
| **Trigger** | user spawns pentester agents for discovery |
| **When** | before |
| **Condition** | discovery phase starts |
| **Facilitator** | Vasilisa (Lead) |
| **Participants** | Gorynych (Infrastructure & Cloud Security Specialist), Kot (Session Memory & Documentation), Vasilisa |
| **Time budget** | 15-20 min |
| **Enabled** | ✅ yes |
| **Sync** | yes (blocks agent spawn) |

**Purpose:** Prevent discovery category misses by enumerating ALL output sinks before agents begin work.

**Agenda:**

1. **Sink Enumeration (5 min)**
   - Vasilisa lists all output sinks: HTTP response, email HTML, email plain, logs, PDFs, external APIs, redirects, webhooks, caches, browser storage
   - Gorynych adds app-specific sinks (e.g., message queues, database triggers, webhooks)

2. **Endpoint → Sink Mapping (7 min)**
   - For each major endpoint, identify which sinks it writes to
   - Fill in Output Context Matrix (`.squad/templates/output-context-matrix.md`)
   - Gorynych verifies app architecture is correctly represented

3. **Query Parameter Inventory (5 min)**
   - Vasilisa extracts all accepted query parameters per endpoint (grep: `req.query`, `request.args`, `@RequestParam`, etc.)
   - Classify each param HIGH/MEDIUM using query-param-fuzzing skill priority table
   - Append query parameter inventory to Output Context Matrix
   - Flag endpoints with sort/filter/search/path params for mandatory path traversal testing
   - **Gate dependency:** Spawn Gate 3 requires this artifact — cannot skip

4. **Encoding Verification (5 min)**
   - For each endpoint-sink pair, note encoding/sanitization checks
   - Mark gaps (where encoding is missing)
   - **Post-ceremony action:** Koschei's first task after spawn is output encoding verification (uses `output-encoding-verification` skill) — runs alongside discovery, not during ceremony
   - Kot logs the matrix version for audit trail

5. **Gate Sign-Off (3 min)**
   - Vasilisa checks: Are ALL sinks covered?
   - Verify: No internal paths (email, logs) were skipped
   - Verify: Matrix is 100% complete
   - Verify: Query Parameter Inventory is appended to Output Context Matrix
   - **Gate decision:** Ready to spawn agents per sink type? YES / NO

**Output:**
- Completed Output Context Matrix (`.squad/templates/output-context-matrix.md`)
- Coverage Gate Checklist signed off
- File: `.squad/decisions/inbox/pentest-sink-matrix-{timestamp}.md`

**If Gate Fails:**
- No agents spawn until matrix is complete
- Identify missing sinks or endpoints
- Add to matrix and re-run gate

**Agent Assignment (After Gate Passes):**
- Agents are assigned per sink type, not by vulnerability class — Output Context Matrix drives assignment
- Each agent receives sink assignments from the matrix and tests ALL applicable vuln classes for those sinks
- Example: Volk assigned email HTML sink → tests stored XSS, template injection, encoding gaps, HTML injection
- Example: Volk assigned HTTP response sink → tests reflected XSS, redirect injection, response splitting
- Example: Yaga assigned login/sso sinks → tests JWT, OAuth, session, trust boundary, auth bypass at each sink

---

## Design Review

| Field | Value |
|-------|-------|
| **Trigger** | auto |
| **When** | before |
| **Condition** | multi-agent task involving 2+ agents modifying shared systems |
| **Facilitator** | lead |
| **Participants** | all-relevant |
| **Time budget** | focused |
| **Enabled** | ✅ yes |

**Agenda:**
1. Review the task and requirements
2. Agree on interfaces and contracts between components
3. Identify risks and edge cases
4. Assign action items

---

## Retrospective

| Field | Value |
|-------|-------|
| **Trigger** | auto |
| **When** | after |
| **Condition** | build failure, test failure, or reviewer rejection |
| **Facilitator** | lead |
| **Participants** | all-involved |
| **Time budget** | focused |
| **Enabled** | ✅ yes |

**Agenda:**
1. What happened? (facts only)
2. Root cause analysis
3. What should change?
4. Action items for next iteration
