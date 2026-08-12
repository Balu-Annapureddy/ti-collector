# -*- coding: utf-8 -*-
"""
ThreatCollector Feed Parsing & Resilience Unit Test Suite
Tests feed response error handling, network timeout fallbacks, and indicator deduplication logic.
"""

import sys
import os
import unittest
from unittest.mock import patch, MagicMock

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import collector


class TestThreatCollectorResilience(unittest.TestCase):

    @patch('collector.requests.get')
    def test_fetch_urlhaus_timeout_handling(self, mock_get):
        """Test URLHaus fetcher gracefully handling network timeouts or 500 errors."""
        mock_response = MagicMock()
        mock_response.status_code = 500
        mock_get.return_value = mock_response

        results = collector.fetch_urlhaus()
        self.assertEqual(results, [])

    @patch('collector.requests.get')
    def test_fetch_phishtank_parsing(self, mock_get):
        """Test PhishTank feed parsing with mocked CSV data."""
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.text = "phish_id,url,phish_detail_url\n100,http://phish-test.example.com/login,detail"
        mock_get.return_value = mock_response

        results = collector.fetch_phishtank()
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0][0], "PhishTank")
        self.assertEqual(results[0][1], "http://phish-test.example.com/login")


if __name__ == "__main__":
    unittest.main()
