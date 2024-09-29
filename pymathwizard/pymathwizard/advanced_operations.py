import math


def power(base: float, exponent: float) -> float:
    """
    Raises the base to the power of the exponent.

    Parameters:
    base (float): first number
    exponent (float): second number

    Returns:
    float: result base ^ exponent
    """
    return base**exponent


def sqrt(value: float) -> float:
    """
    Returns the square root of the value.

    Parameters:
    value (float): input number

    Returns:
    float: square root of value

    Raises:
    ValueError: Square Root of negative numbers is not allowed
    """
    if value < 0:
        raise ValueError("Square root of negative numbers is not allowed")
    return value**0.5


def log(value: float, base: float = 10) -> float:
    """
    Returns the logarithm of the value to the specified base. Default value of base is 10.

    Parameters:
    value (float): input number
    base (float): optional second input number

    Returns:
    float: log of value to base

    Raises:
    ValueError: Value should be > 0, base should be > 0 but != 1
    """
    if value <= 0:
        raise ValueError("log non-positive numbers is not allowed")
    if base <= 0 or base == 1:
        raise ValueError("base has to be positive and not equal to 1")

    return math.log(value, base)


def sin(angle: float) -> float:
    """
    Returns the sine of the angle (in radians).

    Parameters:
    angle (float): input angle in radians

    Returns:
    float: cosine of the angle
    """

    return math.sin(angle)


def cos(angle: float) -> float:
    """
    Returns the cosine of the angle (in radians).

    Parameters:
    angle (float): input angle in radians

    Returns:
    float: cosine of the angle
    """

    return math.cos(angle)


def tan(angle: float) -> float:
    """
    Returns the tangent of the angle (in radians).

    Parameters:
    angle (float): input angle in radians

    Returns:
    float: tangent of the angle

    Raises:
    ValueError: Angle should not be an odd multiple of π/2
    """
    if (angle / (math.pi / 2)) % 2 == 1:
        raise ValueError("Angle should not be an odd multiple of π/2")

    return math.tan(angle)
