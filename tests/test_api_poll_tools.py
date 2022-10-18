"""
test_api_poll_tools.py
"""
# import os
import sys
import logging
import traceback
# folder = os.path.dirname(os.path.abspath(__file__))
# sys.path.insert(0, os.path.normpath(f"{folder}/.."))
sys.path.append('..')
# pylint: disable=wrong-import-position
# pylint: disable=undefined-variable
from api_poll_tools import try_n_times, try_slowly, test_times_straddle_minute,\
    TrySlowlyExpectedException, TrySlowlyUnexpectedException, TooManyRetries,\
    expected_exceptions_valid_tuple

class TestException1(BaseException):
    """Test Exception1"""
    pass
class TestException2(Exception):
    """Test Exception2"""
    pass

def raise_exception1(a):
    """a test"""
    raise TestException1

def raise_exception2(a):
    """a test"""
    raise TestException2

def raise_exception3(a):
    """a test"""
    raise TypeError

def tests():
    """some tests"""
    logging.basicConfig(level=logging.DEBUG)
    testing_test_times_straddle_minute()
    tests_try_slowly()
    tests_try_n_times()
    test_expected_exceptions_valid_tuple()

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
    #TODO: better errors
    #TODO: think about combining try_n_times and try_slowly tests in one function

def tests_try_n_times():
    """test try_n_times"""
    logging.basicConfig(level=logging.DEBUG)
    print("*** test try_n_times")
    result = try_n_times(print, 'x' )
    try:
        result2 = try_n_times(open , '/nonexisting_asdf' , expected_exceptions = FileNotFoundError)
    except (TooManyRetries, TrySlowlyUnexpectedException):
        pass
    try:
        result3 = try_n_times(open , '/nonexisting_asdf')
    except TooManyRetries:
        pass
    try:
        result3 = try_n_times(raise_exception1,'',expected_exceptions = (TestException1, TestException2))
    except TooManyRetries:
        pass
    try:
        result3 = try_n_times(raise_exception2,'',expected_exceptions = (TestException1, TestException2))
    except TooManyRetries:
        pass
    try:
        result3 = try_n_times(raise_exception3,'',expected_exceptions = (TestException1, TestException2))
    except TooManyRetries:
        pass
    try:
        result3 = try_n_times(raise_exception3,'',expected_exceptions = (None,) )
    except TooManyRetries:
        pass

def test_expected_exceptions_valid_tuple():
        expected_exceptions_list = [
            TestException1,
            (TestException1, TestException2),
            (TypeError, NameError, Exception),
            Exception, 'poop'
            ]
        for test in expected_exceptions_list:
            print(f'*** testing exception: {test} type:{type(test)}')
            try:
                result = expected_exceptions_valid_tuple(test)
                print(f'result: {result} type: {type(result)}\n')
            except:
                print(f'exception\n')
                traceback.print_tb(sys.exc_info()[2])
