# API Polling

Tools for polling an API and sending data to monitoring (primarily Zabbix trapper items)

* values are stored and can be configured to be reported (sent) as follows:
    * each time polled
    * reported only when changed  (can report value from last polling interval too)
    * or after certain intervals

* uses the following libraries
	* https://github.com/adubkov/py-zabbix
        * https://py-zabbix.readthedocs.io/en/latest/sender.html

## Current status

* Testing with python 3.9

* Handles connection problems to zabbix moderately well
* api endpoints, keys, polling interval and sending strategies are configured by a YAML
  file generates a dictionary with information about how to handle each key

* Better examples eventually. For now, see https://github.com/mkgin/huawei_LTE_API_Zabbix_Sender

## Configuration

* =config.yml= place for default stuff, ideally safe to be on a public repo
* =own_config.yml= writes over variables in =config.yml=
* =api_poll_config:= in the above config files sets the location of the api polling configuration
  * api polling configuration is defined in =api_design.yml=


### IDEAS / TODO,
- handle parsed arguments
- zabbix related
  - auto generate a simple zabbix template?
    - items suitable for populating zabbix inventory
  - discovery
