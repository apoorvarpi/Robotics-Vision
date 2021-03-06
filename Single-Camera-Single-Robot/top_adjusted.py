#!/usr/bin/env python

import cv2
import numpy as np
from utils import get_four_points
import math

def final_pers_adj(name, name1, xx) :

    M2 = np.load("./Matrices/Base.npy")
    # Reading the image.
    im_src = cv2.imread(name)
    im_base = cv2.imread("./input/Base.jpg")

    # Show image and wait for 4 clicks.
    pts_src = get_four_points(im_src,"Image")
    pts_src = np.float32(pts_src)

    pts_base = get_four_points(im_base, "Image")
    pts_base = np.float32(pts_base)
    #print(M2)
    #print(pts_base)

    #calculate dimensions
    minx = 9999999
    miny = 9999999
    maxx = 0
    maxy = 0
    for i in range(0,4):
        x = pts_base[i][0]
        y = pts_base[i][1]
        if x>maxx:
            maxx = x
        if x<minx:
            minx = x
        if y>maxy:
            maxy = y
        if y<miny:
            miny = y

    #size of base marked
    a = int(maxx - minx)
    b = int(maxy - miny)

    #finding size of complete image
    cols = (M2[1][0]-M2[0][0])
    rows = (M2[3][1]-M2[0][0])

    #translation works
    xtranslate = (pts_base[0][0]-M2[0][0])
    ytranslate = (pts_base[0][1]-M2[0][1])
    print(xtranslate," ",ytranslate)
    if xtranslate<=10.0:
        xtranslate = 0
    if ytranslate<=10.0:
        ytranslate = 0

    #normalise co-ordinates
    for i in range(0,4):
        pts_base[i][0] = (pts_base[i][0] - minx)
        pts_base[i][1] = (pts_base[i][1] - miny)

    # Calculate the homography
    M = cv2.getPerspectiveTransform(pts_src, pts_base)
    name = "./Matrices/C"+str(xx)
    np.save(name, M)
    # Warp source image to destination
    im_dst = cv2.warpPerspective(im_src, M, (a, b))

    M1 = np.float32([[1,0,xtranslate],[0,1,ytranslate],[0,0,1]])
    im_fin = cv2.warpPerspective(im_dst,M1,(int(cols),int(rows)))
    Mx = np.dot(M,M1)
    #print (str(Mx))
    nnn = name+"s"
    np.save(nnn,Mx)
    cv2.imshow("Image", im_fin)
    cv2.imwrite(name1, im_fin)
    cv2.waitKey(0)
