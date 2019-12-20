import unittest
import csv
import os

from parsers.parser import Parser
from utils import fieldnames
from config_loader.config import BaseConfig


class ParserEmptyTestCase(unittest.TestCase):

    def setUp(self):
        self.report_path = "app/fixtures/report"
        self.butcher_report_file_path = f"{self.report_path}/butcher_report.csv"
        if os.path.exists(self.butcher_report_file_path):
            os.remove(self.butcher_report_file_path)
        with open(self.butcher_report_file_path, 'w') as csv_report:
            writer = csv.DictWriter(csv_report, fieldnames=fieldnames)
            writer.writeheader()
            csv_report.close()

    def test_check_existences__empty(self):
        p = Parser("high", self.report_path)
        p.start()
        p._check_existences('12/05-17:35:52.823112 ')
        self.assertFalse(p.timestamps, list)

    def test_check_existences__None(self):
        p = Parser("high", self.report_path)
        p.start()
        p._check_existences(None)
        self.assertFalse(p.timestamps, list)


class ParserCompiledTestCase(unittest.TestCase):

    def setUp(self):
        self.report_path = "app/fixtures/report"
        self.butcher_report_file_path = f"{self.report_path}/butcher_report_compiled.csv"

    def test_check_timestamp_existences(self):
        p = Parser("low", self.report_path)
        p.report_path = self.butcher_report_file_path
        p.start()
        self.assertTrue(p._check_existences('12/05-17:35:52.823112 '))

    def test_check_timestamp_existences_None(self):
        p = Parser("low", self.report_path)
        p.report_path = self.butcher_report_file_path
        p.start()
        self.assertFalse(p._check_existences(None))


class TriggerNotifyTestCase(unittest.TestCase):

    def setUp(self):
        self.baseConfig = BaseConfig(path='app/fixtures/butcher.ini')
        del self.baseConfig.notifications['osd']
        del self.baseConfig.notifications['email']
        self.report_path = "fixtures/report"

    def test_trigger_notify(self):
        p = Parser("low", self.report_path)
        p.events = 4
        p.notify(self.baseConfig)
        self.assertEqual(p.events, 0)

    def test_trigger_0_notify(self):
        p = Parser("low", self.report_path)
        p.events = 0
        p.notify(self.baseConfig)
        self.assertEqual(p.events, 0)


if __name__ == '__main__':
    unittest.main()
