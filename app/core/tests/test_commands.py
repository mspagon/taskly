"""
Test custom django management commands.
"""
from unittest.mock import patch

from psycopg2 import OperationalError as Psycopg2OpError

from django.core.management import call_command
from django.db.utils import OperationalError
from django.test import SimpleTestCase


@patch('core.management.commands.wait_for_db.Command.check')
class TestCommands(SimpleTestCase):
    """Test custom commands."""

    def test_wait_for_db_when_database_is_ready(self, patched_check):
        """Test wait_for_db command when database is in a ready state."""
        patched_check.returned_value = True

        call_command('wait_for_db')

        patched_check.assert_called_once_with(databases=['default'])

    @patch('time.sleep')
    def test_wait_for_db_when_database_is_not_ready(self, patched_sleep, patched_check):
        """Test wait_for_db command when database is not yet ready.

        There exists two different scenarios for when the database is not yet ready:
          1) Postgres is not ready to accept connections:
             'psycopg2.OperationalError' is thrown.
          2) Postgres is ready to accept connections, but it has not set up the test database yet:
             'django.db.utils.OperationalError' is thrown.

        Patches 'time.sleep' so test case is not slow.
        """
        # Call command many times, throwing 2 psycopg2 errors, three django errors, and eventually returning True.
        patched_check.side_effect = [Psycopg2OpError] * 2 + [OperationalError] * 3 + [True]

        call_command('wait_for_db')

        self.assertEqual(patched_check.call_count, 6)
        patched_check.assert_called_with(databases=['default'])
