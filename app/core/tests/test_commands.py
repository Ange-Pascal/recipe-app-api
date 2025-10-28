from unittest.mock import patch
from django.core.management import call_command
from django.db.utils import OperationalError
from psycopg import OperationalError as PsycopgOpError
from django.test import SimpleTestCase


@patch("time.sleep", return_value=None)
class CommandTests(SimpleTestCase):
    """Test commands."""

    def test_wait_for_db_ready(self, patched_sleep):
        """Test waiting for database if database ready."""
        with patch("django.core.management.base.BaseCommand.check") as patched_check:
            patched_check.return_value = True
            call_command("wait_for_db")
            self.assertEqual(patched_check.call_count, 1)
            patched_check.assert_called_with(databases=['default'])

    def test_wait_for_db_delay(self, patched_sleep):
        """Test waiting for database when getting OperationalError."""
        with patch("django.core.management.base.BaseCommand.check") as patched_check:
            patched_check.side_effect = [PsycopgOpError] * 2 + [OperationalError] * 3 + [True]
            call_command("wait_for_db")
            self.assertEqual(patched_check.call_count, 6)
            patched_check.assert_called_with(databases=['default'])
