# coding: utf8
import datetime
from gluon.contrib.simplejson import loads, dumps

sw = db.scheduler_worker
sr = db.scheduler_run
st = db.scheduler_task


def worker1():
    q = st.task_name=='one_time_only'
    try:
        info = scheduler.task_status(q, output=True)
        res = [
            ("task status completed", info.scheduler_task.status == 'COMPLETED'),
            ("task times_run is 1" , info.scheduler_task.times_run == 1),
            ("scheduler_run record is COMPLETED " , info.scheduler_run.status == 'COMPLETED')
        ]
    except:
        res = [("Wait a few seconds and retry the 'verify' button", False)]
    response.view = 'default/verify.load'
    return dict(res=res)

def worker2():
    try:
        task = scheduler.task_status(st.task_name=='repeats')
        task_run = db(sr.task_id == task.id).select()
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
        task = scheduler.task_status(st.task_name=='retry_failed')
        task_run = db(sr.task_id == task.id).select()
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
        task = scheduler.task_status(st.task_name=='expire')
        task_run = db(sr.task_id == task.id).select()
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
        task1 = scheduler.task_status(st.task_name=='priority1', output=True)
        task2 = scheduler.task_status(st.task_name=='priority2', output=True)
        res = [
            ("tasks status completed", task1.scheduler_task.status == task2.scheduler_task.status == 'COMPLETED'),
            ("priority2 was executed before priority1" , task1.scheduler_run.id > task2.scheduler_run.id)
        ]
    except:
        res = []
    response.view = 'default/verify.load'
    return dict(res=res)

def worker6():
    try:
        task1 = scheduler.task_status(st.task_name=='no_returns1')
        task2 = scheduler.task_status(st.task_name=='no_returns2')
        task_run1 = db(sr.task_id == task1.id).select()
        task_run2 = db(sr.task_id == task2.id).select()
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
        task1 = scheduler.task_status(st.task_name=='timeouts1', output=True)
        task2 = scheduler.task_status(st.task_name=='timeouts2', output=True)
        res = [
            ("tasks timeouts1 timeoutted", task1.scheduler_task.status == 'TIMEOUT'),
            ("tasks timeouts2 completed", task2.scheduler_task.status == 'COMPLETED'),
            ("task timeouts1 stop_time-start_time = ~5 seconds", (task1.scheduler_run.stop_time - task1.scheduler_run.start_time).seconds < 7)
        ]
    except:
        res = []
    response.view = 'default/verify.load'
    return dict(res=res)

def worker11():
    try:
        task1 = scheduler.task_status(st.task_name=='percentages', output=True)
        print task1
        res = [
            ("tasks percentages completed", task1.scheduler_task.status == 'COMPLETED'),
            ("output contains only 100%", task1.scheduler_run.run_output.strip() == "100%")
        ]
    except:
        res = []
    response.view = 'default/verify.load'
    return dict(res=res)


def worker12():
    try:
        res = []
        tasks = db(st.task_name=='immediate_task').select()
        for task in tasks:
            run_record = db(sr.task_id == task.id).select().first()
            elapsed = (run_record.start_time - task.start_time).seconds
            res.append(
                ("task %s got executed %s seconds later (less than 10 is good because it means it got assigned soon, and we're using SQLite)" % (task.id,elapsed),  elapsed < 10),
            )
    except:
        res = []
    response.view = 'default/verify.load'
    return dict(res=res)


def worker13():
    try:
        task1 = scheduler.task_status(st.task_name=='task_variable', output=True)
        res = [
                ("task %s returned W2P_TASK correctly" % (task1.scheduler_task.id),  task1.result == [task1.scheduler_task.id, task1.scheduler_task.uuid]),
            ]
    except:
        res = []
    response.view = 'default/verify.load'
    return dict(res=res)

def worker14():
    try:
        task = scheduler.task_status(st.task_name=='prevent_drift')
        task_run = db(sr.task_id == task.id).select()
        res = [
            ("task status completed", task.status == 'COMPLETED'),
            ("task times_run is 2" , task.times_run == 2),
            ("task ran 2 times only" , len(task_run) == 2),
            ("scheduler_run records are COMPLETED " , (task_run[0].status == task_run[1].status == 'COMPLETED')),
            ("next_run_time is exactly start_time + 20 seconds", (task.next_run_time == task.start_time + datetime.timedelta(seconds=20)))
        ]
    except:
        res = [("Wait a few seconds and retry the 'verify' button", False)]
    response.view = 'default/verify.load'
    return dict(res=res)

def worker15():
    try:
        task = scheduler.task_status(st.task_name=='stop_task')
        task_run = db(sr.task_id == task.id).select()
        if len(task_run):
            res = [
                ("task status FAILED", task.status == 'FAILED')
            ]
        else:
            res = [
                ("task status STOPPED", task.status == 'STOPPED')
            ]
    except:
        res = [("Wait a few seconds and retry the 'verify' button", False)]
    response.view = 'default/verify.load'
    return dict(res=res)