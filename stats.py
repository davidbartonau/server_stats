#!/usr/bin/env python
# -*- coding: utf-8 -*-

import argparse
import common
import disk_stats
import cpu_stats
import mem_stats
import network_stats
import apache_logs_stats


def main():
    parser = argparse.ArgumentParser(description='Collect statistics from this server and POST json to a URL.')

    parser.add_argument ("--diskUsed", action='store_true',     help='Collect disk space used at mountpoints specified.')
    parser.add_argument ("--diskIO",   action='store_true',     help='Collect disk blocks read / written.')
    parser.add_argument ("--dirUsed",  action='store_true',     help='Collect space used in directories (slow).')
    parser.add_argument ("--cpu",      action='store_true',     help='Collect CPU utilisation.')
    parser.add_argument ("--memory",   action='store_true',     help='Collect memory usage.')
    parser.add_argument ("--network",  action='store_true',     help='Collect network usage.')
    parser.add_argument ("--apacheLog",  action='store_true',     help='Collect network usage.')
    parser.add_argument ("--verbosity",  nargs=1, type=int,  choices=range(0, 3),  help='Verbosty of logging, a positive number from 0 (nothing except errors) to 2 (a lot).  The default is 1.')

    args = parser.parse_args()
    common.setLogLevel (args.verbosity[0] if args.verbosity else 1)
    common.parse_config()

    stats = []

    if args.diskUsed:
        stats.extend (disk_stats.disks_used_stats())

    if args.diskIO:
        stats.extend (disk_stats.disk_io_stats())

    if args.dirUsed:
        stats.extend (disk_stats.disk_dirs_size())

    if args.cpu:
        stats.extend (cpu_stats.cpu_stats())

    if args.memory:
        stats.extend (mem_stats.mem_stats())

    if args.network:
        stats.extend (network_stats.network_stats())

    if args.apacheLog:
        stats.extend (apache_logs_stats.apache_stats())

    if len (stats) > 0:
        common.check_config_sections(['api_url',], critical=True)
        common.check_config_sections(['api_key',], critical=True)

        common.send_stats(stats)
    else:
        parser.print_help()

    exit(common.EXIT_CODE if common.EXIT_CODE < 256 else 255)

if __name__ == "__main__":
    main()
