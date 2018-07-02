#!/usr/bin/env Python
# coding=utf-8


from Public.common.AEStest import *
import os,logging
import json
import time
import xlrd
import requests
import re
log_file = os.path.join(os.getcwd(),'log/liveappapi.log')
log_format = '[%(asctime)s] [%(levelname)s] %(message)s'
logging.basicConfig(format=log_format,filename=log_file,filemode='w',level=logging.DEBUG)
console = logging.StreamHandler()
console.setLevel(logging.DEBUG)
formatter = logging.Formatter(log_format)
console.setFormatter(formatter)
logging.getLogger('').addHandler(console)
class Interface():

    def __init__(self):
        pass

    def runTest(self):
        ExcelFile = xlrd.open_workbook(r'D:\testCase.xlsx')
        table = ExcelFile.sheet_by_name('Sheet1')
        rows = table.nrows
        correlationDict = {}
        errorCase = []
        for i in range(2, rows):
            # if table.cell(i, 10).value.replace('\n', '').replace('\r', '') != 'Yes':
            #     continue
            num = str(int(table.cell(i, 0).value)).replace('\n', '').replace('\r', '')
            api_purpose = table.cell(i, 1).value.replace('\n', '').replace('\r', '')
            request_url = table.cell(i, 2).value.replace('\n', '').replace('\r', '')
            request_method = table.cell(i, 3).value.replace('\n', '').replace('\r', '')
            request_data_type = table.cell(i, 4).value.replace('\n', '').replace('\r', '')
            request_data = table.cell(i, 5).value.replace('\n', '').replace('\r', '')
            encryption = table.cell(i, 6).value.replace('\n', '').replace('\r', '')
            check_point = table.cell(i, 7).value
            correlation = table.cell(i, 8).value.replace('\n', '').replace('\r', '').split(';')

            if request_data_type == 'File':
                dataFile = request_data
                if os.path.exists(dataFile):
                    fopen = open(dataFile,encoding='utf-8')
                    # tmp = open('TestData/tmp.txt','w')
                    for line in fopen.readlines():
                        newStr = line.replace('\n','').replace('\t','').strip()
                        # tmp.write(newStr)
                        # request_data = tmp
                        request_data = newStr
                    fopen.close()

            for keyword in correlationDict:
                if request_data.find(keyword) > 0:
                    request_data = request_data.replace(keyword, str(correlationDict[keyword]))
                    # print(request_data)
            status,resp = self.interfaceTest(num,api_purpose,request_url,request_data,check_point)
            if status != 200:
                errorCase.append((num + ' ' + api_purpose, str(status), request_url, resp))
                continue
            for j in range(len(correlation)):
                param = correlation[j].split('=')
                if len(param) == 2:
                    if param[1] == '' or not re.search(r'^\[', param[1]) or not re.search(r'\]$', param[1]):
                        print(' ' + api_purpose + ' 关联参数设置有误，请检查[Correlation]字段参数格式是否正确！！！')
                        continue
                    value = resp
                    for key in param[1][1:-1].split(']['):
                        try:
                            temp = value[int(key)]
                            print(temp)
                        except:
                            try:
                                temp = value[key]
                            except:
                                break
                        value = temp
                    correlationDict[param[0]] = value
                    # print(value)

    def interfaceTest(self,num,api_purpose,request_url,request_data,check_point):


        encryptdata = AESinterface.encrypt_oracle(AESObj, str(request_data))  # 加密数据
        data = {"jsonParams": encryptdata}
        headers = {'content-type': "application/x-www-form-urlencoded"}
        responData = requests.post(url=request_url, data=data, headers=headers)
        time.sleep(8)
        ret = responData.text
        result = AESinterface.decrypt_oralce(AESinterface(), ret)
        re1 = json.loads(result)
        status = re1['rspCode']
        if status == 200:

            if re.search(check_point, str(re1)):
                logging.info(num + ' ' + api_purpose + ' 成功, ' + str(status) + ', ' + str(re1))
                return status, re1
            else:
                logging.error(num + ' ' + api_purpose + ' 失败！！！, [ ' + str(status) + ' ], ' + str(re1))
                return 2001, re1
        else:
            logging.error(num + ' ' + api_purpose + ' 失败！！！, [ ' + str(status) + ' ], ' + str(re1))
            return status, re1



if __name__ == '__main__':
    AESObj = AESinterface()
    obj = Interface()

    obj.runTest()












