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

response.files.append(URL('static', 'css/prettify.css'))
response.files.append(URL('static', 'js/prettify.js'))

def test():
    for a in range(1):
        scheduler.queue_task('addmyfunction', pargs=[1,2], immediate=True)
    return dict(a=1, b=2)
    #return myautoscale()

def index():
    steps = [
        'one_time', 'repeats', 'repeats_failed',
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
        'one_time', 'repeats', 'repeats_failed', 'prevent_drift',
        'group_names', 'uuid', 'futures', 'priority',
        'immediate'
        ]
    docs = Storage()
    comments = Storage()
    docs.intro = """
#### Intro
So, here we are trying to learn (and test) web2py's scheduler. This app always
documents the latest scheduler available in web2py, so make sure downloaded
the latest version in "master" repo scheduler
to make it work (backup current gluon/scheduler.py and replace with the one
on "master", just to be safe).

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

We have 7 functions defined into models/scheduler.py (don't get confused). It should be something like this:
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

def demo6():
    time.sleep(5)
    print '50%'
    time.sleep(5)
    print '!clear!100%'
    return 1

import random
def demo7():
    time.sleep(random.randint(1,15))
    print W2P_TASK, request.now
    return W2P_TASK.id, W2P_TASK.uuid

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
 -  demo6 : sleeps for 5 seconds, print something, sleeps 5 seconds, print something, return 1
 -  demo7 : sleeps for a random time, prints and returns W2P_TASK.id and W2P_TASK.uuid

The scheduler is istantiated with the db only. Optionally, you can pass a dictionary
containing a mapping between strings and functions.
In the latter case, all functions are "assigned" to a string that is the function name,
except for function demo5 that we "assigned" to 'foo'.

All interactions with scheduler are done using the public API.

#### Exposed Api

##### Queue Task
- ``scheduler.queue_task(function, pargs=[], pvars={}, **kwargs)`` : accepts a lot of arguments, to make your life easier....
 -- ``function`` : required. This can be a string as ``'demo2'`` or directly the function, i.e. you can use ``scheduler.queue_task(demo2)``
 -- ``pargs`` : p stands for "positional". pargs will accept your args as a list, without the need to jsonify them first.
  ---  ``scheduler.queue_task(demo1, [1,2])``
  ... does the exact same thing as
  ... ``st.validate_and_insert(function_name = 'demo1', args=dumps([1,2]))``
  ... and in a lot less characters
  ... **NB**: if you do ``scheduler.queue_task(demo1, [1,2], args=dumps([2,3]))`` , ``args`` will prevail and the task will be queued with **2,3**
 -- ``pvars`` : as with ``pargs``, will accept your vars as a dict, without the need to jsonify them first.
  --- ``scheduler.queue_task(demo1, [], {'a': 1, 'b' : 2})`` or ``scheduler.queue_task(demo1, pvars={'a': 1, 'b' : 2})``
  ... does the exact same thing as
  ... ``st.validate_and_insert(function_name = 'demo1', vars=dumps({'a': 1, 'b' : 2}))``
  ... **NB**:  if you do ``scheduler.queue_task(demo1, None, {'a': 1, 'b': 2}, vars=dumps({'a': 2, 'b' : 3}))`` , ``vars`` will prevail and the task will be queued with **{'a': 2, 'b' : 3}**
 -- ``kwargs`` : all other scheduler_task columns can be passed as keywords arguments, e.g. :
  ... ``
       scheduler.queue_task(
          demo1, [1,2], {a: 1, b : 2},
          repeats = 0,
          period = 180,
       ....
      )``:python
 -- since version 2.4.1 if you pass an additional parameter ``immediate=True`` it will force the main worker to reassign tasks. Until 2.4.1, the worker checks for new tasks every 5 cycles (so, ``5*heartbeats`` seconds). If you had an app that needed to check frequently for new tasks, to get a "snappy" behaviour you were forced to lower the ``heartbeat`` parameter, putting the db under pressure for no reason. With ``immediate=True`` you can force the check for new tasks: it will happen at most as ``heartbeat`` seconds are passed
The method returns the result of validate_and_insert, with the ``uuid`` of the task you queued (can be the one you passed or the auto-generated one).

``<Row {'errors': {}, 'id': 1, 'uuid': '08e6433a-cf07-4cea-a4cb-01f16ae5f414'}>``

If there are errors (e.g. you used ``period = 'a'``), you'll get the result of the validation, and id and uuid will be None

``<Row {'errors': {'period': 'enter an integer greater than or equal to 0'}, 'id': None, 'uuid': None}>``
##### Task status
- ``task_status(self, ref, output=False)``
 -- ``ref`` can be either:
  --- an integer --> lookup will be done by scheduler_task.id
  --- a string --> lookup will be done by scheduler_task.uuid
  --- a query --> lookup as you wish (as in db.scheduler_task.task_name == 'test1')
  --- **NB**: in the case of a query, only the last scheduler_run record will be fetched
  --- output=True will include the scheduler_run record too, plus a ``result`` key holding the decoded result
"""

    docs.one_time = """
#### One time only

Okay, let's start with the tests....something simple: a function that needs to run one time only.

``
scheduler.queue_task(demo4, task_name='one_time_only')
``:python

Instructions:
 - Push "Clear All"
 - Push "Start Monitoring"
 - If not yet, start a worker in another shell ``web2py.py -K w2p_scheduler_tests``
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
 - ``run_result`` is in json format
 - ``run_output`` is the stdout, so you can watch your nice "print" statements
 - ``start_time`` is when the task started
 - ``stop_time`` is when the task stopped
 - ``worker_name`` gets the worker name that processed the task
    """
    docs.repeats = """
#### Repeating task

Let's say we want to run the demo1 function with some args and vars, 2 times.
``
scheduler.queue_task(demo1, ['a','b'], dict(c=1, d=2), task_name="repeats", repeats=2, period=10)
``

Instructions (same as before):
 - Push "Clear All"
 - Push "Start Monitoring"
 - If not yet, start a worker in another shell ``web2py.py -K w2p_scheduler_tests``
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
#### Retry Failed

We want to run a function once, but allowing the function to raise an exception once.
That is, you want the function to "retry" an attempt if the first one fails.
We'll enqueue demo2, that we know if will fail in both runs, just to check if everything
works as expected (i.e. it gets re-queued only one time after the first FAILED run)

``
scheduler.queue_task(demo2, task_name='retry_failed', retry_failed=1, period=10)
``
    """
    docs.repeats_failed_consecutive = """
#### Retry Failed, round #2: understanding "consecutive failures"

As explained before, demo8 will fail the first two times, and then completes.
As soon as a repeating task completes, the "failed counter" gets resetted.
This means that if we queue demo8 with two allowed failures and 2 repeats,
we'll see 6 executions, also if the total failures will sum up to 4.
This is useful for tasks that are dependant on external resources that may
be occasionally unavailable, and but still want to have the task to be executed if not too
many failures occurred consecutively.

``
scheduler.queue_task(demo8, task_name='retry_failed_consecutive', retry_failed=2, repeats=2, period=10)
``
    """
    docs.expire = """
#### Expired status

To better understand the use of ``stop_time`` parameter we're going to schedule
a function with stop_time < now. Task will have the status **QUEUED**, but as soon
as a worker see it, it will set its status to **EXPIRED**.
``
stop_time = request.now - datetime.timedelta(seconds=60)
scheduler.queue_task(demo4, task_name='expire', stop_time=stop_time)
``
    """
    docs.priority = """
#### Priority

Also if there is no explicit priority management for tasks you'd like to execute
a task putting that "on top of the list", for one-time-only tasks you can force the
``next_run_time`` parameter to something very far in the past (according to your preferences).
A task gets **ASSIGNED** to a worker, and the worker picks up (and execute) first tasks with
minimum ``next_run_time`` in the set.

``
next_run_time = request.now - datetime.timedelta(seconds=60)
scheduler.queue_task(demo1, ['scheduled_first'], task_name='priority1')
scheduler.queue_task(demo1, ['scheduled_second'], task_name='priority2', next_run_time=next_run_time)
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
scheduler.queue_task(demo5, task_name='no_returns1')
scheduler.queue_task(demo3, task_name='no_returns2')
``
    """
    docs.timeouts = """
#### Tasks that will be terminated because they run too long

By default, the ``timeout`` parameter is set to 60 seconds. This means that if a
task takes more than 60 seconds to return, it is terminated and its status becomes
**TIMEOUT**.

We'll queue the function demo4 with a ``timeout`` parameter of 5 seconds and then again the
same function without timeout.
``
scheduler.queue_task(demo4, task_name='timeouts1', timeout=5)
scheduler.queue_task(demo4, task_name='timeouts2')
``


    """
    docs.percentages = """
#### Reporting percentages

A special "word" encountered in the print statements of your functions clear all
the previous output. That word is ``!clear!``.
This, coupled with the ``sync_output`` parameter, allows to report percentages
a breeze. The function ``demo6`` sleeps for 5 seconds, outputs ``50%``.
Then, it sleeps other 5 seconds and outputs ``100%``. Note that the output in the
scheduler_run table is synced every 2 seconds and that the second print statement
that contains ``!clear!100%`` gets the ``50%`` output cleared and replaced
by ``100%`` only.

``
scheduler.queue_task(demo6, task_name='percentages', sync_output=2)
``
"""
    docs.immediate = """
#### The ``immediate`` parameter

You may have found out that n seconds pass between the moment you queue the task and the moment it gets picked up by the worker.
That's because the scheduler - to alleviate the pressure on the db - checks for new tasks every 5 cycles.

This means that tasks gets **ASSIGNED** every 5*heartbeat seconds. Heartbeat by default is 3 seconds, so if you're very unlucky, you may wait **AT MOST** 15 seconds
between queueing the task and the task being picked up.

This lead developers to lower the heartbeat parameter to get a smaller "timeframe" of inactivity, putting the db under pressure for no reason.

Since 2.4.1, this is not needed anymore. You can force the scheduler to inspect the scheduler_task table for new tasks and set them to **ASSIGNED**.
This will happen without waiting 5 cycles: if your worker is not busy processing already queued tasks, it will wait **AT MOST** 3 seconds.
This happens:
 - if you set the worker status with ``is_ticker=True`` to **PICK**
 - if you pass to the ``queue_task`` function the ``immediate=True`` parameter (will set the worker status to **PICK** automatically)

------
Watch out: if you need to queue a lot of tasks, just do it and use the ``immediate=True`` parameter on the last: no need to update the worker_status table multiple times ^_^
------
``
scheduler.queue_task(demo1, ['a','b'], dict(c=1, d=2), task_name="immediate_task", immediate=True)
``

Instructions (same as before):
 - Push "Clear All"
 - Push "Start Monitoring"
 - If not yet, start a worker in another shell ``web2py.py -K w2p_scheduler_tests``
 - Wait a few seconds, a worker shows up
 - Push "Queue Task"
 - Wait a few seconds


Verify that:
 - tasks gets **ASSIGNED** within 3 seconds
 - one scheduler_task gets **QUEUED**, goes into **RUNNING** for a while
 - a scheduler_run record is created, goes **COMPLETED**
 - task becomes **COMPLETED**

Than, click "Stop Monitoring".
"""
    docs.w2p_task = """
#### W2P_TASK

From 2.4.1, scheduler injects a W2P_TASK global variable holding the ``id`` and the ``uuid`` of the task being executed.
You can use it to coordinate tasks, or to do some specialized logging.

``
scheduler.queue_task(demo7, task_name='task_variable')
``
"""

    docs.prevent_drift = """
#### The ``prevent_drift`` parameter

The scheduler replaced a lot of ``cron`` facilities around, but the difference are somehow subtle in some cases.
With a repeating task, by default the scheduler assumes that you want at least ``period`` seconds to pass
between one execution and the following one. You need to remember that the scheduler picks up the tasks as soon as possible:
this means that a task with a specific ``start_time`` will be picked up only if ``start_time`` is in the past.
Usually a few seconds pass by, and this is not an issue, but if you're scheduling a task to start at 9:00AM every morning,
you'll see the start_times of the executions slowly ''drifting'' from 9:00AM to 9:01AM.
This is because if the scheduler is busy processing tasks the first time at 9:00AM, your task will be picked up at 9:01AM,
and the next execution the scheduler will pick up the task only if 9:01AM are passed.
From 2.8.3, you can pass a ``prevent_drift`` parameter that will enable the scheduler to calculate the times between execution
more like cron, i.e. on the ``start_time`` instead of the actual execution of the task.
Beware! This means that the paradigm where the scheduler lets pass at least ``period`` seconds is invalidated.

``
scheduler.queue_task(demo1, ['a','b'], dict(c=1, d=2), task_name="prevent_drift", repeats=2, period=10, prevent_drift=True)
``

"""

    docs.stop_task = """
#### The ``stop_task`` method

If you need to stop a runaway task, the only way is to tell the worker to terminate the running process. Asking users
to retrieve the current worker processing the task and update its status to ``STOP_TASK`` was "Too Much",
so there's an experimental API for it.

NB: If the task is RUNNING it will terminate it, meaning that status will be set as FAILED. If the task is QUEUED,
its stop_time will be set as to "now", the enabled flag will be set to False, and the status to STOPPED

``stop_task`` either takes an integer or a string: if it's an integer it's assumed to be the id, if it's a string it's assumed to
be an uuid

So, given that the runaway task has been queued with
``
scheduler.queue_task(demo6, task_name='stop_task', uuid='stop_task')
``
you can stop it with
``
scheduler.stop_task('stop_task')
``

Instructions (same as before):
 - Push "Clear All"
 - Push "Start Monitoring"
 - If not yet, start a worker in another shell ``web2py.py -K w2p_scheduler_tests``
 - Wait a few seconds, a worker shows up
 - Push "Queue Task"
 - Wait a few seconds
 - Push "Stop Task"


Verify that:
 - task gets **STOPPED** or **FAILED**, according to it was running or not

Than, click "Stop Monitoring".
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
------
Watch out: all the worker management functions take the group_name as an optional parameter. If you have a worker processing ``high_prio`` and ``low_prio``, ``scheduler.disable('high_prio')`` will disable the worker alltogether, even if you didn't want to terminate ``low_prio`` too.
------
``
scheduler.disable()
scheduler.resume()
``:code

Instructions:
 - Push "Clear All"
 - Push "Start Monitoring"
 - If not yet, start a worker in another shell ``web2py.py -K w2p_scheduler_tests``
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

``
scheduler.terminate()
``:code

Instructions:
 - Push "Clear All"
 - Push "Start Monitoring"
 - If not yet, start a worker in another shell ``web2py.py -K w2p_scheduler_tests``
 - Wait a few seconds, a worker shows up
 - Push "Queue task"
 - Wait until the task is reported as **RUNNING**
 - Quick!!! Click on "Terminate worker"
 - Watch the scheduler finish the current task and then die
    """
    docs.kill = """
#### Kill a worker

A worker with the status **KILL** will die also if it's processing a task.

``
scheduler.kill()
``:code

Instructions:
 - Push "Clear All"
 - Push "Start Monitoring"
 - If not yet, start a worker in another shell ``web2py.py -K w2p_scheduler_tests``
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

Worker fine management is hard. This module tries not to leave behind any platform
(Mac, Win, Linux) providing the same feature set.
Right now workers can be started with an "embedded" mode:

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
All of these things are possible managing ``Scheduler`` parameters or using the API.
Altering the status via ``disable()``, ``resume()``, ``terminate()``, ``kill()`` is the way to go.
As tasks, workers can be in some fixed statuses : ACTIVE, DISABLED, TERMINATE or KILLED.

**ACTIVE** and **DISABLED** are "persistent", while **TERMINATE** or **KILL**, as statuses
name suggest, are more "commands" than real statuses.
Hitting ctrl+c in the console where a worker is started is equal to ``kill()`` that worker.

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
    discard_results=False,
    utc_time=False
    )``:python
Let's see them in order:

- ``db`` is the database DAL instance were you want the scheduler tables be placed.
NB: If you're using SQLite it's best to create a separate db to avoid lockings, and using
WAL is recommended

- ``tasks`` can be a dict. Must be defined for the "direct" mode or if you want to call a function
  not by his name, i.e.
  ``tasks=(mynameddemo1=demo1)`` will let you execute function demo1 with
  ``scheduler.queue_task('mynameddemo1')``
  instead of
  ``scheduler.queue_task('demo1')``
  In "embedded" mode, if you don't pass this parameter, function will be searched in the app environment.

- ``worker_name`` is None by default. As soon as the worker is started, a worker name
  is generated as hostname-uuid. If you want to specify that, be sure that it's unique.

- ``group_names`` is by default set to **[main]**. All tasks have a ``group_name`` parameter,
  set to **main** by default.
  Workers can pick up tasks only of their assigned group(s).
  NB: This is useful if you have different workers instances (e.g. on different servers)
  and you want to assign tasks to a specific worker.
  NB2: It's possible to assign a worker more groups, and they can be also all the same, as
  ``['mygroup','mygroup']``. Tasks will be distributed taking into consideration that
  a worker with group_names ``['mygroup','mygroup']`` is able to process the double of the tasks
  a worker with group_names ``['mygroup']`` is.

- ``heartbeat`` is by default set to 3 seconds. This parameter is the one controlling how often
  a scheduler will check its status and see if there are any **ASSIGNED** tasks to itself to process.

- ``max_empty_runs`` is 0 by default, that means that the worker will continue to process tasks
  as soon as they are **ASSIGNED**. If you set this to a value of, let's say, 10, a worker
  will die automatically if it's **ACTIVE** and no tasks are **ASSIGNED** to it for 10 loops.
  A loop is when a worker searches for tasks, every 3 seconds (or the set ``heartbeat``)

- ``discard_results`` is False by default. If set to True, no scheduler_run records will be created.
  NB: scheduler_run records will be created as before for **FAILED**, **TIMEOUT** and
  **STOPPED** tasks's statuses.

-``utc_time`` is False by default. If you need to coordinate with workers living in different
  timezones, or don't have problems with solar/DST times, supplying datetimes from different countries,
  etc, you can set this to True. The scheduler will honour the UTC time and work leaving the local
  time aside. Caveat: you need to schedule tasks with UTC times (for start_time, stop_time, and so on.)
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
If you need it to be executed later, use the ``start_time`` parameter (default = now).
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
from the START time of the first execution to the START time of the next execution).
There's a parameter named ``prevent_drift`` that if set to ``True`` will instead calculate the time
based on the scheduled ``start_time`` (vs the default behaviour that instead calculates the time
based on the **actual** time the task had been picked up)

Another nice addition, you can set how many times the function can raise an exception (i.e.
requesting data from a sloooow webservice) consecutively and be queued again instead of stopping in
**FAILED** status with the parameter ``retry_failed`` (default = 0, -1 = unlimited).
As soon as the task completes, the "failed" counter is reset.

[[task repeats http://yuml.me/7d8b85e4.jpg center]]

Summary: you have
 - ``period`` and ``repeats`` to get an automatically rescheduled function
 - ``timeout`` to be sure that a function doesn't exceed a certain amount of time
 - ``retry_failed`` to control how many times the task can "fail" consecutively
 - ``start_time`` and ``stop_time`` to schedule a function in a restricted timeframe
    """
    return dict(docs=docs)


