"""
api_poll_zabbix.py

ZabbixSender related parts

"""
import socket #for errors from ZabbixSender
import logging #ZabbixSender
from pyzabbix import ZabbixMetric, ZabbixSender, ZabbixResponse


from datetime import datetime

import sys
import traceback


# Count data recieved from zabbix server
zabbix_server_processed = 0 #
zabbix_server_failed = 0    # Zabbix server did not accept (wrong key, wrong type of data)
zabbix_server_total = 0     #
zabbix_send_failed_time = 0

def send_zabbix_packet(zabbix_packet , zabbix_sender_setting):
    """Sends zabbix packet to server(s) and returns a tuple
       bool True if successful False if Failed
       ZabbixSender response
    """
    sending_status = False
    zasender = ZabbixSender(zabbix_sender_setting)
    global epoch_time, zabbix_server_processed, zabbix_server_failed, zabbix_server_total
    try:
        zaserver_response = zasender.send(zabbix_packet)
        zabbix_packet = [] #it's sent now ok to erase
        zabbix_send_failed_time = 0 #in case it failed earlier
        zabbix_server_processed += zaserver_response.processed
        zabbix_server_failed += zaserver_response.failed
        zabbix_server_total += zaserver_response.total
        logging.debug(f'Zabbix Sender succeeded\n{zaserver_response}')
        sending_status = True
    except (socket.timeout, socket.error, ConnectionRefusedError ) as error_msg:
        logging.error('Zabbix Sender Failed to send some or all: {0}'.format(error_msg))
        # if sending fails, Zabbix server may be restarting or rebooting.
        # maybe it gets sent after the next polling attempt.
        # if zabbix_packet is more than x items or if failure time
        # greater than x save to disk
        # this has been an idea for a while but not done yet 20221012...
        # For now just log it
        traceback.print_tb(sys.exc_info()[2])
##        
##        if zabbix_send_failed_time == 0 : #first fail (after successful send or save)
##            zabbix_send_failed_time = epoch_time
##            # could set defaults for failed item sending timeout and count.
##        if  ( epoch_time - zabbix_send_failed_time > zabbix_send_failed_time_max #900
##            or len(zabbix_packet) > zabbix_send_failed_items_max #500
##            ):
##            logging.error(f'Zabbix Sender failed {epoch_time-zabbix_send_failed_time} seconds ago')
##            logging.error(f'{len(zabbix_packet)} items pending.\nWill try to dump them to disk')
##            save_zabbix_packet_to_disk(zabbix_packet)
##            zabbix_send_failed_time = epoch_time
##            zabbix_packet = [] #it's saved now ok to erase
##            # clear keys from lastchanged so fresh values are collected to be sent next time
##            lastchanged={}
    except AttributeError:
        logging.error(f'send_zabbix_packet():AttributeError: Probably the zabbix server returned '
                      'something strange like an empty response header')
        traceback.print_tb(sys.exc_info()[2])
    except:
        logging.error(f'send_zabbix_packet(): Unexpected error: {sys.exc_info()[0]}')
        raise
    return sending_status,zaserver_response
def zabbix_send_result_string( result ):
    """
    Returns a result string (zabbix server response) to print or log the
    result returned by ZabbixSender
    """
    return 'zabbix_send_result[' \
                    f'processed: {result.processed} , ' \
                    f'failed: {result.failed} , ' \
                    f'total: {result.total}]'
