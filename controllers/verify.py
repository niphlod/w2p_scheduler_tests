# coding: utf8
import datetime
from gluon.contrib.simplejson import loads, dumps

sw = db.scheduler_worker
sr = db.scheduler_run
st = db.scheduler_task


def worker1():
    try:
        task = db(st.task_name=='one_time_only').select().first()
        task_run = db(sr.scheduler_task == task.id).select()
        res = [
            ("task status completed", task.status == 'COMPLETED'),
            ("task times_run is 1" , task.times_run == 1),
            ("task ran one time only" , len(task_run) == 1),
            ("scheduler_run record is COMPLETED " , task_run[0].status == 'COMPLETED')
        ]
    except:
        res = [("Wait a few seconds and retry the 'verify' button", False)]
    response.view = 'default/verify.load'
    return dict(res=res)

def worker2():
    try:
        task = db(st.task_name=='repeats').select().first()
        task_run = db(sr.scheduler_task == task.id).select()
        res = [
            ("task status completed", task.status == 'COMPLETED'),
            ("task times_run is 2" , task.times_run == 2),
            ("task ran 2 times only" , len(task_run) == 2),
            ("scheduler_run records are COMPLETED " , (task_run[0].status == task_run[1].status == 'COMPLETED')),
            ("period is respected", (task_run[1].start_time > task_run[0].start_time + datetime.timedelta(seconds=task.period)))
        ]
    except:
        res = [("Wait a few seconds and retry the 'verify' button", False)]
    response.view = 'default/verify.load'
    return dict(res=res)

def worker3():
    try:
        task = db(st.task_name=='retry_failed').select().first()
        task_run = db(sr.scheduler_task == task.id).select()
        res = [
            ("task status failed", task.status == 'FAILED'),
            ("task times_run is 0" , task.times_run == 0),
            ("task times_failed is 2" , task.times_failed == 2),
            ("task ran 2 times only" , len(task_run) == 2),
            ("scheduler_run records are FAILED" , (task_run[0].status == task_run[1].status == 'FAILED')),
            ("period is respected", (task_run[1].start_time > task_run[0].start_time + datetime.timedelta(seconds=task.period)))
        ]
    except:
        res = []
    response.view = 'default/verify.load'
    return dict(res=res)


def worker4():
    try:
        task = db(st.task_name=='expire').select().first()
        task_run = db(sr.scheduler_task == task.id).select()
        res = [
            ("task status expired", task.status == 'EXPIRED'),
            ("task times_run is 0" , task.times_run == 0),
            ("task didn't run at all" , len(task_run) == 0)
        ]
    except:
        res = []
    response.view = 'default/verify.load'
    return dict(res=res)

def worker5():
    try:
        task1 = db(st.task_name=='priority1').select().first()
        task2 = db(st.task_name=='priority2').select().first()
        task_run1 = db(sr.scheduler_task == task1.id).select()
        task_run2 = db(sr.scheduler_task == task2.id).select()
        res = [
            ("tasks status completed", task1.status == task2.status == 'COMPLETED'),
            ("priority2 was executed before priority1" , task_run1[0].id > task_run2[0].id)
        ]
    except:
        res = []
    response.view = 'default/verify.load'
    return dict(res=res)

def worker6():
    try:
        task1 = db(st.task_name=='no_returns1').select().first()
        task2 = db(st.task_name=='no_returns2').select().first()
        task_run1 = db(sr.scheduler_task == task1.id).select()
        task_run2 = db(sr.scheduler_task == task2.id).select()
        res = [
            ("tasks no_returns1 completed", task1.status == 'COMPLETED'),
            ("tasks no_returns2 failed", task2.status == 'FAILED'),
            ("no_returns1 doesn't have a scheduler_run record", len(task_run1) == 0),
            ("no_returns2 has a scheduler_run record FAILED", (len(task_run2) == 1 and task_run2[0].status == 'FAILED')),
        ]
    except:
        res = []
    response.view = 'default/verify.load'
    return dict(res=res)

def worker10():
    try:
        task1 = db(st.task_name=='timeouts1').select().first()
        task2 = db(st.task_name=='timeouts2').select().first()
        task_run1 = db(sr.scheduler_task == task1.id).select()
        task_run2 = db(sr.scheduler_task == task2.id).select()
        res = [
            ("tasks timeouts1 timeoutted", task1.status == 'TIMEOUT'),
            ("tasks timeouts2 completed", task2.status == 'COMPLETED'),
            ("task timeouts1 stop_time-start_time = ~5 seconds", (task_run1[0].stop_time - task_run1[0].start_time).seconds < 7)
        ]
    except:
        res = []
    response.view = 'default/verify.load'
    return dict(res=res)

def worker11():
    try:
        task1 = db(st.task_name=='percentages').select().first()
        task_run1 = db(sr.scheduler_task == task1.id).select()
        res = [
            ("tasks percentages completed", task1.status == 'COMPLETED'),
            ("output contains only 100%", task_run1[0].output.strip() == "100%")
        ]
    except:
        res = []
    response.view = 'default/verify.load'
    return dict(res=res)