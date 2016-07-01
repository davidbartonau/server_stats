#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os, subprocess
import common
import disk_stats


def main():
    stats = disk_stats.disk_dirs_size()

    common.check_config_sections(['api_url',], critical=True)
    common.check_config_sections(['api_key',], critical=True)

    common.send_stats(stats)

    exit(common.EXIT_CODE if common.EXIT_CODE < 256 else 255)

if __name__ == "__main__":
    main()
