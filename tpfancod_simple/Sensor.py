__author__ = 'sugar'

import os
import logging

class Sensor(object):

    def __init__(self, interface, factor, preset=[], sep=' ', debug=False, quiet=False):
        self.valid = True
        try:
            f = open(interface, 'r')
            f.read()
            f.close()
        except Exception, ex:
            self.valid = False
            logging.debug(ex.message)
        
        self.path = interface
        self.factor = factor
        self.sep = sep
        self.preset = preset
        self.level = "auto"
        
        if not debug:
            logging.basicConfig(filename='/var/log/tpfancod-simple.log',
                                level=logging.WARNING if quiet else logging.DEBUG)
        else:
            logging.basicConfig(level=logging.DEBUG)        
        
    def preset_level(self):
        return self.level

    def read_temp(self):
        temp = []
        try:
            # Read temperature
            f = open(self.path)
            temp = [float(p)*self.factor for p in f.read().split(self.sep)]
            f.close()
            self.level = "-1"
            for p in temp:
                for q in self.preset:
                    if p > q[0] and p <= q[1]:
                        if q[2] == "auto":
                            self.level = "auto"
                        elif self.level != "auto":
                            self.level = str(max(int(self.level), int(q[2])))
                        break
                break
        except Exception, ex:
            logging.warn("Failed to read temperature from %s" % self.path)
            logging.debug(ex.message)
            self.level = "auto"
            temp = []
        return temp
