#!/usr/bin/env Python
# coding=utf-8

from Public.common.Interface import *
import json
import xlrd
class Deptinfo():
    def __init__(self):
        self.tokenValue = Interface.gettoken(InterfaceObj)

    def getDeptinfo(self):

        url = 'https://puhui-env.yingu.com/ygph/api/orders/query/getDeptInfo'
        datacom = {"commonParams":{"token":self.tokenValue,"version":"9.0.0","deviceCode":"5131as3dfasdf","sourceType":"3","os":"android.5.0","channel":""}}
        encryptdata = AESinterface.encrypt_oracle(AESObj,str(datacom))#加密数据
        data2 = {"jsonParams":datacom}
        # print(data2)
        headers = {'content-type': "application/json"}
        re = requests.post(url=url, data=json.dumps(data2), headers=headers)
        ret = re.text
        result = AESinterface.decrypt_oralce(AESinterface(), ret)
        result2 = json.loads(result)
        deptName = []
        deptAddress = []
        for i in range(len(result2['data'])):
            areaData = result2['data'][i]
            for j in range(len(areaData['area'])):
                codeData = areaData['area'][j]
                for k in range(len(codeData['area'])):
                    code2Data = codeData['area'][k]#查询出name，address
                    deptName.append(code2Data['name'])
                    deptAddress.append(code2Data['address'])
                    # print(deptName)
        return deptName,deptAddress




    def readAdderss(self):
        ExcelFile = xlrd.open_workbook(r'D:\deft.xlsx')
        sheet = ExcelFile.sheet_by_name('Sheet1')
        rows = sheet.nrows
        nameList = []
        addressList = []
        for row in range(2, rows):
            nameValue = sheet.cell(row, 0).value
            addressValue = sheet.cell(row, 2).value

            nameList.append(nameValue)
            addressList.append(addressValue)
            # print(nameList)
        return nameList, addressList


    def matchAddress(self):


        for i in range(len(self.getDeptinfo()[0])):

            # print(self.getDeptinfo()[0][i])
            if self.getDeptinfo()[0][i] in self.readAdderss()[0]:#营业部名称查询
                indexEexcel = self.readAdderss()[0].index(self.getDeptinfo()[0][i])#根据服务器获取的营业部列表名称查询excel的营业部列表的index，然后再根据index查询excel地址

                if self.getDeptinfo()[1][i] not in self.readAdderss()[1][indexEexcel]:
                    print("未找到营业部地址,服务器地址名称:{0}, excel地址名称为:{1}".format(self.getDeptinfo()[1][i], self.readAdderss()[1][indexEexcel]))
                else:
                    print('已找到营业地址', self.getDeptinfo()[1][i])








if __name__ == '__main__':

    AESObj = AESinterface()
    InterfaceObj = Interface()
    Obj = Deptinfo()
    # Obj.getDeptinfo()
    # Obj.readAdderss()
    Obj.matchAddress()