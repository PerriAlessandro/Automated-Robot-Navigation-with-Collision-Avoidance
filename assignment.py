from __future__ import print_function

import time
import numpy as np
from sr.robot import *

"""
Exercise 3 python script

Put the main code after the definition of the functions. The code should make the robot:
	- 1) find and grab the closest silver marker (token)
	- 2) move the marker on the right
	- 3) find and grab the closest golden marker (token)
	- 4) move the marker on the right
	- 5) start again from 1

The method see() of the class Robot returns an object whose attribute info.marker_type may be MARKER_TOKEN_GOLD or MARKER_TOKEN_SILVER,
depending of the type of marker (golden or silver).
Modify the code of the exercise2 to make the robot:

1- retrieve the distance and the angle of the closest silver marker. If no silver marker is detected, the robot should rotate in order to find a marker.
2- drive the robot towards the marker and grab it
3- move the marker forward and on the right (when done, you can use the method release() of the class Robot in order to release the marker)
4- retrieve the distance and the angle of the closest golden marker. If no golden marker is detected, the robot should rotate in order to find a marker.
5- drive the robot towards the marker and grab it
6- move the marker forward and on the right (when done, you can use the method release() of the class Robot in order to release the marker)
7- start again from 1

	When done, run with:
	$ python run.py solutions/exercise3_solution.py

"""


a_th = 2.0
""" float: Threshold for the control of the linear distance"""

d_th = 0.4
""" float: Threshold for the control of the orientation"""

silver = True
""" boolean: variable for letting the robot know if it has to look for a silver or for a golden marker"""

R = Robot()
""" instance of the class Robot"""


def drive(speed, seconds):
    """
    Function for setting a linear velocity

    Args: speed (int): the speed of the wheels
	  seconds (int): the time interval
    """
    R.motors[0].m0.power = speed
    R.motors[0].m1.power = speed
    time.sleep(seconds)
    R.motors[0].m0.power = 0
    R.motors[0].m1.power = 0


def turn(speed, seconds):
    """
    Function for setting an angular velocity

    Args: speed (int): the speed of the wheels
	  seconds (int): the time interval
    """
    R.motors[0].m0.power = speed
    R.motors[0].m1.power = -speed
    time.sleep(seconds)
    R.motors[0].m0.power = 0
    R.motors[0].m1.power = 0


def find_silver_token():
    """
    Function for retrieving the distance and the angle between the robot and the closest silver token

    Returns:
	dist (float): distance of the closest silver token (-1 if no silver token is detected)
	rot_y (float): angle between the robot and the silver token (-1 if no silver token is detected)
    """
    dist = 100
    for token in R.see():
        if token.dist < dist and token.info.marker_type is MARKER_TOKEN_SILVER:
            dist = token.dist
	    rot_y = token.rot_y
    if dist == 100:
    	return -1, -1
    else:
    	return dist, rot_y


def grab_silver():
	"""
	Function to detect the closest silver token, move forward to it and grab it. After these steps, the robot will turn behind himself, release the token and turn back to the initial position

	"""
	print("SILVER TOKEN DETECTED! LET'S GRAB IT..")
	finished = False # bool: finished is false until the silver token is released and the robot is turned back to his initial position
	while(not finished):
		dist, rot_y = find_silver_token() #retrieving information to manage the process
		if dist == -1:  # if no token is detected, we make the robot turn
			print("I don't see any token!!")
			turn(+10, 1)
	    	elif dist < d_th:  # if we are close to the token, we try grab it.
			print("Found it!")
			if R.grab():  # if we grab the token, we move the robot forward and on the right, we release the token, and we go back to the initial position
			    print("Gotcha!")
		    	    turn(37, 2.5) #turn (+180 degrees)
			    R.release()
			    turn(-37, 2.5) #turn (-180 degrees)
			    finished = True

			else:
			    print("Aww, I'm not close enough.")
			    finished = False
	    	elif -a_th <= rot_y <= a_th:  # if the robot is well aligned with the token, we go forward
		    print("Ah, that'll do.")
		    drive(50, 0.5)
	    	elif rot_y < -a_th:  # if the robot is not well aligned with the token, we move it on the left or on the right
		    print("Left a bit...")
		    turn(-2, 0.5)
	    	elif rot_y > a_th:
		    print("Right a bit...")
		    turn(+2, 0.5)


