import logging
import csv

from parsers.parser import Parser
from utils import journald_handler, logLevel, classtype, safe_list_get
from rule_manager.loader import RuleLoader

logger = logging.getLogger(__name__)
logger.addHandler(journald_handler)
logger.setLevel(logLevel)


class CsvParser(Parser):

    path = None
    rules_path = None

    def __init__(self, warning_lvl, report_path, *args, **kwargs):
        super().__init__(warning_lvl, report_path, *args, **kwargs)
        self.path = self.kwarg['path']
        logger.info("Initializing the CSV parser.")
        logger.info(f"The CSV path is { self.path }")
        self.rules_path = self.kwarg['rules_path']

    def array_to_dict(self, array):
        return {
            "timestamp": safe_list_get(array, 0, '-'),
            "sig_generator": safe_list_get(array, 1, '-'),
            "sig_id": safe_list_get(array, 2, '-'),
            "sig_rev": safe_list_get(array, 3, '-'),
            "msg": safe_list_get(array, 4, '-'),
            "proto": safe_list_get(array, 5, '-'),
            "src": safe_list_get(array, 6, '-'),
            "srcport": safe_list_get(array, 7, '-'),
            "dst": safe_list_get(array, 8, '-'),
            "dstport": safe_list_get(array, 9, '-'),
            "ethsrc": safe_list_get(array, 10, '-'),
            "ethdst": safe_list_get(array, 11, '-'),
            "ethlen": safe_list_get(array, 12, '-'),
            "tcpflags": safe_list_get(array, 13, '-'),
            "tcpseq": safe_list_get(array, 14, '-'),
            "tcpack": safe_list_get(array, 15, '-'),
            "tcplen": safe_list_get(array, 16, '-'),
            "tcpwindow": safe_list_get(array, 17, '-'),
            "ttl": safe_list_get(array, 18, '-'),
            "tos": safe_list_get(array, 19, '-'),
            "id": safe_list_get(array, 20, '-'),
            "dgmlen": safe_list_get(array, 21, '-'),
            "iplen": safe_list_get(array, 22, '-'),
        }

    def start(self):
        super().start()
        with open(self.path, newline='') as alert_file:
            alert_reader = csv.reader(alert_file, delimiter=',')

            logger.info("Start loading rules")
            r = RuleLoader(rules_path=self.rules_path)
            r.run()
            logger.info(f"{len(r.rules.keys())} Rules Loaded")
            for row in alert_reader:
                sid = safe_list_get(row, 2, None)
                if sid is None:
                    pass
                else:
                    class_type = r.rules.get(sid, "unassigned")
                    if classtype[class_type] in self.warning_lvl:
                        data = self.array_to_dict(row)
                        data['warning_lvl'] = classtype[class_type]
                        self.save(data)
        alert_file.close()
