__author__ = 'sugar'

import logging
import threading

class Controller(object):

    fan_control_file = "/proc/acpi/ibm/fan"

    fan_valid_level = ["0", "1", "2", "3", "4", "5", "6", "7", "auto"]

    def __init__(self, debug, quiet, dryrun, sensors):
        if not debug:
            logging.basicConfig(filename='/var/log/tpfancod-simple.log',
                                level=logging.WARNING if quiet else logging.DEBUG)
        else:
            logging.basicConfig(level=logging.DEBUG)

        self.dryrun = dryrun
        self.sensors = sensors

    def write_fan_level(self, level):
        if level not in self.fan_valid_level:
            logging.warn('Invalid level = %s, set to "auto"' % level)
            level = "auto"
        command = 'level %s' % level
        logging.info("Writing %s" % command)
        if not self.dryrun:
            f = open(Controller.fan_control_file, 'w')
            f.write(command)
            f.close()
        logging.info("Writing watchdog 5 > %s" % (Controller.fan_control_file))
        if not self.dryrun:
            f = open(Controller.fan_control_file, 'w')
            f.write("watchdog 5")
            f.close()

    def sensor(self):
        # Well, because I don't have multi-sensor platform, I just use one sensor now.
        temp = {}
        level = []
        for s in self.sensors:
            temp[s.path] = s.read_temp()
            level.append(s.preset_level())

        logging.debug("Temperature readings: " + str(temp))
        logging.debug("Preset fan levels: " + str(level))
        # If auto is set or sensors are empty, we always use auto
        if len(level) == 0 or "auto" in level:
            self.write_fan_level("auto")
        # Else we take maximum level in settings
        else:
            self.write_fan_level(str(max([int(p) for p in level])))

    def run(self):
        while True:
            t = threading.Timer(5.0, self.sensor)
            t.start()
            t.join()

