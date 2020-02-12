import random
import numpy as np
import xlwt
from ExcelTool import ExcelTool



book = xlwt.Workbook()

class Learning:

    def __init__(self):
        self.T = 10  # TIme
        self.G = 100  # Region
        self.D = []  # Orders

        self.D_number = 3000 # the number of orders
        self.D_backup = []
        self.N = np.ones([self.T,self.G])
        self.V_s = np.zeros([self.T,self.G])
        self.path = 'D://Orders.xls'


    def Sub_D(self,D,t): #collect sub set of D,whose started time is t
        sub = []
        for i in range(self.D_number):
            if(D[i][1][0] == t):
                sub.append(D[i])
        return sub

    def OrdersProductor(self):
        # Produce some virtual orders,you can put some reality value into D if you want

        for i in range(self.D_number):  # Producing 20 orders
            t1 = random.randint(0, self.T - 2)
            g1 = random.randint(0, self.G - 1)
            t2 = t1 + random.randint(1, self.T - t1 - 1)
            g2 = random.randint(0, self.G - 1)
            price = random.randint(10, 100)
            self.D.append([(t1, g1), 1,price, (t2, g2)])
            #self.D_backup.append([str(t1),str(g1),str(1),str(price),str(t2),str(g2)])
          #  self.Orderbackup()
        return self.D

    def getData(self):
        ex = ExcelTool()
        self.D = ex.readExcToInt(self.path)
        return self.D


    def learning(self):
        for time in range(self.T-1,-1,-1):  #From T-1 to 0
            sub = self.Sub_D(self.D,time) #sub set
          #  print(sub)
            for time_sub in sub:
                R_t = 0
                self.N[time_sub[1][0]][time_sub[1][1]] += 1
                t1 = time_sub[1][0]
                t2 = time_sub[4][0]
                for i in range(t2-t1,-1,-1):
                    R_t += 2*pow(0.9,i)*(time_sub[3])/(t2-t1+1)  #We find a problem that is the result is less than real value by two times,so we multiple 2 times
                alpha = (1/self.N[time_sub[1][0]][time_sub[1][1]])
                V_s_prime = self.V_s[time_sub[4][0]][time_sub[4][1]]
                self.V_s[time_sub[1][0]][time_sub[1][1]] += alpha * ((pow(0.9,t2-t1+1)) * V_s_prime + R_t - self.V_s[time_sub[1][0]][time_sub[1][1]])

    def getV_s(self):
        return self.V_s

    def Orderbackup(self):
        ex = ExcelTool()
        path = 'D://Orders.xls'
        sheet_name = 'Orders'
        value_title = [["Start time","start region","Used","Price","End time","End eegion"]]
        ex.WriteExcle(path,sheet_name,value_title)
        ex.WriteExcAp(path,self.D_backup)















