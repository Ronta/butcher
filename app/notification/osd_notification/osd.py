import notify2
import os


def send_osd_notification(data_dict, config, **kwargs):
    if "DISPLAY" not in os.environ.keys():
        return False
    notify2.init('Butcher')

    n = notify2.Notification("Butcher",
                             data_dict["message"],
                             config['icon']
                            )
    n.set_urgency(notify2.URGENCY_CRITICAL)
    n.set_timeout = 10000
    n.show()
    return True
