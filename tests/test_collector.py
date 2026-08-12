# -*- coding: utf-8 -*-
"""
ThreatCollector Unit Test Suite
Tests SQLite database schema initialization, user authentication, IoC insertion, search querying, and Flask endpoints.
"""

import sys
import os
import unittest
import sqlite3
import tempfile

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import database
from app import app


class TestThreatCollector(unittest.TestCase):

    def setUp(self):
        """Set up temporary test database and Flask test client."""
        fd, self.temp_db_path = tempfile.mkstemp(suffix=".db")
        os.close(fd)  # Close handle immediately so SQLite can access on Windows
        database.DB_NAME = self.temp_db_path
        database.init_db()

        app.config['TESTING'] = True
        app.config['SECRET_KEY'] = 'test_secret_key'
        self.client = app.test_client()

    def tearDown(self):
        """Clean up temporary test database."""
        if os.path.exists(self.temp_db_path):
            try:
                os.unlink(self.temp_db_path)
            except OSError:
                pass

    def test_database_init(self):
        """Verify database tables created."""
        with sqlite3.connect(database.DB_NAME) as conn:
            c = conn.cursor()
            c.execute("SELECT name FROM sqlite_master WHERE type='table';")
            tables = [row[0] for row in c.fetchall()]
            self.assertIn("iocs", tables)
            self.assertIn("users", tables)

    def test_user_authentication(self):
        """Test adding user and password verification."""
        database.add_user("analyst", "SecurePass123!", role="admin")
        user = database.verify_user("analyst", "SecurePass123!")
        self.assertIsNotNone(user)
        self.assertEqual(user["username"], "analyst")
        self.assertEqual(user["role"], "admin")

        invalid_user = database.verify_user("analyst", "WrongPassword")
        self.assertIsNone(invalid_user)

    def test_ioc_operations(self):
        """Test inserting and searching IoC entries."""
        database.add_ioc("http://malicious-domain.test/phish", source="PhishTank")
        
        recent = database.get_recent(limit=10)
        self.assertGreater(len(recent), 0)
        self.assertEqual(recent[0][0], "http://malicious-domain.test/phish")

        found = database.find_ioc("http://malicious-domain.test/phish")
        self.assertIsNotNone(found)
        self.assertEqual(found[2], "PhishTank")

    def test_unauthorized_admin_access(self):
        """Test blocking unauthorized access to admin dashboard."""
        response = self.client.get('/admin', follow_redirects=True)
        self.assertIn(b"login", response.data.lower())


if __name__ == "__main__":
    unittest.main()
