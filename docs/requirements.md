# Requirements — Word Embeddings Lab

**Source of truth:** [`README.md`](../README.md) — assignment for *Modelos de Linguagem de Grande Escala* (UFCG).
**Status:** these requirements are **fixed**. They must not be extended, reinterpreted or improved.
Whatever the README does not state is a **decision**, and every decision needs explicit human
approval (logged in [`decisions.md`](decisions.md)).

---

## 1. Deliverable

The executed notebook (File > Download > `.ipynb`), every cell run, every `# TODO` cell completed,
every written answer filled in.

`docs/` and `tests/` are our own process artifacts. `AI_USAGE.md` also feeds the Part 6 declaration.

---

## 2. Functional requirements — user stories

### US-1 — Intrinsic evaluation of two GloVe models
As a **student**, I want to evaluate the 50d and 100d GloVe models on Google Analogies,
WordSim-353 and SimLex-999, **so that** I can compare them numerically and explain what each
metric actually measures.
*Source:* README Part 1 · *Points:* 2.0 · *Metrics:* analogy accuracy, Spearman correlation.

### US-2 — My own analogy set
As a **student**, I want to implement an analogy evaluator (3CosAdd and 3CosMul, acc@1 and acc@5)
and run it on analogies I designed myself, **so that** I can judge the method on cases I control
and explain its errors.
*Source:* README Part 2 · *Points:* 2.0.

### US-3 — `doesnt_match` and polysemy
As a **student**, I want to test `doesnt_match` on easy and hard word groups and probe polysemy by
vector subtraction, **so that** I can explain the mechanism and its limits.
*Source:* README Part 3 · *Points:* 1.5.

### US-4 — Visualization in reduced spaces
As a **student**, I want to project 5 categories of 8 words with PCA and t-SNE and draw a relation
as arrows, **so that** I can discuss what each method preserves and distorts.
*Source:* README Part 4 · *Points:* 2.0.

### US-5 — Gender bias
As a **student**, I want to build a gender axis and measure the cosine projection of professions,
**so that** I can quantify the bias and argue about its consequences.
*Source:* README Part 5 · *Points:* 1.5.

### US-6 — Final reflection and AI declaration
As a **student**, I want to state whether I would use static embeddings today and declare my AI
usage, **so that** I close the lab with a grounded position.
*Source:* README Part 6 · *Points:* 1.0.

### US-B — Bonus: train and compare Word2Vec
As a **student**, I want to train two Word2Vec models on `text8` differing in exactly one
hyperparameter and compare them on the same metrics, **so that** I can relate the hyperparameter to
the results and contrast with pre-trained GloVe.
*Source:* README Bonus · *Points:* +1.0.

---

## 3. Non-functional requirements and constraints

| ID | Requirement | Source |
|---|---|---|
| NFR-1 | One single notebook, executable top-to-bottom in a clean session, Colab-compatible (`!pip install`) | README Parte 0, Entrega |
| NFR-2 | Written answers: 3 to 6 lines, in Portuguese, first person, grounded in the student's own numbers | README Regras |
| NFR-3 | AI use is allowed, must be declared in Part 6, and the student must be able to explain every piece of code | README Regras |
| NFR-4 | The professor's ready cells must remain untouched | README ("já está pronta", "apenas execute") |
| NFR-5 | Vocabulary is English and lowercase (GloVe wiki-gigaword) | README Parte 2.2 |
| NFR-6 | Bonus training ≈ 2–6 min per model with `epochs=5`, `workers=4` | README Bônus |
| NFR-7 | No network dependency beyond gensim's downloader and the Colab `pip install` | README Parte 0 |

---

## 4. Business rules

**None.** This is an exploratory analysis lab, not a business system: there is no domain with
invariants to protect. Consequently **DDD / domain modelling is not applicable** (AI-DW §21).

The analogous concern — the *data and model contract* (vocabulary, dimensions, OOV handling,
return shapes of the functions the professor's cells consume) — is captured in
[`specification.md`](specification.md) instead. This substitution is recorded as decision D-08.

---

## 5. Out of scope

- PDF/HTML export of the notebook (the README asks for the `.ipynb` only).
- Any modification to `README.md`.
- New sections in the notebook, beyond a short note telling the professor that automated tests
  exist in `tests/` (decision D-05).
