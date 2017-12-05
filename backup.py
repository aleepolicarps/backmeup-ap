from datetime import datetime
import json
import logging
import urllib2
import os
import time

# Sets logger for current Month and Year
current_year = datetime.now().year
current_month = datetime.now().month
logging.basicConfig(filename='logs/%d-%d.log' % (current_month, current_year),level=logging.DEBUG, format='%(asctime)s %(message)s')

# Load config files for app
config = json.load(open('config.json'))
logging.info('Config for %s loaded.' % config['app_name'])

# compress mysql dump to .gz and stores in a temporary file
file_path = '%s_temp.gz' % config['database']
os.popen("mysqldump -u %s --password='%s' -h %s -e --opt -c %s | gzip -c > %s" %
    (config['user'], config['password'], config['host'], config['database'], file_path))
logging.info('File saved to %s' % file_path)

# get binary of saved file
with open(file_path, 'r') as f:
    data = f.read()

# sets path in Dropbox
timestamp = time.strftime('%Y-%m-%d-%I:%M')
dropbox_path = '/%s/%s/%s_%s.gz' % (config['folder_name'], config['app_name'], config['database'], timestamp)

dropbox_params = {
    'path': dropbox_path,
    'mode': 'add',
    'autorename': False,
    'mute': False
}

headers = {
    'Authorization': 'Bearer %s' % config['access_token'],
    'Dropbox-API-Arg': json.dumps(dropbox_params),
    'Content-Type': 'application/octet-stream'
}

# reference: https://www.dropbox.com/developers/documentation/http/documentation#files-upload
try:
    request = urllib2.Request('https://content.dropboxapi.com/2/files/upload', data, headers)
    f = urllib2.urlopen(request)
    response = f.read()
    logging.info('Upload successful!')
    logging.info(response)
except:
    logging.error('Upload unsuccessful!')
finally:
    f.close()
