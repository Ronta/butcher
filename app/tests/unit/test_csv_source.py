import unittest
import csv
import os

from utils import fieldnames
from parsers.csv_source.parser import CsvParser


class MyTestCase(unittest.TestCase):

    def setUp(self):
        self.report_path = "app/fixtures/report"
        self.butcher_report_file_path = f"{self.report_path}/butcher_report.csv"
        if os.path.exists(self.butcher_report_file_path):
            os.remove(self.butcher_report_file_path)
        with open(self.butcher_report_file_path, 'w') as csv_report:
            writer = csv.DictWriter(csv_report, fieldnames=fieldnames)
            writer.writeheader()
            csv_report.close()

    def test_csv_parser(self):
        obj = CsvParser(warning_lvl="low", report_path="app/fixtures/report",
                        path="app/fixtures/snort_log/alert.csv",
                        rules_path="app/fixtures/rules"
                    )
        obj.start()


if __name__ == '__main__':
    unittest.main()
