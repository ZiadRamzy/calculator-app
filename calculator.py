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

def evaluate_postfix(postfix_tokens: List[str]) -> Union[float, str]:
    """
    Evaluates a mathematical expression given in postfix (Reverse Polish) notation.
    Returns the result of the calculation as a float or an error message as a string.
    """
    operand_stack: List[float] = []
    operators = {'+', '-', '*', '/'} # Define supported operators

    for token in postfix_tokens:
        try:
            # If the token is a number, push it onto the operand stack
            operand_stack.append(float(token))
        except ValueError:
            # If the token is not a number, it must be an operator
            if token in operators:
                if len(operand_stack) < 2:
                    return f"Error: Insufficient operands for operator '{token}'"
                
                # Pop the two most recent operands
                operand2 = operand_stack.pop()
                operand1 = operand_stack.pop()

                # Perform the operation
                if token == '+':
                    result = operand1 + operand2
                elif token == '-':
                    result = operand1 - operand2
                elif token == '*':
                    result = operand1 * operand2
                elif token == '/':
                    if operand2 == 0:
                        return "Division by zero error"
                    result = operand1 / operand2
                else:
                    # This case should ideally not be hit if shunting_yard filters well,
                    # but good to have for robustness.
                    return f"Error: Unknown operator '{token}' in postfix expression"
                
                # Push the result back onto the stack
                operand_stack.append(result)
            else:
                # This should ideally not happen if shunting_yard produces valid tokens,
                # but catches unexpected tokens that aren't numbers or operators.
                return f"Error: Unexpected token '{token}' in postfix expression"

    if len(operand_stack) != 1:
        # If the stack doesn't contain exactly one value at the end, it means
        # the expression was malformed (e.g., too many operands or missing operators).
        return "Error: Malformed postfix expression"
    
    return operand_stack[0]

# --- Integration of shunting_yard and evaluate_postfix ---
def calculate(expression: str) -> Union[float, str]:
    """
    Evaluates a mathematical expression by first converting it from infix to postfix
    and then evaluating the postfix expression.
    """
    postfix_tokens = shunting_yard(expression)

    # Check if shunting_yard returned an error
    if postfix_tokens and postfix_tokens[0].startswith("Error:"):
        return postfix_tokens[0] # Return the error message directly

    return evaluate_postfix(postfix_tokens)

# Test cases for Step 2
print("\n--- Testing with integrated calculate function ---")
print(f"Expression: '1 + 1 * 5' = {calculate('1 + 1 * 5')}")         # Expected: 6.0
print(f"Expression: '(1 + 1) * 5' = {calculate('(1 + 1) * 5')}")     # Expected: 10.0
print(f"Expression: '(1 * 2) - (3 * 4)' = {calculate('(1 * 2) - (3 * 4)')}") # Expected: -10.0
print(f"Expression: '1 * 2' = {calculate('1 * 2')}")                 # Expected: 2.0
print(f"Expression: '10 / (6 - 1)' = {calculate('10 / (6 - 1)')}")   # Expected: 2.0
print(f"Expression: '2.5 + 3.0' = {calculate('2.5 + 3.0')}")         # Expected: 5.5
print(f"Expression: '-5 + 2' = {calculate('-5 + 2')}")               # Expected: -3.0

# Error cases
print(f"Expression: '5 / 0' = {calculate('5 / 0')}")
print(f"Expression: '(5 +)' = {calculate('(5 +)')}") # Should show "Error: Insufficient operands..." or similar
print(f"Expression: '5 + )' = {calculate('5 + )')}")
print(f"Expression: '(5 + 2' = {calculate('(5 + 2')}")
print(f"Expression: '3 ^ 4' = {calculate('3 ^ 4')}")
print(f"Expression: '1 $ 2' = {calculate('1 $ 2')}")
print(f"Expression: '1 2 +' = {calculate('1 2 +')}") # Test for malformed postfix input from shunting yard
print(f"Expression: '1 +' = {calculate('1 +')}") # Example that produces ['1', '+'] from shunting_yard
print(f"Expression: '1 2' = {calculate('1 2')}") # Too many operands without operator