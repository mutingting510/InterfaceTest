# -*- coding: utf-8 -*-

from jpype import *
import os.path
class DESCrypt():
    def desEncry(self,data):
        # data = '{"dataParams": {"phone": "17610827228 ", "password": "7ed651bbfd1387b5397c60fb32925845"},{"commonParams": {"os": "androd 7.0", "sourceType": "1", "channel": "360应用商城", "deviceCode": "5131as3dfasdf","version": "1.0.0", "token": "}'
        jarpath = 'E:\\common-1.0.0-SNAPSHOT.jar'
        if not isJVMStarted():
            startJVM(getDefaultJVMPath(), "-ea", "-Djava.class.path="+jarpath)
        Test = JClass("com.yingu.common.utils.DESCryptUtil")
        DEStest = Test.encryptBasedDes(data)
        # print(DEStest)
    #     shutdownJVM()
        return DEStest


    def desDecry(self,data):
        jarpath = 'E:\\common-1.0.0-SNAPSHOT.jar'
        if not isJVMStarted():
            startJVM(getDefaultJVMPath(), "-ea", "-Djava.class.path=" + jarpath)
        Test = JClass("com.yingu.common.utils.DESCryptUtil")
        DEStest = Test.decryptBasedDes(data)
        # print(DEStest)
        # shutdownJVM()
        return DEStest



# if __name__ == '__main__':
#     obj = DESCrypt()
#     obj.desEncry()
