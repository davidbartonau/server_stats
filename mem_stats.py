#!/usr/bin/env python
# -*- coding: utf-8 -*-

import psutil
import common


# Returns real memory and swap memory in MB
def mem_stats():
    phymem = psutil.phymem_usage()
    virtmem = psutil.virtmem_usage()
    real_used = common.b_to_mb(phymem.used)
    swap_used = common.b_to_mb(virtmem.used)

    date = common.now()
    print "MEM date: %s used: %s swap_used: %s" % (date, real_used, swap_used, )

    mem_stats = [
            {"date": date, "t": "MEM-USED", "d1": common.HOSTNAME, "V": real_used},
            {"date": date, "t": "MEM-SWAP", "d1": common.HOSTNAME, "V": swap_used},
        ]

    return mem_stats



