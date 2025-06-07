import math
from typing import List, Deque, Union
from collections import deque

def shunting_yard(expression: str) -> List[str]:
    """
    Converts an infix mathematical expression to postfix notation (Reverse Polish Notation)
    using the Shunting-Yard algorithm. Now supports functions like sin, cos, tan.
    """
    output_queue: Deque[str] = deque()
    operator_stack: List[str] = []
    # define operator precedence and associativity
    # (precedence, associativity: 'LEFT' or 'RIGHT')
    operators = {'+': (1, 'LEFT'), '-': (1, 'LEFT'), '*': (2, 'LEFT'), '/': (2, 'LEFT')}
    # functions are treated with higher precedence, and usually associated with a '('
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
        elif char.isalpha(): # check for potential function names
            current_token += char
            # check if current_token forms a function name
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
            return ["Error: Invalid character in expression"] # handle completely unknown characters
        i += 1

    if current_token: # add the last token if it exists
        tokens.append(current_token)

    # re-process tokens to handle unary minus and separate function names
    processed_tokens: List[str] = []
    i = 0
    while i < len(tokens):
        token = tokens[i]
        if token == '-' and (i == 0 or processed_tokens and processed_tokens[-1] in ['+', '-', '*', '/', '(']):
            # potentially a unary minus
            if i + 1 < len(tokens):
                next_token = tokens[i+1]
                try:
                    float(next_token) # check if next token is a number
                    processed_tokens.append(token + next_token) #combine for negative number
                    i += 1 # skip next token as it's part of the number
                except ValueError:
                    # if it's not a number (e.g., -sin(x)), treat '-' as a binary operator or unary
                    processed_tokens.append(token)
            else:
                # '-' at the end of expression without a number
                return ["Error: Invalid expression: unary minus at end"]
        elif token in functions: # if it's a recognized function name
            processed_tokens.append(token)
        else:
            processed_tokens.append(token)
        i += 1

    for token in processed_tokens:
        try:
            float(token) # attempt to convert to float to check if it's a number
            output_queue.append(token)
        except ValueError:
            #  not a number, so it must be an operator, function, or parenthesis
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
                # pop operators and functions until a left parenthesis is found
                while operator_stack and operator_stack[-1] != '(':
                    output_queue.append(operator_stack.pop())
                if operator_stack and operator_stack[-1] == '(':
                    operator_stack.pop()  # discard the left parenthesis
                    # if the token atop the stack after popping '(' was a function, pop it to output
                    if operator_stack and operator_stack[-1] in functions:
                        output_queue.append(operator_stack.pop())
                else:
                    return ["Error: Unmatched closing parenthesis"] # no matching opening parenthesis found
            else:
                return ["Error: Invalid token: " + token] # more specific error for unknown tokens

    while operator_stack:
        if operator_stack[-1] == '(':
            return ["Error: Unmatched opening parenthesis"] # remaining '(' means unclosed parenthesis
        output_queue.append(operator_stack.pop())

    return list(output_queue)

# --- evaluate_postfix function  ---
def evaluate_postfix(postfix_tokens: List[str]) -> Union[float, str]:
    """
    Evaluates a mathematical expression given in postfix (Reverse Polish) notation.
    Returns the result of the calculation as a float or an error message as a string.
    """
    operand_stack: List[float] = []
    operators = {'+', '-', '*', '/'} #  supported binary operators
    functions = {'sin', 'cos', 'tan'} #  supported functions

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
                if len(operand_stack) < 1: # functions typically take one argument
                    return f"Error: Insufficient operands for function '{token}'"
                
                operand = operand_stack.pop()
                
                # perform the function call
                if token == 'sin':
                    result = math.sin(math.radians(operand)) # convert to radians for math.sin
                elif token == 'cos':
                    result = math.cos(math.radians(operand)) # convert to radians for math.cos
                elif token == 'tan':
                    # Refined check for tan(90) or tan(270) etc. using a small epsilon
                    cos_val = math.cos(math.radians(operand))
                    if abs(cos_val) < 1e-9: # Check if cosine is very close to zero
                        return "Tangent of 90, 270 degrees (or multiples) is undefined"
                    result = math.tan(math.radians(operand))
                operand_stack.append(result)
            else:
                return f"Error: Unexpected token '{token}' in postfix expression"

    if len(operand_stack) != 1:
        return "Error: Malformed postfix expression"
    
    return operand_stack[0]

# --- Main calculate function ---
def calculate(expression: str) -> Union[float, str]:
    """
    Evaluates a mathematical expression by first converting it from infix to postfix
    and then evaluating the postfix expression.
    """
    postfix_tokens = shunting_yard(expression)

    # check if shunting_yard returned an error
    if postfix_tokens and postfix_tokens[0].startswith("Error:"):
        return postfix_tokens[0] # the error message directly

    return evaluate_postfix(postfix_tokens)


# --- New Test Cases for Step 3 ---
print("\n--- Testing with Step 3 extensions (functions) ---")
# valid function calls
print(f"Expression: 'sin(90)' = {calculate('sin(90)')}") # Expected: 1.0
print(f"Expression: 'cos(0)' = {calculate('cos(0)')}")   # Expected: 1.0
print(f"Expression: 'tan(45)' = {calculate('tan(45)')}") # Expected: 1.0 (approx)
print(f"Expression: '2 * sin(30)' = {calculate('2 * sin(30)')}") # Expected: 1.0 (2 * 0.5)
print(f"Expression: 'sin(1 + 1)' = {calculate('sin(1 + 1)')}") # sin(2) - small non-zero
print(f"Expression: 'cos(90 - 90)' = {calculate('cos(90 - 90)')}") # cos(0) = 1.0
print(f"Expression: '10 + tan(0)' = {calculate('10 + tan(0)')}") # 10 + 0 = 10.0

# edge cases / error cases for functions
print(f"Expression: 'tan(90)' = {calculate('tan(90)')}") # Expected: "Tangent of 90 degrees is undefined"
print(f"Expression: 'sin()' = {calculate('sin()')}") # Expected: error from shunting_yard or evaluation
print(f"Expression: 'sin(90 45)' = {calculate('sin(90 45)')}") # Expected: error for too many args or malformed input
print(f"Expression: 'sin(abc)' = {calculate('sin(abc)')}") # Expected: Error due to invalid token
print(f"Expression: 'sin(30) + cos(60)' = {calculate('sin(30) + cos(60)')}") # 0.5 + 0.5 = 1.0

# ensure existing tests still work
print("\n--- Re-testing original complex expressions ---")
print(f"Expression: '1 + 1 * 5' = {calculate('1 + 1 * 5')}")         # Expected: 6.0
print(f"Expression: '(1 + 1) * 5' = {calculate('(1 + 1) * 5')}")     # Expected: 10.0
print(f"Expression: '(1 * 2) - (3 * 4)' = {calculate('(1 * 2) - (3 * 4)')}") # Expected: -10.0