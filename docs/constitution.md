# Constitution — rules the AI agent must follow

Binding rules for every agent session working on this lab. They exist to prevent drift: an agent
that silently widens scope, rewrites the assignment, or fabricates a result destroys the value of
the deliverable. A rule may be broken only when it is reported and justified in the conversation
and in [`decisions.md`](decisions.md) (Q-4).

---

## 1. Requirements

| ID | Rule |
|---|---|
| R-1 | `README.md` is the **only** source of requirements. Never invent, extend or "improve" them. |
| R-2 | Anything the README does not state is a **decision**, not a requirement. Stop and ask; log it in `decisions.md`. |
| R-3 | Never edit the professor's ready cells ("pronta", "apenas execute"), nor their wording. |
| R-4 | Never rename identifiers supplied by the scaffold — they are Portuguese on purpose and the ready cells depend on them. |
| R-5 | No new dependency beyond the notebook's existing imports without explicit approval. |

## 2. Deliverable integrity

| ID | Rule |
|---|---|
| D-1 | The delivered notebook must execute top-to-bottom in a clean session. A cell that raises is a defect, not a footnote. |
| D-2 | All outputs must come from real execution. Never hand-write an output; never hardcode a value to make a cell "look right". |
| D-3 | Never present a simulated, guessed or placeholder number as a result. |
| D-4 | Every claim in a written answer must be traceable to a specific cell output. |
| D-5 | If a result contradicts the expected narrative, report the discrepancy — do not smooth it over. |
| D-6 | Seed everything the README says to seed (`random_state=42`); otherwise fix the seed of anything stochastic that affects a reported number. |

## 3. Development cycle

| ID | Rule |
|---|---|
| C-1 | Logic-bearing tasks follow **RED → human review → GREEN → human review → REFACTOR**. |
| C-2 | Tests are written before the implementation, and must fail **for the right reason**. |
| C-3 | GREEN implements the minimum needed to pass the approved tests. No speculative generality. |
| C-4 | REFACTOR must not change behaviour; the suite stays green. |
| C-5 | Download / plot / analysis cells are exempt from unit tests (AI-DW §22) but must be executed and their output inspected before being accepted. |
| C-6 | Automated tests live in `tests/`, never inside the notebook. The notebook must not import them. |

## 4. Human authority

| ID | Rule |
|---|---|
| H-1 | The student approves: the authorial content, the written answers, and every decision the README does not fix. |
| H-2 | The agent never declares a task complete on its own. |
| H-3 | The agent explains, in the conversation, the reasoning behind every non-obvious choice, so the student can defend it orally. |
| H-4 | The agent does **not** run `git commit` or `git push`. It hands over the command sequence instead. |

## 5. Language

| ID | Rule |
|---|---|
| L-1 | Process artifacts — `docs/`, code, comments, identifiers the agent creates, commit messages — are written in **English**. |
| L-2 | Everything the professor reads — the notebook's answers, the Part 6 declaration, `AI_USAGE.md` — is written in **Portuguese**, first person, in the student's voice. |

## 6. Quality

| ID | Rule |
|---|---|
| Q-1 | Written answers: 3 to 6 lines, direct, no filler. |
| Q-2 | No dead code, no commented-out code, no leftover `# TODO` in a cell that was completed. |
| Q-3 | Prefer the simplest expression that satisfies the specification. |
| Q-4 | No silent deviation: any rule broken is reported and justified. |
