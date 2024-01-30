# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from django import template
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from django.urls import reverse
from django.shortcuts import render
from django.contrib import messages
import openpyxl
from openpyxl import Workbook
from docx import Document
from .tasks import *

@login_required(login_url="/login/")
def index(request):
    context = {'segment': 'index'}

    html_template = loader.get_template('home/index.html')
    return HttpResponse(html_template.render(context, request))

@login_required(login_url="/login/")
def hello(request):
    return render(request, "home/hello.html")

@login_required(login_url="/login/")
def scan(request):
    if request.method == 'POST':
        ip_file = request.FILES['ipFile']
        user_file = request.FILES['usernameFile']
        pass_file = request.FILES['passwordFile']

        if ip_file and user_file and pass_file:
            ip_list = ip_file.read().decode('utf-8').splitlines()
            username_list = user_file.read().decode('utf-8').splitlines()
            password_list = pass_file.read().decode('utf-8').splitlines()

            scan_task.delay(ip_list, username_list, password_list)

        return render(request, 'home/map.html')  

            # msg = 'Đã gửi yêu cầu quét!'
            # return render(request, "home/map.html")

    elif request.method == 'GET':
        return render(request, "home/map.html")

@login_required(login_url="/login/")
def pages(request):
    context = {}
    # All resource paths end in .html.
    # Pick out the html file name from the url. And load that template.
    try:

        load_template = request.path.split('/')[-1]

        if load_template == 'admin':
            return HttpResponseRedirect(reverse('admin:index'))
        context['segment'] = load_template

        html_template = loader.get_template('home/' + load_template)
        return HttpResponse(html_template.render(context, request))

    except template.TemplateDoesNotExist:

        html_template = loader.get_template('home/page-404.html')
        return HttpResponse(html_template.render(context, request))

    except:
        html_template = loader.get_template('home/page-500.html')
        return HttpResponse(html_template.render(context, request))
    


