"""
Unit tests for SQL injection fix in app.py
"""
import unittest
from unittest.mock import Mock, patch, MagicMock
import sys
import os

# Add the repo directory to the path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))


class TestSQLInjectionFix(unittest.TestCase):
    """Test cases to verify SQL injection vulnerability is fixed."""

    def setUp(self):
        """Set up test fixtures."""
        # Mock the execute_query function in app module
        self.execute_query_patcher = patch('builtins.execute_query', create=True)
        self.mock_execute = self.execute_query_patcher.start()

    def tearDown(self):
        """Clean up after tests."""
        self.execute_query_patcher.stop()

    def test_fetch_user_profile_uses_parameterized_query(self):
        """Test that fetch_user_profile uses parameterized queries."""
        # Import after patching
        import app
        app.execute_query = self.mock_execute

        self.mock_execute.return_value = [{"id": 1, "name": "Test User"}]

        # Test with normal user_id
        user_id = 1
        result = app.fetch_user_profile(user_id)

        # Verify execute_query was called with parameterized query
        self.mock_execute.assert_called_once_with(
            "SELECT * FROM users WHERE id = %s",
            (user_id,)
        )
        self.assertEqual(result, [{"id": 1, "name": "Test User"}])

    def test_fetch_user_profile_prevents_sql_injection(self):
        """Test that malicious input is safely handled as parameter."""
        import app
        app.execute_query = self.mock_execute

        self.mock_execute.return_value = []

        # Attempt SQL injection attack
        malicious_input = "1 OR 1=1; DROP TABLE users; --"
        result = app.fetch_user_profile(malicious_input)

        # Verify the malicious input is passed as a parameter (safely escaped)
        # not interpolated into the SQL string
        self.mock_execute.assert_called_once_with(
            "SELECT * FROM users WHERE id = %s",
            (malicious_input,)
        )

        # The malicious string should be treated as a literal value,
        # not executed as SQL code
        args, kwargs = self.mock_execute.call_args
        self.assertEqual(args[0], "SELECT * FROM users WHERE id = %s")
        self.assertEqual(args[1], (malicious_input,))
        # Verify no f-string or string formatting was used
        self.assertNotIn("OR 1=1", args[0])
        self.assertNotIn("DROP TABLE", args[0])

    def test_fetch_user_profile_with_string_id(self):
        """Test with string user_id (UUID or similar)."""
        import app
        app.execute_query = self.mock_execute

        self.mock_execute.return_value = [{"id": "abc-123", "name": "Test User"}]

        user_id = "abc-123"
        result = app.fetch_user_profile(user_id)

        self.mock_execute.assert_called_once_with(
            "SELECT * FROM users WHERE id = %s",
            (user_id,)
        )
        self.assertEqual(result, [{"id": "abc-123", "name": "Test User"}])

    def test_fetch_user_profile_with_special_characters(self):
        """Test that special SQL characters are safely handled."""
        import app
        app.execute_query = self.mock_execute

        self.mock_execute.return_value = []

        # Test with various special characters that could break SQL
        special_inputs = [
            "'; DELETE FROM users; --",
            "1' UNION SELECT * FROM passwords--",
            "admin'--",
            "1' OR '1'='1",
        ]

        for malicious_id in special_inputs:
            self.mock_execute.reset_mock()
            app.fetch_user_profile(malicious_id)

            # Verify parameterized query is used
            args = self.mock_execute.call_args[0]
            self.assertEqual(args[0], "SELECT * FROM users WHERE id = %s")
            self.assertEqual(args[1], (malicious_id,))

    def test_sql_query_structure_prevents_injection(self):
        """Test that the query structure uses placeholders instead of f-strings."""
        import app
        import inspect

        # Get the source code of fetch_user_profile
        source = inspect.getsource(app.fetch_user_profile)

        # Verify it doesn't use f-string interpolation for SQL
        self.assertNotIn('f"SELECT', source)
        self.assertNotIn("f'SELECT", source)

        # Verify it uses parameterized query placeholder
        self.assertIn('%s', source)
        self.assertIn('execute_query', source)


if __name__ == '__main__':
    unittest.main()