def find_frontal_token(range=30):
    """
    Function to find the closest golden token in a angle between the specified range(i.e. the frontal portion of the robot view)
    
    Args: 
    range (float): positive range in which we want to find the token, default: 30
	
    Returns:
	dist (float): distance of the closest golden token in the specified range(-1 if no golden token is detected)
    """
    
    dist =100
    rot_y = -100   
    for token in R.see():
        if token.dist < dist and token.info.marker_type is MARKER_TOKEN_GOLD and -range < token.rot_y < +range:
            dist = token.dist
	    rot_y = token.rot_y
    if dist == 100:
     return -1
    else:
   	 return dist


def find_lateral_token(range=[80,100]):

	"""
	Function to find the mean of the distances of the two closest golden token on the left and the right portions of the robot view
	Args:
	range (int[]):list of the two positive angles in which the robot will search for
	Returns:
	mean_l (float): mean distance of the two closest golden token on the left
	mean_r (float): mean distance of the two closest golden token on the right
	"""
    
	dist_l_1 = dist_l_2 = dist_r_1 =dist_r_2= 100

	for token in R.see():
		if(token.info.marker_type is MARKER_TOKEN_GOLD and token.dist < 2.5):
			if token.dist < dist_l_1 and -range[1] < token.rot_y < -range[0] :
			    dist_l_1 = token.dist
			    dist_l_2 = dist_l_1
			if token.dist < dist_r_1 and range[0] < token.rot_y < range[1] :
			    dist_r_1 = token.dist
			    dist_r_2 = dist_r_1
	mean_l = np.mean((dist_l_1, dist_l_2))  #mean of the distances already explained before, mean() function from Numpy library
	mean_r = np.mean((dist_r_1, dist_r_2))

	return mean_l,mean_r


def navigation_logic(mean_l,mean_r,front_d):
	"""
	Function that implements the logic with which the robot will decide to navigate in 2D space, it is essentially based on the distance values obtained by find_frontal_token() and
	find_lateral_token() functions
	
	Args:
	mean_l (float): mean distance of the two closest golden token on the left
	mean_r (float): mean distance of the two closest golden token on the right
	front_d (float): distance of the closest golden token in the frontal portion of plane(-1 if no golden token is detected)
	"""
	if(front_d<a_th_gld):	#check if the frontal distance is lower than a_th_gld	
		if(mean_l<=mean_r): #checks if the distance of the left golden token is lower than the one of the right token 
			if(1.5*mean_l<mean_r): #in this case the the left distance (mean_l) is at least 1.5 times smaller than the right distance (mean_r), so i only need to turn to the right 
		    		turn(45,0.1)	
		    		print("right a bit because left= "+str(mean_l)+" and right= "+str(mean_r)) 		
			else:	 		#the two lateral distances are too similar, better to go forward while turning
		    		drive(20,0.1)
				turn(20,0.1)
				print("slightly turn to the right...")	
		#elif(mean_r<mean_l):  #same logic but for turning to the left
		elif(1.5*mean_r<mean_l): #if the cycle arrives here, it means that mean_r<mean_l
		    	print("left a bit because left= "+str(mean_l)+" and right= "+str(mean_r))
		   	turn(-45,0.1)
		else:
			drive(20,0.1)
			turn(-35,0.1)
			print("slightly turn to the left...")		  	
	else:				#if none of the previous conditions occured, then go forward
		drive(80,0.15)
		print("going forward...")   	
	  	  	


counter_l=counter_r=c=0
a_th_svr=1.4 #linear distance threshold of silver token
d_th_svr=70 #orientation threshold of silver token
a_th_gld=1.2 #linear distance threshold of golden token
while 1:
	
	#Updating information about the gold and silver tokens in the specified areas of the robot view
	dist, rot_y = find_silver_token()
	distance= find_frontal_token()
	mean_l,mean_r= find_lateral_token()
	
	#If the distance of the silver token (dist) is lower than the specified threshold (a_th_svr) and within the range of (+- d_th_svr), then grab_silver()
	if(dist<a_th_svr and dist!=-1 and rot_y>-d_th_svr and rot_y<d_th_svr):
		grab_silver()	
	else:
		navigation_logic(mean_l,mean_r,distance) #When the previous condition doesn't happen, just move on
	
	"""  	  	
	c=c+1
	print("C= "+str(c))	
	print("DISTANCE= "+str(distance))
	print("dist_right= "+str(mean_r))
	print("dist_left= "+str(mean_l))
	if(mean_l==100):
		counter_l=counter_l+1
	if(mean_r==100):
		counter_r=counter_r+1
	print("COUNTER L= "+str(counter_l)+", COUNTER R= "+str(counter_r))  	  	
	print("---------------------------------------")   
	"""
