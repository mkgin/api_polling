"""
test_api_poll_config.py
"""
import sys
import pprint # dont really need this except for main()
# pylint: disable=wrong-import-position
# pylint: disable=undefined-variable
sys.path.append('..')
from api_poll_config import *

def main():
    """Example use"""
    logging.basicConfig(level=logging.INFO)
    # Load api config from file
    api_config = yaml.safe_load(open('api_design_test.yml'))
    # get the config
    endpoint_key_config = load_api_endpoint_key_config(api_config)
    # pretty print it
    print('***** api_config[\'endpoint\']')
    pprint.pp(api_config['endpoint'])
    print('***** endpoint_key_config (dict)')
    pprint.pp(endpoint_key_config)
    print('*****')
    print(f'key_prefix: {load_key_prefix_config(api_config)}')
    print(f'polling_interval_minimum: {load_polling_interval_minimum(api_config)}')

main()
