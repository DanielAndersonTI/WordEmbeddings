"""Test harness for the lab notebook.

The deliverable is a self-contained notebook, so the code under test lives *inside* it
rather than in an importable module. These helpers extract the relevant cell and execute
it in an isolated namespace, which keeps the notebook self-contained and still lets its
logic be tested (decision D-10).
"""
from __future__ import annotations

import json
import pathlib

import matplotlib

matplotlib.use("Agg")  # headless: a test run must never open a window
import matplotlib.pyplot as plt  # noqa: E402,F401  (the executed cells use it)

plt.show = lambda *args, **kwargs: None  # the cells end in plt.show(); Agg only warns
import numpy as np  # noqa: E402,F401
import pandas as pd  # noqa: E402,F401

NOTEBOOK = pathlib.Path(__file__).resolve().parents[1] / "atividade_word_embeddings.ipynb"


def _code_cells() -> list[str]:
    nb = json.loads(NOTEBOOK.read_text(encoding="utf-8"))
    return ["".join(cell["source"]) for cell in nb["cells"] if cell["cell_type"] == "code"]


def cell_with(needle: str) -> str:
    """Source of the first notebook code cell containing `needle`."""
    for source in _code_cells():
        if needle in source:
            return source
    raise LookupError(f"no code cell of {NOTEBOOK.name} contains {needle!r}")


def run_cell(needle: str, **names) -> dict:
    """Execute the notebook cell containing `needle` and return its namespace."""
    namespace: dict = {"np": np, "pd": pd, "plt": plt}
    namespace.update(names)
    exec(compile(cell_with(needle), f"<notebook cell containing {needle!r}>", "exec"), namespace)
    return namespace


class StubVectors:
    """Minimal `KeyedVectors` stand-in, ranking by real cosine over hand-made vectors.

    It deliberately does *not* remove the query words from the neighbour list — real gensim
    does not either, and compensating for that is exactly what decision D-01 is about.
    Every call is recorded so tests can assert *which* gensim method was used.
    """

    def __init__(self, vectors: dict):
        self.vectors = {word: np.asarray(vec, dtype=float) for word, vec in vectors.items()}
        self.calls: list[tuple] = []

    def __contains__(self, word: str) -> bool:
        return word in self.vectors

    def __getitem__(self, word: str) -> np.ndarray:
        return self.vectors[word]

    def _query(self, positive, negative) -> np.ndarray:
        dim = len(next(iter(self.vectors.values())))
        query = np.zeros(dim)
        for word in positive:
            query = query + self[word]
        for word in negative:
            query = query - self[word]
        return query

    def _rank(self, query: np.ndarray, topn: int) -> list[tuple[str, float]]:
        qnorm = np.linalg.norm(query)
        scored = [
            (word, float(np.dot(query, vec) / (qnorm * np.linalg.norm(vec))))
            for word, vec in self.vectors.items()
        ]
        scored.sort(key=lambda item: (-item[1], item[0]))
        return scored[:topn]

    def most_similar(self, positive, negative=(), topn=10):
        self.calls.append(("most_similar", tuple(positive), tuple(negative)))
        return self._rank(self._query(positive, negative), topn)

    def most_similar_cosmul(self, positive, negative=(), topn=10):
        self.calls.append(("most_similar_cosmul", tuple(positive), tuple(negative)))
        return self._rank(self._query(positive, negative), topn)
