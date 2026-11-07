# Decisions & Handovers

How the squad routes work, makes binding decisions, and passes work between agents.

---

## The Three Core Files

Every agent reads these three at spawn time:

| File | Answers | Example |
|------|---------|---------|
| `team.md` | **Who are we?** — roster, roles, project context | Vasilisa = Lead, Volk = Web, Mirror = Validator |
| `routing.md` | **How does work flow?** — assignment rules, spawn gates, sequential vs parallel | "All 5 discovery agents spawn together after Phase 0" |
| `decisions.md` | **What's committed?** — standing rules that persist across sessions | "NEEDS_MORE_INFO findings resolved without waiting for agents" |

---

## Decisions — How the Team Remembers

### Lifecycle

```
Agent writes → inbox/{agent}-{slug}.md  →  Kot merges → decisions.md  →  Binding
```

1. **Write** — Any agent drops a decision file in `.squad/decisions/inbox/`
2. **Merge** — Kot appends inbox files into `.squad/decisions.md` and deletes inbox files
3. **Read** — Every agent reads `decisions.md` at next spawn. Decisions are binding.

**Inbox files are temporary and gitignored.** Only merged decisions in `decisions.md` are committed and enforceable.

### What Decisions Capture

| Type | Example |
|------|---------|
| **Scope** | "Test all services, no deferral without user approval" |
| **Methodology** | "NEEDS_MORE_INFO findings resolved by decision tree, never wait for agents" |
| **Constraint** | "Static analysis only — no runtime probing" |
| **Permission** | "All agents have unrestricted read access to project root" |

### Why It Matters

Without decisions, every session re-negotiates scope and methodology. With decisions, the coordinator enforces commitments automatically — "routing.md says no deferral, escalating to user."

---

## Handovers — How Work Flows Between Agents

### Three Patterns

| Pattern | When | Example |
|---------|------|---------|
| **Sequential** | Agent B needs Agent A's output | Vasilisa triages → Koschei Phase 2.5 chains → Mirror validates |
| **Parallel** | No data dependency | Volk, Yaga, Gorynych, Leshy, Koschei all discover together |
| **Blocking gate** | One agent must complete before next spawns | Phase 0 complete before discovery agents spawn |

### Pentest Flow

```
Vasilisa (Phase 0, sync)
  → blocks
Volk + Yaga + Gorynych + Leshy + Koschei (parallel discovery)
  → blocks
Vasilisa (triage → vasilisa-triaged-candidates.md, TRC-xx, sync)
  → blocks
Koschei (Phase 2.5 — chain matrix + hop-by-hop verification → koschei-chains.md, CHN-xx, sync)
  → blocks
Mirror (validation of TRC-xx + CHN-xx, sync)
  → blocks
Vasilisa (final report, sync)
  → blocks
Kot (consolidation + TEAM_EXECUTION_SUMMARY.md, background)
```

### Key Rules

- **Discovery agents run in parallel.** Never stagger.
- **Vasilisa triages before Mirror spawns.** Mirror validates Vasilisa's triaged output, not raw candidates.
- **Koschei Phase 2.5 sits between triage and Mirror.** It runs only after `vasilisa-triaged-candidates.md` exists on disk, and writes `koschei-chains.md` (CHN-xx) — even if the answer is "no verified chains."
- **Mirror must not spawn until `koschei-chains.md` exists on disk.** Mirror validates TRC-xx + CHN-xx, never raw discovery files.
- **Kot spawns after Vasilisa's final report.** Pentest is not complete until both `PENTEST_REPORT_FINAL.md` and `TEAM_EXECUTION_SUMMARY.md` exist.
- **Mirror must not spawn in parallel with Vasilisa triage or Koschei Phase 2.5.**

---

## Charter Enforcement

Every agent has a `charter.md` that defines what they own and what they refuse:

| Agent | Owns | Refuses |
|-------|------|---------|
| **Vasilisa** | `PENTEST_REPORT_FINAL.md` | TEAM_EXECUTION_SUMMARY.md |
| **Kot** | `TEAM_EXECUTION_SUMMARY.md` | PENTEST_REPORT_FINAL.md |
| **Mirror** | Five-Gates validation | Discovery work |

**Charters are enforcing, not advisory.** If the coordinator spawns an agent with the wrong task, the agent rejects it.

---

## Anti-Patterns

| Anti-Pattern | What Happens | Fix |
|---|---|---|
| Narration without spawn | "I'll route Volk..." but no `task` call | Call `task` in same response |
| Sequential discovery | Spawn Volk → wait → spawn Yaga | Spawn all 5 together |
| Parallel triage + validation | Spawn Vasilisa + Mirror at same time | Wait for Vasilisa triage, then spawn Mirror |
| Mirror spawned before Phase 2.5 | No `koschei-chains.md` → Mirror stops or re-derives from raw discovery | Wait for Koschei Phase 2.5; verify `koschei-chains.md` exists on disk before spawning Mirror |
| Chaining attempted in discovery batch | Koschei guesses at cross-agent chains before all findings exist | Chaining only in Phase 2.5, on the triaged TRC set |
| Kot skipped | Pentest reported "complete" without TEAM_EXECUTION_SUMMARY.md | Spawn Kot after Vasilisa report |
| Unauthorized deferral | "Leshy deferred to Phase 2" without user approval | Check `decisions.md`, escalate if not there |
| Charter mismatch | Vasilisa asked to generate TEAM_EXECUTION_SUMMARY.md | Reject, route to Kot |
| Waiting for dead agents | Vasilisa sends evidence request, waits forever | Apply NEEDS_MORE_INFO resolution policy |
