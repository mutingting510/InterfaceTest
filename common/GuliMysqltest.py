#!/usr/bin/env Python
# coding=utf-8
#谷粒儿mysql测试

import pymysql
import xlrd


class CheckMysql:
    def __init__(self, host, user, passwd, db, tableName):
        self.host = host
        self.user = user
        self.passwd = passwd
        self.db = db
        self.tableName = tableName

    def insertUsers(self,name,coirdid,phoneNum):

        db = pymysql.connect(host=str(self.host), user=str(self.user), passwd=str(self.passwd), db=str(self.db), charset="utf8")
        cur = db.cursor()
        try:
            # name = '李四'
            # sql = 'CALL testData(%s)'(name)
            cur.execute('CALL testData(%s,%s,%s)', (name,coirdid,phoneNum))
            data = cur.fetchall()
            print('插入用户成功')

            # cur.execute("SELECT * FROM " + str(self.tableName))
            # for row in cur.fetchall():
            #     #   print(row)
            #     id = row[0]
            #     startHeight = row[1]
            #     endHeight = row[2]
            #     oilV = row[3]
            #     calculateV = row[4]
            #     ratioV = row[5]
            #     print("id=%d ,startHeight=%f,endHeight =%f, oilV=%f, ratio=%f  ",
            #           (id, startHeight, endHeight, oilV, calculateV, ratioV))
        except Exception as e:
            print(e)
        finally:
            db.commit()
            cur.close()
            db.close()

    def insertMySQL(self, ID, CH1, CH2, CHV, calV, ratV):
        conn = pymysql.connect(host=str(self.host), user=str(self.user), passwd=str(self.passwd),
                               db=str(self.db), charset="utf8")
        cur = conn.cursor()
        try:
            sqli = "insert into " + str(
                self.tableName) + "(id,startHeight,endHeight,oilV,calculateV,ratioV) values(%s,%s,%s,%s,%s,%s)"
            param = (ID, CH1, CH2, CHV, calV, ratV)
            cur.execute(sqli, param)

            cur.close()
            conn.commit()
            conn.close()
        except:
            print("MySQL Error :unable to insert data")

    def updateMySQL(self, id, calV, ratV):
        conn = pymysql.connect(host=str(self.host), user=str(self.user), passwd=str(self.passwd),
                               db=str(self.db), charset="utf8")
        cur = conn.cursor()
        try:
            #   sqli = "update checkVolume set calculateV=23.34 ,ratioV=1.6  where id = 123"
            #  cur.execute(sqli)

            sqlit = 'update ' + str(self.tableName) + ' set calculateV=' + str(calV) + ',ratioV=' + str(
                ratV) + 'where id=' + str(id)
            cur.execute(sqlit)
            cur.close()
            conn.commit()
            conn.close()
        except:
            print("MySQL Error :unable to update data")

            # delete a record

    def deleteByphone(self, phoneNum):

        conn = pymysql.connect(host=str(self.host), user=str(self.user), passwd=str(self.passwd),
                               db=str(self.db), charset="utf8")
        cur = conn.cursor()
        try:
            # sqlit = 'delete from ' + str(self.tableName) + ' where id>' + str(id)
            sql1 = 'DELETE FROM phapp_client_idcardocr WHERE user_id IN (SELECT client_id FROM phapp_client_account WHERE account IN (%s)  AND `status`=1);'
            sql2 = 'DELETE FROM phapp_client_authentication WHERE user_id IN (SELECT client_id FROM phapp_client_account WHERE account IN (%s)  AND `status`=1)'
            sql3 = 'DELETE FROM phapp_client_facecontrast WHERE user_id IN (SELECT client_id FROM phapp_client_account WHERE account IN (%s)  AND `status`=1);'
            sql4 = 'DELETE FROM phapp_client_frozenaccount WHERE TYPE = 1 AND DATE(end_date) > DATE(NOW()) AND client_id IN (SELECT client_id FROM phapp_client_account WHERE account IN (%s)  AND `status`=1);'
            sql5 = 'DELETE FROM phapp_client_frozenaccount WHERE TYPE = 2 AND DATE(end_date) > DATE(NOW()) AND client_id IN (SELECT client_id FROM phapp_client_account WHERE account IN (%s)  AND `status`=1);'
            sql6 = 'DELETE FROM phapp_order WHERE user_id IN (SELECT client_id FROM phapp_client_account WHERE account IN (%s)  AND `status`=1);'
            sql7 = 'DELETE FROM phapp_client_register WHERE id IN (SELECT client_id FROM phapp_client_account WHERE account IN (%s));'
            sql8 = 'DELETE FROM phapp_client_account WHERE  account IN (%s) AND `status`=1;'


            cur.execute(sql1,phoneNum)
            cur.execute(sql2,phoneNum)
            cur.execute(sql3,phoneNum)
            cur.execute(sql4,phoneNum)
            cur.execute(sql5,phoneNum)
            cur.execute(sql6,phoneNum)
            cur.execute(sql7,phoneNum)
            cur.execute(sql8,phoneNum)
            cur.close()
            conn.commit()
            conn.close()
        except Exception as e:
            print(e)



def main():
    # CheckH1 = [12.2, 23.4]
    # CheckH2 = [10.8, 23.3]
    # CheckV = [13200.1, 12500]
    # CalculateV = [10020.4, 13000]
    # ratioV = [0.23, 0.12]

    ckl = CheckMysql('10.0.129.135', 'guli_0108', 'U#bfivm3F', "ph_app", '')
    # ckl = CheckMysql('172.24.132.241', 'guli_0108', 'U#bfivm3F', "ph_app", '')
    # ckl.deleteByphone('18600517988')
    # ckl.insertMySQL(39, CheckH1[0], CheckH2[0], CheckV[0], CalculateV[0], ratioV[0])
    # ckl.updateMySQL(39, CalculateV[0], ratioV[0])
    ExcelFile = xlrd.open_workbook(r'D:\user2.xlsx')
    sheet = ExcelFile.sheet_by_name('Sheet1')
    rows = sheet.nrows
    for row in range(1, rows):
        name = sheet.cell(row, 0).value
        cordid = sheet.cell(row, 1).value
        phoneNum = sheet.cell(row, 2).value
        ckl.deleteByphone(phoneNum)
        ckl.insertUsers(name,cordid,phoneNum)
    # ckl.insertUsers('张三','231002198805103222','18600517988')



if __name__ == '__main__':
    main()