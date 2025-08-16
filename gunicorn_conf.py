import multiprocessing
import os

# Server socket
bind = "0.0.0.0:8000"

# Worker processes
workers = int(os.environ.get('GUNICORN_PROCESSES', '2'))
worker_class = "uvicorn.workers.UvicornWorker"
threads = int(os.environ.get('GUNICORN_THREADS', '4'))

# Logging
loglevel = "info"
accesslog = "-"
errorlog = "-"
