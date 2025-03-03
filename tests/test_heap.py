from __future__ import print_function

import random

from heap_dict import HeapDict

N = 100
SEED = hash("Tarjan")
NUM_RANGE = 100_000_000


def check_invariants(h) -> None:
    for i, e in enumerate(h.heap):
        assert e[2] == i
    for i in range(1, len(h.heap)):
        parent = (i - 1) >> 1
        assert h.heap[parent][0] <= h.heap[i][0]


def make_data() -> tuple[HeapDict[int, int], list[tuple[int, int]], dict[int, int]]:
    random.seed(SEED)
    pairs: list[tuple[int, int]] = [
        (
            random.randint(0, NUM_RANGE),
            random.randint(0, NUM_RANGE),
        )
        for _ in range(N)
    ]
    h = HeapDict(pairs)
    d = {k: v for k, v in pairs}
    pairs.sort(key=lambda x: x[1], reverse=True)
    return h, pairs, d


def test_popitem() -> None:
    h, pairs, _ = make_data()

    while pairs:
        v = h.popitem()
        v2 = pairs.pop(-1)
        assert v == v2
    assert len(h) == 0


def test_popitem_ties() -> None:
    h = HeapDict()
    for i in range(N):
        h[i] = 0
    for _ in range(N):
        _, v = h.popitem()
        assert v == 0
        check_invariants(h)


def test_peek() -> None:
    h, pairs, _ = make_data()
    while pairs:
        v = h.peekitem()[0]
        h.popitem()
        v2 = pairs.pop(-1)
        assert v == v2[0]
    assert len(h) == 0


def test_iter() -> None:
    h, _, d = make_data()
    # TODO make it possible to traverse these in order
    assert set(h) == set(d.keys())


def test_keys() -> None:
    h, _, d = make_data()
    assert sorted(h.keys()) == sorted(d.keys())


def test_values() -> None:
    h, _, d = make_data()
    assert set(d.values()) == set(h.values())


# TODO fix this!! del loops forever
def test_del() -> None:
    h, pairs, _ = make_data()
    k, _ = pairs.pop(N // 2)
    del h[k]
    while pairs:
        v = h.popitem()
        v2 = pairs.pop(-1)
        assert v == v2
    assert len(h) == 0


def test_change() -> None:
    h, pairs, _ = make_data()
    k, _ = pairs[N // 2]
    h[k] = 0.5
    pairs[N // 2] = (k, 0.5)
    pairs.sort(key=lambda x: x[1], reverse=True)
    while pairs:
        v = h.popitem()
        v2 = pairs.pop(-1)
        assert v == v2
    assert len(h) == 0


def test_clear() -> None:
    h, _, _ = make_data()
    h.clear()
    assert len(h) == 0
