import logging

from systemd import journal

journald_handler = journal.JournaldLogHandler()
journald_handler.setFormatter(logging.Formatter(
    '[%(levelname)s] %(message)s'
))

logLevel = logging.INFO

fieldnames = ["timestamp", "sig_generator",	"sig_id", "sig_rev", "msg",	"proto", "src",	"srcport",
              "dst", "dstport", "ethsrc", "ethdst",	"ethlen", "tcpflags", "tcpseq",	"tcpack", "tcplen",
              "tcpwindow", "ttl",	"tos", "id", "dgmlen", "iplen", "warning_lvl"
              ]

classtype = {
    "attempted-admin": "high",
    "attempted-user": "high",
    "kickass-porn": "high",
    "policy-violation": "high",
    "shellcode-detect": "high",
    "successful-admin": "high",
    "successful-user ": "high",
    "trojan-activity": "high",
    "unsuccessful-user": "high",
    "web-application-attack": "high",
    "attempted-dos": "medium",
    "attempted-recon": "medium",
    "bad-unknown": "medium",
    "default-login-attempt ": "medium",
    "denial-of-service": "medium",
    "misc-attack": "medium",
    "non-standard-protocol": "medium",
    "rpc-portmap-decode": "medium",
    "successful-dos ": "medium",
    "successful-recon-largescale": "medium",
    "successful-recon-limited": "medium",
    "suspicious-filename-detect": "medium",
    "suspicious-login ": "medium",
    "system-call-detect": "medium",
    "unusual-client-port-connection": "medium",
    "web-application-activity": "medium",
    "sdf": "medium",
    "icmp-event": "low",
    "icmp-event ": "low",
    "misc-activity": "low",
    "network-scan": "low",
    "not-suspicious": "low",
    "protocol-command-decode": "low",
    "string-detect": "low",
    "unknown": "low",
    "tcp-connection": "very_low",
    "unassigned": "unassigned",
}

warning_levels = {
    "very_low": ["unassigned", "very_low", "low", "medium", "high"],
    "low": ["unassigned", "low", "medium", "high"],
    "medium": ["unassigned", "medium", "high"],
    "high": ["unassigned", "high"]
}

notification_methods = ['osd', 'email']
email_parameters = ['host', 'password', 'username', 'port', 'tls', 'author', 'to']


def safe_list_get(l, idx, default):
    try:
        return l[idx]
    except IndexError:
        return default
