#!/usr/bin/env Python
# coding=utf-8
#公积金接口测试

from Public.common.Interface import *
import xlrd

class AccumulationTest():

    # print(tokenValue[0])



    def __init__(self,cityname,name,idcard,si_account,phoneNum,password):
        self.cityname = cityname
        self.name = name
        self.idcard = idcard
        self.si_account = si_account
        self.phone = phoneNum
        self.password = password


    def getAllCity(self):
        url = "http://10.0.129.139:17201/services/fund/getAllCity"
        response = requests.get(url)
        jsonresponse = response.json()
        data = jsonresponse.get('data')
        for i in range(len(data)):
            data2 = data[i].get('sub')
            for j in range(len(data2)):
                getname = data2[j].get('name')
                if self.cityname in getname:
                    url2 = 'http://10.0.129.139:17201/services/fund/getSort/'+data2[j].get('fullcode')
                    responseSort = requests.get(url2)
                    jsondata2 = responseSort.json()

                    json_data = jsondata2.get('data')
                    # print(json_data)
                    getwebsite = json_data[0].get('website')
                    getsorts = json_data[0].get('sorts')
                    for k in range(len(getsorts)):
                        gettype = getsorts[0].get('type')
                        getsort = getsorts[0].get('sort')
                        # print(gettype,getsort,getwebsite)
                        return (gettype,getsort,getwebsite)
#所有城市的公积金接口
    def applytest(self):
        try:
            url = 'http://10.0.129.139:17201/services/fund/apply'
            data = {"type":self.getAllCity()[0],"sort":self.getAllCity()[1],"website":self.getAllCity()[2],"id_card_num":self.idcard,"name":self.name,"cell_phone_num":self.phone,"orderId":"234","si_account":self.si_account,"password":self.password}
            # print(data)
            headers = {'Content-Type':'application/json'}
            re = requests.post(url=url, data=json.dumps(data), headers=headers)
            time.sleep(8)
            # print(re.text)
            # print(self.cityname,data)
            return data
        except Exception as e:
            print("获取城市公积金接口失败",e)
        # print(type(str(data)))

#增加token的公积金接口
    def certification(self):
        try:
            url = 'https://puhui-env.yingu.com/ygph/api/fund/certification'
            datacom = {"commonParams":{"token":tokenValue[0],"version":"9.0.0","deviceCode":"5131as3dfasdf","sourceType":"3","os":"android.5.0","channel":""},"dataParams":self.applytest()}
            encryptdata = AESinterface.encrypt_oracle(AESObj,str(datacom))#加密数据
            data2 = {"jsonParams":encryptdata}
            # print(data2)
            headers = {'content-type': "application/x-www-form-urlencoded "}
            re = requests.post(url=url, data=data2,headers=headers)
            time.sleep(8)
            ret = re.text
            # print("fundcertifation",ret)
            result = AESinterface.decrypt_oralce(AESinterface(), ret)
            respondRecordID = json.loads(result)
            # print("cer:",respondRecordID['data'])
            return respondRecordID['data']
        except Exception as e:
            print("RecordID失败",e)

    def refreshCertification(self):
        try:
            url = 'https://puhui-env.yingu.com/ygph/api/fund/certificationRefresh'
            datacom = {"commonParams": {"token": tokenValue[0], "version": "9.0.0","deviceCode": "5131as3dfasdf", "sourceType": "3", "os": "android.5.0","channel": ""}, "dataParams": self.certification()}
            encryptdata = AESinterface.encrypt_oracle(AESObj, str(datacom))  # 加密数据
            data3 = {"jsonParams": encryptdata}
            # print(data2)
            headers = {'content-type': "application/x-www-form-urlencoded"}
            re = requests.post(url=url, data=data3, headers=headers)
            time.sleep(8)
            ret = re.text
            # print(ret)
            result = AESinterface.decrypt_oralce(AESinterface(), ret)
            print(self.cityname,result)
        except Exception as e:
            print('刷新结果失败',e)



if __name__ == '__main__':


    ExcelFile = xlrd.open_workbook(r'D:\data.xlsx')
    sheet = ExcelFile.sheet_by_name('Sheet1')
    rows = sheet.nrows
    AESObj = AESinterface()
    InterfaceObj = Interface()

    # todyTime = time.strftime('%Y-%m-%d', time.localtime(time.time()))
    for row in range(1, rows):
        cityName = sheet.cell(row, 3).value
        name = sheet.cell(row, 5).value
        idCard = sheet.cell(row, 6).value
        si_account = sheet.cell(row, 7).value
        password = sheet.cell(row, 8).value
        phoneNum = sheet.cell(row, 9).value
    #     # print(cityName,name,idCard,secrect)
    #     tokenName = Interface.gettoken(Interface(), '18332065212')
        tokenName = Interface.gettoken(Interface(), phoneNum)
        tokenValue = []
        tokenValue.append(tokenName)
        obj = AccumulationTest(cityName, 'test', idCard,si_account, phoneNum,password)
        obj.refreshCertification()

        # obj = AccumulationTest('邢台市', 'test', '130582198602122417', '18332065212','605212')

        #     with open('D:\\TestCase.txt', 'a')as testcase_file:
        #         testcase_file.write(receivedata + '\n')
