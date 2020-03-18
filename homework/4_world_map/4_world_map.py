import numpy as np
from PIL import Image
from scipy.ndimage import sobel, gaussian_filter

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

def binarySearch(data, target, l, r):
    while l <= r: 
        mid = int(l + (r - l)/2)
        if np.abs(data[mid][0] - target) < 1:
            return mid
        elif data[mid][0] < target: 
            l = mid + 1
        else: 
            r = mid - 1
    return mid

def findPosition(world, mat, data, patch):
    h, w = mat.shape
    global ph, pw, N
    s = patch.sum()

    l = 0
    r = len(data)

    mid = binarySearch(data, s, 0, len(data))

    if N < 2000:
        offset = 600
    else:
        offset = int(1.5*1e8/(N*pw*ph))
    
    y_m = data[mid][2]
    x_m = data[mid][1]
    min_eps  = np.abs(world[y_m:y_m+ph, x_m:x_m+pw] - patch).sum()

    for idx in range(max(mid - offset, 0), min(mid + offset, len(data))):
        y = data[idx][2]
        x = data[idx][1]
        eps  = np.abs(world[y:y+ph, x:x+pw] - patch).sum()
        if eps < min_eps:
            min_eps = eps
            y_m = y
            x_m = x
        if min_eps < 1e-2:
            break

    return y_m, x_m

    # return data[mid0][2], data[mid0][1]
    # return 172, 281

def main():
    mapPath = input().strip() # 345 x 563
    global N
    N = int(input())
    global ph, pw
    ph, pw = [int(x) for x in input().split(" ")]
    patchPaths = ["" for _ in range(N)]
    for i in range(N):
        patchPaths[i] = input().strip()
    

    # answers = [x.strip().split() for x in open("public/outputs/7.txt").readlines()]
    poeni = 0

    imageFile = Image.open(mapPath)
    worldMap = rgb2gray(np.array(imageFile))
    # worldMap = gaussian_filter(worldMap, 0.9) # filter

    mat, data = preprocess(worldMap)

    # for path, solution in zip(patchPaths, answers):
    for path in patchPaths:

        imageFile = Image.open(path)
        patch = rgb2gray(np.array(imageFile))
        # patch = gaussian_filter(patch, 0.5) # filter

        y, x = findPosition(worldMap, mat, data, patch)

        print(f"{x},{y}")
        # poeni += points(x, y, solution)

    # print(f"Points: {round(poeni/N * 40, 2)}")


if __name__ == "__main__":
    # start_time = time.time()
    main()
    # print(f"--- {round(time.time() - start_time, 2)} seconds ---")