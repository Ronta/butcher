import os
import logging
import datetime

from idstools import unified2
from parsers.parser import Parser
from utils import journald_handler, logLevel, classtype, safe_list_get
from rule_manager.loader import RuleLoader

logger = logging.getLogger(__name__)
logger.addHandler(journald_handler)
logger.setLevel(logLevel)


def rollover_hook(closed, opened):
    os.unlink(closed)


class U2Parser(Parser):

    path = None
    rules_path = None

    def __init__(self, warning_lvl, report_path, *args, **kwargs):
        super().__init__(warning_lvl, report_path, *args, **kwargs)
        self.path = self.kwarg['path']
        logger.info("Initializing the U2 parser.")
        logger.info(f"The U2 path is { self.path }")
        self.rules_path = self.kwarg['rules_path']

    def record_to_dict(self, record):
        return {
            "timestamp": datetime.datetime.fromtimestamp(record.get('event-second', "0")).isoformat(),
            "sig_generator": record.get('sensor-id', "-"),
            "sig_id": record.get('signature-id', "-"),
            "sig_rev": record.get('signature-revision', "-"),
            "msg": record.get('-', "-"),
            "proto": record.get('protocol', "-"),
            "src": record.get('source-ip', "-"),
            "srcport": record.get('-', "-"),
            "dst": record.get('destination-ip', "-"),
            "dstport": record.get('dport-icode', "-"),
            "ethsrc": record.get('-', "-"),
            "ethdst": record.get('-', "-"),
            "ethlen": record.get('-', "-"),
            "tcpflags": record.get('-', "-"),
            "tcpseq": record.get('-', "-"),
            "tcpack": record.get('-', "-"),
            "tcplen": record.get('-', "-"),
            "tcpwindow": record.get('-', "-"),
            "ttl": record.get('-', "-"),
            "tos": record.get('-', "-"),
            "id": record.get('event-id', "-"),
            "dgmlen": record.get('-', "-"),
            "iplen": record.get('-', "-"),
        }

    def start(self):
        super().start()
        reader = unified2.SpoolRecordReader(self.path,
                                            "snort.u2",
                                            rollover_hook=rollover_hook)
        logger.info("Start loading rules")
        r = RuleLoader(rules_path=self.rules_path)
        r.run()
        logger.info(f"{len(r.rules.keys())} Rules Loaded")

        for record in list(reader):
            sid = record.get('signature-id', None)
            if sid is None:
                pass
            else:
                class_type = r.rules.get(sid, "unassigned")
                if classtype[class_type] in self.warning_lvl:
                    data = self.record_to_dict(record)
                    data['warning_lvl'] = classtype[class_type]
                    data['msg'] = class_type
                    self.save(data)
