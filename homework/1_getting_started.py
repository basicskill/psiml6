import numpy as np
from PIL import Image

if __name__ == "__main__":
    image_path = input()
    image_file = Image.open(image_path)
    image = np.array(image_file)
    pixel = image[0, 0]
    print(f"Red: {pixel[0]}")
    print(f"Green: {pixel[1]}")
    print(f"Blue: {pixel[2]}")