#flatland


print("Hello 2D world")


# IMP Notes
"""global variables"""
#img, x_max, y_max


# imports


from numba import autojit
import numpy as np


# Functions


@autojit(nopython=False)
def ray_coord(coord,o):
    # for ray_([x,y],o) returns co-ordinates of pixels of on that ray
    x, y = coord
    coord_lst = []
    if abs(o) < np.pi/2:
        for i in range(x+1,x_max):
            coord_lst.append([i,y+int((i-x)*np.tan(o))])
    else:
        for i in range(0,x):
            coord_lst.append([i,y-1+int((x-i)*np.tan(o))])
        coord_lst = coord_lst[::-1]
    return np.array(coord_lst)

ray_coord([10,10],0.7857) #45deg
ray_coord([10,10],2.3571) #135deg


#@autojit(nopython=False)
def ray_hit(coord,o):
    # retruns first coloured pixel value.
    x, y = coord
    coord_lst = ray_coord([x,y],o)
    for i, val in enumerate(coord_lst):
        #print(img[val[0],val[1]])
        if img[val[0],val[1]] != 255: # 255 = White in 8bit Binary_Image
            ans = img[val[0],val[1]]
            break
        else:
            ans = 255
    return ans

a=ray_hit([10,10],2.357) #135
a=ray_hit([10,10],0.7857) #45

