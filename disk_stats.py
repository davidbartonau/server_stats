#!/usr/bin/env python
# -*- coding: utf-8 -*-

import psutil
import os, subprocess
import common


# Returns used space for mount points from config in MB
def disks_used_stats():
    usages=[]
    if not common.check_config_sections(['disks', 'mount_points']):
        return usages

    for mount_point in common.config['disks']['mount_points']:
        try:
            fs_stats = psutil.disk_usage(mount_point)
        except OSError as e:
            common.process_exception(e)
            continue
        used = common.b_to_mb(fs_stats.used)

        date = common.now()
        print "DISK date: %s mount_point: %s used: %s" % (date, mount_point, used, )
        usages.append({"date": date, "t":"DISK-USAGE", "d1": common.HOSTNAME, "d2": mount_point, "V":used})

    return usages


# Returns disk blocks read and written
def disk_io_stats():
    io_perdev = []
    if not common.check_config_sections(['disks', 'block_devs']):
        return io_perdev

    counters = psutil.disk_io_counters(perdisk=True)
    for dev in common.config['disks']['block_devs']:
        counter = counters.get(dev, None)
        if not counter:
            common.process_exception('cannot find counters for block device %s. skip..' % dev)
            continue

        date = common.now()
        print "DISK date: %s block_dev: %s reads: %s writes: %s" % (date, dev, counter.read_count, counter.write_count, )
        io_perdev.extend([
               {"date": date, "t": "DISK-READS", "d1": common.HOSTNAME, "d2": dev, "V": counter.read_count},
               {"date": date, "t": "DISK-WRITES", "d1": common.HOSTNAME, "d2": dev, "V": counter.write_count},
           ])

    return io_perdev


# Returns size of directory in MB
def disk_dirs_size():
    sizes = []
    if not common.check_config_sections(['disks', 'dirs_size']):
        return sizes

    for directory in common.config['disks']['dirs_size']:
        if not os.path.exists(directory):
            common.process_exception("%s is not exists. skip..." % directory )

        cmd="du -s %s" % directory
        size=subprocess.Popen([cmd], stdout=subprocess.PIPE, shell=True).\
                communicate()[0].split()[0]
        size = common.kb_to_mb(size)
        date = common.now()
        print "DSIZE date: %s directory: %s size: %s" % (date, directory, size, )
        sizes.append({"date": date, "t":"DSIZE", "d1": common.HOSTNAME, "d2": directory, "V":size})

    return sizes

