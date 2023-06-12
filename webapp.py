import sys
import os
os.environ['PYTHONUNBUFFERED'] = 'TRUE'

BASE_DIR = "/home/centos/vector/"
sys.path.append(BASE_DIR)
 
 
bind = '127.0.0.1:8000'
backlog = 2048
 
 
import multiprocessing
workers = multiprocessing.cpu_count() * 2 + 1
worker_class = 'sync'
worker_connections = 1000
timeout = 300
keepalive = 2
capture_output = True
 
spew = False
 
accesslog = '/var/log/webapp_access_log'
loglevel = 'debug'
errorlog = '/var/log/webapp_error_log'
stdout_logfile ='/var/log/webapp_error_log' 
 
def post_fork(server, worker):
    server.log.info("Worker spawned (pid: %s)", worker.pid)
 
 
def pre_fork(server, worker):
    pass
 
 
def pre_exec(server):
    server.log.info("Forked child, re-executing.")
 
 
def when_ready(server):
    server.log.info("Server is ready. Spawning workers")
 
 
def worker_int(worker):
    worker.log.info("worker received INT or QUIT signal")
 
    ## get traceback info
    import threading, sys, traceback
    id2name = dict([(th.ident, th.name) for th in threading.enumerate()])
    code = []
    for threadId, stack in sys._current_frames().items():
        code.append("\n# Thread: %s(%d)" % (id2name.get(threadId,""),
            threadId))
        for filename, lineno, name, line in traceback.extract_stack(stack):
            code.append('File: "%s", line %d, in %s' % (filename,
                lineno, name))
            if line:
                code.append("  %s" % (line.strip()))
    worker.log.debug("\n".join(code))
 
 
def worker_abort(worker):
    worker.log.info("worker received SIGABRT signal")
