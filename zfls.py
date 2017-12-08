#!/usr/bin/env python
# -*- coding: utf-8 -*-

import click
import parsedatetime
from datetime import *
import ConfigParser
import os, re
import io
import sys
from parsehuman import *
from Taskmanager import *


def init():
	reload(sys)
	sys.setdefaultencoding('utf-8')

	home = os.path.expanduser("~")

	# Check if application directory exists, create if not
	apppath = os.path.join(home, '.zeitfluss')
	if not os.path.isdir(apppath):
	    os.mkdir(apppath)

	# Check if a config exists, create if not
	config = ConfigParser.ConfigParser()
	configpath = os.path.join(apppath, "config.ini")
	taskpath = os.path.join(apppath, "tasks.txt")

	if not os.path.exists(configpath):
	     open(configpath, 'a').close()
	     # Write defaults to config

	if not os.path.exists(taskpath):
	     open(configpath, 'a').close()

	config.read(configpath)





if __name__ == "__main__":
	init()