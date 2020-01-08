from setuptools import setup

setup(
    name='butcher',
    version='0.0.1',
    packages=[''],
    url='',
    license='GPLv3',
    author='Fabio Bocconi',
    author_email='fabio.bocconi@gmail.com',
    description='',
    install_requires=[
        'systemd==0.16.1',
        'idstools==0.6.3',
        'pandas==0.25.3',
        'notify2==0.3.1',
        'marrow.mailer==4.0.3',
        'coverage==5.0',
        'tox==3.14.2',
        'dbus-python==1.2.12',
        'pydbus==0.6.0',
    ],
)
