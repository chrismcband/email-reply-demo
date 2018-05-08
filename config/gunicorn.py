bind = "127.0.0.1:9100"
backlog = 256
# workers = 4
# worker_class = 'gevent'
# worker_connections = 256
max_requests = 512
timeout = 90
keepalive = 1

proc_name = 'gunicorn'
default_proc_name = 'gunicorn'
pidfile = '/tmp/emailreplydemo.gunicorn.pid'

preload_app = False
daemon = False

debug = False
spew = False

umask = 0
tmp_upload_dir = None

logfile = '/tmp/emailreplydemo.gunicorn.log'
errorlog = logfile
loglevel = 'warning'
logconfig = None
