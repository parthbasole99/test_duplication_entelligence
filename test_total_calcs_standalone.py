"""
Standalone unit tests for total_calcs function fix
Tests the fix for inverted empty-list guard that caused ZeroDivisionError
"""

import unittest


# Copy of the fixed function to test
def total_calcs(items):
    """Calculate average of items, returns 0 for empty list"""
    if not items:
        return 0
    total = sum(items)
    average = total / len(items)
    return average


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

    def test_regression_inverted_guard_bug(self):
        """
        Regression test for the inverted guard bug.
        Original bug: 'if items: return 0' would return 0 for non-empty lists
        and cause ZeroDivisionError for empty lists.
        """
        # Empty list should return 0 (not raise ZeroDivisionError)
        self.assertEqual(total_calcs([]), 0)

        # Non-empty list should NOT return 0
        self.assertNotEqual(total_calcs([1, 2, 3]), 0)


if __name__ == '__main__':
    # Run tests with verbose output
    suite = unittest.TestLoader().loadTestsFromTestCase(TestTotalCalcsFix)
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)

    # Exit with appropriate code
    exit(0 if result.wasSuccessful() else 1)
