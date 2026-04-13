"""Unit tests for eea.api.redirector.restapi.add module

These tests cover add_redirects validation logic with a mock storage:
- Validation of redirect items (missing path, target, self-redirect)
"""

import unittest
from unittest.mock import MagicMock
from eea.api.redirector.restapi.add import add_redirects


class FakeStorage:
    """Mock storage that always succeeds"""

    def set(self, path, target):
        return True


class FakeStorageFail:
    """Mock storage that always fails"""

    def set(self, path, target):
        return None


class TestAddRedirects(unittest.TestCase):
    """Tests for add_redirects function"""

    def test_add_valid_redirect(self):
        storage = FakeStorage()
        redirects = [{"path": "/old", "redirect-to": "/new"}]
        success, failed = add_redirects(storage, redirects)
        self.assertEqual(success, 1)
        self.assertEqual(len(failed), 0)

    def test_add_multiple_valid_redirects(self):
        storage = FakeStorage()
        redirects = [
            {"path": "/old1", "redirect-to": "/new1"},
            {"path": "/old2", "redirect-to": "/new2"},
        ]
        success, failed = add_redirects(storage, redirects)
        self.assertEqual(success, 2)
        self.assertEqual(len(failed), 0)

    def test_non_dict_item(self):
        storage = FakeStorage()
        redirects = ["not a dict"]
        success, failed = add_redirects(storage, redirects)
        self.assertEqual(success, 0)
        self.assertEqual(len(failed), 1)
        self.assertIn("must be a dictionary", failed[0]["error"])

    def test_missing_path(self):
        storage = FakeStorage()
        redirects = [{"redirect-to": "/new"}]
        success, failed = add_redirects(storage, redirects)
        self.assertEqual(success, 0)
        self.assertEqual(len(failed), 1)
        self.assertIn("Missing 'path'", failed[0]["error"])

    def test_missing_target(self):
        storage = FakeStorage()
        redirects = [{"path": "/old"}]
        success, failed = add_redirects(storage, redirects)
        self.assertEqual(success, 0)
        self.assertEqual(len(failed), 1)
        self.assertIn("Missing 'redirect-to'", failed[0]["error"])

    def test_path_without_leading_slash(self):
        storage = FakeStorage()
        redirects = [{"path": "old", "redirect-to": "/new"}]
        success, failed = add_redirects(storage, redirects)
        self.assertEqual(success, 0)
        self.assertEqual(len(failed), 1)
        self.assertIn("must start with", failed[0]["error"])

    def test_self_redirect(self):
        storage = FakeStorage()
        redirects = [{"path": "/same", "redirect-to": "/same"}]
        success, failed = add_redirects(storage, redirects)
        self.assertEqual(success, 0)
        self.assertEqual(len(failed), 1)
        self.assertIn("cannot be the same", failed[0]["error"])

    def test_empty_target_allowed_for_gone(self):
        storage = FakeStorage()
        redirects = [{"path": "/old", "redirect-to": ""}]
        success, failed = add_redirects(storage, redirects)
        self.assertEqual(success, 1)
        self.assertEqual(len(failed), 0)

    def test_none_target_not_allowed(self):
        storage = FakeStorage()
        redirects = [{"path": "/old", "redirect-to": None}]
        success, failed = add_redirects(storage, redirects)
        self.assertEqual(success, 0)
        self.assertIn("Missing 'redirect-to'", failed[0]["error"])

    def test_storage_failure(self):
        storage = FakeStorageFail()
        redirects = [{"path": "/old", "redirect-to": "/new"}]
        success, failed = add_redirects(storage, redirects)
        self.assertEqual(success, 0)
        self.assertEqual(len(failed), 1)
        self.assertIn("Failed to set", failed[0]["error"])

    def test_mixed_valid_and_invalid(self):
        storage = FakeStorage()
        redirects = [
            {"path": "/old1", "redirect-to": "/new1"},
            "not a dict",
            {"path": "/old2", "redirect-to": "/new2"},
        ]
        success, failed = add_redirects(storage, redirects)
        self.assertEqual(success, 2)
        self.assertEqual(len(failed), 1)


if __name__ == "__main__":
    unittest.main()