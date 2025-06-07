import unittest
import math 
from calculator import calculate

class TestCalculator(unittest.TestCase):

    # --- Tests from Step 1 (basic operations) ---
    def test_addition(self):
        self.assertEqual(calculate("1 + 2"), 3.0)

    def test_subtraction(self):
        self.assertEqual(calculate("2 - 1"), 1.0)

    def test_multiplication(self):
        self.assertEqual(calculate("2 * 3"), 6.0)

    def test_division(self):
        self.assertEqual(calculate("3 / 2"), 1.5)

    def test_division_by_zero(self):
        self.assertEqual(calculate("5 / 0"), "Division by zero error")

    def test_invalid_format_too_few_parts(self):
        self.assertEqual(calculate("1 +"), "Error: Insufficient operands for operator '+'")

    def test_invalid_format_too_many_parts(self):
        self.assertEqual(calculate("1 + 2 3"), "Error: Malformed postfix expression") # Example from shunting yard behavior

    def test_invalid_number_input_first_operand(self):
        self.assertEqual(calculate("hello + 2"), "Error: Invalid token: hello") # From shunting_yard
        
    def test_invalid_number_input_second_operand(self):
        self.assertEqual(calculate("10 * world"), "Error: Invalid token: world") # From shunting_yard

    def test_invalid_operator(self):
        self.assertEqual(calculate("5 % 2"), "Error: Invalid character in expression") # From shunting_yard if % is not tokenized

    # --- Tests for Step 2 (precedence and parentheses) ---
    def test_precedence_multiplication_before_addition(self):
        self.assertEqual(calculate("1 + 1 * 5"), 6.0)

    def test_parentheses_override_precedence(self):
        self.assertEqual(calculate("(1 + 1) * 5"), 10.0)

    def test_nested_parentheses_and_precedence(self):
        self.assertEqual(calculate("(1 * 2) - (3 * 4)"), -10.0)

    def test_division_with_parentheses(self):
        self.assertEqual(calculate("10 / (6 - 1)"), 2.0)

    def test_decimal_numbers(self):
        self.assertEqual(calculate("2.5 + 3.0"), 5.5)

    def test_unary_minus(self):
        self.assertEqual(calculate("-5 + 2"), -3.0)
        self.assertEqual(calculate("3 * -2"), -6.0)

    # --- Tests for Step 2/3 Error Handling ---
    def test_unmatched_closing_parenthesis(self):
        self.assertEqual(calculate("5 + )"), "Error: Unmatched closing parenthesis")

    def test_unmatched_opening_parenthesis(self):
        self.assertEqual(calculate("(5 + 2"), "Error: Unmatched opening parenthesis")

    def test_invalid_character_in_expression(self):
        self.assertEqual(calculate("3 ^ 4"), "Error: Invalid character in expression")
        self.assertEqual(calculate("1 $ 2"), "Error: Invalid character in expression")

    def test_incomplete_expression_operator_at_end(self):
        # Shunting yard will put this as ['1', '+'], then evaluation fails
        self.assertEqual(calculate("1 +"), "Error: Insufficient operands for operator '+'")
        
    def test_incomplete_expression_too_many_operands(self):
        # Shunting yard will put this as ['1', '2'], then evaluation fails
        self.assertEqual(calculate("1 2"), "Error: Malformed postfix expression")

    # --- Tests for Step 3 (trigonometric functions) ---
    def test_sin_90_degrees(self):
        self.assertAlmostEqual(calculate("sin(90)"), 1.0)

    def test_cos_0_degrees(self):
        self.assertAlmostEqual(calculate("cos(0)"), 1.0)

    def test_tan_45_degrees(self):
        self.assertAlmostEqual(calculate("tan(45)"), 1.0)

    def test_multiplication_with_sin(self):
        self.assertAlmostEqual(calculate("2 * sin(30)"), 1.0) # 2 * 0.5

    def test_nested_expression_in_function(self):
        # sin(1+1) = sin(2)
        expected_sin_2_rad = math.sin(math.radians(2))
        self.assertAlmostEqual(calculate("sin(1 + 1)"), expected_sin_2_rad)

    def test_complex_expression_with_functions(self):
        # cos(90 - 90) = cos(0) = 1.0
        self.assertAlmostEqual(calculate("cos(90 - 90)"), 1.0)
        # 10 + tan(0) = 10 + 0 = 10.0
        self.assertAlmostEqual(calculate("10 + tan(0)"), 10.0)
        # sin(30) + cos(60) = 0.5 + 0.5 = 1.0
        self.assertAlmostEqual(calculate("sin(30) + cos(60)"), 1.0)

    def test_tan_90_degrees_undefined(self):
        self.assertEqual(calculate("tan(90)"), "Tangent of 90, 270 degrees (or multiples) is undefined")

    def test_function_with_no_argument(self):
        self.assertEqual(calculate("sin()"), "Error: Insufficient operands for function 'sin'")

    def test_function_with_too_many_arguments(self):
        self.assertEqual(calculate("sin(90 45)"), "Error: Malformed postfix expression")

    def test_function_with_invalid_argument(self):
        self.assertEqual(calculate("sin(abc)"), "Error: Invalid token: abc")
        
    def test_function_as_unary_op_arg(self):
        self.assertAlmostEqual(calculate("sin(-30)"), math.sin(math.radians(-30)))

    # more general test to ensure no regressions for original Step 1 cases
    def test_single_number(self):
        self.assertEqual(calculate("123"), 123.0)
        self.assertEqual(calculate("-42"), -42.0)
        self.assertEqual(calculate("3.14"), 3.14)

    def test_empty_expression(self):
        self.assertEqual(calculate(""), "Error: Malformed postfix expression") # Or similar error from shunting_yard

    def test_only_spaces(self):
        self.assertEqual(calculate("   "), "Error: Malformed postfix expression") # Or similar error

if __name__ == '__main__':
    unittest.main()