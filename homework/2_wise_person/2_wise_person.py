import os
import sys
import numpy as np
from collections import deque


def readData(rootFolder):
    structuredData = dict()
    waitingCA = dict()
    waitingWPA = dict()

    positives = 0
    negatives = 0

    # Go through all nested directories
    for root, _, files in os.walk(rootFolder):

        # Read all files in current dir
        for name in files:
            
            # Read data
            index = name[name.find('a')+1:name.find('.')]
            data = open(os.path.join(root, name)).read() 


            if name[0:2].lower() == "ca":
                data = data == "Yes"

                if data:
                    positives += 1
                else:
                    negatives += 1

                if index in waitingWPA:
                    structuredData[index] = (
                        data, waitingWPA.pop(index, None)
                    )
                else:
                    waitingCA[index] = data
            else:
                data = int(data[:-1])
                if index in waitingCA:
                    structuredData[index] = (
                        waitingCA.pop(index, None), data 
                    )
                else:
                    waitingWPA[index] = data
    return structuredData, f"{positives},{negatives},{len(structuredData)},"

def dict2hist(dictData):
    pos = np.zeros(101)
    neg = np.zeros(101)

    for index in dictData:
        solution, answer = dictData[index]

        if solution:
            pos[answer] += 1
        else:
            neg[answer] += 1
    
    return pos, neg


def calculateRates(pos, neg):

    threshold = 70
    
    TPR = round(pos[threshold:].sum() / pos.sum(), 3)
    FPR = round(neg[threshold:].sum() / neg.sum(), 3)

    return f"{TPR},{FPR},"

def calculateEER(pos, neg):
    mi = neg.sum() / pos.sum()
    eps = 0.05

    
    # for T in range(100, 0, -1):
    for T in range(101):
        FP = neg[T:].sum()
        FN = pos[:T].sum()

        if (FP == 0) or (FN == 0):
            continue
        
        if abs(FP / FN - mi) <= eps:
            return f"{round(neg[T:].sum() / neg.sum(), 3)}"

    return "ERROR"

def main():

    rootFolder = input()
    dictData, firstHalf = readData(rootFolder)
    pos, neg = dict2hist(dictData) 
    secondHalf = calculateRates(pos, neg)
    EER = calculateEER(pos, neg)
    print(firstHalf + secondHalf + EER)


if __name__ == "__main__":
    main()