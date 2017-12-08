#!/usr/bin/env python
# -*- coding: utf-8 -*-

import click
import parsedatetime
from datetime import *
import ConfigParser
import os, re
import io
import sys
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

cal = parsedatetime.Calendar()

def strtodate(string):
    """Parse humanreadable text and return a datetime"""
    time_struct, parse_status = cal.parse(string)
    return datetime(*time_struct[:6])

def sorttasks():
    """Sort the tasks by due time (freshest first)"""
    tasks = readtasks()
    temp = []
    for taskline in tasks:
        # writetask(taskline[1], str(taskline[2]), taskline[3])
        length = taskline[2] - datetime.now()
        temp.append([taskline[1], str(taskline[2]), taskline[3], length])
    from operator import itemgetter
    temp.sort(key=itemgetter(3), reverse=False)
    open(taskpath, 'w').close()
    # Write all other lines
    for i, taskline in enumerate(temp):
        writetask(taskline[0], str(taskline[1]), taskline[2])

def readtasks():
    """Read Tasks from taskpath (default: ~/.zeitfluss/tasks.txt)"""
    tasklist = []
    with io.open(taskpath, 'r', encoding='utf-8-sig') as f:
        for i, line in enumerate(f.readlines()):
            task, date, timeformat = line.split(' || ')
            task = task.strip()
            timeformat = timeformat.strip()
            date = strtodate(date)
            tasklist.append([i, task, date, timeformat])
    return tasklist

def writetask(task, date, timeformat):
    """Append Task to Task List"""
    task = task.decode('utf-8-sig')
    with io.open(taskpath, 'a', encoding='utf-8-sig') as f:
        f.write(task+' || '+str(date)+' || '+timeformat+"\n")

def updatetasks():
    """Update Tasks, delete old tasks"""
    sorttasks()
    tasks = readtasks()
    # Open and delete Taskfile 
    open(taskpath, 'w').close()
    # Write all other lines
    for i, taskline in enumerate(tasks):
        # Check if delta is positive (a week = 604800 seconds)
        if not (taskline[2]-datetime.now()).total_seconds() <= -604800:
            writetask(taskline[1], str(taskline[2]), taskline[3])


def formattask(task, absolute=False):
    """Return a formated String for display"""
    tasknumber, task, date, timeformat = task
    now = datetime.now()
    delta = date - now
    if absolute:
        tstring = date.strftime("%Y-%m-%d %H:%M")
    elif timeformat == "auto":
        # For times bigger than a year
        if delta.total_seconds()/60./60./24./365. >= 1:
            days = delta.total_seconds()/60./60./24.
            years = days//365.
            yearpluralize="s" if years>1 else ""
            tstring = str(abs(int(years)))+" Year"+yearpluralize
            leftdays = days - years*365
            if leftdays >= 30:
                months = leftdays//30.
                monthpluralize="s" if months>1 else ""
                tstring += " and "+str(abs(int(months)))+" Month"+monthpluralize
            elif leftdays >= 7:
                weeks = leftdays//7.
                weekpluralize="s" if weeks>1 else ""
                tstring += " and " +str(abs(int(weeks)))+" Week"+weekpluralize
            elif leftdays != 0:
                daypluralize="s" if leftdays>1 else ""
                tstring += " and " +str(abs(int(leftdays)))+ " Day"+daypluralize
        # For times bigger than 2 Months
        elif delta.total_seconds()/60./60./24. >=60:
            days = delta.total_seconds()/60./60./24.
            months = days//30.
            monthpluralize="s" if months>1 else ""
            tstring = str(abs(int(months)))+ " Month"+monthpluralize
        # For times equal or bigger than 2 weeks
        elif delta.total_seconds()/60./60.//24 >= 14:
            days = delta.total_seconds()/86400.
            weeks = days//7.
            weekpluralize="s" if weeks>1 else ""
            tstring = str(abs(int(weeks)))+" Week"+weekpluralize
        # For times bigger than 3 days
        elif delta.total_seconds()/60./60./24. >= 3:
            days = delta.total_seconds()/86400.
            daypluralize="s" if days>1 else ""
            tstring = str(abs(int(days)))+" Day"+daypluralize
        else:
            hours = delta.total_seconds()/60.//60.
            hourpluralize="s" if hours>1 else ""
            tstring = str(abs(int(hours)))+ " Hour"+hourpluralize
    elif timeformat == "months":
        months = delta.total_seconds()/60./60./24.//30
        monthpluralize="s" if months>1 else ""
        if months >= 1:
            tstring = str(abs(int(months)))+" Month"+monthpluralize
        else:
            if delta.total_seconds() > 60*60*24*7:
                weeks = delta.total_seconds()/60./60./24./7.
                weekpluralize="s" if weeks>1 else ""
                tstring = str(abs(int(weeks)))+" Week"+weekpluralize
            elif delta.total_seconds() > 60*60*24*12:
                days = delta.total_seconds()//86400.
                dayspluralize = ""
                daypluralize="s" if days>1 else ""
                tstring = str(abs(int(days)))+" Day"+dayspluralize
            else:
                tstring = "tomorrow"
    elif timeformat == "days":
        days = delta.total_seconds()/60./60./24.
        if delta.total_seconds() > 60*60*12:
            days = delta.total_seconds()/86400.
            dayspluralize = ""
            daypluralize="s" if days>1 else ""
            tstring = str(abs(int(days)))+" Day"+dayspluralize
        else:
            tstring = "tomorrow"
    elif timeformat == "hours":
        hours = delta.total_seconds()/60./60.
        if hours >= 1:
            hourpluralize="s" if hours>1 else ""
            tstring = str(abs(int(hours)))+ " Hour"+hourpluralize
        else:
            minutes = delta.total_seconds()/60.//60
            minutepluralize="s" if minutes>1 else ""
            tstring = str(abs(int(minutes)))+" Minute"+minutepluralize

    elif timeformat == "minutes":
        minutes = delta.total_seconds()/60.//60
        minutepluralize="s" if minutes>1 else ""
        tstring = str(abs(int(minutes)))+" Minute"+minutepluralize
    tasknumber = "["+str(tasknumber)+"]"
    if not absolute:
        if delta.total_seconds() < 0:
            tstring = tstring+" overdue"
        else:
            tstring = tstring+" remaining"
    return "{:<5}{:<50}{:<25}".format(tasknumber, task, tstring)

