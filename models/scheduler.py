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
