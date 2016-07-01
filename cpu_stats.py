#!/usr/bin/env python
# -*- coding: utf-8 -*-

import psutil
import common


# Returns iowait and user+sus times in milliseconds
def cpu_stats():
    cpu_times = psutil.cpu_times()
    user_system = common.s_to_milliseconds(cpu_times.user + cpu_times.system)
    iowait = common.s_to_milliseconds(cpu_times.iowait)

    date = common.now()
    print "CPU date: %s total: %s iowait: %s" % (date, user_system, iowait, )
    cpu_times = [
            {"date": date, "t": "CPU-IOWAIT", "d1": common.HOSTNAME, "V": iowait},
            {"date": date, "t": "CPU-TOTAL",  "d1": common.HOSTNAME, "V": user_system},
        ]

    return cpu_times



