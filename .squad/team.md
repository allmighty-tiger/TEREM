# TEREM Team

> White-Box Security Agent Team

## Coordinator

| Name | Role | Notes |
|------|------|-------|
| TEREM (technical entry point: `squad`) | Coordinator | Routes work, enforces handoffs and reviewer gates. |

## Members

| Name | Role | Charter | Status |
|------|------|---------|--------|
| Vasilisa | Pentest Lead & Orchestrator | `.squad/agents/vasilisa/charter.md` | Active |
| Volk | Web Application Pentester | `.squad/agents/volk/charter.md` | Active |
| Yaga | Authentication & Identity Specialist | `.squad/agents/yaga/charter.md` | Active |
| Gorynych | Infrastructure & Cloud Security Specialist | `.squad/agents/gorynych/charter.md` | Active |
| Leshy | Codebase Reconnaissance Specialist | `.squad/agents/leshy/charter.md` | Active |
| Koschei | Vulnerability Research & Attack-Chain Analysis | `.squad/agents/koschei/charter.md` | Active |
| Mirror | Validator / Verifier | `.squad/agents/mirror/charter.md` | Active |
| Kot | Session Memory & Documentation | `.squad/agents/kot/charter.md` | Active |

## Project Context

- **Project:** TEREM
- **Description:** White-Box Security Agent Team
- **User:** [Operator]
- **Workspace:** ./
- **Methodology:** Evidence-first, validation-gated, parallel discovery, conservative severity
- **Presentation:** Mysterious professional fairy-tale motifs are identity cues only; they never alter scope, evidence standards, handoffs, or verdicts.

## Discovery Methodology: Sink-First Approach

### Coverage Tradeoff: Class-First Discovery

**Class-first method:** Assign agents by **vulnerability class**.
- An agent may focus on one class (for example, XSS, IDOR, or SQL injection) across the application.
- Without a separate sink inventory, entire output channels such as email, PDF generation, and logs may receive insufficient coverage.
- A sink-first inventory complements vulnerability-class expertise by making those coverage gaps explicit.

### The Sink-First Solution

**Sink-first method:** Assign agents by **output sink** (where data exits the app), then test ALL relevant classes per sink

1. **Inventory Phase (Phase 0 — Pre-Discovery):**
   - Enumerate ALL output sinks: HTTP responses, Email HTML, Logs, PDFs, External APIs, Redirects, Caches, etc.
   - Map endpoints → sinks (which endpoints write to which sinks?)
   - Verify encoding at each sink before discovery agents spawn
   - Deliverable: Output Context Matrix (100% complete before agents start)

2. **Discovery Phase (Per-Sink):**
   - Discovery agents are assigned per sink type, not per vulnerability class
   - Example: An agent assigned to email HTML sinks tests HTML injection, XSS, template issues, encoding gaps
   - Example: An agent assigned to HTTP response sinks tests XSS, redirect injection, response splitting, header injection
   - Each agent applies ALL vulnerability classes to their assigned sink → comprehensive coverage

3. **Validation Phase:**
   - Findings reported to Validator (Mirror) per standard gate
   - Cross-verification before escalation

### Why Sink-First Works Better

| Aspect | Class-First | Sink-First |
|--------|-------------|-----------|
| **Coverage** | Vulnerability classes across the app | ALL sinks reviewed, each sink exhaustively tested |
| **Prioritization bias** | Certain classes may dominate the review | All in-scope sinks inventoried before prioritization |
| **Internal paths** | Risk of under-review without a separate inventory | Explicitly inventoried, same rigor as external |
| **Multi-layer chains** | Hard to trace across files | Sink-first requires tracing all paths TO the sink |
| **Encoding verification** | Input validation checked only | Both input validation AND output encoding verified |
| **Blind spots** | Possible unrecorded sink coverage gaps | Explicit gap visibility via matrix |

### Hypothetical Coverage Example

Consider an illustrative application that renders user-controlled text in both HTTP pages and email HTML. Reviewing only HTTP response paths could overlook output encoding at the email sink. A sink-first inventory explicitly includes both output channels and requires context-appropriate encoding checks for each. This is a methodology example, not a recorded finding.

## Pre-Discovery Checklist Addition

Add the following item to the Phase 0 standard checklist (before spawning discovery agents):

```
□ Query Parameter Inventory (NEW)
  - For each route in scope, extract all accepted query parameters from:
    a) Source code (grep: req.query, request.args, @RequestParam, etc.)
    b) API specification (OpenAPI/Swagger query param definitions)
    c) Frontend code (URL construction, axios/fetch calls with params: {})
  - Classify each param using the HIGH/MEDIUM priority table (see query-param-fuzzing skill)
  - Add HIGH-priority query params to the injection test matrix BEFORE agent spawn
  - Flag any endpoint with sort/filter/search/path params for mandatory path traversal testing
  - Expected output: Query Parameter Inventory (appended to Output Context Matrix)
```

This ensures query parameters are systematically tested alongside body parameters and reduces the risk of overlooking injection vectors that are exposed through query strings.

### Implementation

- **Vasilisa (Lead):** Runs Phase 0 (sink inventory ceremony) and ensures the Query Parameter Inventory is produced and appended to the Output Context Matrix before discovery agents spawn.
- **Discovery Agents (Volk, Yaga, Gorynych, Leshy, Koschei):** Read the Query Parameter Inventory at spawn time and include HIGH-priority query parameter test vectors in their per-endpoint test matrices.
- **Volk & Koschei coordination:** Volk focuses on web-specific vectors (path traversal, SQLi, SSTI via query params); Koschei cross-references findings and helps synthesize chaining opportunities.
- **Mirror (Validator):** Verifies that HIGH-priority query parameters were exercised per the Five-Gates validation (source evidence, attack flow, reproducibility).
- **Kot:** Ensures any decision or new skill evidence is recorded in the decisions inbox for team memory.

---

**Decision:** All future pentests use sink-first discovery and include a Query Parameter Inventory as a mandatory Phase 0 artifact. Vasilisa enforces this via the pre-discovery ceremony.
