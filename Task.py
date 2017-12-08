#!/usr/bin/env python
# -*- coding: utf-8 -*-

from datetime import *
import uuid



class Task():
	"""
	Task class
	"""
	def __init__(self, number, description, duedate, group="", tags=[], status="open"):
		self.number = number
		self.description = description
		self.duedate = duedate
		self.group = group
		self.tags = tags
		# Status: new, due, current, overdue, neglected, done, deleted, marked
		self.status = status
		self.creationdate = datetime.now()
		self.id = uuid.uuid4()

	def getdescription(self, length="short"):
		# Return desciption for different lengths
		pass

	def update(self):
		# Update status based on current time and other aspects
		pass