def jobs():
    docs = Storage()
    docs.jobs = """
### Jobs

It's been a long ride until here but we were still missing a feature (hopefully stable from web2py 2.10+)...Jobs.

What are "Jobs", you ask ? Well, it's a way to coordinate a set of tasks that have dependencies (what in Celery is called "Canvas").

As always, the Scheduler sticks to the basics. Every Job is considered to be a DAG (a [[Directed Acyclic Graph http://en.wikipedia.org/wiki/Directed_acyclic_graph]]).
Without going into silly details, every task can have one or more dependencies, but of course you can't have mutual dependencies among the same tasks.
If a "job" can't be represented as a DAG, then it can't be processed in its entirety. You can still queue it, but it won't ever complete (i.e. you could have a
  complete stall at the first task or just a task left on 100 queued...)

So... what can you do ?
Let's take a trivial example (there are a few based on mathematics, map/reduce, etc... but hey, this is an example!!!)
Suppose you need to create a job that describes what is needed to get dressed ( thanks to http://hansolav.net/sql/graphs.html )...

We have a few items to wear, and there's an "order" to respect...
Items are: watch, jacket, shirt, tie, pants, undershorts, belt, shoes, socks

Now, we can't put on the tie without wearing the shirt first, etc...

[[job http://yuml.me/995413d6 center]]


Suppose we have those tasks queued in a controller (for example's sake, the same function, with different task_name(s))...

``
watch = s.queue_task(fname, task_name='watch')
jacket = s.queue_task(fname, task_name='jacket')
shirt = s.queue_task(fname, task_name='shirt')
tie = s.queue_task(fname, task_name='tie')
pants = s.queue_task(fname, task_name='pants')
undershorts = s.queue_task(fname, task_name='undershorts')
belt = s.queue_task(fname, task_name='belt')
shoes = s.queue_task(fname, task_name='shoes')
socks = s.queue_task(fname, task_name='socks')
``
Now, there's a helper class to construct and validate a "job".
First, let's declare a job named "job_1"

``
#from gluon.scheduler import JobGraph
myjob = JobGraph(db, 'job_1')
``

Next, we'd need to establish dependencies

``
# before the tie, comes the shirt
myjob.add_deps(tie.id, shirt.id)
# before the belt too comes the shirt
myjob.add_deps(belt.id, shirt.id)
# before the jacket, comes the tie
myjob.add_deps(jacket.id, tie.id)
# before the belt, come the pants
myjob.add_deps(belt.id, pants.id)
# before the shoes, comes the pants
myjob.add_deps(shoes.id, pants.id)
# before the pants, comes the undershorts
myjob.add_deps(pants.id, undershorts.id)
# before the shoes, comes the undershorts
myjob.add_deps(shoes.id, undershorts.id)
# before the jacket, comes the belt
myjob.add_deps(jacket.id, belt.id)
# before the shoes, comes the socks
myjob.add_deps(shoes.id, socks.id)
``

Then, we can ask JobGraph if what we asked is a job that is accomplishable
``
myjob.validate('job_1')
``

And voilà, job done!

How it works under the hood ?

There's a new table called ``scheduler_task_deps`` that holds a reference to the job_name, the task parent, the task child and
a boolean to mark the "path" (the arrows in the graph) as "visitable".
To be fair, the job name isn't that important, you can have task dependencies amongst
different jobs, it's just not that easy to verify that the Job is a DAG at a later stage.
If a path is "visitable" it means that the DAG graph can be "walked" in that direction.
Every time a task gets "COMPLETED", the "paths" gets updated to be "visitable". The algo to pick up tasks has been updated
to work fetching only tasks that have no dependencies, or dependencies that have already been satisfied (i.e. tasks that depends
on nothing, or tasks that depend on tasks that are yet COMPLETED).

"""

    return dict(docs=docs)


def user():
    return dict(form=auth())
