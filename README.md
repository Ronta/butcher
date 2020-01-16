# Butcher

Butcher is a snort log parser and notifier. Actually can read CSV and unified2 logs. 

## Getting Started

Install snort and configure the output to CSV or in unfield2. Then locate the folders.

### Prerequisites

```
Python-Virtualenv
Python 3.6 or Python 3.7
Systemd

libsystemd-dev 
libdbus-glib-1-dev 
libdbus-1-dev

```

### Installing
install the dependecies (see Prerequisites section) then create one virtuaenv with python-virtualenv

```
mkvirtualenv buthcher --python=/usr/bin/python3.6
```

then activate the virtualenv, if is not activated after the creation, and install all requirements with pip

```
pip install -r requirements.txt
```

create the folder for the snort configuration

```
sudo mkdir /etc/butcher/
```

and give the privileges to your user

```
sudo chown YOURUSER /etc/butcher/
```

Locate the snort csv log folder or unifield2 log folder and create the configuration file in the folder 

(feel fre to use nano :joy:	)

```
cd /etc/butcher/
nano butcher.ini
```

and this an full example of configuration file:

```
[general]
name=foobar
sleep=180
warning_lvl=high

[data_source]
data_source=unified2

[report]
path=/home/YOURUSER/snort/files/report

[rules]
path=/home/YOURUSER/snort/files/rules

[csv]
path=/home/YOURUSER/snort/files/snort_log/csv_files/alert .csv

[unified2]
path=/home/YOURUSER/snort/files/snort_log/u2_files

[osd]
icon=security-low

[email]
host=smtp.example.com
password=example
username=fabio.bocconi@example.com
port=587
tls=required
author=fabio.bocconi@gmail.com
to=yourmeail@example.com, anotheremail@example.com
```

then create a systemd configuration file

```
[Unit]
Description=Butcher

[Service]
ExecStart=/home/YOURUSER/.virtualenvs/snort/bin/python3.6 /home/YOURUSER/PycharmProjects/u2parser/main.py
Environment=PYTHONUNBUFFERED=1
Restart=on-failure
Type=notify


[Install]
WantedBy=default.target
```
and activate it.

```
systemctl --user start butcher.service
```

the command for checking the status is:

```
systemctl --user status butcher.service
```

and for read the logs:

```
journalctl --user -xe
```


## Understanding the config file

The **general** section is composed by 3 parameters. ___name___, ___sleep___ and ___warning_lvl___

* *name*: the device name
* *sleep*: is the time between the application heartbeat. In seconds.
* *warning_lvl*: is the minimun level for raise a notification. And it can be assume the values: 
    * very_low
    * low
    * medium
    * high

The **data_source** section is composed by 1 parameters. ___data_source___

* *data_source*: is the section where the log source is defined. And it can be assume the values:
    * unified2
    * csv

If you specify _unified2_ you need to create a unified2 section, same thing for csv. See below for the configuration.

The **report** section is composed by 1 parameter. ___path___.
* *path*: the location of report folder. ie: /home/YOURUSER/snort/files/report

The **rules** section is composed by 1 parameters. ___path___.
* *path*: the location of rules folder. ie: /home/YOURUSER/snort/files/rules

The **csv** section is composed by 1 parameters. ___path___.
* *path*: the full path of report file location. ie: /home/YOURUSER/snort/files/snort_log/csv_files/alert.csv

The **unified2** section is composed by 1 parameters. ___path___.
* *path*: the location of unified2 folder. ie: /home/YOURUSER/snort/files/snort_log/u2_files

The **osd** section is composed by 1 parameters. ___icon___.
* *icon*: the icon name for the notification.

The **email** section is composed by 7 parameters. ___host___, ___password___, ___username___, 
___port___, ___tls___, ___author___, ___to___
* *host*: smtp server address
* *password*: your mail psw
* *username*: your email address
* *tls*: required ro no
* *author*: your email address or name
* *to*: the reciever of email, multiple address are possible, comma space separated.


## Running the tests
```
python -m unittest discover -s app/tests -t app/
```
or
```
tox
```
### TODO

Create configuration section for choice the preferred notification method, split the config filte between 
General section, Parser section and Notifcation section, add a loader for SO rules.

## Authors

* **Fabio Bocconi** - *Initial work* - [Ronta](https://github.com/Ronta)

## License

This project is licensed under the GPLv3 License - see the [LICENSE.md](LICENSE.md) file for details

