# Decisions — Word Embeddings Lab

Decisions the requirements do not fix, plus findings made along the way.
Each decision was approved by the student before implementation (Constitution R-2, H-1).
D-11 and D-12 were put to the student at gate G-2 and implemented without an explicit answer,
under their standing instruction to keep going and stop only at the agreed gates; they still need
a yes or no. Everything else is confirmed.

---

## D-01 · Exclude the query terms from the analogy predictions — **approved**

**Context.** `most_similar` returns the input words themselves as candidates. In *a : b :: c : d*
the query terms are `a`, `b` and `c`. The README does not say whether they should be filtered out,
and the choice moves the acc@1/acc@5 numbers.

**Decision.** Remove `a`, `b` and `c` from the neighbour list before computing the rank.

**Why.** It mirrors the evaluator published with Mikolov et al. (2013) and the `questions-words`
benchmark the README cites in Part 1, so our numbers stay comparable to the ones in Part 1.
Without the filter a query term can occupy rank 1 and inflate the score.

**Impact.** acc@1 and acc@5 of Part 2.2 are computed on the filtered list; the raw neighbour list
is unaffected.

---

## D-02 · Notebook filename — **approved**

**Context.** The README does not name the file.

**Decision.** `atividade_word_embeddings.ipynb`.

**Why.** It follows the student's own naming from the previous lab (`atividade_ngramas.ipynb`),
keeping the two deliverables of the course consistent.

---

## D-03 · Bonus: `sg=0` vs `sg=1` — **approved**

**Context.** The README suggests `sg=0` vs `sg=1` or `window=2` vs `window=10`.

**Decision.** Vary `sg` (CBOW vs Skip-gram), everything else fixed.

**Why.** It is the most didactic contrast, and it gives Part B.1 substance: the two architectures
differ in how they use context, which connects directly to the intrinsic metrics of Part 1.

---

## D-04 · Language of the artifacts — **approved**

**Decision.** Process artifacts (`docs/`, code, comments, identifiers the agent creates, commit
messages) in **English**. Everything the professor reads (notebook answers, Part 6 declaration,
`AI_USAGE.md`) in **Portuguese**, first person, in the student's voice.

**Why.** English keeps the process material reusable across projects; Portuguese is what an
assignment read by a Brazilian professor requires, and it is the language the answers must be
defended in.

---

## D-05 · Tests live outside the notebook — **approved**

**Context.** The README asks for the executed notebook only, but the logic of Part 2.1 and Part 5.1
deserves automated tests.

**Decision.** Keep the tests in `tests/` (pytest), outside the deliverable, and add a short note
inside the Part 6 declaration telling the professor that the tests exist and what they buy.

**Why.** It satisfies both: the deliverable stays exactly what was asked for, and the work is
verifiable. The student explicitly asked for the note to be visible to the professor.

---

## D-06 · Remove the `# TODO` markers from completed cells — **approved**

**Decision.** A completed cell drops its `# TODO` comment; the markers stay only where the README's
scaffold text itself is being preserved as prose.

**Why.** A submitted notebook should not advertise unfinished work (Constitution Q-2).

---

## D-07 · AI-DW applied in a proportional ("Lite") profile — **approved**

**Context.** The AI-DW protocol is written for software systems; this is an exploratory analysis lab.

**Decision.** Full RED → review → GREEN → review → REFACTOR only for the two tasks with real
deterministic logic (T-02, T-09). Everything else follows spec + execution + output inspection.
Gates are batched (G-2/G-3 review both full-cycle tasks at once).

**Why.** AI-DW §22 explicitly allows reducing rigorous TDD for exploratory work, and §21 makes
ceremony proportional to complexity. Applying 12 gates to a 7-cell lab would cost more than the lab
itself while adding no protection where there is no logic to protect.

---

## D-08 · DDD is not applicable — **approved**

**Context.** AI-DW §21 makes DDD proportional to domain complexity.

**Decision.** Skip DDD/domain modelling. Replace it with the data-and-model contract in
`specification.md` §2 (vocabulary, dimensions, OOV rules, return shapes).

**Why.** There is no business domain with invariants here. The only thing that can silently break
is the interface between our cells and the professor's ready cells, and that is exactly what the
hidden-contracts table pins down. Creating entities and aggregates would be ceremony without content.

