import csv
import pandas as pd

from utils import fieldnames
from notification.sender import Notification


class Parser(object):
    kwarg = None
    warning_lvl = None
    report_path = None
    timestamps = None

    def __init__(self, warning_lvl, report_path, *args, **kwargs):
        self.warning_lvl = warning_lvl
        self.report_path = f"{report_path}/butcher_report.csv"
        self.kwarg = kwargs
        self.events = 0

    def start(self):
        with open(self.report_path, 'r') as f:
            df = pd.read_csv(f)
            self.timestamps = list(df.timestamp)
            f.close()

    def notify(self, config):
        if self.events != 0:
            data_dict = {"message": f"Butcher: there are {self.events} new events on {config.name}",
                         "body": f"Hey the host {config.name} has {self.events} new events with a warning "
                                 f"level set to {self.warning_lvl}."}
            Notification(config=config, data_dict=data_dict)
            self.events = 0

    def _check_existences(self, timestamp):
        if timestamp is None:
            return False
        if timestamp in self.timestamps:
            return True
        return False

    def save(self, data_dict):
        if not self._check_existences(data_dict['timestamp']):
            with open(self.report_path, mode='a') as csv_report:
                writer = csv.DictWriter(csv_report, fieldnames=fieldnames)
                writer.writerow(data_dict)
                csv_report.close()
                self.events = self.events + 1
