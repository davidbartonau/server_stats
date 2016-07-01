#!/usr/bin/env python
# -*- coding: utf-8 -*-

import psutil
import common
import disk_stats
import cpu_stats
import mem_stats
import network_stats


def main():
    stats = disk_stats.disks_used_stats() + cpu_stats.cpu_stats() + mem_stats.mem_stats() + network_stats.network_stats() + disk_stats.disk_io_stats()

    common.check_config_sections(['api_url',], critical=True)
    common.check_config_sections(['api_key',], critical=True)

    common.send_stats(stats)
    exit(common.EXIT_CODE if common.EXIT_CODE < 256 else 255)

if __name__ == "__main__":
    main()
