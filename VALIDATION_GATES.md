# Decisions & Handovers — TEREM

This document explains the team's key architectural decisions and how handoffs between agents reduce false positives and maintain findings quality.

---

## 🔬 Mirror — Validator / Verifier (Five-Gates)

### Problem: False Positives in Security Testing

Static analysis tools naturally produce **high false-positive rates** — code patterns can look vulnerable without being exploitable. Raw findings aren't ready for user presentation. We needed a **validation gate** before escalation.

### Solution: Five-Gates Verification Framework

**Mirror is our dedicated Validator/Verifier.** Every candidate finding from discovery agents passes through **five sequential gates** before approval. Failure at any gate triggers downgrade or rejection.

---

## The Five Gates — Conservative Verification

### Gate 1: Source Code Verification

**Question:** Is the claimed issue actually in the code?

- ✅ Verify exact file path and line number
- ✅ Confirm the code contains the pattern described
- ✅ Trace the code path: is it reachable from a user-facing endpoint?
- ❌ **Fail:** REJECTED (source doesn't match claim)

**Example:** Candidate says "HTML injection in template rendering." Mirror checks:
- Does `/templates/email.js` line 42 actually render HTML without escaping?
- Is that template called from an endpoint?
- Or is it dead code / internal-only / already deprecated?

**False Positive Prevention:** Dead code, unreachable paths, and internal-only functions are caught here.

---

### Gate 2: Attack Flow Validation

**Question:** Is the attack sequence realistic?

- ✅ Trace the attack from attacker input → vulnerable code → impact
- ✅ Verify all preconditions are achievable (e.g., "requires valid JWT" is different from "requires stealing JWT")
- ✅ Confirm the flow matches the static evidence
- ⚠️ **Inconclusive → OBSERVATION** (interesting, but not reliably exploitable)

**Example:** Candidate says "IDOR — user can change another user's role." Mirror checks:
- Can an attacker reach the endpoint? (public? authenticated?)
- What ID parameter does the attack use?
- Are there permission checks? (role-based auth, ownership verification?)
- Or is the endpoint already protected by a wrapper that's hard to spot?

**False Positive Prevention:** Misunderstanding permission checks, role-based auth, and framework-level protections caught here. Many "vulnerabilities" are actually gated by auth layers discoverers missed.

---

### Gate 3: Severity Calibration

**Question:** Does the claimed severity match the actual impact?

- ✅ Verify CRITICAL claims have clear privilege escalation OR multi-user data access
- ✅ Check if mitigations exist in code (rate limiting, input validation, output encoding)
- ✅ Assess real-world exploitability vs. theoretical risk
- ❌ **Downgrade:** HIGH → MEDIUM, CRITICAL → HIGH if impact is overstated

**Example:** Candidate says "CRITICAL: Arbitrary file upload — unauthenticated RCE." Mirror checks:
- Is the endpoint really unauthenticated, or does the auth check sit elsewhere?
- Are uploaded files executable, or are they stored in a read-only directory?
- Is there antivirus scanning or file type validation?
- → Maybe it's MEDIUM risk (authenticated users only, files not executable)

**False Positive Prevention:** Severity inflation caught here. Many high-sounding claims don't hold up to code review.

---

### Gate 4: False Positive Likelihood & Mitigations

**Question:** Is this a known false positive pattern?

- ✅ Check for framework protections (e.g., Django CSRF, Express CORS middleware)
- ✅ Look for upstream sanitization or output encoding (e.g., `escapeHtml()` already applied)
- ✅ Verify the code path isn't mitigated by defense-in-depth
- ❌ **Reject:** Framework defaults, sanitized output, or legacy/dead code

**Example:** Candidate says "XSS via user input in HTTP response." Mirror checks:
- Is there a templating engine that auto-escapes by default? (many do)
- Did discoverers miss the `renderTemplate('safe')` configuration?
- Is the variable actually rendered in HTML context, or in an escaped context?
- → Likely REJECTED as false positive due to framework auto-escaping

**False Positive Prevention:** This is where discoverers' false positives die. Common patterns:
- Framework auto-escaping (Django, Vue, React all escape by default)
- Context-aware encoding libraries that discoverers miss
- Sanitization libraries used upstream
- Dead code or deprecated endpoints

---

### Gate 5: Reproducibility & Manual PoC for User Verification

**Question:** Can the user verify this themselves?

- ✅ PoC steps must be unambiguous and minimal
- ✅ User can follow steps MANUALLY (no automated exploit execution)
- ✅ Artifact evidence is sufficient for a developer to locate and fix
- ✅ Prerequisites are documented (auth level, app state, assumptions)
- ⚠️ **Inconclusive:** Request additional PoC detail from discoverers

**Example:** Candidate says "Reflected XSS in search parameter." PoC should be:
```
1. Go to https://app.example.com/search?q=<img src=x onerror=alert('XSS')>
2. Observe browser console shows 'XSS' alert
3. Source file: app/handlers/search.js line 42 — `res.send(query)` without escaping
```

NOT: "Run this Node.js exploit script that uses Puppeteer to execute JavaScript and prove RCE."

**False Positive Prevention:** This ensures findings are actually exploitable in practice, not just theoretically vulnerable.

---

## Verdict Outcomes

After all five gates, Mirror assigns ONE of three verdicts:

| Verdict | Meaning | Action |
|---------|---------|--------|
| **CONFIRMED** | Passes all gates. No upstream mitigation. Ready for user. | Add to final report with recommended severity. |
| **OBSERVATION** | Interesting pattern but doesn't meet vulnerability criteria (edge case, defense-in-depth, low likelihood). | Track for awareness; don't publish. |
| **REJECTED** | False positive, mitigated, or insufficient evidence. | Discard. No user escalation. |

---

## Example: How False Positives Get Caught

### Real Case: HTML Injection in Email Template

**Discovery Agent reports:**
> "Found HTML injection vulnerability in email rendering. User input `customerName` is embedded in email template without escaping. CRITICAL."

**Mirror's Five-Gates Review:**

1. **Gate 1 (Source):** ✅ PASS
   - File `/src/email/account-notification.js` line 18 found
   - Code: `<p>Account notification for ${customerName}</p>`
   - Endpoint `/api/notify-user` calls this template

2. **Gate 2 (Attack Flow):** ✅ PASS
   - Attacker provides malicious `customerName` parameter
   - Parameter flows to template
   - Email renders with HTML interpretation
   - Flow is achievable

3. **Gate 3 (Severity):** ⚠️ DOWNGRADE
   - Email sent to INTERNAL staff (admin/ops), not public users
   - Scope: internal HTML injection, not user-facing XSS
   - Impact: less severe than public-facing XSS
   - **Downgrade from CRITICAL → HIGH**

4. **Gate 4 (False Positive):** ✅ PASS
   - Check for framework mitigation: none (Node.js template literals)
   - Check for upstream encoding: none detected
   - NOT a false positive (real code pattern)

5. **Gate 5 (Reproducibility):** ✅ PASS
   - PoC is clear: send request with `customerName=<img src=x onerror=alert('XSS')>`
   - Email renders with JavaScript execution
   - User can verify by examining email template and input flow

**Mirror's Verdict:** CONFIRMED
> "Passes all gates. HTML injection in internal email template. **Severity: HIGH** (downgraded from CRITICAL due to internal-only scope). Root cause: Missing escapeHtml() in template. Developer fix: Apply escapeHtml(customerName) per precedent elsewhere in the codebase."

---

## Why This Approach Reduces False Positives

| Common False Positive Type | Caught By | Example |
|---------------------------|-----------|---------|
| **Framework auto-escaping misses** | Gate 4 | Django templates auto-escape; discoverer didn't notice |
| **Unreachable code** | Gate 1 | Dead endpoint, deprecated route |
| **Already-mitigated by upstream layer** | Gate 4 | Input validation at controller; discoverer only saw data access |
| **Severity inflation** | Gate 3 | "CRITICAL RCE" that requires admin auth + file must be executable |
| **Conceptual flaw in attack chain** | Gate 2 | Attack theoretically works in isolation but middleware blocks it |
| **Non-reproducible patterns** | Gate 5 | Finding looks vulnerable on paper but can't be demonstrated |

---

## Conservative Verdicts: Why Mirror Rejects Uncertain Findings

Mirror operates under one principle: **When uncertain, downgrade or reject.**

**Rationale:**
- False positives damage user trust more than false negatives
- User will lose confidence in 10 real findings if surrounded by 5 fake ones
- Better to miss an edge-case vulnerability than to alarm the user with noise
- Discoverers can refine and re-submit rejected findings with stronger evidence

**Example decision tree:**
```
Candidate: "SQL Injection possible in query builder"
  ↓
Gate 1 (Source): ✅ Found code that builds SQL
Gate 2 (Attack Flow): ⚠️ Unclear if attacker can control the variable
Gate 3 (Severity): ? Can't assess without knowing if it's exploitable
Gate 4 (False Positive): ⚠️ Might be protected by ORM layer
Gate 5 (Reproducibility): ❌ Can't write a PoC — too unclear

Result: REJECTED
Reason: "Inconclusive attack flow. Discovery agents should clarify how attacker controls this variable before re-submitting. Check for ORM protection layers first."
```

---

## Handoff Protocol: Discovery → Validation → Report

```
┌─────────────────────────────────────┐
│  Discovery Agents (Volk, Yaga,    │
│  Gorynych, Leshy, Koschei)               │
│  ↓ Report candidates to Vasilisa     │
└─────────────────────────────────────┘
         ↓
┌─────────────────────────────────────┐
│  Vasilisa (Lead)                     │
│  Triage → TRC-xx set                │
│  (vasilisa-triaged-candidates.md)    │
└─────────────────────────────────────┘
         ↓
┌─────────────────────────────────────┐
│  Koschei (Phase 2.5, gated)            │
│  Chain matrix + per-hop verification│
│  ↓ CHN-xx (koschei-chains.md)          │
└─────────────────────────────────────┘
         ↓  (Mirror blocked until BOTH files exist on disk)
┌─────────────────────────────────────┐
│  Mirror (Validator)                  │
│  Five-Gates on TRC-xx + CHN-xx      │
│  ↓ Returns verdicts (CONFIRMED/     │
│    OBSERVATION/REJECTED)            │
└─────────────────────────────────────┘
         ↓
┌─────────────────────────────────────┐
│  Vasilisa (Lead)                     │
│  - Uses CONFIRMED findings          │
│  - Tracks OBSERVATION findings      │
│  - Discards REJECTED findings       │
│  ↓ Reports to user                  │
└─────────────────────────────────────┘
```

**Key feature:** Validation happens BEFORE presentation to user. User only sees findings that pass all five gates.

---

## Quality Metrics

### What Success Looks Like

- **Low false-positive rate:** <5% of reported findings are rejected at validation
- **Accurate severity:** Most findings keep their original severity; downgrades are justified
- **Reproducible findings:** Every CONFIRMED finding includes a clear manual PoC
- **User trust:** User confidence in findings remains high across sessions

### Common Metrics Tracked

- % of candidates passing Gate 1 (source verification)
- % of candidates passing Gate 2 (attack flow)
- Average severity downgrade at Gate 3 (typically HIGH → MEDIUM if mitigations exist)
- % rejected at Gate 4 (false positive catch rate)
- % requiring PoC refinement at Gate 5 (reproducibility gaps)

---

## Why Validation Is Not Optional

Without validation:
- ❌ User receives hundreds of low-confidence findings
- ❌ User loses trust after first false positive
- ❌ Team's credibility suffers

With validation:
- ✅ User receives only high-confidence findings
- ✅ Each finding is backed by verified code evidence
- ✅ Severity is accurate, not inflated
- ✅ Every finding is reproducible by user
- ✅ Team maintains high credibility across sessions

---

## Decision: Five-Gates Validation Is Standard

**This team operates under a binding decision:**

> Every finding from discovery agents MUST pass Mirror's Five-Gates verification before presentation to the user. No exceptions. Bypassing validation is not permitted.

**Rationale:**
- Maintains user trust through low false-positive rate
- Ensures findings are code-backed and reproducible
- Allows severity downgrade when evidence is weak
- Prevents alarm fatigue from inflated or theoretical vulnerabilities

**Enforcement:**
- Vasilisa routes all candidates to Mirror
- Mirror applies all five gates before releasing verdict
- Only CONFIRMED findings reach the final report
- REJECTED findings are discarded; OBSERVATION findings are tracked separately

---

## Evolution: How Validation Improves Over Time

Mirror's verdicts inform future discovery:

1. **Session N:** Discovery agent reports finding → Mirror rejects (false positive pattern detected)
2. **Session N+1:** Mirror writes pattern to history: "Common false positive: framework auto-escaping in template render calls"
3. **Session N+2:** Discoverers read pattern, adjust their heuristics, avoid the false positive class

This is why validation improves accuracy across sessions — rejected findings teach discoverers what NOT to report.

---

**This document is the authoritative explanation of Mirror's validation approach. Use it to justify validation quality to stakeholders.**