---

## D-09 · One commit at the end — **approved**

**Decision.** No per-stage commits. The student commits once at the end, or whenever they choose,
using the command sequence the agent hands over. Commit messages carry **no co-authorship
attribution**.

**Why.** The student's own decision on 2026-10-12: the history is evaluated as their work.

---

## D-10 · The notebook's code is tested by extracting its cells — **agent's call, reported at G-2**

**Context.** The deliverable is a self-contained notebook, so its logic is not importable. The
alternative was to duplicate each function in a module and test the copy, which tests the copy
instead of the deliverable.

**Decision.** `tests/conftest.py` reads the `.ipynb`, finds the cell containing a given anchor
string, and executes it in an isolated namespace. The notebook never imports the tests.

**Why.** It tests the bytes the professor will run, and it keeps the notebook free of any
dependency the README did not ask for (Constitution R-5).

---

## D-11 · Two extra guards on the line `pd.DataFrame(detalhes)` of Part 2.1 — **reported at G-2, not yet confirmed**

**Context.** The scaffold ends with `pd.DataFrame(detalhes)`. With an empty input that produces a
DataFrame with **no columns at all**, and the ready cell of Part 2.2 immediately does
`detalhes[~detalhes["acertou@1"]]` — a `KeyError` waiting to happen.

**Decision.** `pd.DataFrame(detalhes, columns=colunas).astype({"acertou@1": bool})`.

**Why.** It is one line of the professor's, and we change it only to keep the contract that the
professor's own next cell depends on. `columns=` alone would type the empty `acertou@1` column as
`object`, so the boolean cast is needed too: without it the "no analogies evaluated" path is not
merely empty, it is a different type.

**Impact.** Column order, names and dtypes are now fixed regardless of how many analogies survive.

---

## D-12 · `gender_axis()` and `projection_on_axis()` extracted inside the Part 5.1 cell — **reported at G-2, not yet confirmed**

**Context.** Part 5.1 asks for the axis and the projections inline. Written inline they can only be
tested by loading the real 400k-word GloVe, which makes the test slow and the assertion circular.

**Decision.** The two formulas become named functions in the same cell (`eixo = gender_axis(wv, ...)`,
`projecoes = ... projection_on_axis(...)`), so the test can drive them with a 2-D stub.

**Why.** The notebook stays self-contained and the formulas stay in the file the professor reads;
nothing moves to the test suite.

---

## D-13 · `sort_values(kind="stable")` for the profession ranking — **agent's call, found by the tests**

**Context.** The first GREEN run failed `test_projections_are_cosines_with_the_axis_and_are_sorted`.
The cause was not the projection: `Series.sort_values()` uses an unstable quicksort, so two
professions with the *same* projection came out in an order that depends on the sort internals.

**Decision.** Sort with `kind="stable"`, which keeps the order of `profissoes` for tied values.

**Why.** A ranking that reorders itself between runs is not reproducible, and the bar chart is read
by a human who will compare it with the text. This is the kind of defect the RED step is for: no
exception, no wrong number on the happy path, just a silent non-determinism.

---

# Findings

Appended as the work proceeds. Empty sections are removed.

## Environment

- `WordEmbeddings/` is its own git repository (`github.com/DanielAndersonTI/WordEmbeddings.git`),
  so the nested-repository hazard of the parent `I.T` folder does not apply here.
- Local Python is 3.12.0; `gensim` was not installed.
- The previous lab of the course was delivered as `.ipynb` + `.html` + `.pdf`; this README asks for
  the `.ipynb` only.
- **Avast TLS interception does break the gensim downloader**, exactly as feared: `api.load(...)`
  died with `CERTIFICATE_VERIFY_FAILED: unable to get local issuer certificate`. Fixed by exporting
  Avast's root (`CN=Avast Web/Mail Shield Root`) to a PEM and pointing `PIP_CERT` /
  `REQUESTS_CA_BUNDLE` / `SSL_CERT_FILE` at a bundle that is `certifi`'s `cacert.pem` plus that root.
  `--trusted-host` was deliberately **not** used: it would silence the check instead of satisfying it.
- `gensim 4.4.0` + `smart_open 7.x` is broken (`ImportError: cannot import name 'smart_open'`), so the
  environment pins `smart_open<7` (6.4.0). This is an environment concern, not a notebook change.
