from perspective_new import *
from top_adjusted import *
import cv2
import numpy as np
from utils import get_four_points

def main(size):
    im_base = cv2.imread("./input/Base.jpg")
    print('mark complete base')
    M = get_four_points(im_base, "Image")

    name = "./Matrices/Base.npy"
    np.save(name,M);
    print('Now mark for individual images')
    for i in range(1,size+1):
        name = "./input/C"+str(i)+"/bw.jpg"
        name1 = "./input/C"+str(i)+"/perss2.jpg"
        final_pers_adj(name, name1, i)

main(2)
