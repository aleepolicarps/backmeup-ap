from datetime import datetime
import dropbox
import json
import logging
import os
import time

current_year = datetime.now().year
current_month = datetime.now().month
logging.basicConfig(filename='logs/%d-%d.log' % (current_month, current_year),level=logging.DEBUG, format='%(asctime)s %(message)s')

config = json.load(open('config.json'))
logging.info('Config for %s loaded.' % config['app_name'])

file_path = '%s_temp.gz' % config['database']
os.popen("mysqldump -u %s --password='%s' -h %s -e --opt -c %s | gzip -c > %s" %
    (config['user'], config['password'], config['host'], config['database'], file_path))

logging.info('File saved to %s' % file_path)

dbx = dropbox.Dropbox(config['access_token']);
logging.info('Dropbox authentication successful.')

timestamp = time.strftime('%Y-%m-%d-%I:%M')
dropbox_path = '/%s/%s_%s.gz' % (config['app_name'], config['database'], timestamp)
with open(file_path, 'r') as f:
    dbx.files_upload(f.read(), dropbox_path)

dropbox_folder = 'https://www.dropbox.com/home/Apps/rk_backup';
logging.info('Backup uploaded to dropbox! -- %s%s' % (dropbox_folder, dropbox_path))
