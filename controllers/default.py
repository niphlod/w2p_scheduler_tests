# -*- coding: utf-8 -*-
# this file is released under public domain and you can use without limitations

#########################################################################
## This is a samples controller
## - index is the default action of any application
## - user is required for authentication and authorization
## - download is for downloading files uploaded in the db (does streaming)
## - call exposes all registered services (none by default)
#########################################################################

from gluon.storage import Storage

def index():
    steps = [
        'one-time', 'repeats', 'repeats_failed',
        'group_names', 'uuid', 'futures', 'priority',
        'enabled', 'expiring', 'group_names_percentage',
        'die_automatically', 'traceback', 'kill', 'terminate',
        'disabled', 'return_values', 'discard'
        ]

    return dict(steps=steps)


def download():
    """
    allows downloading of uploaded files
    http://..../[app]/default/download/[filename]
    """
    return response.download(request,db)


def call():
    """
    exposes services. for example:
    http://..../[app]/default/call/jsonrpc
    decorate with @services.jsonrpc the functions to expose
    supports xml, json, xmlrpc, jsonrpc, amfrpc, rss, csv
    """
    return service()

def tasks():
    steps = [
        'intro',
        'one_time', 'repeats', 'repeats_failed',
        'group_names', 'uuid', 'futures', 'priority',
        ]
    docs = Storage()
    comments = Storage()
    docs.intro = """
#### Intro
So, here we are trying to learn (and test) web2py's scheduler.

Actually you have to download latest trunk scheduler to make it work (backup current gluon/scheduler.py and replace with the one on trunk).

This app ships with a default SQLite database, feel free to test on your preferred db engine.

All examples code should work if you just prepend
``
import datetime
from gluon.contrib.simplejson import loads, dumps
sr = db.scheduler_run
sw = db.scheduler_worker
st = db.scheduler_task
``:python

DRY!

Additionally, every example uses ``task_name``, but that is not a required parameter.
It just helps **this app** to verify that all is working correctly when you press the **Verify** button.

We have 3 functions defined into models/scheduler.py (don't get confused). It should be something like this:
``
# coding: utf8
import time
from gluon.scheduler import Scheduler

def demo1(*args,**vars):
    print 'you passed args=%s and vars=%s' % (args, vars)
    return args[0]

def demo2():
    1/0

def demo3():
    time.sleep(15)
    print 1/0
    return None

def demo4():
    time.sleep(15)
    print "I'm printing something"
    return dict(a=1, b=2)

def demo5():
    time.sleep(15)
    print "I'm printing something"
    rtn = dict(a=1, b=2)


scheduler = Scheduler(db)
##or, alternatively :
#scheduler = Scheduler(db,
#                      dict(
#                        demo1=demo1,
#                        demo2=demo2,
#                        demo3=demo3,
#                        demo4=demo4,
#                        foo=demo5
#                        )
#                      )
``:python

So, we have:
 -  demo1 : standard function, with some printed output, returning the first arg
 -  demo2 : never returns, throws exception
 -  demo3 : sleeps for 15 seconds, tries to print something, throws exception
 -  demo4 : sleeps for 15 seconds, print something, returns a dictionary
 -  demo5 : sleeps for 15 seconds, print nothing, doesn't return anything

The scheduler istantiated with the db only. Optionally, you can pass a dictionary
containing a mapping between strings and functions.
In the latter case, all functions are "assigned" to a string that is the function name,
except for function demo5 that we "assigned" to 'foo'.

All interactions with scheduler is done acting on the scheduler_* tables.
    """

    docs.one_time = """
#### One time only

Okay, let's start with the tests....something simple: a function that needs to run one time only.

``
st.insert(task_name='one_time_only', function_name='demo4')
``:python

Instructions:
 - Push "Clear All"
 - Push "Start Monitoring"
 - If not yet, start a worker in another shell ``web2py.py -K scheduler_tests``
 - Wait a few seconds, a worker shows up
 - Push "Queue Task"
 - Wait a few seconds

What you should see:
 - one worker is **ACTIVE**
 - one scheduler_task gets **QUEUED**, goes into **RUNNING** for a while and then becomes **COMPLETED**
 - when the task is **RUNNING**, a scheduler_run record pops up (**RUNNING**)
 - When the task is **COMPLETED**, the scheduler_run record is updated to show a **COMPLETED** status.

Than, click "Stop Monitoring" and "Verify"
    """
    comments.one_time = """
So, we got a task executed by scheduler, yeeeeahh!

Please note that you can get a lot of data to inspect execution in this mode
###### scheduler_task
 - start_time is when you queued the task
 - task_name is useful for retrieving the results later ``db(sr.scheduler_task.id == st.id)(st.task_name == 'one_time_only')(st.status == 'COMPLETED').select(sr.result, sr.output)``:python
 - task gets a ``uuid`` by default
###### scheduler_run
 - ``result`` is in json format
 - ``output`` is the stdout, so you can watch your nice "print" statements
 - ``start_time`` is when the task started
 - ``stop_time`` is when the task stopped
 - ``worker_name`` gets the worker name that processed the task
    """
    docs.repeats = """
#### Repeating task

Let's say we want to run the demo1 function with some args and vars, 2 times.
``
st.insert(task_name="repeats", function_name='demo1', args=dumps(['a','b']), vars=dumps(dict(c=1, d=2)), repeats=2, period=30)
``

Instructions (same as before):
 - Push "Clear All"
 - Push "Start Monitoring"
 - If not yet, start a worker in another shell ``web2py.py -K scheduler_tests``
 - Wait a few seconds, a worker shows up
 - Push "Queue Task"
 - Wait a few seconds


Verify that:
 - one worker is **ACTIVE**
 - one scheduler_task gets **QUEUED**, goes into **RUNNING** for a while
 - a scheduler_run record is created, goes **COMPLETED**
 - task gets **QUEUED** again for a second round
 - a new scheduler_run record is created
 - task becomes **COMPLETED**
 - a second scheduler_run record is created

Than, click "Stop Monitoring".
    """
    comments.repeats = """
So, we got a task executed twice automatically, yeeeeahh!

###### scheduler_task
 - times_run is 2
 - last_run_time is when the second execution started
###### scheduler_run
 - output args and vars got printed ok.
 - start_time of the second execution is after ``period*seconds`` after start_time of the first_run
    """

    docs.repeats_failed = """
#### Repeats Failed
We want to run a function once, but allowing the function to raise an exception once.
That is, you want the function to "retry" an attempt if the first one fails.
Remember, repeats_failed==1 will let a task fail only once, that is the default behaviour.
If you want the task to repeat once AFTER it is failed, you need to specify repeats_failed=2.
We'll enqueue demo2, that we know if will fail in bot runs, just to check if everything
works as expected (i.e. it gets re-queued only one time after the first FAILED run)

``
st.insert(task_name='repeats_failed', function_name='demo2', repeats_failed=2, period=30)
``
    """
    docs.expire = """
#### Expired status
To better understand the use of ``stop_time`` parameter we're going to schedule
a function with stop_time < now. Task will have the status **QUEUED**, but as soon
as a worker see it, it will set its status to **EXPIRED**.
``
stop_time = request.now - datetime.timedelta(seconds=60)
st.insert(task_name='expire', function_name='demo4', stop_time=stop_time)
``
    """
    docs.priority = """
#### Priority
Also if there is no explicit priority management for tasks you'd like to execute
a task putting that "on top of the list", for one-time-only tasks you can force the
``next_run_time`` parameter to something very far in the past (according to your preferences).
A task gets **ASSIGNED** to a worker, and the worker picks up (and execute) first tasks with
minimum ``next_run_time``.

``
next_run_time = request.now - datetime.timedelta(seconds=60)
st.insert(task_name='priority1', function_name='demo1', args=dumps(['scheduled_first']))
st.insert(task_name='priority2', function_name='demo1', args=dumps(['scheduled_second']), next_run_time=next_run_time)
``
    """
    docs.returns_null = """
#### Tasks with no return value
Sometimes you want a function to run, but you're not interested in the return value
(because you save it in another table, or you simply don't mind the results).
Well, there is no reason to have a record into the scheduler_run table!
So, by default, if a function doesn't return anything, its scheduler_run record
will be automatically deleted.
The record gets created anyway while the task is **RUNNING** because it's a way to
tell if a function is taking some time to be "executed", and because if task fails
(timeouts or exceptions) the record is needed to see what went wrong.
We'll queue 2 functions, both with no return values, demo3 that generates an exception
``
st.insert(task_name='no_returns1', function_name='demo5')
st.insert(task_name='no_returns2', function_name='demo3')
``
    """

    return dict(docs=docs, comments=comments)

