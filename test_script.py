# To run this test, run the below command in your terminal:
# python -m unittest test_script.py

import unittest
from main import get_project_diff, summarize_changes, update_changelog

class TestCodeActivityLogger(unittest.TestCase):

    def test_diff_extraction(self):
        # Replace /path/to/old with your backup dir
        # Replace /path/to/new with your test project dir, make sure to have diff codes or atleast some modified code between backup and yur test project
        diff_text = get_project_diff("/path/to/old", "/path/to/new")
        self.assertIsNotNone(diff_text)

    def test_gemini_summary(self):
        summary = summarize_changes("Added logging function.")
        self.assertTrue(len(summary) > 0)

    def test_changelog_update(self):
        changelog_entries = [("2025-02-08", "Test-Project", "Updated logging.")]
        update_changelog(changelog_entries)

        # Replace /Path/to/your/changelog.md with your changelog.md of the workflow-tracker with git initalized, easiest way is to create a repo on GitHub web and git clone to your system
        with open("/Path/to/your/changelog.md", "r") as f:
            content = f.read()
        self.assertIN("Updated logging.", content)

if __name__ == '__main__':
    unittest.main() 