- `api.load("text8")` returns a **lazy `Dataset`**, not a list of tokens, so it has no `len()` — an
  assumption worth not carrying into the bonus cell. It is iterable, which is all `Word2Vec` needs.
- Figures embed correctly when the notebook is executed headless by `nbconvert`: `plt.show()` is
  captured as `image/png` with no need for `%matplotlib inline`. Verified with a three-cell probe
  notebook before committing to a 20-minute run, so the planned fallback deviation was not needed.
- Executing the notebook shells out to `!pip install -q gensim`, so the kernel needs the same
  `PIP_CERT` as the shell — otherwise the first cell is the one that fails.
- `api.load("text8")` yields **1701 chunks of ~10,000 tokens**, not one document per sentence. Two
  consequences: the corpus is 1701 "sentences" as far as `Word2Vec` is concerned (harmless — the
  window rarely straddles a chunk boundary), and materialising it as a list costs gigabytes. The
  bonus iterates it lazily, which is also what lets the same object feed both trainings.

## Specification

- The prose of the README never mentions the boolean column `acertou@1`, yet the ready cell of
  Part 2.2 indexes it. Fourteen such contracts were found by reading the ready cells before writing
  any code (C-01…C-14). This is the concrete payoff of the Specification step in this lab.
- The OOV rule of Part 2.1 is ambiguous about a *partially* out-of-vocabulary analogy (E-3).
  Resolved as: any of the four terms missing ⇒ skip the analogy.

## Verification

- RED was real, not staged: `9 failed, 5 errors`, every one from absent behaviour
  (`KeyError: 'previsto_top5'` on the empty details frame; `TypeError: '<' not supported` when the
  unfinished gender cell tried to sort `Ellipsis`). A test that fails for an unrelated reason would
  have proven nothing.
- GREEN found two defects the tests were written to catch, neither of them a typo — the unstable
  sort (D-13) and the rounded "orthogonal" constants (see below).
- **The tests were not enough.** The first full execution died at Part 1.2 on `KeyError: ' 100d'`:
  `merge(suffixes=(" 50d", " 100d"))` appends to the *existing* column name, so the merged column
  is `acurácia 100d`. No test covered that cell, because it is chart plumbing rather than logic.
  This is the honest boundary of the test suite: it protects the two functions with real rules, not
  the glue — which is why the notebook still has to be executed before it is handed in.
- A stub-based test asserts `actor > 0 > actress`; real GloVe 100d gives `actor = -0.039`,
  marginally on the feminine side, and `actress = -0.449`. This is not a contradiction: the test
  pins the *formula* against a space built to have a clean sign, and makes no claim about GloVe.
  The notebook reports the real numbers.
- A first draft of the test suite hard-coded its "neutral" control vectors as rounded constants.
  They were only approximately perpendicular to the axis (residual ~3e-5) — indistinguishable from
  a small but real gender lean, which is precisely what the assertion was meant to detect. The
  controls are now derived from the analytic axis (residual ~1e-17). A tolerance wide enough to
  accept rounded constants would have accepted a real effect too.

## Results

Everything below is read from the executed notebook (`atividade_word_embeddings.ipynb`, 18/18 code
cells executed, 4 embedded figures). These are the numbers the answers quote, so they live in one
place and can be checked against the outputs.

### Part 1 — intrinsic evaluation

| model | Google analogies (acc) | WordSim-353 (Spearman) | SimLex-999 (Spearman) |
|---|---|---|---|
| GloVe 50d | 0.470 | 0.503 | 0.263 |
| GloVe 100d | 0.639 | 0.533 | 0.296 |

Per-category accuracy of the 100d model, best and worst (the chart of Part 1.2 shows all of them):
`capital-common-countries` 0.939, `capital-world` 0.898, `gram6-nationality-adjective` 0.879,
`family` 0.816, `gram3-comparative` 0.791 against `currency` 0.156, `gram2-opposite` 0.217,
`gram1-adjective-to-adverb` 0.244, `city-in-state` 0.308.

Doubling the dimensions gains most on analogies (+0.169) and least on the two word-pair sets
(+0.030 and +0.033) — consistent with the reading that the extra capacity is spent separating
*relations*, which is what an analogy needs, while pairwise similarity was already well served.

