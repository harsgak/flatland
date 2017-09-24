#flatland


# Imports


import numpy as np
import scipy.ndimage as ndimage
import matplotlib.pyplot as plt
from numba import autojit


# Global variables 
## global items: img, x_max, y_max, DEBUG


img_file = "cut-ring.png"
img = ndimage.imread(img_file, mode = "L")
x_max, y_max = img.shape[0], img.shape[1]
DEBUG=True


# Init Script


plt.imshow(img,origin='lower')
plt.show()
print(img.shape)
print(x_max,y_max)


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
def ray_coords_dda(pos,theta):
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
        

ray_coords_dda([10,10],0.7857) #45deg
ray_coords_dda([10,10],2.3571) #135deg


#@autojit(nopython=False)
def ray_hit(coord,theta):
    # retruns first coloured pixel value.
    x, y = coord
    coord_lst = ray_coords_dda([x,y],theta)
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
    n_points = int((theta_max-theta_min)*(180/np.pi)*theta_res)
    for theta in np.linspace(theta_min,theta_max,n_points):
        out.append(ray_hit(coord,theta))
    return np.array(out).reshape(1,-1)
	
a=angle_view([10,10],[0,2*np.pi],0.1).reshape(1,-1)


def showview(t=0, pos=[0,0], theta=np.pi/4, fig=None, ax=None, theta_res=1, AOV=2*np.pi/3, layout='strip'):
    """
    pos=[x,y] | must be inside image bounds
    theta     | angle(in radians) at which flatlander views.
    theta_res | no of vision cells per unit degree
    AOV       | angle of vision (in radiians)
    
    """
    theta_min, theta_max = theta - AOV/2, theta + AOV/2    #AOV = angle of vision
    theta_range = [theta_min, theta_max]
    view = angle_view(pos,theta_range,theta_res)
    if layout=='strip':
        if not fig:
            fig = plt.figure()
        if not ax:
            ax = fig.add_axes([0, 0, 1, 1])    #Full window
            ax.axis('off')    #no-ticks
        if DEBUG:
            ax = fig.add_subplot(111) #Default axes with ticks etc.
            ax.axis('on')
            pass
        extent= [np.rad2deg(theta_min),np.rad2deg(theta_max),-0.5,0.5]
        plt.imshow(view, aspect=1, origin = 'lower', extent=extent)
    return fig, ax

showview(pos=[2,2]);plt.show()


def draw_ray(pos, theta, img, ax=None, color=128):
    #Note: This draws directly onto image. Does not copy automatically. So pass a copy if required.
    if not ax:
        fig,ax = plt.subplots()
    diagonalxs, diagonalys =  ray_coords_dda(pos, theta).T
    #print (diagonalxs, diagonalys)
    img [diagonalxs, diagonalys] = color
    ax.imshow(img, origin='lower');plt.show()