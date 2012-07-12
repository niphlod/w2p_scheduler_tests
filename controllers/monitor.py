# -*- coding: utf-8 -*-

def get_status():
    sw = db.scheduler_worker
    sr = db.scheduler_run
    st = db.scheduler_task

    swstatus = db(sw.id>0).select()

    srstatus = db(sr.id>0).select()

    ststatus = db(st.id>0).select()

    return dict(swstatus=swstatus, srstatus=srstatus, ststatus=ststatus)
