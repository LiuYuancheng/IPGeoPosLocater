#!/usr/bin/python
#-----------------------------------------------------------------------------
# Name:        geoLRun.py
#
# Purpose:     This module is speed test API to get: 
#               1 - Real time upload/download speed & latency
#               2 - Network packet inspection (based on data extracted via wireshark)
#               3 - IP addresses of machines that are directly connected to our gateways
#               4 - Location of our gateways
# Author:      Yuancheng Liu
#
# Created:     2019/11/07
# Copyright:   YC @ Singtel Cyber Security Research & Development Laboratory
# License:     YC
#-----------------------------------------------------------------------------

import speedtest

servers = []
# If you want to test against a specific server
# servers = [1234]

threads = None
# If you want to use a single threaded test
# threads = 1

s = speedtest.Speedtest()
s.get_servers(servers)
s.get_best_server()
s.download(threads=threads)
s.upload(threads=threads)
s.results.share()

results_dict = s.results.dict()
print(results_dict)