import math
from pymathwizard.advanced_operations import power, sqrt, log, sin, cos, tan
import pytest


def test_power():
    assert power(2, 3) == 8
    assert power(-1, 1) == -1
    assert power(0, 0) == 1
    assert power(3.5, 2.5) == pytest.approx(22.917651494)


def test_sqrt():
    assert sqrt(4) == 2
    assert sqrt(5) == pytest.approx(2.2360679775)
    assert sqrt(0) == 0
    with pytest.raises(ValueError):
        sqrt(-2)


def test_log():
    assert log(100) == 2
    assert log(1) == 0
    with pytest.raises(ValueError):
        log(-2)
    with pytest.raises(ValueError):
        log(2, 1)


def test_trig():
    assert sin(math.pi / 2) == 1
    assert cos(math.pi / 3) == pytest.approx(0.5)
    assert tan(math.pi / 4) == pytest.approx(1)
    with pytest.raises(ValueError):
        tan(math.pi / 2)
