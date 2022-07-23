import csv
import smtplib, ssl
from datetime import datetime
import datafile

email_content_template = '''\
Subject: IAMPEXMYACYB-IAM CERT EXPIRY NOTIFICATION

Account Name: {{acname}} {0} {{/acname}}
Application Name: {{apname}} {{/apname}}
Directory: {{directory}} {{/directory}}
Owner Name: {{oname}} {{/oname}}
Password Expiration Date: {{pexpd}} ({1}) {{/pexpd}}
Description: {{desc}} {{/desc}}
Password Cannot Expire: {{passcantexp}} {{/passcantexp}}
Password Object: {{passobj}} {{/passobj}}
Safe: {{safe}} {{/safe}}
Device User Name: {{dun}} {{/dun}}
System: {{system}} Venafi {{/system}}
'''


def send_email_to_generate_ticket(smtp_server_domain, smtp_server_port, from_addr, password, to_addr, csv_file_path):
    csv_row_values = read_csv_file(csv_file_path)
    counter = 0
    print('Sending emails...')
    for item in csv_row_values:
        account_name, exp_date = item
        counter += 1
        email_data = email_content_template.format(account_name, exp_date)
        send_email(smtp_server_domain, smtp_server_port, from_addr, password, to_addr, email_data)
    print('Complete!')
    print(f'Total Emails Sent: {counter}')


def send_email(smtp_server_domain, smtp_server_port, from_addr, password, to_addr, email_data):
    context = ssl.create_default_context()
    try:
        with smtplib.SMTP_SSL(smtp_server_domain, smtp_server_port, context=context,) as server:
            server.login(from_addr, password)
            server.sendmail(from_addr, to_addr, email_data)
    except Exception as e:
        print(f'Sending email Failed: {e}')


def read_csv_file(csv_file_path):
    csv_rows_list = []
    try:
        with open(csv_file_path, 'r') as csv_file:
            csv_reader = csv.reader(csv_file)
            for i in range(2): next(csv_reader)
            for item in csv_reader:
                values = (item[0], datetime.strptime(item[6],'%m/%d/%Y').date())
                csv_rows_list.append(values)
            return csv_rows_list

    except FileNotFoundError:
        print(csv_file_path + " not found.")


if __name__ == '__main__':
    smtp_server_domain = 'smtp.host.com'
    smtp_server_port = 465
    from_addr = 'sender@email.com'
    password = datafile.password
    to_addr = 'receiver@email.com'
    csv_file_path = 'sample.csv'
    send_email_to_generate_ticket(smtp_server_domain, smtp_server_port, from_addr, password, to_addr, csv_file_path)
