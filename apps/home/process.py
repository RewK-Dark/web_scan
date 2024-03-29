from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import time
import paramiko
import json
import smtplib
from .models import *
import traceback, sys
timeout_ips = set()
import nmap
# def check_ssh(ip, username, password):
#     client = paramiko.SSHClient()
#     client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
#     try:
#         if ip in timeout_ips:  # Kiểm tra xem IP có trong danh sách timeout hay không
#             return False, "Skip because timed out"
        
#         client.connect(ip, username=username, password=password, banner_timeout=1000, timeout=5)
#         client.close()
#         return True, None
#     except paramiko.ssh_exception.AuthenticationException:
#         return False, "Authentication failed"
#     except Exception as e:
#         timeout_ips.add(ip)  # Thêm IP vào danh sách timeout
#         exc_type, exc_value, exc_traceback = sys.exc_info()
#         lines = traceback.format_exception(exc_type, exc_value, exc_traceback)
#         log = ''.join('!! ' + line for line in lines)  # Log it or whatever here
#         #print("Log detail {}".format(log))
#         client.close()
#         return False, e
def check_ssh(ip, username, password):
    nm = nmap.PortScanner()
    nm.scan(ip, '22,23,3389')  # Kiểm tra các cổng 22, 23 và 3389
    open_ports = [port for port in [22, 23, 3389] if 'tcp' in nm[ip] and nm[ip]['tcp'][port]['state'] == 'open']
    
    if 22 in open_ports:
        # Thực hiện kết nối SSH
    elif 23 in open_ports:
        # Thực hiện kết nối Telnet
    elif 3389 in open_ports:
        # Thực hiện kết nối RDP
    else:
        return False, "No supported port open"
         
def scan(ip_list, username, password_list):
    login_false = 0
    error = 0
    for password in password_list:
        for ip in ip_list:
            status, log = check_ssh(ip, username, password)
            if status:
                result.objects.create(ip=ip, username=username, password=password, status="success")
                # send_email(ip, username, password, "success")
                return
            else:
                result.objects.create(ip=ip, username=username, password=password, status=log)
                login_false += 1
                if login_false == 5:
                    # time.sleep(300)   # Đợi 5 phuytyút trước khi quét tiếp
                    login_false = 0
            # if check_ssh(ip, username, password) == 3:
            #     result.objects.create(ip=ip, username=username, password=password, status="not connected")
            #     # error +=1
            #     # if error == 3:
            #     return
def send_email(ip, username, password, status):
    # Cấu hình thông tin email
    sender_email = 'hinhlx@viettel.com.vn'
    receiver_email = 'dangnq@viettel.com.vn'
    smtp_server = 'smtp.viettel.com.vn'
    smtp_port = 465
    smtp_username = 'hinhlx@viettel.com.vn'
    smtp_password = '@'

    # Tạo nội dung email
    subject = 'Kết quả quét SSH'
    message = f'IP: {ip}\nUsername: {username}\nPassword: {password}\nStatus: {status}'

    # Tạo đối tượng MIMEMultipart để chứa nội dung email
    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = receiver_email
    msg['Subject'] = subject

    # Thêm nội dung email vào phần body
    msg.attach(MIMEText(message, 'plain'))

    # Kết nối đến SMTP server và gửi email
    try:
        server = smtplib.SMTP_SSL(smtp_server, smtp_port)
        server.login(smtp_username, smtp_password)
        server.send_message(msg)
        server.quit()
        print('Email đã được gửi thành công!')
    except Exception as e:
        print('Gửi email thất bại:', str(e))