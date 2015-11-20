#-*- coding: utf-8 -*-
__author__ = 'root'

import epics
import scan
import sys, time

def monitorM3():
    while True:
        print epics.caget('mobiis:m3.RBV')
        time.sleep(1)

monitorM3()