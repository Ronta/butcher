import unittest
import os
import dbus

from notification.osd_notification.osd import send_osd_notification


class OsdTestCase(unittest.TestCase):

    def test_osd(self):
        data_dict = {}
        config = {}
        data_dict['message'] = "test"
        config['icon'] = 'test-icon'
        if "DISPLAY" in os.environ.keys():
            self.assertTrue(send_osd_notification(data_dict, config))
        else:
            self.assertFalse(send_osd_notification(data_dict, config))
