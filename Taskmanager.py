#!/usr/bin/env python
# -*- coding: utf-8 -*-

from datetime import *
import uuid
from Task import *

class TaskManager():
	"""
	Manages a pool of tasks
	Writes and Reads that pool from and to disk

	"""
	def __init__(self, path):
		self.path = path

	def updatetasks(self, tasknumbers):
		# Update Tasks (due dates etc)
		pass

	def deletetasks(self, filters):
		# Delete one or more tasks
		if "all" in "filters" or "*" in "filters":
			self.resettasks()

	def movetask(self, tasknumber):
		pass

	def marktasks(self, tasknumbers):
		pass

	def dotasks(self, filters):
		pass

	def grouptasks(self, filters, groupname):
		pass

	def ungrouptasks(self, filtersorgroup):
		pass

	def edittask(self, tasknumber):
		pass

	def tasksaddtags(self, filters, tags):
		pass

	def tasksremovetags(self, filters, tags):
		pass

	def listtasks(self, filters):
		pass

	def resettasks(self):
		# Delete all tasks for a fresh start
		pass

	def createtesttasks(self):
		# Create Example Tasks for testing
		pass

	def writetodisk(self):
		pass

	def readfromdisk(self):
		pass