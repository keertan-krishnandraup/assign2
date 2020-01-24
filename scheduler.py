from datetime import datetime
import time
import os
from joiner import get_and_update_data

from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.jobstores.mongodb import MongoDBJobStore
from apscheduler.executors.pool import ThreadPoolExecutor,ProcessPoolExecutor
from apscheduler.triggers.cron import CronTrigger

jobstores = {
    'default':MongoDBJobStore()
}
executors = {
    'default':ThreadPoolExecutor(20)
}
job_defaults = {
    'coalesce' : False,
    'max_instances' : 3
}


if __name__ == '__main__':
    scheduler = BlockingScheduler(jobstores = jobstores, executors = executors, job_defaults = job_defaults)
    scheduler.add_job(get_and_update_data, CronTrigger(minute='*/1'))
    print('Press Ctrl+{0} to exit'.format('Break' if os.name == 'nt' else 'C'))
    try:
        scheduler.start()
    except (KeyboardInterrupt, SystemExit):
        scheduler.shutdown()