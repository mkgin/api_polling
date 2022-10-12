# BUGS.md

List of stuff to look into..., strange but have seen it before.
- Zabbix trappers may have been too busy.
Nothing seen in logs but looking at zabbix server processes.
- preprocessing queue and internal housekeeper processes were busy near the time of the error
- over the longer term, discovery processes busy
- it appears the data did not get saved to zabbix
- instead of the normal JSON response, it returned b'' (Empty response header)


```
1665591773.778963 DEBUG:pyzabbix.sender:Sending data to ('ZABBIX_SERVER', 10051)
1665591782.708861 DEBUG:pyzabbix.sender:Response header: b''
1665591782.708954 DEBUG:pyzabbix.sender:Zabbix return not valid response.
1665591782.708978 DEBUG:pyzabbix.sender:('z4p.private', 10051) response: False
1665591782.709124 ERROR:root:Unexpected error: <class 'AttributeError'>
1665591782.709447 Traceback (most recent call last):
1665591782.709502   File "/home/username/git/pytradfri_zabbix/pytradfri_to_zabbix.py", line 327, in <module>
1665591782.709695     main()
1665591782.709750   File "/home/username/git/pytradfri_zabbix/pytradfri_to_zabbix.py", line 266, in main
1665591782.709774     zabbix_send_result = send_zabbix_packet(ivlist, zabbix_config)
1665591782.709805   File "api_polling/api_poll_zabbix.py", line 38, in send_zabbix_packet
1665591782.709884     zaserver_response = zasender.send(zabbix_packet)
1665591782.709927   File "/home/username/.local/lib/python3.9/site-packages/pyzabbix/sender.py", line 443, in send
1665591782.710027     result.parse(self._chunk_send(metrics[m:m + self.chunk_size]))
1665591782.710071   File "/home/username/.local/lib/python3.9/site-packages/pyzabbix/sender.py", line 67, in parse
1665591782.710095     info = response.get('info')
```
