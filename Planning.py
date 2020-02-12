import numpy as np
import random

from Learning import Learning
from  Kuh_Munkras import KM_Algorithm
import  time as t
from copy import deepcopy


class planning:
    def __init__(self):
        self.result = []
        self.OrdNum = 10  #The number of Orders each period
        self.DriNum =  20#The number of dirvers,it should be not greater than OrdNum
        self.totalTime = 10  #The period is 10
        self.Region = 100 #the size of grid is 10*10
        self.Orders = []
        self.Drivers = []
        self.finalresult = np.full((self.DriNum,self.totalTime),-1,dtype=int)
        self.OrdNo = -1
        self.flag = 0 #Default model(DirNum < OrdNum)

    def OrdersProductor(self,timestap):
        # Produce some virtual orders,you can put some reality value into D if you want

        for i in range(self.OrdNum):  # Producing 20 orders
            self.OrdNo += 1
            t1 = timestap  #start time should be same with timestap
            g1 = random.randint(0, self.Region - 1)
            t2 = t1 + random.randint(1, self.totalTime - t1 -1)
            g2 = random.randint(0, self.Region - 1)
            self.Orders.append([self.OrdNo,(t1, g1), 0, random.randint(10, 100), (t2, g2),0])
            #self.Orders = [[1, (1, 99), 0, 70, (6, 29)], [2, (1, 71), 0, 76, (2, 62)], [3, (1, 15), 0, 38, (8, 53)], [4, (1, 27), 0, 20, (2, 80)], [5, (1, 28), 0, 49, (4, 67)], [6, (1, 34), 0, 99, (2, 63)],[7,(1,25),0,67,(6,50)]]
            #, [4, (1, 27), 0, 20, (2, 80)], [5, (1, 28), 0, 49, (4, 67)], [6, (1, 34), 0, 99, (2, 63)],[7,(1,25),0,67,(6,50)]
        return self.Orders

    def DriverProductor(self):
        for i in range(self.DriNum):
            g = random.randint(0, self.Region - 1)  #Choose a place randomly
            self.Drivers.append([i,(0,g),0,0])   #No,state,used,money
        #self.Drivers = [[0, (0, 63), 0, 0], [1, (0, 38), 0, 0],[2, (0, 36), 0, 0], [3, (0, 88), 0, 0]]
        #, [2, (0, 36), 0, 0], [3, (0, 88), 0, 0], [4, (0, 24), 0, 0]
        return self.Drivers

    def getFreeOrd(self,timestap):
        bk = deepcopy(self.Orders)
        for sub in bk:
            if(sub[5] > 1 or sub[2] == 1 or sub[1][0]<timestap):
                print("delete invaild and mathed Order No.: "+str(sub[0]))
                self.Orders.remove(sub)  #Remove the order that is unmatched for long time(3 timestap)
                continue
        return self.Orders

    def getFreeDri(self,timestap):
        subDri = []
        for sub in self.Drivers:
            if(sub[2] == 0):
                subDri.append(sub)

        return subDri


    def Calc_AdvFuc(self,freeDri,freeOrd,V_s):
        global Af
        if(len(freeOrd) > len(freeDri)):
            self.flag = 0
            Af = np.zeros((len(freeOrd),len(freeOrd)))  #Advantage function
        if (len(freeDri) > len(freeOrd)):
            self.flag = 1 #Special model
            Af = np.zeros((len(freeDri), len(freeDri)))  # Advantage function
        for i in range(0,len(freeDri)):
            for j in range(0,len(freeOrd)):
                t = freeOrd[j][4][0] - freeOrd[j][1][0]  #Time gap
                Af[i][j] = round (pow(0.9,t)*V_s[freeOrd[j][4][0]][freeOrd[j][4][1]] - V_s[freeDri[i][1][0]][freeDri[i][1][1]] + freeOrd[j][3],2)
                if(Af[i][j] < 0):   #The result is bad,make it zero!
                    Af[i][j] = 0
               # print('('+str(i)+str(j)+'):'+str(V_s[freeOrd[j][4][0]][freeOrd[j][4][1]])+'-'+str(V_s[freeOrd[i][1][0]][freeOrd[i][1][1]])+'+'+str(freeOrd[j][3])+'='+str(Af[i][j]))
        return  Af

    def getFlag(self):
        return self.flag

    def getNum(self):
        if(self.DriNum > self.OrdNum):
            return self.OrdNum
        else:
            return self.DriNum

    def RecR_Update(self,timestap,fo,fd):
        re = KM.getResult()
        #find free driver and let them status time +1

        if(self.flag == 0): #default model ,dir < ord
            print("This round we have match :")
            for i in range(0,len(fo)):
                #print('i is '+str(i))
                if(re[i] < len(fd)):

                    self.finalresult[fd[re[i]][0]][timestap] = self.Orders[i][0]  #Mark the order acceptd by driver re[i]
                    self.Orders[i][2] = 1 #Change the used mark
                    self.Drivers[fd[re[i]][0]][1] = self.Orders[i][4]
                    self.Drivers[fd[re[i]][0]][2] =1 #The driver has a mission,change the used mark


                    print('('+str(self.Drivers[fd[re[i]][0]][0])+','+str(self.Orders[i][0])+')')

        if(self.flag == 1):  #special model,dri > ord
            for i in range(0,len(fo)):
                self.finalresult[self.Drivers[re[i]][0]][timestap] = fo[i][0]
                for j in range(len(self.Orders)):  #Mark the used flag
                    if(self.Orders[j][0] == fo[i][0]):
                        self.Orders[j][2] = 1
                self.Drivers[re[i]][1] = fo[i][4]
                self.Drivers[re[i]][2] = 1#The driver has a mission,change the used mark

                print('(' + str(self.Drivers[re[i]][0]) + ',' + str(fo[i][0]) + ')')




        for od in self.Orders:
            od[5] += 1
            if(od[4][0] < self.totalTime-1):

                s,g = od[1][0],od[1][1]
                od[1] = (s+1,g)
                e,f = od[4][0],od[4][1]
                od[4] = (e+1,f)

        for dr in self.Drivers:
            if(dr[1][0] == timestap+1):
                dr[2] = 0 #Changed the used mark





        return self.finalresult
        # if(self.flag == 0):
        #     temp = np.zeros(self.DriNum,dtype=int)
        #     re = KM.getResult()
        #     for i in range(len(PL.getFreeOrd(time))):
        #         if(re[i] < self.DriNum):
        #             temp[re[i]] = i
        # if(self.flag == 1):
        #     temp = np.zeros(self.DriNum, dtype=int)
        #     re = KM.getResult()
        #     for i in range(1,len(PL.getFreeOrd(time))):
        #         temp[re[i-1]] = i
        # self.finalresult.append(temp)







