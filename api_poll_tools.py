"""
Module api_poll_tools.py
"""
import sys
import time
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
    """
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
        return result
    except expected_exceptions:
        try_slowly.expected_exception_count += 1
        logging.warning(
            'try_slowly(): try_slowly expected exception')
        raise TrySlowlyExpectedException().with_traceback(sys.exc_info()[2])
    except:
        try_slowly.unexpected_exception_count += 1
        logging.error(
            'try_slowly(): try_slowly unexpected exception')
        raise TrySlowlyUnexpectedException().with_traceback(sys.exc_info()[2])
    finally:
        try_slowly.previous_timestamp = time.time()
        logging.debug(f'try_slowly.previous_timestamp {try_slowly.previous_timestamp}')
        logging.debug(f'try_slowly.expected_exception_count: {try_slowly.expected_exception_count}')
        logging.debug(f'try_slowly.unexpected_exception_count: '
                      f'{try_slowly.unexpected_exception_count}')
        logging.info(
            'try_slowly(): in \'finally:\'')
    logging.error('try_slowly(): should not be here unless testing')
    #try_slowly.previous_timestamp = time.time() #just in case the one expects the Unexpected
    #raise UnexpectedException

def try_n_times( function, parameters,  n=3, expected_exceptions='',
                 seconds=1, try_slowly_seconds=1):
    """ Try a function up to n times (default 3)

        Return result on first success
        Try again with expected_exceptions after sleep.
        eg "expected_exceptions=(NameError , TimeoutError)
        otherwise raise exception
    """
    try_it_times = n
    for try_it in range(1,try_it_times):
        #try_error = True
        try:
            # print(x) #test exception name error (when x is not defined)
            result = try_slowly(function, parameters,
                                expected_exceptions, seconds=try_slowly_seconds )
            #try_error = False
            return result
        # FIXME except TrySlowlyUnexpectedException: #depends on what is using this...
        except (UnexpectedException, TrySlowlyUnexpectedException):
            logging.warning(
                f'try_n_times(): try {try_it} expected exception, sleeping {seconds} s')
            if try_it < try_it_times:
                time.sleep(seconds)
        except expected_exceptions:
            logging.warning(
                f'try_n_times(): try {try_it} expected exception, sleeping {seconds} s')
            if try_it < try_it_times:
                time.sleep(seconds)
    raise TooManyRetries

def tests():
    """some tests"""
    logging.basicConfig(level=logging.DEBUG)
    testing_test_times_straddle_minute()
    tests_try_slowly()
    tests_try_n_times()

def testing_test_times_straddle_minute():
    """test test_times_straddle_minute"""
    #test test_times_straddle_minute
    time_15m41s = 941
    time_16m41s = 1001
    test16after = 16 # True
    test10after = 10 # False
    list_true = [20, 0 ,59, test16after] # true
    list_false = [1, 2, 4, 55] #False
    list_empty = []
    broken1 = [1, 60, 61, 1000] # some out of range
    broken2 = "2"
    broken3 = [1, 2, 'wer']
    broken4 = False
    tests = [test16after,test10after ,list_true,list_false, list_empty,
             broken1, broken2, broken3, broken4 ]
    print("*** test_times_straddle_minute")
    for test in tests:
        print(f'testing: {test} ')
        try:
            x = test_times_straddle_minute(time_16m41s,time_15m41s, test )
            print(f'result {x}')
        except:
            print('Exception error:') # {sys.exc_info()[0]}')
        print("***")

def tests_try_slowly():
    """test try_slowly"""
    #test try_slowly
    print("*** test try_slowly")
    #print(try_slowly.expected_exception_count)
    print("*** test that should work")
    result = try_slowly( print, 'x' )
    print(f'returned: {result}')
    print('below exception counts should be 0')
    print(f'try_slowly.expected_exception_count: {try_slowly.expected_exception_count}')
    print(f'try_slowly.unexpected_exception_count: {try_slowly.unexpected_exception_count}')
    print("*** test that should be expected")
    result2= result3 = None
    try:
        result2 = try_slowly( open , '/nonexisting_asdf' , expected_exceptions = FileNotFoundError)
    except TrySlowlyExpectedException:
        pass
    if result2 is not None:
        print(f'very strange... returned: {result2}')
    print("*** test that should be unexpected")
    try:
        result3 = try_slowly( open , '/nonexisting_asdf')
    except TrySlowlyExpectedException:
        print("expected")
    except TrySlowlyUnexpectedException:
        print("unexpected")
    except:
        print("completely unexpected")
    if result3 is not None:
        print(f'very strange... returned: {result3}')
    print('below exception counts should be 1')
    print(f'try_slowly.expected_exception_count: {try_slowly.expected_exception_count}')
    print(f'try_slowly.unexpected_exception_count: {try_slowly.unexpected_exception_count}')
    #TODO: test single exception and set of exceptions
    #TODO: better errors

def tests_try_n_times():
    """test try_n_times"""
    #TODO
    print("TODO: test try_n_times")
