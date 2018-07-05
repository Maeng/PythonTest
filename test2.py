
# coding: utf-8

workArrStr = input("Input Array of works : ")
workArr = list(map(int, workArrStr.replace("[", "").replace("]", "").split(",")))

remainTime = input("Input remained work time : ")
remainTime = int(remainTime)

import numpy as np

def checkFatigue(arr, time) : 
    for _ in range(time) :
        #print(arr)
        if arr[np.argmax(arr)] > 0 : 
            arr[np.argmax(arr)] -= 1
        if sum(arr) == 0 :
            return 0
    
    return sumOfSqr(arr)

def sumOfSqr(workArr) :
    sqrArr = np.square(workArr)
    return sum(sqrArr)


print(checkFatigue(workArr, remainTime))




