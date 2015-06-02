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
    def create(cls, app):
        worker = cls(app)
        worker.start()
        worker.wait()
        return worker

    def terminate(self):
        inspect = self.app.control.inspect()
        hostname = self.worker.hostname

        self.app.finalize()
        self.worker.stop()

        while inspect.scheduled()[hostname] or inspect.active()[hostname]:
            time.sleep(.3)

        super(CeleryTestWorker, self).terminate()

    def __enter__(self):
        self.start()
        self.wait()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.terminate()