def workers():
    steps = ['enabled', 'expiring', 'group_names_percentage',
        'die_automatically', 'traceback', 'kill', 'terminate',
        'disabled', 'return_values', 'discard']
    docs = Storage()
    comments = Storage()

    docs.disabled = """
#### Disable a worker
A disabled worker won't pick any tasks at all, but as soon as its status is set to **ACTIVE**
again, it will start to process tasks.

Instructions:
 - Push "Clear All"
 - Push "Start Monitoring"
 - If not yet, start a worker in another shell ``web2py.py -K scheduler_tests``
 - Wait a few seconds, a worker shows up
 - Push "Disable worker"
 - Wait a few seconds
 - Push "Queue task"
 - see that the task remain in the **QUEUED** status
 - Push "Activate worker"
 - the task get **ASSIGNED** and processed a few seconds later
    """
    docs.terminate = """
#### Terminate a worker
A worker with the status **TERMINATE** will die only if it's not processing any task.

Instructions:
 - Push "Clear All"
 - Push "Start Monitoring"
 - If not yet, start a worker in another shell ``web2py.py -K scheduler_tests``
 - Wait a few seconds, a worker shows up
 - Push "Queue task"
 - Wait until the task is reported as **RUNNING**
 - Quick!!! Click on "Terminate worker"
 - Watch the scheduler finish the current task and then die
    """
    docs.kill = """
#### Kill a worker
A worker with the status **KILL** will die also if it's processing a task.

Instructions:
 - Push "Clear All"
 - Push "Start Monitoring"
 - If not yet, start a worker in another shell ``web2py.py -K scheduler_tests``
 - Wait a few seconds, a worker shows up
 - Push "Queue task"
 - Wait until the task is reported as **RUNNING**
 - Quick!!! Click on "Kill worker"
 - Watch the scheduler die within 3 seconds
    """

    return dict(docs=docs, comments=comments)

