import numpy as np
from PIL import Image
import time
import scipy.ndimage


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

def preprocess(world):
    height, width = world.shape

    # Filter calculations
    w = 3
    sigma = 0.5
    gaus = np.array([[1, 2, 1],
                     [2, 5, 2],
                     [1, 2, 1]])
    T = 0.6

    Iy = np.zeros((height + w - 1, width + w - 1))
    Iy[w//2+1:-w//2+1, w//2:-w//2+1] = np.diff(world, axis=0)
    Iy[w//2, w//2+1:-w//2+1] = Iy[w//2+1, w//2+1:-w//2+1]

    Ix = np.zeros((height + w - 1, width + w - 1))
    Ix[w//2:-w//2+1, w//2+1:-w//2+1] = np.diff(world, axis=1)
    Ix[w//2+1:-w//2+1, w//2] = Ix[w//2+1:-w//2+1, w//2+1]

    c = np.zeros(world.shape)
    H = np.zeros((2, 2))
    Ix = np.power(Ix, 2)
    Iy = np.power(Iy, 2)
    start_time = time.time()
    for y in range(0, c.shape[0]):
        for x in range(0, c.shape[1]):
            subIx = Ix[y:y+w, x:x+w]
            subIy = Iy[y:y+w, x:x+w]

            a = (gaus * subIx).sum()
            
            b = (gaus * (subIx * subIy)).sum()
            
            d = (gaus * subIy).sum()

            c[y, x] = a*d - np.power(b, 2) - 0.1 * (a + d)

    

    print(f"--- Preproces time: {round(time.time() - start_time, 2)} seconds ---")
            
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

    preprocess(worldMap)

    for path, solution in zip(patchPaths, answers):
        print(path)
        imageFile = Image.open(path)
        patch = rgb2gray(np.array(imageFile))
        # Locate hire
        # TODO
        print(f"guess: {x, y} -- solution: {solution}")



if __name__ == "__main__":
    start_time = time.time()
    main()
    print(f"--- {round(time.time() - start_time, 2)} seconds ---")