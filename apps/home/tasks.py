# your_project/tasks.py
from celery import shared_task
from .process import *
from .models import result
from concurrent.futures import ThreadPoolExecutor, as_completed
@shared_task
def scan_task(ip_list, username_list, password_list):
    thread_pool_size = 4
    with ThreadPoolExecutor(max_workers=thread_pool_size) as executor:
        futures = []

        for user in username_list:
            executor.submit(scan, ip_list, user, password_list)

    return 'Scan task has been initiated successfully.'