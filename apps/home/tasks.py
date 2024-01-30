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

        for ip in ip_list:
            future = executor.submit(scan, ip, username_list, password_list)
            futures.append(future)

        for future in as_completed(futures):
            result = future.result()

    return result