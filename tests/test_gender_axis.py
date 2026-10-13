"""T-09 / T-10 — tests for the gender axis and the projections (Part 5.1).

Specification: docs/specification.md §3 (S-07). Acceptance criteria AC-1..AC-4.

The stub is a 2-D space where every gender pair differs along a known direction, so the
expected axis can be written down analytically and the projection of any control word is
known in advance.
"""
import hashlib
import math

import numpy as np
import pandas as pd
import pytest

from conftest import StubVectors, run_cell

CELL_NEEDLE = "def normalizar"

# Each pair differs by (1, -1) or (1, -2). After the inner normalisation all six unit
# differences collapse onto two directions, so the mean is known by construction.
GENDER_PAIRS = [("he", "she"), ("man", "woman"), ("his", "her"),
                ("male", "female"), ("boy", "girl"), ("father", "mother")]

GENDERED = {
    "he": (1, 0), "she": (0, 1),
    "man": (1, 0), "woman": (0, 2),
    "his": (1, 0), "her": (0, 1),
    "male": (1, 0), "female": (0, 2),
    "boy": (1, 0), "girl": (0, 1),
    "father": (1, 0), "mother": (0, 2),
    # Explicitly gendered controls: extreme, opposite signs.
    "king": (1, 0), "queen": (0, 1), "actor": (1, 0), "actress": (0, 1),
}


def _unit(vector):
    return np.asarray(vector, dtype=float) / np.linalg.norm(vector)


# The axis the specification prescribes, computed here rather than written down by hand,
# so that the neutral controls below can be built *exactly* perpendicular to it. Writing
# rounded constants instead leaves a ~1e-5 residual that is indistinguishable from a real
# (if small) gender lean.
ANALYTIC_AXIS = _unit(np.mean(
    [_unit(np.subtract(GENDERED[m], GENDERED[f])) for m, f in GENDER_PAIRS], axis=0))
PERPENDICULAR = np.array([-ANALYTIC_AXIS[1], ANALYTIC_AXIS[0]])

GENDER_2D = {
    **GENDERED,
    # Neutral controls: collinear with PERPENDICULAR, so the projection is exactly zero.
    "table": tuple(PERPENDICULAR),
    "water": tuple(-PERPENDICULAR),
    "computer": tuple(2 * PERPENDICULAR),
    "tree": tuple(-3 * PERPENDICULAR),
}


class AnyWordStub(StubVectors):
    """Stub that also invents a deterministic vector for words it was not given.

    The notebook's own word lists (20 professions) are used as-is, without duplicating
    them in the test — the vector for each is a stable function of the word itself.
    """

    def __contains__(self, word: str) -> bool:
        return True

    def __getitem__(self, word: str) -> np.ndarray:
        if word not in self.vectors:
            digest = int(hashlib.sha256(word.encode("utf-8")).hexdigest()[:8], 16)
            angle = math.radians(digest % 360)
            self.vectors[word] = np.array([math.cos(angle), math.sin(angle)])
        return self.vectors[word]


@pytest.fixture
def gender_cell():
    stub = AnyWordStub(GENDER_2D)
    namespace = run_cell(CELL_NEEDLE, wv=stub)
    return namespace, stub


@pytest.fixture
def expected_axis(gender_cell):
    """The axis as written in the specification, computed independently of the notebook."""
    namespace, _ = gender_cell
    assert list(namespace["pares_genero"]) == GENDER_PAIRS, \
        "the notebook changed its gender pairs; the stub no longer describes it"
    return ANALYTIC_AXIS


def _cosine(vector: np.ndarray, axis: np.ndarray) -> float:
    return float(np.dot(vector / np.linalg.norm(vector), axis))


def test_axis_has_unit_norm(gender_cell):
    """AC-1: the axis is normalised, or every projection is scaled arbitrarily."""
    namespace, _ = gender_cell

    assert np.isclose(np.linalg.norm(namespace["eixo"]), 1.0, atol=1e-9)


def test_axis_follows_the_specified_formula(gender_cell, expected_axis):
    """AC-2: mean of the *normalised* pair differences, then normalised again.

    Averaging the raw differences instead is the obvious mistake; the second assertion
    proves this test can actually tell the two apart.
    """
    namespace, _ = gender_cell
    axis = np.asarray(namespace["eixo"], dtype=float)

    assert np.allclose(axis, expected_axis, atol=1e-9)

    pairs = namespace["pares_genero"]
    naive = np.mean([np.asarray(GENDER_2D[m]) - np.asarray(GENDER_2D[f]) for m, f in pairs], axis=0)
    naive = naive / np.linalg.norm(naive)
    assert not np.allclose(axis, naive, atol=1e-3), \
        "stub no longer distinguishes the normalised mean from the raw mean"


def test_projections_are_cosines_with_the_axis_and_are_sorted(gender_cell, expected_axis):
    """`projecoes` is a sorted Series holding the cosine of each profession with the axis."""
    namespace, stub = gender_cell
    projections = namespace["projecoes"]
    professions = namespace["profissoes"]

    assert isinstance(projections, pd.Series)
    assert list(projections.index) == sorted(professions, key=lambda p: projections[p])
    assert projections.is_monotonic_increasing
    for profession in professions:
        assert projections[profession] == pytest.approx(
            _cosine(stub[profession], expected_axis), abs=1e-9
        )


def test_gendered_controls_land_on_opposite_sides(gender_cell, expected_axis):
    """AC-3: the sanity check the README asks for — king/queen and actor/actress."""
    namespace, stub = gender_cell
    projection = namespace["projection_on_axis"]

    king = projection(stub, "king", expected_axis)
    queen = projection(stub, "queen", expected_axis)
    actor = projection(stub, "actor", expected_axis)
    actress = projection(stub, "actress", expected_axis)

    assert king > 0 > queen
    assert actor > 0 > actress


def test_neutral_controls_sit_closer_to_zero_than_gendered_ones(gender_cell, expected_axis):
    """AC-4: words with no gender should not be pulled onto the axis."""
    namespace, stub = gender_cell
    projection = namespace["projection_on_axis"]

    gendered = [abs(projection(stub, w, expected_axis)) for w in ("king", "queen", "actor", "actress")]
    neutral = [abs(projection(stub, w, expected_axis)) for w in ("table", "water", "computer", "tree")]

    assert np.mean(neutral) < np.mean(gendered) / 10
    assert max(neutral) < 1e-6
