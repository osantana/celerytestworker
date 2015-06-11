#!/usr/bin/env python3
# coding: utf-8


import sys
import time
import logging
import multiprocessing

from celery import signals
from .utils import get_application

if sys.version_info >= (3, 0):
    basestring = str


RETRY_INTERVAL = 0.3  # seconds


class TerminateTimeout(Exception):
    def __init__(self, pending_tasks, *args, **kwargs):
        self.pending_tasks = pending_tasks
        super(TerminateTimeout, self).__init__(*args, **kwargs)


# noinspection PyUnusedLocal
class CeleryTestWorker(multiprocessing.Process):
    def __init__(self, app, purge=True, log=False):
        super(CeleryTestWorker, self).__init__()
        self.ready = multiprocessing.Event()

        if isinstance(app, basestring):
            app = get_application(app)

        self.app = app

        loglevel = logging.INFO if log else logging.CRITICAL + 10
        self.worker = self.app.Worker(purge=purge, loglevel=loglevel)

    def on_worker_ready(self, sender=None, **kwargs):
        if not self.ready.is_set():
            self.ready.set()

    def wait(self):
        while not self.ready.is_set():
            time.sleep(.3)

    def run(self):
        signals.worker_ready.connect(self.on_worker_ready)
        self.worker.start()

    @classmethod
    def create(cls, app, purge=True, log=False):
        worker = cls(app, purge, log)
        worker.start()
        worker.wait()
        return worker

    def terminate(self, timeout=3):
        inspect = self.app.control.inspect()
        hostname = self.worker.hostname

        self.app.finalize()
        self.worker.stop()

        pending_tasks = []
        retries = 0
        max_retries = int(round(timeout / RETRY_INTERVAL, 0))
        while retries < max_retries:
            pending_tasks = []
            scheduled = inspect.scheduled()
            active = inspect.active()

            if scheduled and hostname in scheduled:
                pending_tasks.extend(scheduled[hostname])

            if active and hostname in active:
                pending_tasks.extend(active[hostname])

            if not pending_tasks:
                break

            retries += 1
            time.sleep(RETRY_INTERVAL)
        else:
            raise TerminateTimeout(pending_tasks)

        return super(CeleryTestWorker, self).terminate()

    def __enter__(self):
        self.start()
        self.wait()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.terminate()

