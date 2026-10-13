"""T-02 — tests for `avaliar_analogias` (Part 2.1).

Specification: docs/specification.md §3 (S-02). One test per acceptance criterion
(AC-1..AC-6) and per edge case (E-1..E-5).

The stubs are tiny hand-made vector spaces where the intended answer is known by
construction, so the tests check the *evaluator's* logic — OOV handling, ranking,
query-term filtering and the returned shape — not gensim itself.
"""
import numpy as np
import pandas as pd
import pytest

from conftest import StubVectors, run_cell

CELL_NEEDLE = "def avaliar_analogias(wv"

DETAIL_COLUMNS = ["a", "b", "c", "esperado", "previsto_top5", "acertou@1"]

# b - a + c == d exactly, so "d" is the intended answer of ("a", "b", "c", "d").
# The f* words are fillers that make the neighbour list longer than topn.
VECTORS = {
    "a": (1, 0, 0), "b": (2, 0, 0), "c": (0, 1, 0), "d": (1, 1, 0),
    "p": (1, 0, 0), "q": (2, 0, 0), "r": (0, 1, 0), "s": (0, 0, 1),
    "f1": (0, 0, 1), "f2": (0, 1, 1), "f3": (1, 0, 1), "f4": (1, 1, 1), "f5": (1, 1, 0.2),
}

HIT = ("a", "b", "c", "d")      # query = (1, 1, 0) = d  -> d must rank first
MISS = ("p", "q", "r", "s")     # same query, but s = (0, 0, 1) is orthogonal -> never top 5


@pytest.fixture
def avaliar_analogias():
    return run_cell(CELL_NEEDLE)["avaliar_analogias"]


def test_counts_only_the_known_hits(avaliar_analogias):
    """AC-1: on a controlled stub, acc@1/acc@5 match the analytically expected hits."""
    resumo, _ = avaliar_analogias(StubVectors(VECTORS), [HIT, MISS])

    assert resumo["avaliadas"] == 2
    assert resumo["oov"] == 0
    assert resumo["acc@1"] == pytest.approx(0.5)   # only HIT is a first-position hit
    assert resumo["acc@5"] == pytest.approx(0.5)   # MISS's "s" is orthogonal to the query


def test_add_uses_most_similar_and_mul_uses_cosmul(avaliar_analogias):
    """AC-2: `metodo` selects the gensim method, and the query direction is b-a+c."""
    stub = StubVectors(VECTORS)

    avaliar_analogias(stub, [HIT], metodo="add")
    avaliar_analogias(stub, [HIT], metodo="mul")

    assert stub.calls[0] == ("most_similar", ("b", "c"), ("a",))
    assert stub.calls[1] == ("most_similar_cosmul", ("b", "c"), ("a",))


def test_query_terms_cannot_become_the_prediction(avaliar_analogias):
    """AC-6 / decision D-01: a query term must never occupy the answer slot.

    Here b == a, so the query collapses onto `c` exactly. Unfiltered, `c` would be the
    first neighbour and the analogy would score zero; the evaluator must discard it.
    """
    vectors = {"a": (1, 0, 0), "b": (1, 0, 0), "c": (1, 1, 0),
               "d": (1, 1, 0.4), "f": (1, 0, 0.5)}
    stub = StubVectors(vectors)

    raw_first = stub.most_similar(positive=["b", "c"], negative=["a"], topn=5)[0][0]
    assert raw_first == "c", "stub no longer reproduces the trap this test guards against"

    resumo, detalhes = avaliar_analogias(stub, [("a", "b", "c", "d")])

    assert resumo["acc@1"] == pytest.approx(1.0)
    assert detalhes.loc[0, "previsto_top5"][0] == "d"


def test_oov_analogies_are_skipped_and_counted(avaliar_analogias):
    """AC-3 / E-3: any missing term skips the whole analogy, even when only `d` is missing."""
    analogias = [
        HIT,
        ("a", "b", "c", "zzz"),   # only the expected answer is out of vocabulary
        ("zzz", "b", "c", "d"),   # a query term is out of vocabulary
    ]

    resumo, detalhes = avaliar_analogias(StubVectors(VECTORS), analogias)

    assert resumo["avaliadas"] == 1
    assert resumo["oov"] == 2
    assert len(detalhes) == 1


def test_all_oov_leaves_avaliadas_at_zero(avaliar_analogias):
    """E-2: nothing evaluable must not raise and must report zero accuracy."""
    resumo, detalhes = avaliar_analogias(StubVectors(VECTORS), [("zzz", "yyy", "xxx", "www")])

    assert resumo["avaliadas"] == 0
    assert resumo["oov"] == 1
    assert resumo["acc@1"] == pytest.approx(0.0)
    assert resumo["acc@5"] == pytest.approx(0.0)
    assert len(detalhes) == 0


def test_empty_list_returns_zeros_and_typed_columns(avaliar_analogias):
    """E-1: the empty input is a valid input — no ZeroDivisionError, columns still typed."""
    resumo, detalhes = avaliar_analogias(StubVectors(VECTORS), [])

    assert resumo == {"acc@1": 0.0, "acc@5": 0.0, "avaliadas": 0, "oov": 0}
    assert list(detalhes.columns) == DETAIL_COLUMNS
    assert detalhes["acertou@1"].dtype == bool


def test_details_has_one_row_per_evaluated_analogy(avaliar_analogias):
    """AC-5 / C-03: the details frame backs the professor's ready cell."""
    resumo, detalhes = avaliar_analogias(StubVectors(VECTORS), [HIT, MISS, ("a", "b", "c", "zzz")])

    assert len(detalhes) == resumo["avaliadas"] == 2
    assert list(detalhes.columns) == DETAIL_COLUMNS
    assert detalhes["acertou@1"].dtype == bool
    assert detalhes["acertou@1"].tolist() == [True, False]
    assert detalhes["esperado"].tolist() == ["d", "s"]


def test_short_neighbour_list_does_not_crash(avaliar_analogias):
    """E-4: fewer surviving neighbours than `topn` is not an error."""
    stub = StubVectors({"a": (1, 0, 0), "b": (2, 0, 0), "c": (0, 1, 0), "d": (1, 1, 0)})

    resumo, detalhes = avaliar_analogias(stub, [HIT])

    assert resumo["acc@1"] == pytest.approx(1.0)
    assert detalhes.loc[0, "previsto_top5"] == ["d"]


def test_top5_is_a_list_of_strings(avaliar_analogias):
    """E-5: `previsto_top5` is printable and JSON-friendly, as the error table needs."""
    _, detalhes = avaliar_analogias(StubVectors(VECTORS), [HIT, MISS])

    for words in detalhes["previsto_top5"]:
        assert isinstance(words, list)
        assert 0 < len(words) <= 5
        assert all(isinstance(word, str) for word in words)
