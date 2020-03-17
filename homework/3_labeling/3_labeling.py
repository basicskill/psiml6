import numpy as np
import json
from pydantic import BaseModel

def is_bounded(point, box, err=0):
    """ pass joint and box dict """
    if point["x"] - box["x"] < err or point["y"] - box["y"] < err:
        return False
    if point["x"] - box["x"] - box["w"] > err or point["y"] - box["y"] - box["h"] > err:
        return False
    return True

def point2box(point, box):
    """ distance from point to box center """
    x = box["x"] + box["w"] / 2
    y = box["y"] + box["h"] / 2
    # ne mora sqrt!
    return np.sqrt(np.power(point["x"] - x, 2) + np.power(point["y"] - y, 2))

def loadData():
    boxesPath = input()
    jointsPath = input()

    joint_list = json.load(open(jointsPath))["frames"]
    box_list = json.load(open(boxesPath))["frames"]

    return joint_list, box_list

def findIndexes(joint_list, box_list):
    j_indexes = []
    b_indexes = []
    for frame in box_list:
        b_indexes.append(frame["frame_index"]) 
    for frame in joint_list:
        j_indexes.append(frame["frame_index"]) 
    j_indexes = sorted(j_indexes)
    b_indexes = sorted(b_indexes)

    return j_indexes, b_indexes

def interpolate(j_json, b_json, j_indexes, b_indexes):
    """ aproximate missing frames """
    print("TODO: Nejednaki indeksi!")

def calcPointDict(joint_list, box_list, indexes, err=0):
    jointDict = dict()
    interactions = dict()
     
    for jFrame, bFrame in zip(joint_list, box_list):
        for joint in jFrame["joints"]:
            if not joint["identity"] in jointDict:
                jointDict[joint["identity"]] = set()
                interactions[joint["identity"]] = set()
                for box in bFrame["bounding_boxes"]:
                    interactions[joint["identity"]].add(box["identity"])
                    if is_bounded(joint["joint"], box["bounding_box"], err):
                        jointDict[joint["identity"]].add(box["identity"])
            else:
                for box in bFrame["bounding_boxes"]:
                    if not box["identity"] in interactions[joint["identity"]]:
                        if is_bounded(joint["joint"], box["bounding_box"], err):
                            jointDict[joint["identity"]].add(box["identity"])
                    


                    if (box["identity"] in jointDict[joint["identity"]]):
                        if (box["identity"] in jointDict[joint["identity"]]) and (
                            not is_bounded(joint["joint"], box["bounding_box"])):
                                jointDict[joint["identity"]].remove(box["identity"])
    return jointDict
                    
def printDict(d):
    for key in d:
        print(f"{key}:{d[key]}")


def main():
    err = 0.0001
    joint_list, box_list = loadData()

    j_idx, b_idx = findIndexes(joint_list, box_list)
    if (j_idx != b_idx):
        interpolate(joint_list, box_list, j_idx, b_idx)
    
    joint_list = sorted(joint_list, key=lambda k: k["frame_index"])
    box_list = sorted(box_list, key=lambda k: k["frame_index"])

    jointDict = calcPointDict(joint_list, box_list, j_idx, err)
    printDict(jointDict)

if __name__ == "__main__":
    main()