import math
from typing import List, Deque, Union
from collections import deque

# --- shunting_yard function (copy your current, fully updated shunting_yard here) ---
def shunting_yard(expression: str) -> List[str]:
    """
    Converts an infix mathematical expression to postfix notation (Reverse Polish Notation)
    using the Shunting-Yard algorithm. Now supports functions like sin, cos, tan.
    """
    output_queue: Deque[str] = deque()
    operator_stack: List[str] = []
    operators = {'+': (1, 'LEFT'), '-': (1, 'LEFT'), '*': (2, 'LEFT'), '/': (2, 'LEFT')}
    functions = {'sin', 'cos', 'tan'}

    def get_precedence(operator: str) -> int:
        return operators.get(operator, (0, 'LEFT'))[0]

    def get_associativity(operator: str) -> str:
        return operators.get(operator, (0, 'LEFT'))[1]

    tokens = []
    current_token = ""
    i = 0
    while i < len(expression):
        char = expression[i]
        if char.isdigit() or char == '.':
            current_token += char
        elif char.isalpha():
            current_token += char
        elif char in ['+', '-', '*', '/', '(', ')']:
            if current_token:
                tokens.append(current_token)
                current_token = ""
            tokens.append(char)
        elif char.isspace():
            if current_token:
                tokens.append(current_token)
                current_token = ""
        else:
            return ["Error: Invalid character in expression"]

        i += 1

    if current_token:
        tokens.append(current_token)

    processed_tokens: List[str] = []
    i = 0
    while i < len(tokens):
        token = tokens[i]
        if token == '-' and (i == 0 or processed_tokens and processed_tokens[-1] in ['+', '-', '*', '/', '(']):
            if i + 1 < len(tokens):
                next_token = tokens[i+1]
                try:
                    float(next_token)
                    processed_tokens.append(token + next_token)
                    i += 1
                except ValueError:
                    processed_tokens.append(token)
            else:
                return ["Error: Invalid expression: unary minus at end"]
        elif token in functions:
            processed_tokens.append(token)
        else:
            processed_tokens.append(token)
        i += 1

    for token in processed_tokens:
        try:
            float(token)
            output_queue.append(token)
        except ValueError:
            if token in functions:
                operator_stack.append(token)
            elif token in operators:
                while operator_stack and operator_stack[-1] in operators and \
                      (get_precedence(operator_stack[-1]) > get_precedence(token) or \
                       (get_precedence(operator_stack[-1]) == get_precedence(token) and get_associativity(token) == 'LEFT')):
                    output_queue.append(operator_stack.pop())
                operator_stack.append(token)
            elif token == '(':
                operator_stack.append(token)
            elif token == ')':
                while operator_stack and operator_stack[-1] != '(':
                    output_queue.append(operator_stack.pop())
                if operator_stack and operator_stack[-1] == '(':
                    operator_stack.pop()
                    if operator_stack and operator_stack[-1] in functions:
                        output_queue.append(operator_stack.pop())
                else:
                    return ["Error: Unmatched closing parenthesis"]
            else:
                return ["Error: Invalid token: " + token]

    while operator_stack:
        if operator_stack[-1] == '(':
            return ["Error: Unmatched opening parenthesis"]
        output_queue.append(operator_stack.pop())

    return list(output_queue)


# --- evaluate_postfix function (copy your current, fully updated evaluate_postfix here) ---
def evaluate_postfix(postfix_tokens: List[str]) -> Union[float, str]:
    """
    Evaluates a mathematical expression given in postfix (Reverse Polish) notation.
    Returns the result of the calculation as a float or an error message as a string.
    """
    operand_stack: List[float] = []
    operators = {'+', '-', '*', '/'}
    functions = {'sin', 'cos', 'tan'}

    for token in postfix_tokens:
        try:
            operand_stack.append(float(token))
        except ValueError:
            if token in operators:
                if len(operand_stack) < 2:
                    return f"Error: Insufficient operands for operator '{token}'"

                operand2 = operand_stack.pop()
                operand1 = operand_stack.pop()

                if token == '+': result = operand1 + operand2
                elif token == '-': result = operand1 - operand2
                elif token == '*': result = operand1 * operand2
                elif token == '/':
                    if operand2 == 0: return "Division by zero error"
                    result = operand1 / operand2
                operand_stack.append(result)
            elif token in functions:
                if len(operand_stack) < 1:
                    return f"Error: Insufficient operands for function '{token}'"

                operand = operand_stack.pop()

                if token == 'sin':
                    result = math.sin(math.radians(operand))
                elif token == 'cos':
                    result = math.cos(math.radians(operand))
                elif token == 'tan':
                    cos_val = math.cos(math.radians(operand))
                    if abs(cos_val) < 1e-9:
                        return "Tangent of 90, 270 degrees (or multiples) is undefined"
                    result = math.tan(math.radians(operand))
                operand_stack.append(result)
            else:
                return f"Error: Unexpected token '{token}' in postfix expression"

    if len(operand_stack) != 1:
        return "Error: Malformed postfix expression"

    return operand_stack[0]

# --- Main calculate function (unchanged, it orchestrates) ---
def calculate(expression: str) -> Union[float, str]:
    """
    Evaluates a mathematical expression by first converting it from infix to postfix
    and then evaluating the postfix expression.
    """
    postfix_tokens = shunting_yard(expression)

    if postfix_tokens and postfix_tokens[0].startswith("Error:"):
        return postfix_tokens[0]

    return evaluate_postfix(postfix_tokens)


# --- New Interactive Loop for the Calculator ---
if __name__ == '__main__':
    print("Welcome to the Interactive Calculator!")
    print("Enter 'exit' to quit.")
    print("Supported operations: +, -, *, /, sin(), cos(), tan(), ()")
    print("Angles for sin, cos, tan are in degrees.")

    while True:
        try:
            user_input = input("Enter expression: ")
            if user_input.lower() == 'exit':
                print("Exiting calculator. Goodbye!")
                break
            if not user_input.strip(): # Handle empty input
                continue

            result = calculate(user_input)
            print(f"Result: {result}")
        except EOFError: # Handles Ctrl+D or Ctrl+Z (on Windows)
            print("\nExiting calculator. Goodbye!")
            break
        except Exception as e:
            print(f"An unexpected error occurred: {e}")

    # The previous test cases (print statements) can be removed or commented out
    # from the main part of calculator.py if you intend to only use the interactive mode
    # or rely solely on test_calculator.py for automated testing.
    # For example:
    # print("\n--- Testing with Step 3 extensions (functions) ---")
    # print(f"Expression: 'sin(90)' = {calculate('sin(90)')}")
    # ... and so on ...