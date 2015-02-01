__author__ = 'Vineet Shivhare'

import fabric.api as fab
from fabric.api import warn_only
from fabric.network import disconnect_all
from contextlib import contextmanager
from fabric import exceptions


@contextmanager
def ssh(settings):
    """

    :type settings: object
    :param settings:
    """
    with settings:
        try:
            yield
        finally:
            disconnect_all()


def ssh5(host, user, pw, command, passw=None):
    """
    :param host:
    :param user:
    :param pw:
    :param command:
    :param passw:
    :return Unix output:
    """
    with ssh(fab.settings(host_string=host, user=user, key_filename=pw, password=passw, warn_only=True)):
        return fab.run(command, pty=False, combine_stderr=False)


def scp5(host, user, pw, local_file, remote_file, passw=None):
    with ssh(fab.settings(host_string=host, user=user, key_filename=pw, password=passw, warn_only=True)):
        return fab.put(local_file, remote_file, mode=400)


def ssh5_sudo(host, user, pw, command, passw=None):
    with ssh(fab.settings(host_string=host, user=user, key_filename=pw, password=passw, warn_only=True)):
        return fab.sudo(command, pty=False)


import sys, os
import os.path
import stat


class setup():
    def __init__(self, ip, user, key):
        self.ip = ip
        self.user = user
        self.key = key

    def copy_to_remote(self, local, remote):
        try:
            scp5(self.ip, self.user, self.key, os.getcwd() + local, remote)
        except Exception as e:
            print e

    def run_command(self, command):
        try:
            ssh5(self.ip, self.user, self.key, command)
        except Exception as e:
            print e

    def run_sudo_command(self, command):
        try:
            ssh5_sudo(self.ip, self.user, self.key, command)
        except Exception as e:
            print e

    def run(self):
        try:
            self.copy_to_remote('/angular-flask-sqlalchemy', '/tmp')
            print self.run_sudo_command(
                ' pip install -r /tmp/angular-flask-sqlalchemy/requirement.txt')

            print self.run_command(' mv /tmp/angular-flask-sqlalchemy/ . ')

            self.run_command(' cd  angular-flask-sqlalchemy/ ; screen  -d  -m  python server.py; sleep 1')
            si, so, se = os.popen3('nc -vz -w3  {0} 8082'.format(str(ip)))
            out = se.read()
            if not out:
                print "access this site http://{0}:{1}".format(str(ip), '8082')
            else:
                print "Port not access able from outside you need to enable port {0} for public".format("8082")
        except Exception as e:
            print e


if __name__ == "__main__":
    if len(sys.argv[1:]) >= 3 :
        ip, user, pem = sys.argv[1:]

        if os.path.isfile(pem):
            print "File exist {0}".format(str(pem))
            setup(ip, user, pem).run()
        else:
            print "File not exist {0}".format(str(pem))
    else:
         print  "Some Argument missing "
         print "Run below command with respected information"
         print  "python setup.py <ec2 ip/url/dns> <user-name> <pem key>"






