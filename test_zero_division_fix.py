"""
Unit tests for zero division fixes in average calculations.

Tests the fixes for:
- data_processor.py::total_calcs
- app.py::calculate_total
- app2.py::total_calcs
"""
import unittest
import sys
import os
from unittest.mock import MagicMock

# Mock external dependencies before importing modules
sys.modules['requests'] = MagicMock()

# Add the repo directory to the path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))


class TestZeroDivisionFixes(unittest.TestCase):
    """Test cases to verify zero division vulnerabilities are fixed."""

    def test_data_processor_total_calcs_empty_list(self):
        """Test data_processor.total_calcs with empty list returns 0."""
        from data_processor import total_calcs

        result = total_calcs([])
        self.assertEqual(result, 0, "Empty list should return 0, not raise ZeroDivisionError")

    def test_data_processor_total_calcs_single_item(self):
        """Test data_processor.total_calcs with single item."""
        from data_processor import total_calcs

        result = total_calcs([10])
        self.assertEqual(result, 10.0)

    def test_data_processor_total_calcs_multiple_items(self):
        """Test data_processor.total_calcs with multiple items."""
        from data_processor import total_calcs

        result = total_calcs([1, 2, 3, 4, 5])
        self.assertEqual(result, 3.0)

    def test_data_processor_total_calcs_negative_numbers(self):
        """Test data_processor.total_calcs with negative numbers."""
        from data_processor import total_calcs

        result = total_calcs([-10, -20, -30])
        self.assertEqual(result, -20.0)

    def test_data_processor_total_calcs_mixed_numbers(self):
        """Test data_processor.total_calcs with mixed positive/negative."""
        from data_processor import total_calcs

        result = total_calcs([-5, 0, 5, 10])
        self.assertEqual(result, 2.5)

    def test_app_calculate_total_empty_list(self):
        """Test app.calculate_total with empty list returns 0."""
        import app

        result = app.calculate_total([])
        self.assertEqual(result, 0, "Empty list should return 0, not raise ZeroDivisionError")

    def test_app_calculate_total_single_item(self):
        """Test app.calculate_total with single item."""
        import app

        result = app.calculate_total([42])
        self.assertEqual(result, 42.0)

    def test_app_calculate_total_multiple_items(self):
        """Test app.calculate_total with multiple items."""
        import app

        result = app.calculate_total([10, 20, 30, 40])
        self.assertEqual(result, 25.0)

    def test_app_calculate_total_float_values(self):
        """Test app.calculate_total with float values."""
        import app

        result = app.calculate_total([1.5, 2.5, 3.5])
        self.assertAlmostEqual(result, 2.5)

    def test_app2_total_calcs_empty_list(self):
        """Test app2.total_calcs with empty list returns 0."""
        import app2

        result = app2.total_calcs([])
        self.assertEqual(result, 0, "Empty list should return 0, not raise ZeroDivisionError")

    def test_app2_total_calcs_single_item(self):
        """Test app2.total_calcs with single item."""
        import app2

        result = app2.total_calcs([100])
        self.assertEqual(result, 100.0)

    def test_app2_total_calcs_multiple_items(self):
        """Test app2.total_calcs with multiple items."""
        import app2

        result = app2.total_calcs([5, 10, 15, 20, 25])
        self.assertEqual(result, 15.0)

    def test_app2_total_calcs_large_numbers(self):
        """Test app2.total_calcs with large numbers."""
        import app2

        result = app2.total_calcs([1000, 2000, 3000])
        self.assertEqual(result, 2000.0)

    def test_all_functions_consistent_behavior(self):
        """Test that all three functions behave consistently."""
        from data_processor import total_calcs as dp_total_calcs
        import app
        import app2

        test_cases = [
            [],
            [5],
            [1, 2, 3, 4, 5],
            [10, 20, 30],
        ]

        for test_input in test_cases:
            # Calculate expected result
            if not test_input:
                expected = 0
            else:
                expected = sum(test_input) / len(test_input)

            # All three functions should produce the same result
            result_dp = dp_total_calcs(test_input)
            result_app = app.calculate_total(test_input)
            result_app2 = app2.total_calcs(test_input)

            self.assertEqual(result_dp, expected,
                           f"data_processor.total_calcs failed for {test_input}")
            self.assertEqual(result_app, expected,
                           f"app.calculate_total failed for {test_input}")
            self.assertEqual(result_app2, expected,
                           f"app2.total_calcs failed for {test_input}")

    def test_no_zero_division_error_raised(self):
        """Explicitly test that ZeroDivisionError is not raised."""
        from data_processor import total_calcs as dp_total_calcs
        import app
        import app2

        # These should NOT raise ZeroDivisionError
        try:
            dp_total_calcs([])
            app.calculate_total([])
            app2.total_calcs([])
        except ZeroDivisionError:
            self.fail("ZeroDivisionError was raised for empty list - fix not working!")


if __name__ == '__main__':
    unittest.main()
