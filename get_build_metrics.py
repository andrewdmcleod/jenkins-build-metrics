#!/usr/bin/python3

# Generate metrics from builds for prometheus / grafana

import urllib.request, json , os, time, keyboard, sys, re, operator
from collections import OrderedDict
from shutil import copyfile
import time
import copy

def get_build_metrics():
    charm_avg_str = ''
    charm_high_str = ''
    charm_low_str = ''

    os.environ['http_proxy'] = ''
    
    class E(Exception):
        pass
    
    #test_name = "test_charm_pipeline_func_full"
    #test_name = "test_charm_func_smoke"
    
    tests = [
    'test_charm_func_full',
    'test_charm_func_smoke',
    'test_charm_lint',
    'test_charm_unit',
    'test_charm_single'
    ]
    
    debug = False
    
    def debugprint(str):
        if debug == True:
            print(str) 
       
    for test in tests:
        with urllib.request.urlopen("http://osci:8080/job/{}/api/json".format(test)) as jsonurl:
            charms = {}
            jsdata = json.loads(jsonurl.read().decode())
            for build in jsdata['builds']:
                with urllib.request.urlopen("{}/api/json/".format(build['url'])) as jsonurl2:
                    build_data = json.loads(jsonurl2.read().decode())
                    #for name in build_data.items():
                    #	print(name)
                    #print(build_data['fullDisplayName'])
                    #print(build_data['fullDisplayName'].split(" ")[2])
                    try:
                        charm_name = build_data['fullDisplayName'].split()[2].split("/")[1]
                        charm_name = charm_name + "_" +build_data['fullDisplayName'].split()[3]
                        debugprint("TRY: {}".format(build_data['fullDisplayName']))
                    except:
                        charm_name = build_data['fullDisplayName'].split()[2]
                        charm_name = charm_name + "_" + build_data['fullDisplayName'].split()[3]
                        debugprint("EXCEPT: {}".format(build_data['fullDisplayName']))
                    charm_name = charm_name.replace("-", "_")
                    if not build_data['building']:
                        try:
                            charms[charm_name].append(build_data['duration'])
                        except:
                            charms[charm_name] = [build_data['duration']]
                            #print("excepting")
                            pass
                        print(charm_name, build_data['duration'], build_data['building'])
                    #for k, v in build_data.items():
                    #    print(k)
            for charm, values in charms.items():
                charm_avg = (sum(values) / len(values))
                charm_high = max(values)
                charm_low = min(values) 
                charm_avg_str = charm_avg_str + ("{}-{}-avg {}\n".format(test, charm, charm_avg))
                debugprint(charm_avg)
                charm_high_str = charm_high_str + ("{}-{}-high {}\n".format(test, charm, charm_high))
                debugprint(charm_high)
                charm_low_str = charm_low_str + ("{}-{}-low {}\n".format(test, charm, charm_low))
                debugprint(charm_low)
     
    return charm_avg_str, charm_high_str, charm_low_str

#avg, high, low = get_build_metrics()

#print(avg, high, low)
