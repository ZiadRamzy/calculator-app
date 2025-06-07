from typing import List, Deque, Union
from collections import deque

def shunting_yard(expression: str) -> List[str]:
    """
    Converts an infix mathematical expression to postfix notation (Reverse Polish Notation)
    using the Shunting-Yard algorithm.
    """
    output_queue: Deque[str] = deque()
    operator_stack: List[str] = []
    # Define operator precedence and associativity
    # (precedence, associativity: 'LEFT' or 'RIGHT')
    operators = {'+': (1, 'LEFT'), '-': (1, 'LEFT'), '*': (2, 'LEFT'), '/': (2, 'LEFT')}

    def get_precedence(operator: str) -> int:
        return operators.get(operator, (0, 'LEFT'))[0]

    def get_associativity(operator: str) -> str:
        return operators.get(operator, (0, 'LEFT'))[1]

    tokens = []
    current_token = ""
    for char in expression:
        if char.isdigit() or char == '.':
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
            return ["Error: Invalid character in expression"] # Handle completely unknown characters

    if current_token: # Add the last token if it exists
        tokens.append(current_token)

    processed_tokens: List[str] = []
    i = 0
    while i < len(tokens):
        token = tokens[i]
        # Handle unary minus: if '-' is at the start or after an operator/opening parenthesis
        # and the next token is a number
        if token == '-' and (i == 0 or tokens[i-1] in ['+', '-', '*', '/', '(']):
            if i + 1 < len(tokens):
                next_token = tokens[i+1]
                try:
                    float(next_token) # Check if next token is a number
                    processed_tokens.append(token + next_token) # Combine for negative number
                    i += 1 # Skip next token as it's part of the number
                except ValueError:
                    # If it's not a number, treat '-' as a binary operator
                    processed_tokens.append(token)
            else:
                # '-' at the end of expression without a number following it
                return ["Error: Invalid expression: unary minus at end"]
        else:
            processed_tokens.append(token)
        i += 1

    for token in processed_tokens:
        try:
            # Attempt to convert to float to check if it's a number
            float(token)
            output_queue.append(token)
        except ValueError:
            # Not a number, so it must be an operator or parenthesis
            if token in operators:
                while operator_stack and operator_stack[-1] in operators and \
                      (get_precedence(operator_stack[-1]) > get_precedence(token) or \
                       (get_precedence(operator_stack[-1]) == get_precedence(token) and get_associativity(token) == 'LEFT')):
                    output_queue.append(operator_stack.pop())
                operator_stack.append(token)
            elif token == '(':
                operator_stack.append(token)
            elif token == ')':
                # Pop operators until a left parenthesis is found
                while operator_stack and operator_stack[-1] != '(':
                    output_queue.append(operator_stack.pop())
                if operator_stack and operator_stack[-1] == '(':
                    operator_stack.pop()  # Discard the left parenthesis
                else:
                    return ["Error: Unmatched closing parenthesis"] # No matching opening parenthesis found
            else:
                return ["Error: Invalid token: " + token] # More specific error for unknown tokens

    # After processing all tokens, pop any remaining operators from the stack to the output queue
    while operator_stack:
        if operator_stack[-1] == '(':
            return ["Error: Unmatched opening parenthesis"] # Remaining '(' means unclosed parenthesis
        output_queue.append(operator_stack.pop())

    return list(output_queue)

# Test cases for shunting_yard
print(f"Infix: 1 + 1 * 5 -> Postfix: {shunting_yard('1 + 1 * 5')}")
print(f"Infix: (1 + 1) * 5 -> Postfix: {shunting_yard('(1 + 1) * 5')}")
print(f"Infix: (1 * 2) - (3 * 4) -> Postfix: {shunting_yard('(1 * 2) - (3 * 4)')}")
print(f"Infix: 1 * 2 -> Postfix: {shunting_yard('1 * 2')}")
print(f"Infix: 10 / (6 - 1) -> Postfix: {shunting_yard('10 / (6 - 1)')}")
print(f"Infix: 2.5 + 3.0 -> Postfix: {shunting_yard('2.5 + 3.0')}")
print(f"Infix: -5 + 2 -> Postfix: {shunting_yard('-5 + 2')}")
print(f"Infix: (5 +) -> Postfix: {shunting_yard('(5 +)')}")
print(f"Infix: 5 + ) -> Postfix: {shunting_yard('5 + )')}")
print(f"Infix: (5 + 2 -> Postfix: {shunting_yard('(5 + 2')}") # Another unmatched opening parenthesis case
print(f"Infix: 3 ^ 4 -> Postfix: {shunting_yard('3 ^ 4')}") # Unsupported operator
print(f"Infix: 1 $ 2 -> Postfix: {shunting_yard('1 $ 2')}") # Invalid character