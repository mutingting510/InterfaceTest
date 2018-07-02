#!/usr/bin/env Python
# coding=utf-8

import requests
import base64
from Crypto.Cipher import AES
class AESinterface():

    key = '2En!HE%SYQc#W-B3'
    IV = '16-Bytes--String'
    def __init__(self):
        self.BS = AES.block_size

        self.pad = lambda s: s + (self.BS - len(s) % AES.block_size) * chr(self.BS - len(s) % self.BS)  # PCKS5Padding的方式是缺几个字符就补几个字符的字
        self.unpad = lambda s: s[0:-ord(s[-1])]


    def str_to_byte(self, value):
        while len(value) % 16 != 0:
            value += '\0'
        return str.encode(value)  # 返回byte


    def encrypt_oracle(self):
        data1 = '{"commonParams":{"deviceCode":"H5-1a36f229260f85dd861c3ba372be7111","sourceType":"3","version":"1.0.0","os":"null","channel":"H5","token":""},"dataParams":{"phone":"18010117861","password":"9cbf8a4dcb8e30682b927f352d6559a0"}}'
        encrycommonParams = '{"token":"AYF3rfCpbuiW0bxhwVnR9imecCEheIK1kpplikwADagUcUAS1byrMzm7dHHyzGE6cyG1sHxSHESx8vH_h2EaeDh8ezhiBqWdMX7Qy3AC7bruEeCUe4BMbcbg7FhK7tfdQOCMgZ-QxQG0tmfmp2tf3Q4NH_s8MFT2W9BqQSFOJlx9tLhZUSzLr6T8W4x80f73GVk","version":"9.0.0","deviceCode":"0050f483ff67417093b273aa71b77fb5","sourceType":"3","os":"android.5.0","channel":""}'
        encrydataParams = '{"type":"auth_auto","sort":"004459500000-1204","website":"si_huizhou","id_card_num":"445221199405231019","name":"test","cell_phone_num":"18811772343","orderId":"123","si_account":"445221199405231019","password":"660364"}}'

        aes = AES.new(self.str_to_byte(AESinterface.key), AES.MODE_CBC, self.str_to_byte(AESinterface.IV))
        comdata = str.encode(self.pad(encrycommonParams))
        datadata = str.encode(self.pad(encrydataParams))
        # 先进行aes加密dump
        # datadata2 =
        encryptAesCommonParams = aes.encrypt(comdata)
        encryptAesDataParams = aes.encrypt(datadata)
        # 用base64转成字符串形式
        encrypted_text_comdata = str(base64.b64encode(encryptAesCommonParams), encoding='utf-8')  # 执行加密并转码返回bytes
        encrypted_text_datadata = str(base64.b64encode(encryptAesDataParams), encoding='utf-8')  # 执行加密并转码返回bytes\

        print(encrypted_text_comdata)
        print(encrypted_text_datadata)
        return (encrycommonParams, encrycommonParams)



if __name__ == '__main__':
    obj = AESinterface()
    obj.encrypt_oracle()