def how_it_works():
    docs = Storage()
    docs.workers = """
### Scheduler
Workers's fine management is hard. This module tries not to leave behind any platform
(Mac, Win, Linux) . Right now workers can be started with an "embedded" mode:

``web2py.py -K appname``

or "directly", using:

``python gluon/scheduler.py -u sqlite://storage.sqlite \
                             -f applications/myapp/databases/ \
                             -t mytasks.py``

When you start a worker, you may want later to:
 - kill it "no matter what its doing"
 - kill it only if its not processing tasks
 - put it to sleep
Maybe you have yet some tasks queued, and you want to save some resources.
You know you want them processed every hour, so, you'll want to:
 - process all queued tasks and die automatically
All of these things are possible managing ``Scheduler`` parameters or the ``scheduler_worker`` table.
To be more precise, for started workers you will change the ``status`` value of any worker to influence
its behaviour.
As tasks, workers can be in some fixed statuses : ACTIVE, DISABLED, TERMINATE or KILLED.

**ACTIVE** and **DISABLED** are "persistent", while **TERMINATE** or **KILL**, as statuses
name suggest, are more "commands" than real statuses.
Hitting ctrl+c is equal to set a worker to **KILL**

[[workers statuses http://yuml.me/bd891eed.jpg center]]
The complete signature of the scheduler class is
``
Scheduler(
    db,
    tasks=None,
    migrate=True,
    worker_name=None,
    group_names=None,
    heartbeat=HEARTBEAT,
    max_empty_runs=0,
    discard_results=False
    )``:python
Let's see them in order:

``db`` is the database DAL instance were you want the scheduler tables be placed.
NB: If you're using SQLite it's best to create a separate db to avoid lockings

``tasks`` can be a dict. Must be defined for the "direct" mode or if you want to call a function
not by his name, i.e.
``tasks=(mynameddemo1=demo1)`` will let you execute function demo1 with
``st.insert(task_name='mytask', function_name='mynameddemo1')``
or
``st.insert(task_name='mytask', function_name='demo1')``
In "embedded" mode, if you don't pass this parameter, function will be searched in the app environment.

``worker_name`` is None by default. As soon as the worker is started, a worker name
is generated as hostname-uuid. If you want to specify that, be sure that it's unique.

``group_names`` is by default set to **[main]**. All tasks have a ``group_name`` parameter,
set to **main** by default.
Workers can pick up tasks of their assigned group.
NB: This is useful if you have different workers instances (e.g. on different machines)
and you want to assign tasks to a specific worker.
NB2: It's possible to assign a worker more groups, and they can be also all the same, as
``['mygroup','mygroup']``. Tasks will be distributed taking into consideration that
a worker with group_names ``['mygroup','mygroup']`` is able to process the double of the tasks
a worker with group_names ``['mygroup']`` is.

``heartbeat`` is by default set to 3 seconds. This parameter is the one controlling how often
a scheduler will check its status on the ``scheduler_worker`` table and see if there are any
**ASSIGNED** tasks to itself to process.

``max_empty_runs`` is 0 by default, that means that the worker will continue to process tasks
as soon as they are **ASSIGNED**. If you set this to a value of, let's say, 10, a worker
will die automatically if it's **ACTIVE** and no tasks are **ASSIGNED** to it for 10 loops.
A loop is when a worker searches for tasks, every 3 seconds (or the set ``heartbeat``)

``discard_results`` is False by default. If set to True, no scheduler_run records will be created.
NB: scheduler_run records will be created as before for **FAILED**, **TIMEOUT** and
**STOPPED** tasks's statuses.
    """
    docs.tasks = """
### Tasks lifecycle

The ``scheduler_task`` table is the one where tasks are organized.

Task is going to be scheduled and several values will be auto-filled (we'll analyze
those later).

All tasks follow a lifecycle

[[scheduler tasks http://yuml.me/ce8edcc3.jpg center]]

Let's go with order. By default, when you send a task to the scheduler, you'll want
that to be executed. It's in **QUEUED** status.
If you need it to be executed later, use the ``stop_time`` parameter (default = now).
If for some reason you need to be sure that the task don't
get executed after a certain point in time (maybe a request to a webservice
that shuts down at 1AM, a mail that needs to be sent not after the working hours,
etc...) you can set a ``stop_time`` (default = None) for it.
If your task is NOT picked up by a worker before stop_time, it will be set as
**EXPIRED**.
Tasks with no stop_time set or picked up **BEFORE** stop_time are **ASSIGNED**
to a worker. When a workers picks up them, they become **RUNNING**.
**RUNNING** tasks may end up:
 - **TIMEOUT** when more than n seconds passed with ``timeout`` parameter (default = 60 seconds)
 - **FAILED** when an exception is detected
 - **COMPLETED** when all went ok

Additionally, you can control how many times a task should be repeated (i.e. you
need to aggregate some data at specified intervals). To do so, set the ``repeats``
parameter (default = 1 time only, 0 = unlimited). You can influence how many seconds should pass between executions
with the ``period`` parameter (default = 60 seconds).
NB: the time is not calculated between the END of the first round and the START of the next, but
from the START time of the first round to the START time of the next cycle)

Another nice addition, you can set how many times the function can raise an exception (i.e.
requesting data from a sloooow webservice) and be queued again instead of stopping in **FAILED**
status with the parameter ``repeats_failed`` (default = 1, 0 = unlimited).

[[task repeats http://yuml.me/e2f1c1be.jpg center]]

Summary: you have
 - ``period`` and ``repeats`` to get an automatically rescheduled function
 - ``timeout`` to be sure that a function doesn't exceed a certain amount of time
 - ``repeats_failed`` to control how many times the task can "fail"
 - ``start_time`` and ``stop_time`` to schedule a function in a restricted timeframe
    """
    return dict(docs=docs)