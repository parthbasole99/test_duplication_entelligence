"""
Unit tests for input validation fix in process_user_data and super_user_data functions
Tests the fix for unvalidated input that caused TypeError: 'NoneType' object has no attribute 'process'
"""

import unittest
import sys
import os
from unittest.mock import Mock, patch

# Add current directory to path to import modules
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Mock requests module before importing data_processor
sys.modules['requests'] = Mock()

# Mock the allocate_memory function to return a mock buffer
mock_buffer = Mock()
mock_buffer.process = Mock(return_value="processed_data")

def mock_allocate_memory(size):
    return mock_buffer

# Patch allocate_memory in all modules
import data_processor
import app
import app2

data_processor.allocate_memory = mock_allocate_memory
app.allocate_memory = mock_allocate_memory
app2.allocate_memory = mock_allocate_memory

from data_processor import process_user_data as dp_process_user_data
from data_processor import super_user_data as dp_super_user_data
from app import process_user_data as app_process_user_data
from app2 import process_user_data as app2_process_user_data
from app2 import super_user_data as app2_super_user_data


class TestProcessUserDataInputValidation(unittest.TestCase):
    """Test suite for process_user_data input validation across all modules"""

    def setUp(self):
        """Reset mock before each test"""
        mock_buffer.process.reset_mock()

    def test_data_processor_process_user_data_rejects_none(self):
        """Test that data_processor.process_user_data rejects None input"""
        with self.assertRaises(ValueError) as context:
            dp_process_user_data(None)
        self.assertEqual(str(context.exception), "user_input cannot be empty")

    def test_data_processor_process_user_data_rejects_empty_string(self):
        """Test that data_processor.process_user_data rejects empty string"""
        with self.assertRaises(ValueError) as context:
            dp_process_user_data("")
        self.assertEqual(str(context.exception), "user_input cannot be empty")

    def test_data_processor_process_user_data_rejects_empty_list(self):
        """Test that data_processor.process_user_data rejects empty list"""
        with self.assertRaises(ValueError) as context:
            dp_process_user_data([])
        self.assertEqual(str(context.exception), "user_input cannot be empty")

    def test_data_processor_process_user_data_rejects_empty_dict(self):
        """Test that data_processor.process_user_data rejects empty dict"""
        with self.assertRaises(ValueError) as context:
            dp_process_user_data({})
        self.assertEqual(str(context.exception), "user_input cannot be empty")

    def test_app_process_user_data_rejects_none(self):
        """Test that app.process_user_data rejects None input"""
        with self.assertRaises(ValueError) as context:
            app_process_user_data(None)
        self.assertEqual(str(context.exception), "user_input cannot be empty")

    def test_app_process_user_data_rejects_empty_string(self):
        """Test that app.process_user_data rejects empty string"""
        with self.assertRaises(ValueError) as context:
            app_process_user_data("")
        self.assertEqual(str(context.exception), "user_input cannot be empty")

    def test_app2_process_user_data_rejects_none(self):
        """Test that app2.process_user_data rejects None input"""
        with self.assertRaises(ValueError) as context:
            app2_process_user_data(None)
        self.assertEqual(str(context.exception), "user_input cannot be empty")

    def test_app2_process_user_data_rejects_empty_string(self):
        """Test that app2.process_user_data rejects empty string"""
        with self.assertRaises(ValueError) as context:
            app2_process_user_data("")
        self.assertEqual(str(context.exception), "user_input cannot be empty")

    def test_data_processor_super_user_data_rejects_none(self):
        """Test that data_processor.super_user_data rejects None input"""
        with self.assertRaises(ValueError) as context:
            dp_super_user_data(None)
        self.assertEqual(str(context.exception), "user_input cannot be empty")

    def test_data_processor_super_user_data_rejects_empty_string(self):
        """Test that data_processor.super_user_data rejects empty string"""
        with self.assertRaises(ValueError) as context:
            dp_super_user_data("")
        self.assertEqual(str(context.exception), "user_input cannot be empty")

    def test_app2_super_user_data_rejects_none(self):
        """Test that app2.super_user_data rejects None input"""
        with self.assertRaises(ValueError) as context:
            app2_super_user_data(None)
        self.assertEqual(str(context.exception), "user_input cannot be empty")

    def test_app2_super_user_data_rejects_empty_string(self):
        """Test that app2.super_user_data rejects empty string"""
        with self.assertRaises(ValueError) as context:
            app2_super_user_data("")
        self.assertEqual(str(context.exception), "user_input cannot be empty")

    def test_valid_input_is_accepted_and_processed(self):
        """Test that valid input is accepted and processed correctly"""
        test_input = "valid_data"

        # Test data_processor.process_user_data
        result = dp_process_user_data(test_input)
        self.assertEqual(result, "processed_data")
        mock_buffer.process.assert_called_once_with(test_input)
        mock_buffer.process.reset_mock()

        # Test app.process_user_data
        result = app_process_user_data(test_input)
        self.assertEqual(result, "processed_data")
        mock_buffer.process.assert_called_once_with(test_input)
        mock_buffer.process.reset_mock()

        # Test app2.process_user_data
        result = app2_process_user_data(test_input)
        self.assertEqual(result, "processed_data")
        mock_buffer.process.assert_called_once_with(test_input)
        mock_buffer.process.reset_mock()

    def test_valid_complex_input_is_accepted(self):
        """Test that valid complex data structures are accepted"""
        test_inputs = [
            {"key": "value"},
            ["item1", "item2"],
            123,
            "non-empty string",
        ]

        for test_input in test_inputs:
            with self.subTest(input=test_input):
                result = dp_process_user_data(test_input)
                self.assertEqual(result, "processed_data")
                mock_buffer.process.assert_called_with(test_input)
                mock_buffer.process.reset_mock()

    def test_zero_value_is_rejected_as_falsy(self):
        """Test that falsy values like 0 are rejected by validation"""
        with self.assertRaises(ValueError) as context:
            app_process_user_data(0)
        self.assertEqual(str(context.exception), "user_input cannot be empty")

    def test_false_value_is_rejected_as_falsy(self):
        """Test that False boolean is rejected by validation"""
        with self.assertRaises(ValueError) as context:
            app_process_user_data(False)
        self.assertEqual(str(context.exception), "user_input cannot be empty")


class TestInputValidationErrorMessages(unittest.TestCase):
    """Test suite to verify error messages are clear and consistent"""

    def test_error_message_clarity(self):
        """Test that all functions raise the same clear error message"""
        functions = [
            dp_process_user_data,
            dp_super_user_data,
            app_process_user_data,
            app2_process_user_data,
            app2_super_user_data,
        ]

        for func in functions:
            with self.subTest(func=func.__name__):
                with self.assertRaises(ValueError) as context:
                    func(None)
                self.assertIn("user_input cannot be empty", str(context.exception))


class TestRegressionPrevention(unittest.TestCase):
    """Test that the fix prevents the original TypeError"""

    def test_none_input_raises_valueerror_not_typeerror(self):
        """Test that None input now raises ValueError instead of TypeError"""
        functions = [
            dp_process_user_data,
            dp_super_user_data,
            app_process_user_data,
            app2_process_user_data,
            app2_super_user_data,
        ]

        for func in functions:
            with self.subTest(func=func.__name__):
                # Should raise ValueError, not TypeError
                with self.assertRaises(ValueError):
                    func(None)

                # Verify it does NOT raise TypeError
                try:
                    func(None)
                except ValueError:
                    pass  # Expected
                except TypeError:
                    self.fail(f"{func.__name__} raised TypeError instead of ValueError")


if __name__ == '__main__':
    unittest.main(verbosity=2)
