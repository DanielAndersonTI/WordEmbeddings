# Tasks — Word Embeddings Lab

Decomposition of [`specification.md`](specification.md) into small, executable tasks.
**Cycle** is either `light` (spec + execute + inspect the output) or `full` (RED → review → GREEN →
review → REFACTOR), following AI-DW §22 and Constitution C-1/C-5.

Gates are batched to keep the Lite profile lean (decision D-07): the two REDs are reviewed
together, then the two GREENs. Finer gates are available on request.

---

## 1. Board

| ID | Task | Cycle | Depends on | Gate |
|---|---|---|---|---|
| T-00 | Environment and data: venv, dependencies, GloVe 50/100 + text8 in the gensim cache | light | — | — |
| T-01 | Notebook skeleton: rebuild the `.ipynb` preserving the ready cells; snapshot the baseline for the final diff | light | — | — |
| T-02 | `avaliar_analogias` (Part 2.1) | **full** | T-00, T-01 | **G-2** |
| T-03 | Part 1.2 comparison table + per-category chart | light | T-00 | — |
| T-04 | Authorial analogy set: ≥12 across ≥3 categories, OOV-checked | content | T-02 | **G-4** |
| T-05 | `doesnt_match`: 6 groups (3 easy, 3 hard) | content | T-00 | **G-4** |
| T-06 | Polysemy: 3 extra ambiguous words + sense subtractions | content | T-00 | **G-4** |
| T-07 | Visualization: 5 categories × 8 words, PCA + t-SNE (2×2) | light | T-00 | — |
| T-08 | Relation pairs (≥6) drawn as arrows with `plotar_relacoes` | content | T-00 | **G-4** |
| T-09 | Gender axis + profession projections (Part 5.1) | **full** | T-00, T-01 | **G-3** |
| T-10 | Gender sanity controls (4 gendered + 4 neutral words) | light | T-09 | — |
| T-11 | Bonus: two Word2Vec models on `text8`, one hyperparameter apart | light + prototype | T-00 | — |
| T-12 | Single top-to-bottom execution; extract the real numbers into `findings.md` | light | all | — |
| T-13 | Written answers, in Portuguese, grounded in the extracted numbers | human-in-the-loop | T-12 | **G-5** |
| T-14 | Final verification and handover | light | T-13 | **G-6** |

**Gates.** G-1: this document set · G-2: RED of T-02 and T-09 reviewed together · G-3: GREEN of
T-02 and T-09 reviewed together · G-4: authorial content approved · G-5: answers reviewed and
rewritten by the student · G-6: final acceptance.

---

## 2. Detail — the two full-cycle tasks

### T-02 · `avaliar_analogias`

- **Objective.** Implement the evaluator specified in S-02, exactly to its return contract.
- **Context.** Consumed by two ready cells (Part 2.2), one of which reads a column named
  `acertou@1` — a contract the prose never states (C-01…C-04).
- **Files.** `tests/test_analogy_eval.py` (new), notebook cell of Part 2.1.
- **Restrictions.** No production code during RED. `tests/` must not be imported by the notebook.
- **Definition of done.** RED fails for the right reason; the student approves the tests; GREEN
  passes; REFACTOR keeps them green; the cell runs on the real `wv` and the Part 2.2 ready cell
  consumes its output without error.
- **Tests expected.** AC-1…AC-6 of S-02, plus edge cases E-1…E-5.

### T-09 · Gender axis

- **Objective.** Build the gender axis and the profession projections per S-07.
- **Context.** The projection function is the same cosine used in the sanity controls (T-10),
  so it is factored once.
- **Files.** `tests/test_gender_axis.py` (new), notebook cell of Part 5.1.
- **Restrictions.** Same as T-02.
- **Definition of done.** RED fails for the right reason and is approved; GREEN passes; REFACTOR
  keeps it green; `||eixo|| ≈ 1`; the chart renders ordered.
- **Tests expected.** AC-1…AC-5 of S-07, on a stub vocabulary with an analytically known axis.

---

## 3. Definition of Done — per task

1. Objective met within the task's scope — nothing beyond it (Constitution R-1, C-3).
2. Acceptance criteria of the corresponding specification section satisfied.
3. For `full` tasks: RED reviewed, GREEN reviewed, REFACTOR done, suite green.
4. Output inspected on real data, not just on the stub.
5. Relevant decisions recorded in `decisions.md`; AI usage recorded in `AI_USAGE.md` at the end of
   the corresponding user story.
6. No rule of the Constitution broken silently.
