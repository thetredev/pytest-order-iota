# prerequisites: pip install pytest pytest-order

import pytest


class Iota:
    """Instances of this class hold their own iota value and increase it each time on __call__()."""

    def __init__(self, initial: int = 0, step: int = 1) -> None:
        self.initial = initial
        self.step = step

        self.reset()

    def __call__(self) -> int:
        value = self.value
        self.value += self.step

        return value

    def reset(self) -> None:
        self.value = self.initial


# global instance for this specific hypothetical test suite
iota = Iota()


# order marker (iota.value) will be 0 (iota.initial)
@pytest.mark.order(iota())
def test_1():
    assert True


# order marker (iota.value) will be 1 (iota.value increased by iota.step)
@pytest.mark.order(iota())
def test_2():
    assert True
