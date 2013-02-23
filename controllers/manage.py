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
    cont = '#' + request.cid.replace('_cleara', '_status_container')

    response.js = "$('%s').removeClass('disabled');$('%s').removeClass('disabled');$('%s').removeClass('w2p_component_stop');" % (btn_status, btn_queue, cont)
    response.flash = "Cleared correctly"

def worker1():
    scheduler.queue_task(demo4, task_name='one_time_only')
    response.js = "$('#worker_1_queue').addClass('disabled');"
    response.flash = "Function demo4 scheduled"

def worker2():
    scheduler.queue_task(demo1, ['a','b'], dict(c=1, d=2), task_name='repeats', repeats=2, period=10)
    response.js = "$('#worker_2_queue').addClass('disabled');"
    response.flash = "Function demo1 scheduled"

def worker3():
    for a in range(100):
        scheduler.queue_task(demo2, task_name='retry_failed', retry_failed=1, period=10)
    response.js = "$('#worker_3_queue').addClass('disabled');"
    response.flash = "Function demo2 scheduled"

def worker4():
    stop_time = request.now - datetime.timedelta(seconds=60)
    scheduler.queue_task(demo4, task_name='expire', stop_time=stop_time)
    response.js = "$('#worker_4_queue').addClass('disabled');"
    response.flash = "Function demo4 scheduled with stop time %s" % stop_time

def worker5():
    next_run_time = request.now - datetime.timedelta(seconds=60)
    scheduler.queue_task(demo1, ['scheduled_first'], task_name='priority1')
    scheduler.queue_task(demo1, ['scheduled_second'], task_name='priority2', next_run_time=next_run_time)
    response.js = "$('#worker_5_queue').addClass('disabled');"
    response.flash = "Function demo1 scheduled two times"

def worker6():
    scheduler.queue_task(demo5, task_name='no_returns1')
    scheduler.queue_task(demo3, task_name='no_returns2')
    response.js = "$('#worker_6_queue').addClass('disabled');"
    response.flash = "Function demo5 and demo3 scheduled"

def worker7():
    scheduler.queue_task(demo4, task_name='one_time_only')
    response.js = "$('#worker_7_queue').addClass('disabled');"
    response.flash = "Function demo4 scheduled"

def worker8():
    scheduler.queue_task(demo4, task_name='one_time_only')
    response.js = "$('#worker_8_queue').addClass('disabled');"
    response.flash = "Function demo4 scheduled"

def worker9():
    scheduler.queue_task(demo4, task_name='one_time_only')
    response.js = "$('#worker_9_queue').addClass('disabled');"
    response.flash = "Function demo4 scheduled"

def worker10():
    scheduler.queue_task(demo4, task_name='timeouts1', timeout=5)
    scheduler.queue_task(demo4, task_name='timeouts2')
    response.js = "$('#worker_10_queue').addClass('disabled');"
    response.flash = "Functions demo4 scheduled"

def worker11():
    scheduler.queue_task(demo6, task_name='percentages', sync_output=2)
    response.js = "$('#worker_11_queue').addClass('disabled');"
    response.flash = "Function demo6 scheduled"

def worker12():
    scheduler.queue_task(demo1, ['a','b'], dict(c=1, d=2), task_name="immediate_task", immediate=True)
    response.js = "$('#worker_12_queue').addClass('disabled');"
    response.flash = "Function demo1 scheduled with immediate=True"

def worker13():
    scheduler.queue_task(demo7, task_name='task_variable')
    response.js = "$('#worker_13_queue').addClass('disabled');"
    response.flash = "Function demo7 scheduled"

def enable_workers():
    scheduler.resume()
    response.flash = 'Workers enabled'

def disable_workers():
    scheduler.disable()
    response.flash = 'Workers disabled'

def terminate_workers():
    scheduler.terminate()
    response.flash = 'TERMINATE command sent'

def kill_workers():
    scheduler.kill()
    response.flash = 'KILL command sent'
