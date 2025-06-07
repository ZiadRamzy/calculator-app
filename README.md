# Calculator App

A robust command-line calculator application capable of parsing and evaluating mathematical expressions, including operator precedence, parentheses, and trigonometric functions. This project was built as part of a coding challenge to explore expression parsing and the use of stack data structures.

This project was developed as a solution to the ["Build Your Own Calculator"](https://codingchallenges.fyi/challenges/challenge-calculator/) challenge from codingchallenges.fyi. The challenge encourages building a calculator that can parse mathematical expressions and make use of the stack data structure.

## Table of Contents

- [Features](#features)
- [How It Works](#how-it-works)
- [Getting Started](#getting-started)
  - [Prerequisites](#prerequisites)
  - [Installation](#installation)
  - [Running the Calculator](#running-the-calculator)
  - [Running Tests](#running-tests)
- [Project Structure](#project-structure)


## Features

- **Basic Arithmetic Operations:** Supports addition (`+`), subtraction (`-`), multiplication (`*`), and division (`/`).
- **Operator Precedence:** Correctly handles the order of operations (e.g., multiplication and division before addition and subtraction).
- **Parentheses Support:** Allows grouping of operations using `()` to override standard precedence.
- **Trigonometric Functions:** Includes `sin()`, `cos()`, and `tan()` (angles are assumed to be in degrees).
- **Decimal Numbers:** Supports calculations with floating-point numbers.
- **Unary Minus:** Correctly handles negative numbers (e.g., `-5 + 2`).
- **Robust Error Handling:** Provides informative error messages for:
    - Invalid input format.
    - Division by zero.
    - Unmatched parentheses.
    - Invalid or unsupported operators/characters.
    - Insufficient operands for operations or functions.
    - Malformed expressions.

## How It Works

This calculator leverages advanced parsing techniques to accurately evaluate mathematical expressions:

1.  **Tokenization:** The input mathematical expression string is first broken down into individual meaningful units (tokens), such as numbers, operators, function names, and parentheses.
2.  **Infix to Postfix Conversion (Shunting-Yard Algorithm):** The tokens, which are initially in infix notation (the standard human-readable format), are converted into postfix notation (Reverse Polish Notation - RPN). This conversion is performed using the [Shunting-Yard Algorithm](https://en.wikipedia.org/wiki/Shunting-yard_algorithm), which makes extensive use of a stack data structure to correctly handle operator precedence and parentheses.
3.  **Postfix Evaluation:** The resulting postfix expression (a sequence of numbers and operators/functions) is then evaluated. This process also uses a stack: numbers are pushed onto the stack, and when an operator or function is encountered, the necessary operands are popped from the stack, the operation is performed, and the result is pushed back onto the stack. The final result is the single value remaining on the stack.

## Getting Started

### Prerequisites

* Python 3.6 or higher installed on your system.
* A code editor (like VS Code) and a terminal.

### Installation

1.  **Clone the repository:**
    ```bash
    git clone [https://github.com/ZiadRamzy/calculator-app.git](https://github.com/ZiadRamzy/calculator-app.git)
    ```
    (Replace `your-username` with your actual GitHub username)
2.  **Navigate to the project directory:**
    ```bash
    cd calculator-app
    ```

### Running the Calculator

You can run the calculator directly from your terminal by executing the `calculator.py` script.
Expressions should be enclosed in quotes to prevent your shell from interpreting special characters like `*`.

```bash
python calculator.py '
```
You'll then see a prompt like Enter expression:. Type your mathematical expression and press Enter. To exit the calculator, simply type exit and press Enter.

### Examples of interaction:
```
Welcome to the Interactive Calculator!
Enter 'exit' to quit.
Supported operations: +, -, *, /, sin(), cos(), tan(), ()
Angles for sin, cos, tan are in degrees.
Enter expression: 2 + 3 * 4
Result: 14.0
Enter expression: (5 + 5) / 2
Result: 5.0
Enter expression: sin(90) + cos(0)
Result: 2.0
Enter expression: tan(90)
Result: Tangent of 90, 270 degrees (or multiples) is undefined
Enter expression: exit
Exiting calculator. Goodbye!
```


### Running Tests
The project includes a comprehensive suite of unit tests using Python's built-in unittest framework. It's highly recommended to run these tests after making any changes to ensure functionality remains intact.

To run the tests:
```bash
python -m unittest test_calculator.py
```

### Project Structure
```
calculator-app/
├── calculator.py       # Contains the core calculator logic (shunting_yard, evaluate_postfix, calculate)
├── test_calculator.py  # Unit tests for the calculator's functionality
└── README.md           # This file
```

