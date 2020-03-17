import numpy as np
import os
import sys
from PIL import Image
import time

import cv2

def show(m):
    cv2.imshow("Slika", m / 255)
    cv2.waitKey(0)
    cv2.destroyAllWindows()


def rgb2gray(image):
    b = image[:, :, 2]
    g = image[:, :, 1]
    r = image[:, :, 0]
    gray_image = (r +  g +  b) / 3 # Sturo

    return gray_image

# Euclidean distance
def D(m1, m2):
    return np.power(m1 * m2 ,2).sum()


def findPatch(world, patch):
    global h, w
    R = np.zeros(world.shape)
    for y in range(world.shape[0] - h):
        for x in range(world.shape[1] - w):
            R[y, x] = D(patch, world[y:y+h, x:x+w])
    show(R / np.max(R))

    return np.unravel_index(np.argmax(R), R.shape)


def points(x, y, sol):
    d = np.sqrt((x - int(sol[1]))**2 + (y - int(sol[0]))**2)
    return max(1 - (d/100)**2, 0)

def main():
    mapPath = input().strip() # 345 x 563
    N = int(input())
    global h, w
    h, w = [int(x) for x in input().split(" ")]
    patchPaths = ["" for _ in range(N)]
    for i in range(N):
        patchPaths[i] = input().strip()
    

    answers = [x.strip().split() for x in open("public/outputs/0.txt").readlines()]


    imageFile = Image.open(mapPath)
    worldMap = rgb2gray(np.array(imageFile))
    show(worldMap)
    poeni = 0
    for path, solution in zip(patchPaths, answers):
        print(path)
        imageFile = Image.open(path)
        patch = rgb2gray(np.array(imageFile))
        show(patch)
        x, y = findPatch(worldMap, patch)
        print(f"guess: {x, y} -- solution: {solution}")
        poeni += points(x, y, solution)

    print(f"Points: {round(poeni/N * 40, 2)}")

if __name__ == "__main__":
    start_time = time.time()
    main()
    print(f"--- {round(time.time() - start_time, 2)} seconds ---")