def checkdate(tasknumber):
    """Check if a date passed the threshold"""
    tasks = readtasks()
    tasknumber, taskname, taskdate, timeformat = tasks[tasknumber]
    delta = taskdate - datetime.now()
    if timeformat == "auto" or timeformat == "months" or timeformat == "days":
        threshold = 60*60*12
        if delta.total_seconds() < threshold:
            return True
    elif timeformat == "hours":
        threshold = 60*60*2
        if delta.total_seconds() < threshold:
            return True
    elif timeformat == "minutes":
        threshold = 60*15
        if delta.total_seconds() < threshold:
            return True
    else:
        return False

def checkoverdue(tasknumber):
    """Check if a date passed the threshold"""
    tasks = readtasks()
    tasknumber, taskname, taskdate, timeformat = tasks[tasknumber]
    delta = taskdate - datetime.now()
    if delta.total_seconds() < 0:
        return True
    else:
        return False


@click.group()
def cli():
        """zeitfluss is a countdown timer. You may add tasks with due dates to it and it can list those tasks with the remaining time available to finish each task. Good to keep track of deadlines. The tasks file is a simple text file located at ~/.zeitfluss/tasks.txt"""
        pass

@cli.command()
@click.option('--timeformat', '-t', type=click.Choice(['auto', 'months', 'weeks', 'days', 'hours', 'minutes']), default='auto', help='Specify a format for timer display')
@click.argument('task', default='eat pizza', required=True)
@click.argument('date', default='tomorrow', required=True)
def add(task, date, timeformat):
    """Add a task with a due date. Example: zeitfluss add 'eat pizza' 'in 2 days'"""
    task = task
    date = strtodate(date)
    # Write Task, Date and Displayformat to Disk
    writetask(task, str(date), timeformat)
    click.secho("Added Task:\t"+task+" (Date: "+date.strftime("%Y-%m-%d %H:%M, a %A in Week %W of %Y)"), fg='green')
    sorttasks()


@cli.command()
@click.option('--absolute', '-a', is_flag=True, help='Display absolute dates instead of deltas')
def list(absolute):
    """Displays all Tasks with due time. Example: zeitfluss list"""
    updatetasks()
    sorttasks()
    tasks = readtasks()
    taskpluralize="s" if len(tasks)>1 else ""
    header = '{:-^80}'.format("  zeitfluss - "+str(len(tasks))+" Task"+taskpluralize+" in List  ")
    if not len(tasks) == 0:
        click.echo()
        click.secho(header, fg='green')
        for i, tasklist in enumerate(tasks):
            message = formattask(tasklist, absolute)
            if checkoverdue(i):
                click.secho(message, fg="white", bg="red")
            elif checkdate(i):
                click.secho(message, fg="white", bg="green")
            else:
                click.secho(message, fg='green')
        click.secho("-"*80, fg="green")
        click.echo()
    else:
        click.echo("No Tasks in List. Add with zeitfluss add TASKNAME DUETIME")



def parsenumbers(string):
    """
    Take lists like '0, 1, 15-20' and return 
    [0, 1, 15, 16, 17, 18, 19, 20]
    """
    # Find ranges like 0-15 or 30-10
    ranges = re.findall("\d+\s*\-\s*\d+", str(string))
    # Remove already found ranges from string
    string = re.sub("\d+\s*\-\s*\d+", "", str(string))
    # In the rest search for normal numbers
    singlenumbers = re.findall("(\d+)", str(string))
    # Convert all to int
    singlenumbers = [int(x) for x in singlenumbers]
    # Iterate through the ranges and append the numbers to rangenumbers
    rangenumbers = []
    for r in ranges:
        values = [int(x) for x in r.replace(" ", "").split("-")]
        for value in range(min(values),max(values)):
            rangenumbers.append(value)
    # Join single numbers and ranges and sort them
    allnumbers = rangenumbers + singlenumbers
    allnumbers.sort()
    return allnumbers



@cli.command()
@click.argument('string', default="0")
def delete(string):
    """Delete a task. Example: zeitfluss delete 0"""
    tasks = readtasks()
    tasknumbers = parsenumbers(string)
    for tasknumber in tasknumbers:
        if (tasknumber < 0) or (tasknumber >= len(tasks)):
            click.echo(click.style("ERROR: Task ["+str(tasknumber)+"] not found in list",fg='red'))
            exit(0)
        tasknumber, task, date, timeformat = tasks[tasknumber]
        message = "Deleted → "+formattask(tasks[tasknumber]).replace("\t", " ")
        click.secho(message, fg='red')
        tasks = readtasks()
        # Open and delete Taskfile 
        # open(taskpath, 'w').close()
        # Write all other lines
        with open(taskpath, 'r+') as f:
            output = []
            lines = f.readlines()
            for i, line in enumerate(lines):
                 if not i == tasknumber:
                    output.append(line)
            f.truncate(0)
            f.writelines(output) 
