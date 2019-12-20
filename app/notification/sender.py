import logging

from utils import journald_handler, logLevel
from .email_notifiction.send_email import send_email_notification
from .osd_notification.osd import send_osd_notification

logger = logging.getLogger(__name__)

logger.addHandler(journald_handler)
logger.setLevel(logLevel)


class Notification(object):
    data_dict = None
    config = None

    notification = {
        'osd': send_osd_notification,
        'email': send_email_notification
    }

    def __init__(self, data_dict, config):
        self.data_dict = data_dict
        self.config = config
        for key in self.config.notifications.keys():
            try:
                self.notification[key](data_dict, self.config.notifications[key])
            except Exception as e:
                logger.error(f"notification {key} error {e}")



