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
def ray_coord(coord,theta):
    # for ray_([x,y],theta) returns co-ordinates of pixels on that ray
    x, y = coord
    coord_lst = []
    if abs(theta) < np.pi/2:
        for i in range(x+1,x_max):
            temp_y = y+int((i-x)*np.tan(theta))
            if temp_y >= y_max:
                break
            coord_lst.append([i,temp_y])
    else:
        for i in range(0,x):
            temp_y = y-1+int((x-i)*np.tan(theta))
            if temp_y < 0:
                break
            coord_lst.append([i,temp_y])
        coord_lst = coord_lst[::-1]
    return np.array(coord_lst)


@autojit(nopython=False)
def ray_coord_dda(pos,theta):
    """
      \2|1/
      3\|/0
     ---+---
      4/|\7
      /5|6\
    """
    #digital differential analyzer algo
    x0,y0 = pos
    m=np.tan(theta)
    pi = np.pi
    theta = theta%(2*pi)
    coord_lst=[]
    if  0 <= theta < pi/4 : # Octant 0
        for i,x in enumerate(range(x0,x_max)):
            y = int(y0+i*m)
            coord_lst.append([x,y])
    elif pi/4 <= theta < 3*pi/4 : # Octant 1,2
        for i,y in enumerate(range(y0,y_max)):
            x = int(x0+i*1/m)
            coord_lst.append([x,y])
    elif 3*pi/4 <= theta < 5*pi/4 : # Octant 3,4
        for i,x in enumerate(range(x0,0,-1)):
            y = int(x0+i*m)
            coord_lst.append([x,y])
    elif 5*pi/4 <= theta < 7*pi/4 : # Octant 5,6
        for i,y in enumerate(range(y0,0,-1)):
            x = int(y0+i*1/m)
            coord_lst.append([x,y])
    elif 7*pi/4 <= theta < 2*pi : #Octant 7
        for i,x in enumerate(range(x0,x_max)):
            y = int(y0+i*m)
            coord_lst.append([x,y])
    
    return np.array(coord_lst)
        

ray_coord([10,10],0.7857) #45deg
ray_coord([10,10],2.3571) #135deg


#@autojit(nopython=False)
def ray_hit(coord,theta):
    # retruns first coloured pixel value.
    x, y = coord
    coord_lst = ray_coord([x,y],theta)
    ans = 255    #default value
    for i, val in enumerate(coord_lst):
        if img[val[0],val[1]] != 255: # 255 = White in 8bit Binary_Image
            ans = img[val[0],val[1]]
            break
    return ans

a=ray_hit([10,10],2.357) #135
a=ray_hit([10,10],0.7857) #45


def angle_view(coord,theta_range,theta_res):
    # returns array of first coloured pixel value for theta limits.
    # theta_res = scale_resolution ie. 360*x
    theta_min, theta_max = theta_range # min & max - convention should be followed always
    out = []
    for theta in np.linspace(theta_min,theta_max,(theta_max-theta_min)*100*theta_res):
        out.append(ray_hit(coord,theta))
    return np.array(out)
	
a=angle_view([10,10],[0,2*np.pi],0.1)

