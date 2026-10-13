# Specification — Word Embeddings Lab

A verifiable description of the expected behaviour. Every acceptance criterion below must be
checkable either from the notebook's own output or from the automated tests in `tests/`.

Derived from [`requirements.md`](requirements.md); constrained by [`constitution.md`](constitution.md).

---

## 1. Global invariants

| ID | Invariant |
|---|---|
| INV-1 | The notebook executes top-to-bottom, in order, without exceptions. |
| INV-2 | Cells the README marks as *pronta* / *apenas execute* stay byte-identical to the README version. |
| INV-3 | Every output in the delivered `.ipynb` was produced by execution — none is hand-written. |
| INV-4 | Every number quoted in a written answer appears somewhere in the notebook output. |
| INV-5 | Identifiers supplied by the scaffold keep their exact names (they are Portuguese on purpose). |

---

## 2. Hidden contracts

These are requirements that the prose never states but that the professor's **ready cells** enforce.
Violating one breaks the notebook at runtime. They are the main reason this Specification exists.

| ID | Contract | Enforced by | If violated |
|---|---|---|---|
| C-01 | `avaliar_analogias(wv, analogias, metodo="add", topn=5)` returns a **tuple** `(dict, pd.DataFrame)` | `res, det = avaliar_analogias(...)` | unpack error |
| C-02 | The returned dict has keys `acc@1`, `acc@5`, `avaliadas`, `oov` | `{**res}` is spread into the summary rows | missing columns |
| C-03 | The returned DataFrame has a **boolean** column named exactly `acertou@1` | `detalhes[~detalhes["acertou@1"]]` | `KeyError` |
| C-04 | That DataFrame also carries columns `a`, `b`, `c`, `esperado`, `previsto_top5` | scaffold `# TODO` comment | incomplete error table |
| C-05 | `minhas_analogias` is `dict[str, list[tuple[str, str, str, str]]]` | `for cat, lista in minhas_analogias.items()` | unpack error |
| C-06 | `grupos` is a list of `(list[str], str, str)` with level in `{"fácil", "difícil"}` | `f"{nivel:7s}"` format spec | format error |
| C-07 | `ambiguas` is `dict[str, tuple[str, str]]` | `for palavra, (s1, s2) in ambiguas.items()` | unpack error |
| C-08 | `categorias` is `dict[str, list[str]]` with 8 words per category | `cores = dict(zip(categorias, plt.cm.tab10.colors))` and `plotar_2d` | `KeyError` on colour lookup |
| C-09 | Module-level names `palavras`, `rotulos`, `cores`, `X` | `plotar_2d` closes over them | `NameError` |
| C-10 | `meus_pares` is a list of **2-tuples** | `plotar_relacoes` flattens it and pairs `ps[i]` / `ps[i+1]` | misaligned arrows |
| C-11 | `eixo` is a numpy array of unit norm | cosine projection of each profession | meaningless projections |
| C-12 | `projecoes` is a `pd.Series` | `.sort_values()` and the bar plot | `AttributeError` |
| C-13 | In Part 1.2, `tabela` has index `modelo` and columns `analogias`, `wordsim353`, `simlex999` | the README's ready cell builds it | malformed table |
| C-14 | In Part 4.2, `axes` is a 2×2 array and `axes[0, 0].legend()` is called | README's ready cell | `AttributeError` |

---

## 3. Per-task specification

### S-01 · Part 1.2 — model comparison

**Behaviour.** Evaluate `wv50` on the Google analogies with the same function the ready cell uses
for `wv100` (`restrict_vocab=100_000`), then evaluate **both** models on WordSim-353 and SimLex-999
with `evaluate_word_pairs`, taking the **Spearman** coefficient (`spearman[0]`). Assemble one row per
model.

**Output shape.** `tabela`: index `modelo` ∈ {`GloVe 50d`, `GloVe 100d`}; columns `analogias`,
`wordsim353`, `simlex999`; rounded to 3 decimals.

**Chart.** `df50` and `df100` merged on `categoria`; horizontal bars comparing accuracy per category.

**Acceptance criteria.**
- AC-1 Two rows, three numeric columns, no `NaN`.
- AC-2 Values equal those returned by the model methods (no rounding before comparison).
- AC-3 The chart shows every category present in both DataFrames.

---

### S-02 · Part 2.1 — `avaliar_analogias` *(full RED→GREEN→REFACTOR cycle)*

**Behaviour.** For each tuple `(a, b, c, d)` meaning *a : b :: c : d*, produce the top-`topn`
predictions for the query and score whether `d` is the first answer (acc@1) and whether `d` is
among the first five (acc@5).

**Query direction.** `a : b :: c : d` ⇒ `b − a + c ≈ d`, therefore:
- `metodo="add"` → `wv.most_similar(positive=[b, c], negative=[a], topn=topn)`
- `metodo="mul"` → `wv.most_similar_cosmul(positive=[b, c], negative=[a], topn=topn)`

**OOV rule.** If **any** of `a`, `b`, `c`, `d` is outside the vocabulary, the analogy is skipped,
counted in `oov`, and **not** counted in `avaliadas`.

