"""
Unit tests for total_calcs function fix using unittest
Tests the fix for inverted empty-list guard that caused ZeroDivisionError
"""

import unittest
import sys
import os

# Add current directory to path to import data_processor
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from data_processor import total_calcs


class TestTotalCalcsFix(unittest.TestCase):
    """Test suite for total_calcs function"""

    def test_total_calcs_with_empty_list(self):
        """Test that empty list returns 0 without ZeroDivisionError"""
        result = total_calcs([])
        self.assertEqual(result, 0, "Empty list should return 0")

    def test_total_calcs_with_single_item(self):
        """Test calculation with a single item"""
        result = total_calcs([10])
        self.assertEqual(result, 10, "Single item [10] should return average of 10")

    def test_total_calcs_with_multiple_items(self):
        """Test calculation with multiple items"""
        result = total_calcs([10, 20, 30])
        self.assertEqual(result, 20, "Items [10, 20, 30] should return average of 20")

    def test_total_calcs_with_negative_numbers(self):
        """Test calculation with negative numbers"""
        result = total_calcs([-5, -10, -15])
        self.assertEqual(result, -10, "Negative numbers should be handled correctly")

    def test_total_calcs_with_mixed_numbers(self):
        """Test calculation with mixed positive and negative numbers"""
        result = total_calcs([-10, 0, 10])
        self.assertEqual(result, 0, "Mixed numbers should be handled correctly")

    def test_total_calcs_with_floats(self):
        """Test calculation with floating point numbers"""
        result = total_calcs([1.5, 2.5, 3.0])
        expected = 7.0 / 3
        self.assertAlmostEqual(result, expected, places=5,
                               msg="Float numbers should be handled correctly")

    def test_total_calcs_with_large_list(self):
        """Test calculation with a large list"""
        large_list = list(range(1, 101))  # 1 to 100
        result = total_calcs(large_list)
        expected = sum(large_list) / len(large_list)
        self.assertEqual(result, expected, "Large list should be calculated correctly")

    def test_total_calcs_does_not_raise_zero_division_error(self):
        """Explicit test that empty list does not raise ZeroDivisionError"""
        try:
            result = total_calcs([])
            self.assertEqual(result, 0)
        except ZeroDivisionError:
            self.fail("total_calcs raised ZeroDivisionError on empty list")

    def test_total_calcs_with_truthy_list_does_not_return_zero(self):
        """Test that non-empty lists don't incorrectly return 0 (the original bug)"""
        result = total_calcs([5, 10, 15])
        self.assertNotEqual(result, 0, "Non-empty list should not return 0")
        self.assertEqual(result, 10, "Should calculate correct average")


if __name__ == '__main__':
    unittest.main(verbosity=2)
