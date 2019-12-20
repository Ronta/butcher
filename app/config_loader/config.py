import configparser
import csv
import platform

from os import path

from ButcherExceptions import MissingConfigurationFileError, MissingRulesPathError, MissingConfigurationSectionError
from parsers.csv_source.parser import CsvParser
from utils import fieldnames, warning_levels, notification_methods, email_parameters


class BaseConfig(object):
    _config = None
    _path = None

    data_source = None
    sleep = None
    name = None
    parser = None
    report_path = None
    rules_path = None
    warning_lvl = None
    notifications = {}

    def __init__(self, path):
        self._path = path

        self._check_config_path()
        self._load_config()
        self._load_general_configuration()
        self._check_data_source()
        self._check_rules_path()
        self._check_report()
        self._check_data_source_configuration()
        self._check_notifications()

    def _check_config_path(self):
        if not path.exists(self._path):
            raise MissingConfigurationFileError(f"Can't find the configuration file, check the path {self._path}")

    def _load_config(self):
        config = configparser.ConfigParser()
        config.read(self._path)
        self._config = config

    def _handle_warning_level(self, warning_lvl):
        self.warning_lvl = warning_levels[warning_lvl]

    def _load_general_configuration(self):
        try:
            general = self._config['general']
            self.sleep = general.getint('sleep', 60)
            warning_lvl = general.get('warning_lvl', 'high')
            self._handle_warning_level(warning_lvl=warning_lvl)
            self.name = general.get('name', platform.node())
        except KeyError:
            raise MissingConfigurationSectionError("Missing general section")

    def _check_data_source(self):
        try:
            self.data_source = self._config['data_source']['data_source']
        except KeyError:
            raise MissingConfigurationSectionError("Missing data_source section")

    def _check_rules_path(self):
        try:
            rules = self._config['rules']
            self.rules_path = rules.get('path', None)
        except KeyError:
            self.rules_path = None

    def _check_report(self):
        try:
            self.report_path = self._config['report']['path']
        except KeyError:
            raise MissingConfigurationSectionError("Missing report path")

        if not path.exists(f"{self.report_path}/butcher_report.csv"):
            with open(f"{self.report_path}/butcher_report.csv", 'w') as csv_report:
                writer = csv.DictWriter(csv_report, fieldnames=fieldnames)
                writer.writeheader()
                csv_report.close()

    def _check_csv_data(self):
        try:
            csv_path = self._config['csv']['path']
        except KeyError:
            raise MissingConfigurationSectionError("Missing csv section")

        if not path.exists(csv_path):
            raise MissingConfigurationFileError(f"The csv path {csv_path} is wrong")

        if self.rules_path is None:
            raise MissingRulesPathError("The rules path is missing")

        self.parser = CsvParser(path=csv_path, rules_path=self.rules_path, warning_lvl=self.warning_lvl,
                                report_path=self.report_path)

    def _check_data_source_configuration(self):
        getattr(self, f"_check_{self.data_source}_data")()

    def _check_notifications(self):
        for notification in notification_methods:
            if notification in self._config.keys():
                getattr(self, f"_check_{notification}_notification")()

    def _check_osd_notification(self):
        try:
            icon = self._config['osd']['icon']
        except KeyError:
            icon = 'security-low'

        self.notifications['osd'] = {'icon': icon}

    def _check_email_notification(self):
        self.notifications['email'] = {}
        for parameter in email_parameters:
            try:
                value = self._config['email'][parameter]
                self.notifications['email'][parameter] = value
            except KeyError:
                raise MissingConfigurationSectionError(f"Missing email {parameter} value")