**Query-term exclusion** *(decision D-01)*. The words `a`, `b`, `c` are removed from the returned
neighbours before the rank is computed, mirroring the original Mikolov et al. (2013) evaluator.

**Return value.**
- `summary` = `{"acc@1": hits1 / max(avaliadas, 1), "acc@5": hits5 / max(avaliadas, 1), "avaliadas": n, "oov": k}`
- `details` = DataFrame with one row per **evaluated** analogy and columns
  `a, b, c, esperado, previsto_top5, acertou@1` (`acertou@1` boolean).

**Edge cases.**

| ID | Case | Expected |
|---|---|---|
| E-1 | Empty analogy list | `acc@1 = acc@5 = 0.0`, `avaliadas = oov = 0`, empty DataFrame **with the right columns**, no `ZeroDivisionError` |
| E-2 | Every analogy OOV | `avaliadas = 0`, `oov = len(analogias)`, accuracies `0.0` |
| E-3 | `d` in vocabulary but `a` is not | skipped, counted in `oov` |
| E-4 | Fewer than `topn` distinct neighbours survive the exclusion | rank computed on what is available, no crash |
| E-5 | `previsto_top5` | list of strings, possibly shorter than `topn` |

**Acceptance criteria.**
- AC-1 Given a controlled stub `wv` whose intended answer is known, `metodo="add"` counts exactly the known hits.
- AC-2 Given the same stub, `metodo="mul"` calls `most_similar_cosmul` (not `most_similar`).
- AC-3 An analogy with any OOV term appears in `oov` and never in `avaliadas`.
- AC-4 An empty list returns `0.0 / 0.0 / 0 / 0` without raising.
- AC-5 `details["acertou@1"].dtype` is boolean and its row count equals `avaliadas`.
- AC-6 Excluding the query terms changes the rank only in the direction intended: a query term
  sitting in the neighbour list must not be able to become the prediction.

---

### S-03 · Part 2.2 — authorial analogy set

- At least **12** analogies, at least **4** per category, across at least **3** categories.
- Categories must not repeat the Google Analogy set (capitals, currencies, family, plural, …).
- Every word exists in `wv` and is lowercase English — verified before the lists are frozen.

---

### S-04 · Part 3.1 — `doesnt_match` groups

- **6** groups, 4 to 6 words each: 3 **easy** (intruder from another domain) and 3 **hard**
  (intruder from the same domain, differing in one trait).
- All words in `wv`. The expected intruder is stated up front, so hits and misses are both reportable.

---

### S-05 · Part 3.2 — polysemy

- **5** ambiguous words total: `bank` and `apple` are given, plus 3 chosen.
- For each: the 8 nearest neighbours, then the neighbours after subtracting each of the two
  sense words, in the format the ready cell prints.

---

### S-06 · Part 4 — visualization

- **5** categories × **8** words; at least one pair deliberately hard to separate.
- All words in `wv` (the cell prints the ones that are not).
- Figure 2×2: PCA at `[0, 0]` with the **explained variance** in the title; t-SNE with
  `perplexity` 5, 15 and 30 in the remaining axes; `random_state=42`; legend on `[0, 0]`.
- Relation plot: at least **6** pairs of a single relation — not gender, not country→capital —
  drawn with `plotar_relacoes`.

---

### S-07 · Part 5.1 — gender axis *(full RED→GREEN→REFACTOR cycle)*

**Behaviour.**
1. `eixo = normalize(mean(normalize(wv[m] − wv[f]) for (m, f) in pares_genero))` — the mean of the
   **normalized** differences, then normalized again to unit norm.
2. `projecoes[p] = cosine(wv[p], eixo)` for each profession, as a `pd.Series` sorted ascending.
3. Horizontal bar chart, positive and negative values in distinguishable colours.

**Sanity check.** The same projection for 4 explicitly gendered words (`king`, `queen`, `actor`,
`actress` — expect extreme values, opposite signs) and 4 neutral words (`table`, `water`,
`computer`, `tree` — expect values near zero).

**Acceptance criteria.**
- AC-1 `||eixo|| ≈ 1` (within `1e-9`).
- AC-2 The test suite checks the axis construction against a stub vocabulary where the expected
  axis is known analytically.
- AC-3 `king` and `queen` land on opposite sides; `actor` and `actress` likewise.
- AC-4 The neutral controls are closer to zero than the gendered controls (by mean absolute value).
- AC-5 The chart is ordered by projection value.

---

### S-08 · Bonus — Word2Vec on `text8`

- `FAZER_BONUS = True`.
- Two models differing in exactly **one** hyperparameter *(decision D-03: `sg=0` vs `sg=1`)*,
  `epochs=5`, `workers=4`.
- The same three metrics as Part 1, with `restrict_vocab=30_000` on the analogies.
- Nearest neighbours of 3 chosen words, compared side by side.
- Model training is prototyped outside the notebook; the final run happens inside it so the
  delivered file carries real outputs.

---

## 4. Decisions the requirements do not fix

See [`decisions.md`](decisions.md) — D-01 to D-09. Each was approved by the student before
implementation, as required by the Constitution (R-2, H-1).
