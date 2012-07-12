# coding: utf8
import datetime
from gluon.contrib.simplejson import loads, dumps

sw = db.scheduler_worker
sr = db.scheduler_run
st = db.scheduler_task

def clear_all():
    sw = db.scheduler_worker
    sr = db.scheduler_run
    st = db.scheduler_task

    swstatus = db(sw.id>0).delete()
    srstatus = db(sr.id>0).delete()
    ststatus = db(st.id>0).delete()

    btn_status = '#' + request.cid.replace('_cleara', '_status')
    btn_queue = '#' + request.cid.replace('_cleara', '_queue')

    response.js = "$('%s').removeClass('disabled');$('%s').removeClass('disabled');" % (btn_status, btn_queue)
    response.flash = "Cleared correctly"

def worker1():
    st.insert(task_name='one_time_only', function_name='demo4')
    response.js = "$('#worker_1_queue').addClass('disabled');"
    response.flash = "Function demo4 scheduled"

def worker2():
    st.insert(task_name='repeats', function_name='demo1', args=dumps(['a','b']), vars=dumps(dict(c=1, d=2)), repeats=2, period=30)
    response.js = "$('#worker_2_queue').addClass('disabled');"
    response.flash = "Function demo1 scheduled"

def worker3():
    st.insert(task_name='repeats_failed', function_name='demo2', repeats_failed=2, period=30)
    response.js = "$('#worker_3_queue').addClass('disabled');"
    response.flash = "Function demo2 scheduled"

def worker4():
    stop_time = request.now - datetime.timedelta(seconds=60)
    st.insert(task_name='expire', function_name='demo4', stop_time=stop_time)
    response.js = "$('#worker_4_queue').addClass('disabled');"
    response.flash = "Function demo4 scheduled with stop time %s" % stop_time

def worker5():
    next_run_time = request.now - datetime.timedelta(seconds=60)
    st.insert(task_name='priority1', function_name='demo1', args=dumps(['scheduled_first']))
    st.insert(task_name='priority2', function_name='demo1', args=dumps(['scheduled_second']), next_run_time=next_run_time)
    response.js = "$('#worker_5_queue').addClass('disabled');"
    response.flash = "Function demo1 scheduled two times"

def worker6():
    st.insert(task_name='no_returns1', function_name='demo5')
    st.insert(task_name='no_returns2', function_name='demo3')
    response.js = "$('#worker_6_queue').addClass('disabled');"
    response.flash = "Function demo5 and demo3 scheduled"

def worker7():
    st.insert(task_name='one_time_only', function_name='demo4')
    response.js = "$('#worker_7_queue').addClass('disabled');"
    response.flash = "Function demo4 scheduled"

def worker8():
    st.insert(task_name='one_time_only', function_name='demo4')
    response.js = "$('#worker_8_queue').addClass('disabled');"
    response.flash = "Function demo4 scheduled"

def worker9():
    st.insert(task_name='one_time_only', function_name='demo4')
    response.js = "$('#worker_9_queue').addClass('disabled');"
    response.flash = "Function demo4 scheduled"

def enable_workers():
    db(sw.id>0).update(status='ACTIVE')
    response.flash = 'Workers enabled'

def disable_workers():
    db(sw.id>0).update(status='DISABLED')
    response.flash = 'Workers disabled'

def terminate_workers():
    db(sw.id>0).update(status='TERMINATE')
    response.flash = 'TERMINATE command sent'

def kill_workers():
    db(sw.id>0).update(status='KILL')
    response.flash = 'KILL command sent'
