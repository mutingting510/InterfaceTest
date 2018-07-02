#!/usr/bin/env Python
# coding=utf-8
#谷粒儿mysql测试

import pymysql
import xlrd


class CheckMysql:
    def __init__(self, host, user, passwd, db):
        self.host = host
        self.user = user
        self.passwd = passwd
        self.db = db
        # self.tableName = tableName

    # 渠道客户表
    def select_mis_receive_customer(self):
        db = pymysql.connect(host=str(self.host), user=str(self.user), passwd=str(self.passwd), db=str(self.db), charset="utf8")
        cur = db.cursor()
        try:
            cur.execute("SELECT * FROM mis_receive_customer ")
            for row in cur.fetchall():
                #   print(row)
                phone = row[4]  #手机号
                check_status = row[24]  #查重状态 0：本地校验不通过 1：未校验 2.运营系统校验不通过 3.信审系统校验不通过 4.校验通过
                match_status = row[25]  #客户匹配状态 0:未匹配 1：匹配成功 2：匹配失败
                rob_status = row[26]  #被抢状态 0：未被抢 1：抢中
                issue_status = row[27]  #下发状态0：未下发 1：已下发 2.下发失败
                is_effective = row[29]  #客户是否有效 0：无效 1：有效

                if check_status == 4 and rob_status == '1'and is_effective == '1' and match_status == '1' and issue_status == '1':
                    print(phone,check_status,match_status,rob_status,issue_status,is_effective)
        except Exception as e:
            print(e)
        finally:
            db.commit()
            cur.close()
            db.close()

    def select_mis_customer_validate(self):
        db = pymysql.connect(host=str(self.host), user=str(self.user), passwd=str(self.passwd), db=str(self.db), charset="utf8")
        cur = db.cursor()
        try:
            cur.execute("SELECT * FROM mis_customer_validate ")
            for row in cur.fetchall():
                  print(row)
                # phone = row[4]  #手机号
                # check_status = row[24]  #查重状态 0：本地校验不通过 1：未校验 2.运营系统校验不通过 3.信审系统校验不通过 4.校验通过
                # match_status = row[25]  #客户匹配状态 0:未匹配 1：匹配成功 2：匹配失败
                # rob_status = row[26]  #被抢状态 0：未被抢 1：抢中
                # issue_status = row[27]  #下发状态0：未下发 1：已下发 2.下发失败
                # is_effective = row[29]  #客户是否有效 0：无效 1：有效
                #
                # if check_status == 4 and rob_status == '1'and is_effective == '1' and match_status == '1' and issue_status == '1':
                #     print(phone,check_status,match_status,rob_status,issue_status,is_effective)
        except Exception as e:
            print(e)
        finally:
            db.commit()
            cur.close()
            db.close()
def main():
    # CheckH1 = [12.2, 23.4]
    # CheckH2 = [10.8, 23.3]
    # CheckV = [13200.1, 12500]
    # CalculateV = [10020.4, 13000]
    # ratioV = [0.23, 0.12]

    ckl = CheckMysql('10.0.129.135', 'guli_0108', 'U#bfivm3F', "ph_mis" )
    # ExcelFile = xlrd.open_workbook(r'D:\user1.xlsx')
    # sheet = ExcelFile.sheet_by_name('Sheet1')
    # rows = sheet.nrows
    # for row in range(1, rows):
    #     name = sheet.cell(row, 0).value
    #     cordid = sheet.cell(row, 2).value
    #     phoneNum = sheet.cell(row, 1).value
    #     ckl.deleteByphone(phoneNum)
    #     ckl.insertUsers(name,cordid,phoneNum)
    ckl.select_mis_receive_customer()



if __name__ == '__main__':
    main()
