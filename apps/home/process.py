from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import time
import paramiko
import json
import smtplib
from .models import *

def check_ssh(ip, username, password):
    try:
        transport = paramiko.Transport(ip)
        transport.connect(username=username, password=password)
        transport.close()
        return 1
    except (paramiko.AuthenticationException, OSError):
        return 2
    except (paramiko.SSHException):
        return 3
def send_email(ip, username, password, status):
    # Cấu hình thông tin email
    sender_email = 'hinhlx@viettel.com.vn'
    receiver_email = 'dangnq@viettel.com.vn'
    smtp_server = 'smtp.viettel.com.vn'
    smtp_port = 465
    smtp_username = 'hinhlx@viettel.com.vn'
    smtp_password = 'Xincamondangnq123@'

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
def scan(ip, username_list, password_list):
    login_false = 0
    for username in username_list:
        for password in password_list:
            if check_ssh(ip, username, password) == 1:
                result.objects.create(ip=ip, username=username, password=password, status="success")
                send_email(ip, username, password, "success")
                return
            if check_ssh(ip, username, password) == 2:
                result.objects.create(ip=ip, username=username, password=password, status="failed")
                login_false += 1
                if login_false == 5:
                    # time.sleep(300)   # Đợi 5 phút trước khi quét tiếp
                    login_false = 0
            if check_ssh(ip, username, password) == 3:
                result.objects.create(ip=ip, username=username, password=password, status="not connected")
                return