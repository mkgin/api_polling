"""
test_api_poll_tools.py
"""
# import os
import sys
import logging

# folder = os.path.dirname(os.path.abspath(__file__))
# sys.path.insert(0, os.path.normpath(f"{folder}/.."))
sys.path.append('..')
# pylint: disable=wrong-import-position
# pylint: disable=undefined-variable
from api_poll_tools import try_n_times, try_slowly, test_times_straddle_minute,\
    TrySlowlyExpectedException, TrySlowlyUnexpectedException, TooManyRetries

def tests():
    """some tests"""
    logging.basicConfig(level=logging.DEBUG)
    testing_test_times_straddle_minute()
    tests_try_slowly()
    tests_try_n_times()

def testing_test_times_straddle_minute():
    """test test_times_straddle_minute"""
    # test test_times_straddle_minute
    time_15m41s = 941
    time_16m41s = 1001
    test16after = 16  # True
    test10after = 10  # False
    list_true = [20, 0, 59, test16after]  # true
    list_false = [1, 2, 4, 55]  # False
    list_empty = []
    broken1 = [1, 60, 61, 1000]  # some out of range
    broken2 = "2"
    broken3 = [1, 2, 'wer']
    broken4 = False
    time_tests = [test16after, test10after, list_true, list_false, list_empty,
                  broken1, broken2, broken3, broken4]
    print("*** test_times_straddle_minute")
    for test in time_tests:
        print(f'** testing: {test} ')
        try:
            x = test_times_straddle_minute(time_16m41s, time_15m41s, test)
            print(f'result {x}')
        except TypeError:
            print('Exception error:') # {sys.exc_info()[0]}')
        except:  # other    
            raise
        print("***")

def tests_try_slowly():
    """test try_slowly"""
    #test try_slowly
    print("*** test try_slowly")
    #print(try_slowly.expected_exception_count)
    print("*** test that should work")
    result = try_slowly(print, 'x' )
    print(f'returned: {result}')
    print('below exception counts should be 0')
    print(f'try_slowly.expected_exception_count: {try_slowly.expected_exception_count}')
    print(f'try_slowly.unexpected_exception_count: {try_slowly.unexpected_exception_count}')
    print("*** test that should be expected")
    result2 = result3 = None
    try:
        result2 = try_slowly(open , '/nonexisting_asdf' , expected_exceptions = FileNotFoundError)
    except TrySlowlyExpectedException:
        pass
    if result2 is not None:
        print(f'very strange... returned: {result2}')
    print("*** test that should be unexpected")
    try:
        result3 = try_slowly(open , '/nonexisting_asdf')
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
    #TODO: think about combining try_n_times and try_slowly tests in one function

def tests_try_n_times():
    """test try_n_times"""
    print("*** test try_n_times")
    result = try_n_times(print, 'x' )
    try:
        result2 = try_n_times(open , '/nonexisting_asdf' , expected_exceptions = FileNotFoundError)
    except (TooManyRetries, TrySlowlyUnexpectedException):
        pass
    try:
        result3 = try_slowly(open , '/nonexisting_asdf')
    # except (TooManyRetries, TrySlowlyUnexpectedException):
    except TrySlowlyUnexpectedException:
        pass

tests()
