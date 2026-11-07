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

| Endpoint | HTTP Response (HTML) | HTTP Response (JSON) | HTTP Headers | Email HTML | Email Plain | Logs | PDFs | External APIs | Redirects | Browser Storage |
|----------|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
| POST /api/notifications | — | ✓ JSON.parse() | — | ✓ HTML template? **ENCODING?** | ✓ subject + body | ✓ audit log | — | Webhook | — | — |
| GET /user/dashboard | ✓ EJS template + escapeHtml() | — | — | — | — | ✓ no PII | — | — | — | LocalStorage |
| POST /auth/login | — | ✓ JSON.stringify() | ✓ Set-Cookie | — | — | ✓ audit log + **PASSWORD?** | — | — | ✓ /dashboard redirect | Session cookie |
| DELETE /account | — | ✓ 204 No Content | — | ✓ Confirmation email | — | ✓ PII audit log | — | Webhook (delete event) | — | — |
| GET /report/export | — | — | ✓ Content-Disposition | — | — | ✓ download log | ✓ User data in PDF | — | — | — |
| GET /redirect?url= | — | — | ✓ **Location header?** | — | — | ✓ redirect log | — | — | ✓ **Open redirect?** | — |

**Legend:**
- ✓ = encoding verified / sanitization applied
- ✗ = encoding MISSING / gap found
- ? = requires verification
- — = not applicable

---

## Encoding Verification Summary

| Endpoint | Source Data | Sink Type | Validation | Encoding | Status | Finding |
|----------|-------------|-----------|-----------|----------|--------|---------|
| POST /api/notifications | customerName (Joi.string()) | Email HTML | ✓ Input validated | ✗ **NO escapeHtml()** | GAP | HTML injection in email |
| POST /api/notifications | customerName | Email Plain | ✓ Input validated | ✓ Plain-text, no encode needed | OK | — |
| POST /api/notifications | message | HTTP JSON | ✓ Input validated | ✓ JSON.stringify() | OK | — |
| GET /user/dashboard | userName | HTTP HTML | ✓ Input validated | ✓ escapeHtml() in template | OK | — |
| POST /auth/login | email + password | Logs | ✓ Input validated | ✗ **PASSWORD IN LOGS** | GAP | PII leakage |
| GET /redirect?url= | url param | HTTP Headers (Location) | ✗ **NO VALIDATION** | — | GAP | Open redirect |

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
- "Encoding" means output-level sanitization (escapeHtml, JSON.stringify, etc.), NOT input validation.
- Internal communication (email, logs, notifications) gets the same rigor as external surfaces.
