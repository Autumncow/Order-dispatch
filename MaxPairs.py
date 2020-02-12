import numpy as np
Number = 4
Net = [[0,1,0,1],[0,1,1,0],[0,0,1,0],[0,0,1,0]]
ux , uy = np.zeros(Number,dtype=int),np.zeros(Number,dtype=int)
result = np.zeros(Number,dtype=int)

def match(u):
    #  global inc
    u = int(u)
    ux[u] = 1  # record node that was explored
    for v in range(Number):
        if (uy[v] == 0 and Net[u][v] == 1):  #
                uy[v] = 1

                if (result[v] == -1 or match(result[v])):
                    result[v] = u
                    return 1
    return 0

def CoverUsed():
    global ux,uy
    ux, uy = np.zeros(Number, dtype=int), np.zeros(Number, dtype=int)

if __name__ == '__main__':
    for k in range(Number):
        result[k] = -1
    sum = 0
    for i in range(Number):
        CoverUsed()
        if(match(i)):
            sum += 1
    print("Here are "+str(sum)+" pairs\n")
    for j in range(Number):
        if(result[j] == -1):
            continue
        else:
            print(result[j],j)