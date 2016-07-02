#!/usr/bin/env python
# -*- coding: utf-8 -*-
import logging
import os, time, sys
import yaml, json
import requests

EXIT_CODE=0
HOSTNAME = os.uname()[1]
CONFIG_FILE = "/etc/stats.yaml"
DATEFMT = '%Y-%m-%d %H:%M:%S'
LOG_FMT = "%(asctime)s %(levelname)-8.8s: %(message)s"
DATA_DIR = '/var/stats_data'
CONFIG = None

def setLogLevel (logLevel):
    if logLevel == 0:
        logging.basicConfig(format = LOG_FMT, level = logging.WARNING, datefmt = DATEFMT)
    elif logLevel == 1:
        logging.basicConfig(format = LOG_FMT, level = logging.INFO, datefmt = DATEFMT)        
    elif logLevel == 2:
        logging.basicConfig(format = LOG_FMT, level = logging.DEBUG, datefmt = DATEFMT)
    elif logLevel == 3:
        logging.basicConfig(format = LOG_FMT, level = logging.DEBUG, datefmt = DATEFMT)

def process_exception(e, critical = False):
    global EXIT_CODE
    EXIT_CODE+=1
    if critical:
        logging.critical(e)
        sys.exit(EXIT_CODE)

    logging.warning(e)

def parse_config():
    global CONFIG

    with open(CONFIG_FILE) as config_file:
        try:
            CONFIG = yaml.load(config_file)
        except Exception as e:
            process_exception(e, critical = True)

def now():
    return time.strftime(DATEFMT)

def b_to_mb(val):
    return float(val) / 2**20

def kb_to_mb(val):
    return float(val) / 2**10

def s_to_milliseconds(val):
    return int(val * 10**3)

def send_stats(stats={}):
    json_data = json.dumps({
            "apiKey":  CONFIG['api_key'],
            "records": stats
            })
    date = now()
    logging.info ("API request date: %s json %s", date, json_data, )

    resp = requests.post(CONFIG['api_url'], data = {'json': json_data})
    if resp.status_code != 200:
        process_exception("API responded with non 200 status. code: %s body: %s" %(resp.status_code, resp.text), critical = True)

    if json.loads(resp.content)['status'] == 'ERROR':
        process_exception("Error while sending data status: %(status)s errorDetails: %(errorDetails)s" % resp.json(), critical = True)

def check_config_sections(sections=[], critical=False):
    section=CONFIG
    for section_name in sections:
        section = section.get(section_name, None)
        if not section:
            process_exception("config error: no section %s." % section_name, critical = critical)
            return False

    return True

if not os.path.exists(DATA_DIR):
    try:
        os.makedirs(DATA_DIR)
    except OSError as e:
        process_exception(e, critical = True)

if not os.path.isdir(DATA_DIR):
    process_exception("%s is not directory" % DATA_DIR, critical = True)
