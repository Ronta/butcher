import unittest

from rule_manager.loader import RuleLoader


class RuleLoaderTestCase(unittest.TestCase):

    def test_run_with_empty_path(self):
        r = RuleLoader()
        self.assertTrue(r.run())

    def test_get_all_rule_files(self):
        r = RuleLoader(rules_path='app/fixtures/rules')
        self.assertTrue(r.run())

    def test_get_all_rule_files_with_empty_path(self):
        r = RuleLoader()
        r.run()
        self.assertEqual(type(r.rules_files), type([]))

    def test_rule_parser(self):
        r = RuleLoader(rules_path='app/fixtures/rules')
        r.get_all_rule_files()
        r.rule_parser(rules_file=r.rules_files[0])
        self.assertEqual(type(r.rules_files), type([]))


if __name__ == '__main__':
    unittest.main()
