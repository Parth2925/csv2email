import csv
import smtplib
from datetime import datetime
import logging
import os

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


def set_logging():
    log_filename = 'logs/csv2email-i' + datetime.now().strftime('%Y%m%d-%H%M%S') + '.log'
    os.makedirs(os.path.dirname(log_filename), exist_ok=True)
    logger = logging.getLogger('Main')
    logger.setLevel(logging.INFO)
    formatter = logging.Formatter('%(asctime)s|%(levelname)s|%(name)s|%(message)s')
    file_handler = logging.FileHandler(log_filename, mode="w", encoding=None, delay=False)
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)
    return logger


def send_email_to_generate_ticket(smtp_server_domain, from_addr, password, to_addr, csv_file_path):
    csv_row_values = read_csv_file(csv_file_path)
    counter = 0
    log.info('Sending emails...')
    for item in csv_row_values:
        account_name, exp_date = item
        email_data = email_content_template.format(account_name, exp_date)
        counter = send_email(smtp_server_domain, from_addr, password, to_addr, email_data, counter)
    log.info('Process completed!')
    log.info(f'Total Emails Sent: {counter}')


def send_email(smtp_server_domain, from_addr, password, to_addr, email_data, count):
    try:
        with smtplib.SMTP_SSL(smtp_server_domain, timeout=15) as server:
            server.login(from_addr, password)
            server.sendmail(from_addr, to_addr, email_data)
            count += 1
            return count
    except (smtplib.socket.error, smtplib.SMTPException) as e:
        log.error(f'Server connection Timeout: {e}')
    except Exception as e:
        log.error(f'Sending email Failed: {e}')


def read_csv_file(csv_file_path):
    csv_rows_list = []
    try:
        with open(csv_file_path, 'r') as csv_file:
            csv_reader = csv.reader(csv_file)
            for i in range(2): next(csv_reader)
            for item in csv_reader:
                values = (item[0], datetime.strptime(item[6], '%m/%d/%Y').date())
                csv_rows_list.append(values)
            log.info(f'{csv_file_path} Loaded.')
            return csv_rows_list

    except FileNotFoundError:
        log.error(csv_file_path + " not found.")


if __name__ == '__main__':
    log = set_logging()
    smtp_server_domain = 'smtp.email.com'
    from_addr = 'sender@email.com'
    password = ''
    to_addr = 'receiver@email.com'
    csv_file_path = 'sample.csv'
    send_email_to_generate_ticket(smtp_server_domain, from_addr, password, to_addr, csv_file_path)
