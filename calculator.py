from typing import Union

def calculate(expression: str) -> Union[float, str]:
    """
    Parse a simple mathematical expression with two operands and a single operator(+, -, *, /).
    Returns the result of the calculation as a float or an error message as a string.
    """

    parts = expression.split()
    if len(parts) != 3:
        return "Invalid input format: Expected 'number operator number'"
    
    number1_string, operator, number2_string = parts

    try:
        number1 = float(number1_string)
        number2 = float(number2_string)
    except ValueError:
        return "Invalid number input: Both operands must be valid numbers"
    
    if operator == '+':
        return number1 + number2
    elif operator == '-':
        return number1 - number2
    elif operator == '*':
        return number1 * number2
    elif operator == '/':
        if number2 == 0:
            return "Division by zero error: Cannot divide by zero"
        return number1 / number2
    else:
        return "Invalid operator: Supported operators are +, -, *, /"

