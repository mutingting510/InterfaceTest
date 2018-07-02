#!/usr/bin/env Python
# coding=utf-8

import time
testTime = time.time()
print(testTime)
day120 = 121*86400
timetmp = testTime - day120
timeArray = time.localtime(timetmp)
otherStyleTime = time.strftime("%Y-%m-%d %H:%M:%S", timeArray)
timestamp = time.mktime(timeArray)
print ("120天之前的时间为：{},      120天之前的时间戳为：{}".format(otherStyleTime,timestamp))