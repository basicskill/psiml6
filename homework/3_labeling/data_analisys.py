import json

def data_analisys():
    for i in range(0, 16):
        jointsPath = f"public/set/{i}/joints.json"
        boxesPath = f"public/set/{i}/bboxes.json"

        joint_json = json.load(open(jointsPath))
        box_json = json.load(open(boxesPath))

        mB = 0
        mJ = 0

            

        for bFrame, jFrame in zip(box_json["frames"], joint_json["frames"]):
            mB = max(mB, len(bFrame["bounding_boxes"]))
            mJ = max(mJ, len(jFrame["joints"]))

        print(f"{i}. -> frames: {len(joint_json['frames'])}, maxJ: {mJ}, maxB: {mB}")

        if len(box_json["frames"]) != len(joint_json["frames"]):
            print(f'{len(box_json["frames"])} != {len(joint_json["frames"])}')
        j = []
        b = []
        for frame in box_json["frames"]:
            b.append(frame["frame_index"]) 
        for frame in joint_json["frames"]:
            j.append(frame["frame_index"]) 
        j = sorted(j)
        b = sorted(b)
        if (j != b):
            print(j)
            print(b)

if __name__ == "__main__":
    data_analisys()
    # TEMP
    # set starting positions
    # if int(j_list[0]["frame_index"]) > int(b_list[0]["frame_index"]):
    #     l_bound = int(j_list[0]["frame_index"])
    #     # Pazi iskakanje iz granica liste!!!
    #     while int(b_list[idxB+1]["frame_index"]) < l_bound:
    #         idxB += 1
    #         if int(b_list[idxB+1]["frame_index"]) == l_bound:
    #             break
    # elif int(j_list[0]["frame_index"]) < int(b_list[0]["frame_index"]):
    #     l_bound = int(b_list[0]["frame_index"])
    #     # Pazi iskakanje iz granica liste!!!
    #     while int(j_list[idxJ+1]["frame_index"]) < l_bound:
    #         idxJ += 1
    #         if int(j_list[idxJ+1]["frame_index"]) == l_bound:
    #             break