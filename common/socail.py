#!/usr/bin/env Python
# coding=utf-8
#社保接口测试
from Public.common.Interface import *
import xlrd

class SocailTest():

    def __init__(self,cityname,name,idcard,phone,password,account):
        self.cityname = cityname
        self.name = name
        self.idcard = idcard
        self.phone = phone
        self.password = password
        self.account = account


    def getAllCity(self):
        url = "https://puhui-env.yingu.com/ygph/api/social/getCitys"
        data = {"commonParams":{"token":tokenValue[0],"version":"9.0.0","deviceCode":"5131as3dfasdf","sourceType":"3","os":"android.5.0","channel":""}}
        headers = {'Content-Type': 'application/json'}
        re = requests.post(url=url, data=json.dumps(data), headers=headers)
        # time.sleep(8)
        ret = re.text
        result = AESinterface.decrypt_oralce(AESinterface(), ret)
        respone = json.loads(result)
        # print(respone['data'])

        for i in range(len(respone['data'])):
            dataSub = respone['data'][i]
            # print(dataSub)
            for j in range(len(dataSub['sub'])):
                dataFullcode = dataSub['sub'][j]
                if self.cityname in dataFullcode['name']:
                    nameFullCode = dataFullcode['fullcode']
                    return nameFullCode


    def getForms(self):
        try:
            url = 'https://puhui-env.yingu.com/ygph/api/social/getForms'
            datacom = {"commonParams":{"token":tokenValue[0],"version":"9.0.0","deviceCode":"5131as3dfasdf","sourceType":"3","os":"android.5.0","channel":""},"dataParams":{"fullcode":self.getAllCity()}}
            encryptdata = AESinterface.encrypt_oracle(AESObj,str(datacom))#加密数据
            data2 = {"jsonParams":encryptdata}
            # print(data2)
            headers = {'content-type': "application/x-www-form-urlencoded "}
            re = requests.post(url=url, data=data2,headers=headers)
            time.sleep(8)
            ret = re.text
            result = AESinterface.decrypt_oralce(AESinterface(), ret)
            respond = json.loads(result)
            # print(respond['data']['sorts'])
            website = respond['data']['website']
            for i in range(len(respond['data']['sorts'])):

                sort = respond['data']['sorts'][i]['sort']
                # print(website,sort)
                return website,sort
        except Exception as e:
            print("根据城市动态获取表单失败getForms",e)

    def socialCertification(self):
        try:
            url = 'https://puhui-env.yingu.com/ygph/api/social/certification'
            # print("提交接口",self.getForms()[0],self.getForms()[1])
            data = {"commonParams":{"token":tokenValue[0],"version":"9.0.0","deviceCode":"5131as3dfasdf","sourceType":"3","os":"android.5.0","channel":""},"dataParams":{"type":"auth_auto","sort":self.getForms()[1],"website":self.getForms()[0],"id_card_num":self.idcard,"name":self.name,"cell_phone_num":self.phone,"orderId":"234","si_account":self.account,"password":self.password}}
            # datacom = {"commonParams":{"token":tokenValue[0],"version":"9.0.0","deviceCode":"5131as3dfasdf","sourceType":"3","os":"android.5.0","channel":""},"dataParams":{"type":"auth_auto","sort":"004459500000-1204","website":"si_huizhou","id_card_num":"445221199405231019","name":"蔡志坚","cell_phone_num":"18811772343","orderId":"123","si_account":"445221199405231019","password":"660364"}}

            # print("社保提交接口",data)
            encryptdata = AESinterface.encrypt_oracle(AESObj, str(data))  # 加密数据
            data2 = {"jsonParams": encryptdata}
            headers = {'content-type': "application/x-www-form-urlencoded "}
            re = requests.post(url=url, data=data2, headers=headers)
            time.sleep(8)
            ret = re.text
            result = AESinterface.decrypt_oralce(AESinterface(), ret)
            respond = json.loads(result)
            return respond['data']
            # print("提交接口返回数据：",respond['data'])
        except Exception as e:
            print("社保认证提交接口失败",e)

    def refreshCertification(self):
        try:
            url = 'https://puhui-env.yingu.com/ygph/api/social/certificationRefresh'
            datacom = {"commonParams": {"token": tokenValue[0], "version": "9.0.0","deviceCode": "5131as3dfasdf", "sourceType": "3", "os": "android.5.0","channel": ""}, "dataParams": self.socialCertification()}
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
            print('社保认证刷新接口失败',e)



if __name__ == '__main__':



    ExcelFile = xlrd.open_workbook(r'D:\data.xlsx')
    sheet = ExcelFile.sheet_by_name('Sheet2')
    rows = sheet.nrows
    AESObj = AESinterface()
    InterfaceObj = Interface()


    for row in range(1, rows):
        cityName = sheet.cell(row, 3).value
        name = sheet.cell(row, 5).value
        idCard = sheet.cell(row, 6).value
        phoneNum = sheet.cell(row, 9).value
        secrect = sheet.cell(row, 8).value
        account = sheet.cell(row, 7).value
    # print(cityName,name,idCard,secrect)
    # tokenName = Interface.gettoken(Interface(), '13820517151')
        tokenName = Interface.gettoken(Interface(), phoneNum)
        tokenValue = []
        tokenValue.append(tokenName)
        AESObj = AESinterface()
        InterfaceObj = Interface()
        obj = SocailTest(cityName, 'test', idCard, phoneNum, secrect, account)
        # obj = SocailTest('天津', 'test', '620104199207250582', '13820517151','gsm09110725')
        obj.refreshCertification()
        # obj.getForms()



