#!/usr/bin/env Python
# coding=utf-8

import requests
import base64
from Crypto.Cipher import AES
class AESinterface():

    key = '2En!HE%SYQc#W-B3'
    IV = '16-Bytes--String'
    def __init__(self):

        self.pad = lambda s: s + (AES.block_size - len(s) % AES.block_size) * chr(AES.block_size - len(s) % AES.block_size)  # PCKS5Padding的方式是缺几个字符就补几个字符的字
        self.unpad = lambda s: s[0:-ord(s[-1])]


    def str_to_byte(self, value):
        while len(value) % 16 != 0:
            value += '\0'
        return str.encode(value)  # 返回byte
    #加密方法
    def encrypt_oracle(self,data):
        # data1 = '{"commonParams":{"deviceCode":"H5-1a36f229260f85dd861c3ba372be7111","sourceType":"3","version":"1.0.0","os":"null","channel":"H5","token":""},"dataParams":{"phone":"18010117861","password":"9cbf8a4dcb8e30682b927f352d6559a0"}}'
        # data = '{"commonParams":{"token":"AYF3rfCpbuiW0bxhwVnR9imecCEheIK1kpplikwADagUcUAS1byrMzm7dHHyzGE6cyG1sHxSHESx8vH_h2EaeDh8ezhiBqWdMX7Qy3AC7bruEeCUe4BMbcbg7FhK7tfdQOCMgZ-QxQG0tmfmp2tf3Q4NH_s8MFT2W9BqQSFOJlx9tLhZUSzLr6T8W4x80f73GVk","version":"9.0.0","deviceCode":"0050f483ff67417093b273aa71b77fb5","sourceType":"3","os":"android.5.0","channel":""},"dataParams":{"type":"auth_auto","sort":"004459500000-1204","website":"si_huizhou","id_card_num":"445221199405231019","name":"蔡志坚","cell_phone_num":"18811772343","orderId":"123","si_account":"445221199405231019","password":"660364"}}'
        aes = AES.new(self.str_to_byte(AESinterface.key), AES.MODE_CBC, self.str_to_byte(AESinterface.IV))
        #先进行aes加密dump
        # raw = AES.c_uint8_ptr(data)
        # print(self.pad(data))
        encrypt_aes = aes.encrypt(self.pad(data).encode("utf-8"))
        #用base64转成字符串形式
        encrypted_text = str(base64.b64encode(encrypt_aes), encoding='utf-8')  # 执行加密并转码返回bytes
        # print(encrypted_text)
        return encrypted_text


    #解密方法
    def decrypt_oralce(self,decrypt_data):
        # 初始化加密器
        data = 'vWFNxfd+6ip3HMOt4+5No/oyTNJaY0ab2lRqtLSzjC3kCTIvFlOTWYgl2scOyvMNNobpSgY3GzX9Y9Io9ncv0C4mw2hzazQB7pMDZ4/L0l5bmGpx0vARBmQ7rlEgapoJ'
        aes = AES.new(self.str_to_byte(self.key), AES.MODE_CBC, self.str_to_byte(self.IV))
        base64_decrypted = base64.b64decode(decrypt_data.encode(encoding='utf-8'))
        decrypted_text = str(aes.decrypt(base64_decrypted), encoding='utf-8') # 执行解密密并转码返回str
        # print(self.unpad(decrypted_text))
        return self.unpad(decrypted_text)
#
# if __name__ == '__main__':
#     obj = AESinterface()
# #     obj.encrypt_oracle('{"commonParams":{"token":"AYF3rfCpbuiW0bxhwVnR9imecCEheIK1kpplikwADagUcUAS1byrMzm7dHHyzGE6cyG1sHxSHESx8vH_h2EaeDh8ezhiBqWdMX7Qy3AC7bruEeCUe4BMbcbg7FhK7tfdQOCMgZ-QxQG0tmfmp2tf3Q4NH_s8MFT2W9BqQSFOJlx9tLhZUSzLr6T8W4x80f73GVk","version":"9.0.0","deviceCode":"0050f483ff67417093b273aa71b77fb5","sourceType":"3","os":"android.5.0","channel":""},"dataParams":{"type":"auth_auto","sort":"004459500000-1204","website":"si_huizhou","id_card_num":"445221199405231019","name":"蔡志坚","cell_phone_num":"18811772343","orderId":"123","si_account":"445221199405231019","password":"660364"}}')
# #