if __name__ == '__main__':
    time = 0
    totalSum = 0
    RL = Learning()
    RL.getData()   #Get train data
    RL.learning()  #Trainning
    PL = planning()
    PL.DriverProductor()  #Create drivers

    while(time < 9):


      #  RL.OrdersProductor()

        PL.OrdersProductor(time)  #timestap

        fo = PL.getFreeOrd(time)
        fd = PL.getFreeDri(time)
        print(str(time) + ' has drivers:')
        print(fd)
        print(str(time) + 'have orders:')
        print(fo)

        af = PL.Calc_AdvFuc(fd,fo,RL.getV_s())
        print("Current Model:"+str(PL.getFlag()))
        KM = KM_Algorithm(af,PL.getFlag(),PL.getNum())
        KM.Kuh_Munkras()
        PL.RecR_Update(time,fo,fd)
        totalSum += KM.calculateSum()

        print("Current Sum is: "+str(totalSum))
        print("A round if time is " + str(time) + " finish!\n\n\n")
        time += 1


        t.sleep(1)
    print(PL.finalresult)
        #
        # print(KM.getResult())
        # print(KM.calculateSum())







# P = planning()
# P.DriverProductor()
# P.OrdersProductor(0)
# print(P.Orders)
# print(P.Drivers)
#
# freeord = P.getFreeOrd()
# freedri = P.getFreeDri(0)
#
# print(freeord)
# print(freedri)
#
# af = P.Calc_AdvFuc(freedri,freeord,[[2,3],[4,5]])