SimLex-999 sits far below WordSim-353 for both models, and the gap is expected rather than a
defect: WordSim scores relatedness, SimLex scores similarity, and a co-occurrence model represents
the first much better than the second.

### Part 2 — analogies of my own

acc@1 / acc@5, for the two ranking methods:

| category | 3CosAdd | 3CosMul |
|---|---|---|
| animal → filhote | 0.0 / 0.2 | 0.2 / 0.2 |
| instrumento → músico | 0.6 / 0.8 | 0.8 / 0.8 |
| esporte → equipamento | 0.0 / 0.4 | 0.2 / 0.2 |

3CosMul matched or beat 3CosAdd everywhere. The two failures worth reporting are both informative
rather than random: `tennis : racket :: hockey : stick → puck` (a *different* piece of hockey gear
— the relation has no single direction, since a sport has several iconic pieces), and
`cow : calf :: horse : foal → ankle, leg, knee` (the corpus-dominant sense of `calf` is anatomy,
not "young cow", and `foal` is rare).

### Part 3 — `doesnt_match` and polysemy

5 of 6 groups correct. The failure is the hard group designed to be ambiguous:
`["violin", "guitar", "cello", "harp", "drum"] → harp` (expected `drum`). The method returns the
word farthest from the group mean, so it detects *atypicality*, not category membership — and
`harp` is the rarer, less band-like word, so it sits farther out than the actual intruder.

Polysemy: subtraction recovers the minority sense only sometimes. `apple` is the clean case —
neighbours are all companies (microsoft, ibm, intel, dell, iphone), but subtracting `iphone` yields
berry, pecan, cherry, peach, grove, pine. `bank` is the hard case — both subtractions (`money` and
`river`) stay in finance, and the river sense never surfaces.

### Part 4 — visualisation

- PCA keeps 34.0% of the variance in two components (PC1 21.3%, PC2 12.7%).
- The hard pair (frutas ↔ cores) is the **closest** pair of category centroids in the PCA plane,
  and the overlap is concrete: in that plane `orange`'s nearest neighbours are green, purple and
  blue, and `green`'s nearest neighbour is `orange`.
- Changing only the t-SNE `perplexity` (5 → 15 → 30) leaves the *organisation* fairly stable
  (pairwise-distance Spearman 0.877–0.940 between layouts) while changing the *scale* drastically.
  A reader who took those distances as measurements would be badly misled — which is exactly the
  point the answer makes.
- Country→language arrows in the PCA plane are close to parallel (spread roughly 15°, extremes
  `brazil → portuguese` and `france → french`); what varies between them is length, not direction.
  This is the assumption 3CosAdd rests on, seen directly.

### Part 5 — gender axis

Projections onto the axis (positive = masculine), most extreme at both ends:
`architect +0.170`, `ceo +0.164`, `engineer +0.148`, `mechanic +0.142` … `dancer -0.288`,
`nanny -0.314`, `receptionist -0.335`, `nurse -0.351`, `housekeeper -0.377`.

Two details the answer reports honestly rather than smoothing over:

- `secretary` lands on the **masculine** side (+0.086), against the expectation from Bolukbasi et
  al. — plausibly because in Wikipedia+Gigaword "Secretary" is mostly a government post.
- The explicit-gender controls do not all behave: `king +0.240` / `queen -0.220` split cleanly, but
  `actor -0.039` / `actress -0.449` do not straddle zero, because `actor` is now used for both
  genders. The neutral controls sit near zero as intended (`table +0.018`, `tree -0.022`,
  `computer +0.088`, `water -0.091`).

### Bonus — Word2Vec on text8

| model | Google analogies | WordSim-353 | SimLex-999 |
|---|---|---|---|
| CBOW (sg=0) | 0.314 | 0.617 | 0.261 |
| Skip-gram (sg=1) | 0.375 | 0.685 | 0.304 |

Skip-gram wins all three, at roughly three times the training cost (CBOW ≈160 s, Skip-gram ≈482 s
on this machine). Both trail the pretrained GloVe badly, and the dominant reason is scale, not
architecture: 17M tokens and a 71,290-word vocabulary against GloVe's ~6B tokens and 400,000 words.
