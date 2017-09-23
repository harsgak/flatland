#flatland


print("Hello 2D world")


# IMP Notes
"""global variables"""
#img, x_max, y_max
from scipy import ndimage
import matplotlib.pyplot as plt

img_file = "im1.png"
img = ndimage.imread(img_file, mode = "L")
x_max, y_max = img.shape[0], img.shape[1]


plt.imshow(img)
plt.show()

print(img.shape)
print(x_max,y_max)


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
            temp_y = y+int((i-x)*np.tan(o))
            if temp_y >= y_max:
                break
            coord_lst.append([i,temp_y])
    else:
        for i in range(0,x):
            temp_y = y-1+int((x-i)*np.tan(o))
            if temp_y < 0:
                break
            coord_lst.append([i,temp_y])
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
        if img[val[0],val[1]] != 255: # 255 = White in 8bit Binary_Image
            ans = img[val[0],val[1]]
            break
        else:
            ans = 255
    return ans

a=ray_hit([10,10],2.357) #135
a=ray_hit([10,10],0.7857) #45


def angle_view(coord,o_range,o_res):
    # returns array of first coloured pixel value for theta limits.
    # o_res = scale_resolution ie. 360*x
    o_min, o_max = o_range # min & max - convention should be followed always
    out = []
    for theta in np.linspace(o_min,o_max,(o_max-o_min)*100*o_res):
        out.append(ray_hit(coord,theta))
    return np.array(out)
	
a=angle_view([10,10],[0.7857,2.357],0.1) #some_error_???

