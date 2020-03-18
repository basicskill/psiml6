import numpy as np
import json

def keysWithMaxVal(d):
    return [key for key in d if d[key] == max(d.values())]

def is_bounded(point, box, err=0):
    """ pass joint and box dict """
    if point["x"] - box["x"] < err or point["y"] - box["y"] < err:
        return False
    if point["x"] - box["x"] - box["w"] > err or point["y"] - box["y"] - box["h"] > err:
        return False
    return True

def point2box(point, box):
    """ distance from point to x, y of box """
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

def sameIndexes(joint_list, box_list):
    j_indexes = []
    b_indexes = []
    for frame in box_list:
        b_indexes.append(frame["frame_index"]) 
    for frame in joint_list:
        j_indexes.append(frame["frame_index"]) 
    j_indexes = sorted(j_indexes)
    b_indexes = sorted(b_indexes)

    return j_indexes == b_indexes

def interJointFrame(leftFrame, rightFrame, frame_index):

    result = {"frame_index": frame_index, "joints": []}

    for left in leftFrame["joints"]:
        for right in rightFrame["joints"]:
            if left["identity"] == right["identity"]:
                result["joints"].append(interJoint(left, right, 
                        leftFrame["frame_index"], rightFrame["frame_index"], 
                        frame_index))

    return result

def interBoxFrame(leftFrame, rightFrame, frame_index):
    result = {"frame_index": frame_index, "bounding_boxes": []}

    for left in leftFrame["bounding_boxes"]:
        for right in rightFrame["bounding_boxes"]:
            if left["identity"] == right["identity"]:
                result["bounding_boxes"].append(interBox(left, right, 
                        leftFrame["frame_index"], rightFrame["frame_index"], 
                        frame_index))

    return result

def interJoint(left, right, f0, f1, frame):
    l = left["joint"]
    r = right["joint"]

    newJoint = {"identity": left["identity"], "joint": {}}

    newJoint["joint"]["x"] = l["x"] + ((r["x"] - l["x"])/(f1 - f0)) * (frame - f0)
    newJoint["joint"]["y"] = l["y"] + ((r["y"] - l["y"])/(f1 - f0)) * (frame - f0)

    return newJoint

def interBox(left, right, f0, f1, frame):
    l = left["bounding_box"]
    r = right["bounding_box"]

    newBox = {"identity": left["identity"], "bounding_box": {}}

    newBox["bounding_box"]["x"] = l["x"] + ((r["x"] - l["x"])/(f1 - f0)) * (frame - f0)
    newBox["bounding_box"]["y"] = l["y"] + ((r["y"] - l["y"])/(f1 - f0)) * (frame - f0)
    newBox["bounding_box"]["w"] = max(l["w"], r["w"]) + 0.005
    newBox["bounding_box"]["h"] = max(l["h"], r["h"]) + 0.005

    return newBox

def interpolate(j_list, b_list):
    """ aproximate missing frames """
    newJ = []
    newB = [] 

    l_bound = max(j_list[0]["frame_index"], b_list[0]["frame_index"])
    r_bound = min(j_list[-1]["frame_index"], b_list[-1]["frame_index"])

    j_idx = set([x["frame_index"] for x in j_list if x["frame_index"] >= l_bound and x["frame_index"] <= r_bound])
    b_idx = set([x["frame_index"] for x in b_list if x["frame_index"] >= l_bound and x["frame_index"] <= r_bound])
    overlap = sorted(list(j_idx.union(b_idx)))

    idx = 0
    while j_list[idx]["frame_index"] < l_bound:
        idx += 1

    for frame_index in overlap:
        if j_list[idx]["frame_index"] == frame_index:
            newJ.append(j_list[idx])
            idx += 1
        else:
            newJ.append(interJointFrame(j_list[idx-1], j_list[idx], frame_index))

    idx = 0
    while b_list[idx]["frame_index"] < l_bound:
        idx += 1

    for frame_index in overlap:
        if b_list[idx]["frame_index"] == frame_index:
            newB.append(b_list[idx])
            idx += 1
        else:
            newB.append(interBoxFrame(b_list[idx-1], b_list[idx], frame_index))

    # print("== Joints ==")
    # for i in newJ:
    #     print(i)
    # print("==  Boxes ==")
    # for i in newB:
    #     print(i)
    # print("============")
    return newJ, newB


def calcPointDict(joint_list, box_list, err=0):
    jointDict = dict()
    interactions = dict()
     
    for jFrame, bFrame in zip(joint_list, box_list):
        for joint in jFrame["joints"]:
            if not joint["identity"] in jointDict:
                jointDict[joint["identity"]] = dict()
                for box in bFrame["bounding_boxes"]:
                    if is_bounded(joint["joint"], box["bounding_box"], err):
                        jointDict[joint["identity"]][box["identity"]] = 1
            else:
                for box in bFrame["bounding_boxes"]:
                    if is_bounded(joint["joint"], box["bounding_box"], err):
                        if box["identity"] in jointDict[joint["identity"]]:
                            jointDict[joint["identity"]][box["identity"]] += 1
                        else:
                            jointDict[joint["identity"]][box["identity"]] = 1

    return jointDict

def fineTune(joint_list, box_list, d, key, letters):
    distances = dict()
    for k in letters:
        distances[k] = 0
                    
    for jFrame, bFrame in zip(joint_list, box_list):

        # Find joint location in frame
        for j in jFrame["joints"]:
            if j["identity"] == key:
                joint = j["joint"]
                break
        if j["identity"] != key:
            continue

        # Calculate distance for interesting boxes
        for box in bFrame["bounding_boxes"]:
            if box["identity"] in letters:
                distances[box["identity"]] += point2box(joint, box["bounding_box"])

    v = list(distances.values())
    k = list(distances.keys())
    try:
        return k[v.index(min(v))]
    except:
        return None

def main():
    err = 0.01
    joint_list, box_list = loadData()

    joint_list = sorted(joint_list, key=lambda k: k["frame_index"])
    box_list = sorted(box_list, key=lambda k: k["frame_index"])

    if (not sameIndexes(joint_list, box_list)):
        joint_list, box_list = interpolate(joint_list, box_list)
    
    jointDict = calcPointDict(joint_list, box_list, err)


    surePredictions = []

    indexes = sorted([int(x) for x in list(jointDict)])
    for key in indexes:
        key = str(key)
        letters = keysWithMaxVal(jointDict[key])
        if len(letters) != 1:
            continue
            letter = fineTune(joint_list, box_list, jointDict[key], key, letters)

        letter = letters[0]
        surePredictions.append((key, letter))

        print(f"{key}:{letter}")

    for key, letter in surePredictions:
        jointDict.pop(key, None)
        for key2 in jointDict:
            if letter in jointDict[key2]:
                jointDict[key2].pop(letter, None)

    for key in jointDict:
        letters = keysWithMaxVal(jointDict[key])
        if len(letters) != 1:
            letter = fineTune(joint_list, box_list, jointDict[key], key, letters)
        else:
            letter = letters[0]

        if letter == None:
            continue

        print(f"{key}:{letter}")



if __name__ == "__main__":
    main()