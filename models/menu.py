# -*- coding: utf-8 -*-
# this file is released under public domain and you can use without limitations

#########################################################################
## Customize your APP title, subtitle and menus here
#########################################################################

response.title = ' '.join(word.capitalize() for word in request.application.split('_'))
response.subtitle = "Testing Scheduler"

## read more at http://dev.w3.org/html5/markup/meta.name.html
response.meta.author = 'Niphlod <niphlod@gmail.com>'
response.meta.description = 'get along with the scheduler'
response.meta.keywords = 'web2py, python, framework'
response.meta.generator = 'Web2py Web Framework'
response.meta.copyright = 'Copyright 2012'

## your http://google.com/analytics id
response.google_analytics_id = None

#########################################################################
## this is the main application menu add/remove items as required
#########################################################################

response.menu = [
    ('Home', False, URL('default','index'), []),
    ('Tasks', False, None, [
        ('Intro', False, URL('default', 'tasks', anchor='intro')),
        ('One Time Only', False, URL('default', 'tasks', anchor='worker_1')),
        ('Repeating task', False, URL('default', 'tasks', anchor='worker_2')),
        ('Repeats Failed', False, URL('default', 'tasks', anchor='worker_3')),
        ('Expired status', False, URL('default', 'tasks', anchor='worker_4')),
        ('Priority', False, URL('default', 'tasks', anchor='worker_5')),
        ('Tasks with no return value', False, URL('default', 'tasks', anchor='worker_6')),
        ('Timeouts', False, URL('default', 'tasks', anchor='worker_10')),
        ('Percentages', False, URL('default', 'tasks', anchor='worker_11'))
        ]),
    ('Workers', False, None, [
        ('Disable', False, URL('default', 'workers', anchor='worker_7')),
        ('Terminate', False, URL('default', 'workers', anchor='worker_8')),
        ('Kill', False, URL('default', 'workers', anchor='worker_9'))
        ]),
    ('How it works', False, None, [
        ('Scheduler', False, URL('default', 'how_it_works', anchor='workers')),
        ('Task Lifecycle', False, URL('default', 'how_it_works', anchor='tasks'))
        ])
    ]
