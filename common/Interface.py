#!/usr/bin/env Python
# coding=utf-8


from Public.common.AEStest import *
# from Public.common.Accumulation_fund import *
import json
import time

class Interface():
    def __init__(self):
        pass


    def gettoken(self,phoneNum):
        try:
            url = 'https://puhui-env.yingu.com/ygph/api/client/login'
            data = '{"commonParams":{"deviceCode":"d38470fd8sahf3","sourceType":"3","version":"1.0.0","os":"null","channel":"H5","token":""},"dataParams":{"phone":'+phoneNum+',"password":"9cbf8a4dcb8e30682b927f352d6559a0"}}'
            jsondata = {'jsonParams': AESinterface.encrypt_oracle(AESinterface(),data)}
            # time.sleep(4)
            re = requests.post(url=url, data=jsondata)
            time.sleep(5)
            ret = re.text
            result = AESinterface.decrypt_oralce(AESinterface(), ret)
            re1 = json.loads(result)
            if 'data' in re1:
                token = re1['data']['token']
                # print(token)
                return token
            else:
                print("服务器繁忙:", re1)
        except Exception as e:
            print("gettoken失败",e)


    def getUserInfo(self,phoneNum):
        url = 'https://puhui-env.yingu.com/ygph/api/client/getUserInfo'
        data = '{"commonParams":{"token":'+self.gettoken(phoneNum)+',"version":"1.0.0","deviceCode":"d38470fd8sahf3","sourceType":"3","os":"android.5.0","channel":"1"},"dataParams":{}}'
        jsondata = {'jsonParams': AESinterface.encrypt_oracle(AESinterface(), data)}
        # time.sleep(4)
        re = requests.post(url=url, data=jsondata)
        time.sleep(5)
        ret = re.text
        result = AESinterface.decrypt_oralce(AESinterface(), ret)
        re1 = json.loads(result)
        print(re1)


if __name__ == '__main__':
    obj = Interface()
    obj.getUserInfo('18600517988')









