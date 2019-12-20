import notify2


def send_osd_notification(data_dict, config, **kwargs):
    notify2.init('Butcher')

    n = notify2.Notification("Butcher",
                             data_dict["message"],
                             config['icon']
                            )
    n.set_urgency(notify2.URGENCY_CRITICAL)
    n.set_timeout = 10000
    n.show()