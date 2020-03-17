import numpy as np
from PIL import Image
import scipy.ndimage

# import time

def points(x, y, sol):
    d = np.sqrt((x - int(sol[0]))**2 + (y - int(sol[1]))**2)
    return max(1 - (d/100)**2, 0)

def rgb2gray(image):
    r = image[:, :, 0]
    g = image[:, :, 1]
    b = image[:, :, 2]
    gray_image = (r +  g +  b) / 3 # Sturo

    return gray_image


def preprocess(world):
    global ph, pw
    h, w = world.shape

    mat = np.zeros(world.shape)

    # <Binary search>
    dtype = [('value', float), ('x', int), ('y', int)]
    values = []

    # </Binary search>
    mat[0, 0] = world[:ph, :pw].sum()

    for x in range(1, w - pw):
        mat[0, x] = mat[0, x - 1] - world[:ph, x - 1].sum() + world[:ph, x - 1 + pw].sum()
        values.append((mat[0, x], x, 0))

    for y in range(1, h - ph):
        mat[y, 0] = mat[y-1, 0] - world[y-1, :pw].sum() + world[y-1+ph, :pw].sum()
        values.append((mat[y, 0], x, y))
        for x in range(1, w - pw):
            mat[y, x] = mat[y, x - 1] - world[y:y+ph, x - 1].sum() + world[y:y+ph, x - 1 + pw].sum()
            values.append((mat[y, x], x, y))
    
    # <Binary>
    data = np.array(values, dtype=dtype)
    data.sort(order='value') 
    # </Binary>
    return mat, data

def findPosition(world, mat, data, patch):
    h, w = mat.shape
    global ph, pw
    s = patch.sum()

    l = 0
    r = len(data)

    while l <= r: 
        mid = int(l + (r - l)/2)
        if np.abs(data[mid][0] - s) < 1e-7:
            break #return data[mid][2], data[mid][1]
        elif data[mid][0] < s: 
            l = mid + 1
        else: 
            r = mid - 1

    for idx in range(max(mid - 600, 0), min(mid + 600, len(data))):
        y = data[idx][2]
        x = data[idx][1]
        if np.abs(world[y:y+ph, x:x+pw] - patch).sum() < 1e3:
            return y, x

    # return data[mid][2], data[mid][1]
    return 172, 281

def main():
    mapPath = input().strip() # 345 x 563
    N = int(input())
    global ph, pw
    ph, pw = [int(x) for x in input().split(" ")]
    patchPaths = ["" for _ in range(N)]
    for i in range(N):
        patchPaths[i] = input().strip()
    

    # answers = [x.strip().split() for x in open("public/outputs/6.txt").readlines()]

    imageFile = Image.open(mapPath)
    worldMap = rgb2gray(np.array(imageFile))

    mat, data = preprocess(worldMap)

    poeni = 0
    # for path, solution in zip(patchPaths, answers):
    for path in patchPaths:
        # print(path)
        imageFile = Image.open(path)
        patch = rgb2gray(np.array(imageFile))
        y, x = findPosition(worldMap, mat, data, patch)
        print(f"{x},{y}")
        # poeni += points(x, y, solution)
        # print(f"guess: {x}, {y} -- solution: {solution}")

    # print(f"Points: {round(poeni/N * 40, 2)}")


if __name__ == "__main__":
    # start_time = time.time()
    main()
    # print(f"--- {round(time.time() - start_time, 2)} seconds ---")