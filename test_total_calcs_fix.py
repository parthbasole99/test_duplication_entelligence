"""
Unit tests for total_calcs function fix
Tests the fix for inverted empty-list guard that caused ZeroDivisionError
"""

import pytest
from data_processor import total_calcs


def test_total_calcs_with_empty_list():
    """Test that empty list returns 0 without ZeroDivisionError"""
    result = total_calcs([])
    assert result == 0, "Empty list should return 0"


def test_total_calcs_with_single_item():
    """Test calculation with a single item"""
    result = total_calcs([10])
    assert result == 10, "Single item [10] should return average of 10"


def test_total_calcs_with_multiple_items():
    """Test calculation with multiple items"""
    result = total_calcs([10, 20, 30])
    assert result == 20, "Items [10, 20, 30] should return average of 20"


def test_total_calcs_with_negative_numbers():
    """Test calculation with negative numbers"""
    result = total_calcs([-5, -10, -15])
    assert result == -10, "Negative numbers should be handled correctly"


def test_total_calcs_with_mixed_numbers():
    """Test calculation with mixed positive and negative numbers"""
    result = total_calcs([-10, 0, 10])
    assert result == 0, "Mixed numbers should be handled correctly"


def test_total_calcs_with_floats():
    """Test calculation with floating point numbers"""
    result = total_calcs([1.5, 2.5, 3.0])
    assert result == pytest.approx(7.0 / 3), "Float numbers should be handled correctly"


def test_total_calcs_with_large_list():
    """Test calculation with a large list"""
    large_list = list(range(1, 101))  # 1 to 100
    result = total_calcs(large_list)
    expected = sum(large_list) / len(large_list)
    assert result == expected, "Large list should be calculated correctly"


def test_total_calcs_does_not_raise_zero_division_error():
    """Explicit test that empty list does not raise ZeroDivisionError"""
    try:
        result = total_calcs([])
        assert result == 0
    except ZeroDivisionError:
        pytest.fail("total_calcs raised ZeroDivisionError on empty list")
