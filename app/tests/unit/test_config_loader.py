import unittest
import configparser

from ButcherExceptions import MissingConfigurationFileError, MissingConfigurationSectionError, MissingRulesPathError
from config_loader.config import BaseConfig
from parsers.csv_source.parser import CsvParser
from utils import notification_methods, email_parameters


class GoodConfigTestCase(unittest.TestCase):

    def setUp(self):
        self.baseConfig = BaseConfig(path='app/fixtures/butcher.ini')

    def test_load_config(self):
        self.assertIsNotNone(self.baseConfig._config)

    def test_warning_level_very_low(self):
        self.baseConfig._handle_warning_level("very_low")
        self.assertEqual(self.baseConfig.warning_lvl,
                         ["unassigned", "very_low", "low", "medium", "high"])

    def test_warning_level_low(self):
        self.baseConfig._handle_warning_level("low")
        self.assertEqual(self.baseConfig.warning_lvl, ["unassigned", "low", "medium", "high"])

    def test_warning_level_medium(self):
        self.baseConfig._handle_warning_level("medium")
        self.assertEqual(self.baseConfig.warning_lvl, ["unassigned", "medium", "high"])

    def test_warning_level_high(self):
        self.baseConfig._handle_warning_level("high")
        self.assertEqual(self.baseConfig.warning_lvl, ["unassigned", "high"])


class CheckPathConfigTestCase(unittest.TestCase):

    def setUp(self):
        self.baseConfig = BaseConfig(path='app/fixtures/butcher.ini')
        self.baseConfig._path = '/foo/bar/antani.ini'

    def test_check_config_path(self):
        with self.assertRaises(MissingConfigurationFileError):
            self.baseConfig._check_config_path()


class EmptyConfigurationTestCase(unittest.TestCase):

    def test_load_general_empty_configuration(self):
        with self.assertRaises(MissingConfigurationSectionError):
            self.baseConfig = BaseConfig(path='app/fixtures/butcher_empty.ini')

    def test_empty_data_source(self):
        empty_config = configparser.ConfigParser()
        empty_config.read('app/fixtures/butcher_empty.ini')
        with self.assertRaises(MissingConfigurationSectionError):
            base_config = BaseConfig(path='app/fixtures/butcher.ini')
            base_config._config = empty_config
            base_config._check_data_source()

    def test_empty_rules_path(self):
        empty_config = configparser.ConfigParser()
        empty_config.read('app/fixtures/butcher_empty.ini')
        base_config = BaseConfig(path='app/fixtures/butcher.ini')
        base_config._config = empty_config
        base_config._check_rules_path()
        self.assertIsNone(base_config.rules_path)

    def test_empty_report_path(self):
        empty_config = configparser.ConfigParser()
        empty_config.read('app/fixtures/butcher_empty.ini')
        with self.assertRaises(MissingConfigurationSectionError):
            base_config = BaseConfig(path='app/fixtures/butcher.ini')
            base_config._config = empty_config
            base_config._check_report()


class CheckCsvDataConfigTestCase(unittest.TestCase):

    def test_empty_csv_path(self):
        empty_config = configparser.ConfigParser()
        empty_config.read('app/fixtures/butcher_empty.ini')
        with self.assertRaises(MissingConfigurationSectionError):
            base_config = BaseConfig(path='app/fixtures/butcher.ini')
            base_config._config = empty_config
            base_config._check_csv_data()

    def test_rule_path_empty(self):
        with self.assertRaises(MissingRulesPathError):
            base_config = BaseConfig(path='app/fixtures/butcher.ini')
            base_config.rules_path = None
            base_config._check_csv_data()

    def test_csv_data_source_configuration(self):
        base_config = BaseConfig(path='app/fixtures/butcher.ini')
        self.assertEqual(type(base_config.parser), CsvParser)


class NotificationsConfigTestCase(unittest.TestCase):

    def setUp(self):
        self.baseConfig = BaseConfig(path='app/fixtures/butcher.ini')

    def test_check_notification(self):
        self.assertEqual(list(self.baseConfig.notifications.keys()), notification_methods)

    def test_osd_notification(self):
        self.assertEqual(list(self.baseConfig.notifications['osd'].keys()), ['icon'])

    def test_email_notification(self):
        self.assertEqual(list(self.baseConfig.notifications['email'].keys()), email_parameters)

    def test_email_empty_dict_notification(self):
        empty_config = configparser.ConfigParser()
        empty_config.read('app/fixtures/butcher_empty.ini')
        with self.assertRaises(MissingConfigurationSectionError):
            base_config = BaseConfig(path='app/fixtures/butcher.ini')
            base_config._config = empty_config
            base_config._check_email_notification()


if __name__ == '__main__':
    unittest.main()
