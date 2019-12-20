from marrow.mailer import Mailer, Message


def send_email_notification(data_dict, config, **kwargs):
    if config['to'] == "fabio.bocconi@example.com":
        pass
    else:
        mailer = Mailer(dict(
            transport=dict(
                use='smtp',
                host=config['host'],
                password=config['password'],
                username=config['username'],
                port=config['port'],
                tls='required')))
        mailer.start()

        message = Message(author=config['author'], to=config['to'])
        message.subject = data_dict["message"]
        message.plain = data_dict["body"]
        mailer.send(message)

        mailer.stop()
