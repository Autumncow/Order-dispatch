import numpy as np
import time


class KM_Algorithm:
    def __init__(self,Net = [[3, 10, 6, 4, 9], [6, 9, 5, 3, 8], [7, 8, 3, 4, 2],[0,1,0,0,0],[0,1,0,0,0]],flag=0,Num = 0):
        #Net = [[4,6,3,12],[5,9,2,19],[7,9,2,10]]
        #Net = [[3, 4, 6, 4, 9], [6, 4, 5, 3, 8], [7, 5, 3, 4, 2], [6, 3, 2, 2, 5], [8, 4, 5, 4, 7]]
        # Net = [[20,27,0,59,0],
        #        [10,16,0,48,0],
        #        [12,19,0,51,0],
        #        [17,24,0,56,0],
        #        [17,23,0,55,0]]
        #Net = [[3,4,6,4,9],[6,4,5,3,8],[7,5,3,4,2],[6,3,2,2,5],[8,4,5,4,7]]  #NGraphic net
        #self.Net = [[2,3,0,0],[0,4,4,0],[5,6,0,0],[0,0,7,0]]
        #Net = [[1,1,0,0],[0,1,1,0],[1,1,0,0],[0,0,1,0]]
        #Net = [[2,1,1],[3,2,1],[1,1,1]]
        self.Net = Net
        self.flag = flag
        self.resultNum = Num
        self.Number = len(self.Net)
       # print(self.Number,len(self.Net[0]),self.Net)
        self.ux = np.zeros(self.Number,dtype=int) #variable for record path
        self.uy =np.zeros(len(self.Net[0]),dtype=int)
        self.lx,self.ly = np.zeros(self.Number,dtype=float),np.zeros(len(self.Net[0]),dtype=float)  #sign
        self.result = np.zeros(len(self.Net[0]),dtype=int)  #Store the final result
        self.inc = 99999






    def match(self,u):

      #  global inc
        u = int(u)
        self.ux[u] = 1  #record node that was explored
       # print("Matching point:"+str(u))
        for v in range(len(self.Net[0])):
            #if(Net[u][v] == lx[u] + ly[v] and uy[v] == 0):
            if (self.uy[v] == 0):
                t = round(self.lx[u] + self.ly[v],2) - self.Net[u][v]
                if((abs(t)) < 0.1):   #it means here is possible to find a pair
                    #print(str(abs(t))+" is in!")
                    self.uy[v] = 1
                   # print('current result[i]:'+str(self.result[v]))
                    if(self.result[v] == -1 or self.match(self.result[v])):
                        # print("success! the match is :")
                        # print(u,v)
                        self.result[v] = u
                        return 1
                elif(self.inc > t):
                    self.inc = t
                   # print("current inc is :"+str(self.inc))
        return 0

    def Kuh_Munkras(self):
        #initialize lx,ly
        for  k in range(len(self.Net[0])):
            self.result[k] = -1
        for p in range(self.Number):

            self.ly[p] = 0.0
            self.result[p] = -1
            self.lx[p] = -999999.0 #minus infinite
            for q in range(len(self.Net[0])):
                if(self.lx[p] < self.Net[p][q]):    #Choose the biggest value to lx[i]
                    self.lx[p] = self.Net[p][q]

       # print(self.lx,self.ly)

        #find the perfect match
        for u in range(self.Number):
            while(1):
               # time.sleep(1)
                self.inc = 999999  # the minimum gap
                self.coverUsed()
                if(self.match(u)):
                    break

                for i in  range(self.Number):  #Change sign,and try again
                    if (self.ux[i]):
                        self.lx[i] -= self.inc
                    if (self.uy[i]):
                        self.ly[i] += self.inc
                   # print(self.lx[i],self.ly[i])


    def calculateSum(self):
        sum = 0
        if(self.flag == 0):
            for i in range(len(self.Net[0])):
                if(self.result[i] >= self.resultNum ):
                    continue
                sum += self.Net[self.result[i]][i]
        elif(self.flag == 1):
            for i in range(0,self.resultNum ):
                sum += self.Net[self.result[i]][i]
        return sum

    def getResult(self):
        return self.result

    def set_Net(self,Net):
        self.Net = Net

    def coverUsed(self):
        self.ux, self.uy = np.zeros(self.Number, dtype=int), np.zeros(len(self.Net[0]),dtype=int)  # variable for record path



if __name__ == '__main__':
    sum = 0
    Net = []
    if(Net == []):
        print("System is ready to use defaulted setting to start!")
        km = KM_Algorithm()

    else:
        km = KM_Algorithm(Net)

    km.Kuh_Munkras()
    print('final result:')
    print(km.result)
    print(km.calculateSum())



