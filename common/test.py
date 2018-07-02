import json
import requests

encryptdata = {"dataParams":{"phone":"17610827222","password":"dc483e80a7a0bd9ef71d8cf973673924"},"commonParams":{"os":"androd 7.0","sourceType":"1","channel":"360","deviceCode":"5131as3dfasdf","version":"1.0.0","token":""}}

data = {"jsonParams":encryptdata,"type":"2"}
url = 'https://puhui-env.yingu.com/mis/api/misReceiveCustomer/encodeParams'
res = requests.post(url,data= data,)
print(res.text)