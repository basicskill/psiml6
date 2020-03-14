from collections import deque
import os
import sys


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

            # print(index)

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


def calculateRates(structuredData):
    positives = 0
    negatives = 0

    TPR = 0
    FPR = 0

    # Calculate TPR and FPR for T = 70%
    for index in structuredData:
        solution, answer = structuredData[index]
        if solution:
            positives += 1
            TPR += (answer >= 70)
        else:
            negatives += 1
            FPR += (answer >= 70)
    
    TPR = round(TPR / positives, 3)
    FPR = round(FPR / negatives, 3)

    return f"{TPR},{FPR},"


def main():

    rootFolder = input()
    structuredData, firstHalf = readData(rootFolder)
    secondHalf = calculateRates(structuredData)

    print(firstHalf + secondHalf)


if __name__ == "__main__":
    main()