#!/usr/bin/env python
# -*- coding: utf-8 -*-

import psutil
import common
import logging


# Returns MB sent and received.
def network_stats():
    network_bytes = []
    if not common.check_config_sections(['networking', 'interfaces']):
        return network_bytes

    counters = psutil.network_io_counters(pernic=True)
    for interface in common.CONFIG['networking']['interfaces']:
        counter = counters.get(interface, None)
        if not counter:
            common.process_exception('cannot find counters for interface %s. skip..' % interface)
            continue

        date = common.now()
        mb_rcv = common.b_to_mb(counter.bytes_recv)
        mb_sent = common.b_to_mb(counter.bytes_sent)

        logging.info ("NET date: %s interface: %s recv: %s sent: %s", date, interface, mb_rcv, mb_sent, )
        network_bytes.extend([
                {"date": date, "t": "NET-RCV", "d1": common.HOSTNAME, "d2": interface, "V": mb_rcv},
                {"date": date, "t": "NET-SENT", "d1": common.HOSTNAME, "d2": interface, "V": mb_sent},
            ])

    return network_bytes



