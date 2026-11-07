# Output Context Matrix — {AppName}

**Purpose:** Map all endpoints to their output sinks and verify encoding/sanitization is applied. This matrix is the discovery gate — it must be 100% complete before agents begin vulnerability discovery work.

**Filled by:** Vasilisa (Lead) in consultation with Gorynych (app structure) and Kot (logging)

**Date:** {YYYY-MM-DD}

---

## Sink Definitions

| Sink Type | Description | Examples | Risk |
|-----------|-------------|----------|------|
| **HTTP Response (HTML)** | HTML response body with user-controlled content | HTML pages, template rendering | XSS, response splitting, header injection |
| **HTTP Response (JSON)** | JSON response body | API responses, data endpoints | JSON injection, response splitting |
| **HTTP Headers** | Response headers (Location, Set-Cookie, etc.) | Redirects, custom headers | Header injection, redirect injection |
| **Email HTML** | User-facing email body in HTML format | Notifications, receipts, reports | HTML injection, XSS in email clients |
| **Email Plain-Text** | Plain-text email body | Notifications, alerts | Log injection patterns, formula injection |
| **Logs** | Application logs (file, stdout, centralized) | Error logs, audit logs, request logs | Log injection, PII leakage, injection patterns |
| **PDFs** | Generated PDF documents | Reports, invoices, certificates | PDF injection, template issues |
| **External APIs** | Calls to external services | Webhooks, third-party APIs | Payload injection, encoding issues |
| **Redirects** | HTTP redirect responses | POST-redirect-GET, auth flows | Open redirect, host header injection |
| **Browser Storage** | LocalStorage, SessionStorage, Cookies | Session data, preferences | XSS via storage, injection |

---

## Endpoint → Sink Mapping

> **Blank working template.** All entries are placeholders, not findings, tested endpoints, or evidence from a previous engagement. Replace these rows with inventory data from the current authorized codebase.

| Endpoint | HTTP Response (HTML) | HTTP Response (JSON) | HTTP Headers | Email HTML | Email Plain | Logs | PDFs | External APIs | Redirects | Browser Storage |
|----------|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
| {METHOD} {ROUTE} | TBD | TBD | TBD | TBD | TBD | TBD | TBD | TBD | TBD | TBD |

**Legend:**
- TBD = not yet assessed; replace with verified evidence from the current codebase
- ✓ = encoding verified / sanitization applied
- ✗ = encoding missing / gap found
- ? = requires verification
- — = not applicable

---

## Encoding Verification Summary

| Endpoint | Source Data | Sink Type | Validation | Encoding | Status | Finding |
|----------|-------------|-----------|------------|----------|--------|---------|
| {METHOD} {ROUTE} | {INPUT} | {SINK} | TBD | TBD | NOT ASSESSED | — |

Only record a GAP or finding after source-backed analysis and the required validation gates.

---

## Vulnerability Sweep Per Sink Type

### HTTP Response (HTML)
- [ ] XSS (reflected, stored, DOM-based)
- [ ] Response splitting / header injection
- [ ] Content-type confusion
- [ ] Cache poisoning

### HTTP Response (JSON)
- [ ] JSON injection
- [ ] Response splitting via headers
- [ ] Prototype pollution

### Email HTML
- [ ] HTML injection
- [ ] XSS via email client rendering
- [ ] Template injection
- [ ] Encoding gaps (innerHTML vs textContent)

### Logs
- [ ] Log injection (newline + command execution)
- [ ] PII leakage
- [ ] Unsanitized user input in structured logs

### Redirects
- [ ] Open redirect
- [ ] Header injection via Location
- [ ] Method override (POST → GET)

### External APIs
- [ ] Payload injection in webhook body
- [ ] Encoding issues in upstream call
- [ ] Header injection in API calls

---

## Gate Checklist (Must be 100% complete)

- [ ] All unique endpoints enumerated
- [ ] All output sinks mapped for each endpoint
- [ ] For each endpoint-sink pair: encoding/sanitization verified or gap noted
- [ ] For each sink type: vulnerability sweep defined
- [ ] Internal paths (email, logs, notifications) were NOT skipped
- [ ] Kot has signed off on matrix accuracy
- [ ] Vasilisa has approved matrix completeness
- [ ] Ready to spawn discovery agents per sink type

**Matrix Signed Off:**
- Vasilisa (Lead): _____________ Date: _______
- Gorynych (Web Arch): _____________ Date: _______
- Kot (Logging): _____________ Date: _______

---

## Notes

- This matrix is the **discovery gate.** No discovery work begins until Phase 0 is complete.
- Agents are assigned to sink types, not vulnerability classes. This ensures comprehensive coverage per sink.
- "Encoding" means context-appropriate output encoding or sanitization, NOT input validation.
- Internal communication (email, logs, notifications) gets the same rigor as external surfaces.
