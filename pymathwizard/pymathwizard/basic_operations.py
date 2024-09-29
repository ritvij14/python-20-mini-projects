def add(a: float, b: float) -> float:
    """
    Function to add 2 floating point numbers.

    Parameters:
    a (float): first number
    b (float): second number

    Returns:
    float: result of addition of a and b
    """
    return a + b


def subtract(a: float, b: float) -> float:
    """
    Function to subtract 2 floating point numbers.

    Parameters:
    a (float): first number
    b (float): second number

    Returns:
    float: result of subtracting b from a
    """
    return a - b


def multiply(a: float, b: float) -> float:
    """
    Function to multiply 2 floating point numbers.

    Parameters:
    a (float): first number
    b (float): second number

    Returns:
    float: result of multiplication of a and b
    """
    return a * b


def divide(a: float, b: float) -> float:
    """
    Function to divide 2 floating point numbers.

    Parameters:
    a (float): first number
    b (float): second number

    Returns:
    float: result of dividing a by b

    Raises:
    ValueError: Division by 0 is not allowed. b cannot be 0
    """
    if b == 0:
        raise ValueError("Division by 0 is not allowed")
    return a / b
