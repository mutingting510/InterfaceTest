#!/usr/bin/env Python
# coding=utf-8


from Public.common.javatest import *
import os,logging
import json
import time
import xlrd
import requests
import re
from email.mime.text import MIMEText
import smtplib

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
        table = ExcelFile.sheet_by_name('Sheet2')
        rows = table.nrows
        correlationDict = {}
        errorCase = []
        correlationDict['${session}'] = None
        for i in range(2, rows):
            if table.cell(i, 9).value.replace('\n', '').replace('\r', '') != 'Yes':
                continue
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
                    fopen = open(dataFile, encoding='utf-8')
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
            status,resp = self.interfaceTest(num,api_purpose,request_url,request_data,check_point,correlationDict['${session}'])
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
                            # print(temp)
                        except:
                            try:
                                temp = value[key]
                            except:
                                break
                        value = temp
                    correlationDict[param[0]] = value
                    # print(value)
        return errorCase

    def interfaceTest(self,num,api_purpose,request_url,request_data,check_point,session):


        encryptdata = DESCrypt.desEncry(DESObj,str(request_data))
        # 加密数据
        data = {"jsonParams":encryptdata}
        headers = {'Content-Type':'application/x-www-form-urlencoded; charset=UTF-8',
            'X-Requested-With':'XMLHttpRequest',
            'Connection':'keep-alive',
            'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/43.0.2357.134 Safari/537.36'
        }
        if session is not None:
            headers['Cookie'] = 'session=' + session
        # print(data)
        responData = requests.post(url=request_url, data=data, headers=headers)
        time.sleep(8)
        ret = responData.text
        result = DESCrypt.desDecry(DESObj,ret)
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


    def sendMail(self,text):
        sender = 'ph-monitor@yingu.com'
        receiver = ['moutingting@yingu.com']
        # mailToCc = ['chenyuan1@yingu.com']
        subject = '[AutomantionTest]接口自动化测试报告通知'
        smtpserver = 'smtp.qiye.163.com'
        username = 'ph-monitor@yingu.com'
        password = 'ygph_2017'

        msg = MIMEText(text, 'html', 'utf-8')
        msg['Subject'] = subject
        msg['From'] = sender
        msg['To'] = ';'.join(receiver)
        msg['Cc'] = ';'.join(mailToCc)
        smtp = smtplib.SMTP()
        smtp.connect(smtpserver)
        smtp.login(username, password)
        smtp.sendmail(sender, receiver + mailToCc, msg.as_string())
        smtp.quit()




if __name__ == '__main__':
    DESObj = DESCrypt()
    obj = Interface()

    errorTest = obj.runTest()
    print(errorTest)
    if len(errorTest) > 0:
        html = '<html><body>接口自动化定期扫描，共有 ' + str(len(errorTest)) + ' 个异常接口，列表如下：'
        for test in errorTest:
            html = html+'<table><tbody><tr><th style="width:100px;">接口</th><th style="width:50px;">状态</th><th style="width:200px;">接口地址</th><th>接口返回值</th></tr><tr><td>' + test[0] + '</td><td>' + test[1] + '</td><td>' + test[2] + '</td><td>' + str(test[3]) + '</td></tr></tbody></table>'
            # html = html+'<tr><td>'+test[0]+'</td><td>'+test[1]+'</td><td>'+test[2]+ '</td><td>'+str(test[3])+'</td></tr>'
        # html = html+'</table></body></html>'
        obj.sendMail(html)












