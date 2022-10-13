"""
Module api_poll_tools.py
"""
import sys
import time
import traceback
from calendar import timegm
import logging
class UnexpectedException(BaseException):
    """UnexpectedException"""
    pass
class TrySlowlyExpectedException(BaseException):
    """UnexpectedException"""
    pass
class TrySlowlyUnexpectedException(BaseException):
    """UnexpectedException"""
    pass
class TrySlowlyEmptyExpectedException(BaseException):
    """expectedexception is default, used as a filler to
       skip the First Exception test and move on to
       TrySlowlyUnexpectedException
    """
    pass
class TooManyRetries(BaseException):
    """TooManyRetries"""
    pass
def test_times_straddle_minute( time_1,time_2, minutes ):
    """
    Tests if start of a minute or list of minutes is between time1 and time2.

    minute can be an int or list of minutes and it is assumed to be the start
    of the minute (seconds is 0)
    time_1 and time_2 are in seconds since the start of epoch_time
    and can be any order.
    """
    if type(minutes) is int:
        minutes = [minutes]
    # calculate the start of the minute for within last hour
    this_minute = list(time.gmtime(max(time_1,time_2)))
    this_minute[5] = 0 # set seconds to 0
    for minute in minutes:
        this_minute[4] = minute # set minute
        # convert back to timestamp as it is easier to move back 1 hour
        this_minute_timestamp = timegm(time.struct_time(tuple(this_minute)))
        # check if minute is after the larger timestamp
        # if so move back 1 hour
        if this_minute_timestamp > max(time_1,time_2):
            this_minute_timestamp -= 3600
        if ( this_minute_timestamp <= max(time_1,time_2) and \
             this_minute_timestamp >= min(time_1,time_2)):
            return True
    return False

def try_slowly(function, parameters, expected_exceptions=TrySlowlyEmptyExpectedException,
               seconds = 1):
    """
        Try a function but sleep if this has been called before
        seconds since try_slowly was last called

        expected_exceptions can be an exception or tuple of exceptions
        try_slowly.success is True on success False on failure
    """
    try_slowly.success = False
    if not hasattr(try_slowly,'expected_exception_count'):
        try_slowly.expected_exception_count = 0
    if not hasattr(try_slowly,'unexpected_exception_count'):
        try_slowly.unexpected_exception_count = 0
    current_timestamp = time.time()
    if not hasattr(try_slowly,'previous_timestamp'):
        try_slowly.previous_timestamp = current_timestamp - seconds
        logging.info(f'try_slowly: first time: setting previous_timestamp now - {seconds} s')
    logging.debug(f'current_timestamp: {current_timestamp}')
    logging.debug(f'try_slowly.previous_timestamp {try_slowly.previous_timestamp}')
    logging.debug(f'try_slowly: expected_exceptions: {expected_exceptions}')
    interval = current_timestamp - try_slowly.previous_timestamp
    logging.debug(f'try_slowly: interval: {interval} s')
    if interval < seconds:
        logging.info(f'try_slowly: sleeping for {seconds-interval} s')
        time.sleep(seconds-interval)
    try:
        result = function(parameters)
        try_slowly.success = True
        return result
    except expected_exceptions:
        try_slowly.expected_exception_count += 1
        logging.warning('try_slowly(): try_slowly expected exception')
        traceback.print_tb(sys.exc_info()[2])
        raise TrySlowlyExpectedException
    except:
        try_slowly.unexpected_exception_count += 1
        logging.error('try_slowly(): try_slowly unexpected exception')
        traceback.print_tb(sys.exc_info()[2])
        raise TrySlowlyUnexpectedException
    finally:
        try_slowly.previous_timestamp = time.time()
        logging.info('try_slowly(): in \'finally:\'')
        logging.debug(f'try_slowly.previous_timestamp {try_slowly.previous_timestamp}')
        logging.debug(f'try_slowly.expected_exception_count: {try_slowly.expected_exception_count}')
        logging.debug(f'try_slowly.unexpected_exception_count: '
                      f'{try_slowly.unexpected_exception_count}')
    logging.error('try_slowly(): should not be here')


def try_n_times( function, parameters,  n=3, expected_exceptions='',
                 seconds=1, try_slowly_seconds=1):
    """ Try a function up to n times (default 3)

        Return result on first success
        Try again with expected_exceptions after sleep.
        eg "expected_exceptions=(NameError , TimeoutError)
        otherwise raise exception

        try_n_times.success is True on success False on failure
    """
    try_n_times.success = False
    try_it_times = n
    for try_it in range(1,try_it_times+1):
        #try_error = True
        logging.info(f'try_n_times(): try # {try_it}/{try_it_times}')
        try:
            result = try_slowly(function, parameters,
                                expected_exceptions, seconds=try_slowly_seconds )
            try_n_times.success = True
            return result
        except ( (TrySlowlyExpectedException,) + (expected_exceptions, )):
            logging.info(
                f'try_n_times(): expected exception (in try_slowly)\n sleeping {seconds} s')
            if try_it <= try_it_times:
                time.sleep(seconds)
            else:
                raise TooManyRetries
        except TrySlowlyUnexpectedException:
            logging.error(
                f'try_n_times(): **Unexpected exception** (in try_slowly), sleeping {seconds} s')
            logging.error(sys.exc_info())
            if try_it <= try_it_times:
                time.sleep(seconds)
            else:
                raise TooManyRetries
    raise TooManyRetries

