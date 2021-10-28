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
    Function to find the closest silver token

    Returns:
	dist (float): distance of the closest silver token (-1 if no silver token is detected)
	rot_y (float): angle between the robot and the silver token (-1 if no silver token is detected)
    """
    dist=100
    for token in R.see():
        if token.dist < dist and token.info.marker_type is MARKER_TOKEN_SILVER:
            dist=token.dist
	    rot_y=token.rot_y
    if dist==100:
	return -1, -1
    else:
   	return dist, rot_y

def find_golden_token():
    """
    Function to find the closest golden token

    Returns:
	dist (float): distance of the closest golden token (-1 if no golden token is detected)
	rot_y (float): angle between the robot and the golden token (-1 if no golden token is detected)
    """
    dist=100
    rot1=rot2=-99
   #print(str(R.see()))
    for token in R.see():
        if token.dist < dist and token.info.marker_type is MARKER_TOKEN_GOLD and -30<token.rot_y<+30:
            
            dist=token.dist
            rot3=rot2
            rot2=rot1
	    rot1=token.rot_y
    if dist==100:
	return -1, -1
    else:
   	return dist,rot1,rot2,rot3
   	
def grab_silver():
	finished=False
	while(not finished):
		dist, rot_y = find_silver_token()	
		if dist==-1: # if no token is detected, we make the robot turn 
			print("I don't see any token!!")
			turn(+10, 1)
	    	elif dist <d_th: # if we are close to the token, we try grab it.
			print("Found it!")
			if R.grab(): # if we grab the token, we move the robot forward and on the right, we release the token, and we go back to the initial position
			    print("Gotcha!")
		    	    turn(23, 3) 
			    R.release()
			    turn(-23,3)
			    finished=True
			    
			else:
			    print("Aww, I'm not close enough.")
			    finished=False
	    	elif -a_th<= rot_y <= a_th: # if the robot is well aligned with the token, we go forward
		    print("Ah, that'll do.")
		    drive(50, 0.5)
	    	elif rot_y < -a_th: # if the robot is not well aligned with the token, we move it on the left or on the right
		    print("Left a bit...")
		    turn(-2, 0.5)
	    	elif rot_y > a_th:
		    print("Right a bit...")
		    turn(+2, 0.5)
		
	
	
def seek_right():
	dist=100
        exists=False
        for token in R.see():
       	    if token.dist < dist and token.info.marker_type is MARKER_TOKEN_GOLD and 85<token.rot_y<95 and token.dist<2.5:
            	    	    exists=True
            	    	    dist=token.dist
    
        return exists, dist	


def seek_left():
	dist=100
        exists=False
        for token in R.see():
       	    if token.dist < dist and token.info.marker_type is MARKER_TOKEN_GOLD and -95<token.rot_y<-85 and token.dist<2.5:
            	    	    exists=True
    		            dist=token.dist   		
        return exists,dist





dist_right_ex=dist_left_ex=-1	
while 1:
	distance, rot1,rot2,rot3 = find_golden_token()
	dist, rot_y = find_silver_token()
	
	
	if(dist_right_ex==-1):
		exists,dist_right_ex=seek_right()
	elif(dist_right!=100):
		dist_right_ex=dist_right
		
		
		
	if(dist_left_ex==-1):
		exists,dist_left_ex=seek_left()
	elif(dist_left!=100):
		dist_left_ex=dist_left
		
		
	exists_left,dist_left= seek_left()
	exists_right,dist_right= seek_right()
	
	#rotations=np.mean((rot1,rot2,rot3))
	print("rot1= "+str(rot1))
	
    
	
	distance, rot1,rot2,rot3 = find_golden_token()
	print("GOING, rot1= "+str(rot1)) 
	#print("right= "+str(exists_right)+", left= "+str(exists_left))
	print("right_ex= "+str(dist_right_ex))
	print("left_ex= "+str(dist_left_ex))
	print("     ------") 
	print("right= "+str(dist_right))
	print("left= "+str(dist_left))
	#print("left= "+str(dist_left)+" and right= "+str(dist_right))
    	print("DISTANCE= "+str(distance))	
	     	    
       
	
	if(dist<1 and dist!=-1 and rot_y>-70 and rot_y<70):
		grab_silver()
	
	if (dist_right==100):
		dist_right=dist_right_ex
	if (dist_left==100):
		dist_left=dist_left_ex
	print("       -----") 
	print("dist_right_new= "+str(dist_right))
	print("dist_left_new= "+str(dist_left))
	
	
	
	
	
	    	
	if(dist_left<dist_right and distance<1.5):		
		if(1.5*dist_left<dist_right):
	    		turn(20,0.1)	
	    		print("right a bit because left= "+str(dist_left)+" and right= "+str(dist_right))	
	 	else:
			drive(20,0.1)
			turn(10,0.1)	 
	    		
	elif(dist_right<dist_left and distance<1.5):  
		if(1.5*dist_right<dist_left):
		    	print("left a bit because left= "+str(dist_left)+" and right= "+str(dist_right))	
		    	turn(-20,0.1)
		else:
			drive(20,0.1)
			turn(-10,0.1)
		  	
	else:
		drive(100,0.1)   	
	    	
	print("---------------------------------------")    	
	
