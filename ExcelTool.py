import xlwt
import xlrd
from xlutils.copy import copy
import numpy as np

class ExcelTool:

    def WriteExcle(self,path,sheet_name,value):
        index = len(value)
        book = xlwt.Workbook()  #Create a excel file
        sheet = book.add_sheet(sheet_name)  #Create a sheet
        for  i in range(0,index):
            for j in range(0,len(value[i])):
                sheet.write(i,j,value[i][j])
        book.save(path)
        print("Write success!")

    def WriteExcAp(self,path,value):
        index = len(value)
        book = xlrd.open_workbook(path)  #Open the file exist already
        sheet_name = book.sheet_names()  #Get all sheet name of this file
        worksheet = book.sheet_by_name(sheet_name[0])
        rows_old = worksheet.nrows  #Get the number of rows
        newbook = copy(book)
        newsheet = newbook.get_sheet(0)
        for i in range(0,index):
            for j in range(0,len(value[i])):
                newsheet.write(i+rows_old,j,value[i][j])
        newbook.save(path)
        print("append is suucess!")

    def readExcToInt (self,path):
        book = xlrd.open_workbook(path)
        sheet_name = book.sheet_names()  # Get all sheet name of this file
        worksheet = book.sheet_by_name(sheet_name[0])
        temp = []
        sub = np.zeros([worksheet.nrows,worksheet.ncols],dtype=int)
        for i in range(1,worksheet.nrows):
            for j in range(0,worksheet.ncols):
                sub[i][j] = int(worksheet.cell_value(i,j))
            temp.append([i,(sub[i][0],sub[i][1]),sub[i][2],sub[i][3],(sub[i][4],sub[i][5])])
        return temp








bookname = 'D://Orders.xls'
sheet_name = 'Orders'
value_title = [["起始时间", "起始地址", "订单状态", "订单价格", "终止时间","终止地点"]]
value = [["1","(2,3)",3,4,5,6]]

ex = ExcelTool()
ex.readExcToInt(bookname)





