#!/usr/bin/python2.7
__author__ = 'sugar'

import sys
import os

import argparse

from tpfancod_simple.Sensor import Sensor
from tpfancod_simple.Controller import Controller

arg_dict = {'debug': __debug__,
            'quiet': False,
            'noreal': os.getuid() != 0}

def daemonize(callback):
    """turns the current process into a daemon"""

    if not arg_dict['debug']:  # don't go into daemon mode if debug mode is active
        """go into daemon mode"""
        # from: http://aspn.activestate.com/ASPN/Cookbook/Python/Recipe/66012
        # do the UNIX double-fork magic, see Stevens' "Advanced
        # Programming in the UNIX Environment" for details (ISBN
        # 0201563177)
        try:
            pid = os.fork()
            if pid > 0:  # exit first parent
                sys.exit(0)
        except OSError, e:
            print >>sys.stderr, 'fork #1 failed: %d (%s)' % (e.errno, e.strerror)
            sys.exit(1)

        # decouple from parent environment
        os.chdir('/')
        os.setsid()
        os.umask(0)

        # do second fork
        try:
            pid = os.fork()
            if pid > 0:
                sys.exit(0)
        except OSError, e:
            print >>sys.stderr, 'fork #2 failed: %d (%s)' % (e.errno, e.strerror)
            sys.exit(1)

        # write pid file
        try:
            pidfile = open("/tmp/tpfancod-simple.pid", 'w')
            pidfile.write(str(os.getpid()) + '\n')
            pidfile.close()
        except IOError:
            print >>sys.stderr, 'could not write pid-file at /tmp/tpfancod-simple.pid',
            sys.exit(1)

        callback()

    raise Exception("WRONG PLACE: Daemonize when debugging")

def main():
    s = []
    s.append(Sensor('/sys/bus/platform/drivers/coretemp/coretemp.0/hwmon/hwmon0/temp1_input', 0.001,
                    preset=[(0,75,"auto"),(75,150,"7")], debug=arg_dict['debug'], quiet=arg_dict['quiet']))
    #s.append(Sensor('/sys/bus/platform/drivers/coretemp/coretemp.0/hwmon/hwmon0/temp2_input', 0.001,
    #                preset=[(0,35,"3"), (35,55,"4"), (55,150,"5")]))
    #s.append(Sensor('/sys/bus/platform/drivers/coretemp/coretemp.0/hwmon/hwmon0/temp3_input', 0.001,
    #                preset=[(0,35,"3"), (35,55,"auto"), (55,150,"7")]))
    c = Controller(arg_dict['debug'], arg_dict['quiet'], arg_dict['noreal'], s)
    c.run()
    pass

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('-d', '--debug', help='enable debugging output',
                        action='store_true')
    parser.add_argument('-q', '--quiet', help='minimize console output',
                        action='store_true')
    parser.add_argument('-n', '--noreal', help='not a real run')

    args = parser.parse_args()

    arg_dict['debug'] = args.debug or __debug__
    arg_dict['quiet'] = args.quiet
    arg_dict['noreal'] = args.noreal or os.getuid() != 0

    if arg_dict['debug']:
        main()
    else:
        daemonize(main)
