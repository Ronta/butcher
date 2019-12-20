import os
from idstools import rule


class RuleLoader(object):

    rules = {}
    rules_path = None
    rules_files = None

    def __init__(self, rules_path=None):
        self.rules_path = rules_path
        super().__init__()

    def get_all_rule_files(self):
        rules_files = []
        for file in os.listdir(self.rules_path):
            if file.endswith(".rules"):
                rules_files.append(os.path.join(self.rules_path, file))
        self.rules_files = rules_files

    def rule_parser(self, rules_file):
        for line in rule.parse_file(rules_file):
            self.rules[str(line.sid)] = line.classtype

    def run(self):
        self.get_all_rule_files()
        for rules_file in self.rules_files:
            self.rule_parser(rules_file)
        return True
