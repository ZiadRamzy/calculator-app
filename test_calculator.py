import unittest
from calculator import calculate

class TestCalculator(unittest.TestCase):

    def test_addition(self):
        self.assertEqual(calculate("1 + 2"), 3.0)

    def test_substraction(self):
        self.assertEqual(calculate("2 - 1"), 1.0)
        self.assertEqual(calculate("1 - 2"), -1.0)

    def test_multiplication(self):
        self.assertEqual(calculate("2 * 3"), 6.0)

    def test_division(self):
        self.assertEqual(calculate("3 / 2"), 1.5)

    def test_division_by_zero(self):
        self.assertEqual(calculate("3 / 0"), "Division by zero error: Cannot divide by zero")

    def test_invalid_format_too_few_parts(self):
        self.assertEqual(calculate("1 + "), "Invalid input format: Expected 'number operator number'")

    def test_invalid_format_too_many_parts(self):
        self.assertEqual(calculate("1 + 2 3"), "Invalid input format: Expected 'number operator number'")

    def test_invalid_number_input_first_operand(self):
        self.assertEqual(calculate("hello + 2"), "Invalid number input: Both operands must be valid numbers")

    def test_invalid_number_input_second_operand(self):
        self.assertEqual(calculate("10 * world"), "Invalid number input: Both operands must be valid numbers")

    def test_invalid_operator(self):
        self.assertEqual(calculate("5 % 2"), "Invalid operator: Supported operators are +, -, *, /")

if __name__ == '__main__':
    unittest.main()