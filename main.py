#flatland


print("Hello 2D world")


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
        for i in range(x+1,x_max+1):
            coord_lst.append([i,y+int((i-x)*np.tan(o))])
    else:
        for i in range(0,x):
            coord_lst.append([i,y-1+int((x-i)*np.tan(o))])
		coord_lst = coord_lst[::-1]
    return np.array(coord_lst)

ray_coord([10,10],0.7857) #45deg
ray_coord([10,10],2.3571) #135deg

