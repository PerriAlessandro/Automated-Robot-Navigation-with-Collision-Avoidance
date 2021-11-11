"""
		Research Track I - First Assignment (October 2021)  - Perri Alessandro (n. 4476726)

This assignment is based on a simple, portable robot simulator developed by Student Robotics. 
Aim of the project:
The project aimed to write a Python script in which we had to manage the behaviour of the robot using this kind of logic:
	- constantly drive the robot around the circuit in the counter-clockwise direction
	- avoid touching the golden boxes
	- when the robot is close to a silver box, it should grab it, and move it behind itself

Imported Modules:
	-__future__
	- time
	- sr.robot
	
Methods:
	- turn(speed,seconds)
	- drive(speed,seconds)
	- find_silver_token()
	- grab_silver()
	- find_obstacles(range_front,range_lat)
	- drive_around(dist_front, dist_left,dist_right)
	- main()

How to run:
	$python2 run.py assignment.py

"""

from __future__ import print_function
import time
from sr.robot import *
import math

a_th = 2.0
""" float: Threshold for the control of the linear distance"""

d_th = 0.4
""" float: Threshold for the control of the orientation"""

R = Robot()
""" instance of the class Robot"""

a_th_svr=1.2
""" float: Threshold for the detection of the silver token (linear distance)"""

d_th_svr=70 
""" float: Threshold for the detection of the silver token (orientation)"""


##############################################################################################################

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

##############################################################################################################

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

##############################################################################################################

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

##############################################################################################################

def grab_silver():
	"""
	Function to detect the closest silver token, move forward to it and grab it. After these steps, the robot will turn behind himself, release the token and turn back to the initial position
	Function to find the mean of the distances of the two closest golden token on the left and the right portions of the robot view
	
	Args:
		None
	Returns:
		None
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
			grab=R.grab()
			if grab:  # if we grab the token, we move the robot forward and on the right, we release the token, and we go back to the initial position
			    print("Gotcha!")
			    print("turning..")
		    	    turn(23, 3) #turn (+180 degrees)
		    	    print("releasing..")
			    R.release()
			    print("turning again..")
			    turn(-23, 3) #turn (-180 degrees)
			    print("Ok, my work is done!")
			    finished = True

			else:
			   print("Aww, I'm not close enough.")
			   drive(-10,1)
			   turn(10,2)
	    	elif -a_th <= rot_y <= a_th:  # if the robot is well aligned with the token, we go forward
		    print("Ah, that'll do.")
		    drive(50, 0.5)
	    	elif rot_y < -a_th:  # if the robot is not well aligned with the token, we move it on the left or on the right
		    print("Left a bit...")
		    turn(-2, 0.5)
	    	elif rot_y > a_th:
		    print("Right a bit...")
		    turn(+2, 0.5)


##############################################################################################################

def find_obstacles(range_front=30,range_lat=[80,100]):

	"""
	Function to find the mean of the distances of the closest golden token (i.e. of the obstacles) on the frontal, the left and the right portions of the robot view.
	Args:
		range_front (float): positive range in which we want to find the frontal token, default: 30 degrees
		range_lat (int[]):list of the two positive angles (that correspond to the lateral areas) in which the robot will search for, default: [80,100] degrees
	Returns:
		dist_front (float): distance of the closest golden token on the front
		dist_left (float): distance of the closest golden token on the left
		dist_right (float): distance of the closest golden token on the right
	"""
    
	dist_left=dist_right=dist_front= 100

	for token in R.see():
		if(token.info.marker_type is MARKER_TOKEN_GOLD and token.dist < 2.5):
		
			if token.dist < dist_front and -range_front < token.rot_y < +range_front:
			    dist_front=token.dist
			if token.dist < dist_left and -range_lat[1] < token.rot_y < -range_lat[0] :
			    dist_left = token.dist
			 
			if token.dist < dist_right and range_lat[0] < token.rot_y < range_lat[1] :
			    dist_right = token.dist
			
			
	return dist_front,dist_left,dist_right


##############################################################################################################

def drive_around(dist_front,dist_left,dist_right,a_th_gld=1.2):
	"""
	Function that implements the logic with which the robot will decide to navigate in 2D space, it is essentially based on the (frontal and lateral) 
	distance values of the golden tokens obtained by find_obstacles()
	
	Args:
		dist_left (float): distance of the closest golden token on the left
		dist_right (float): distance of the closest golden token on the right
		dist_front (float): distance of the closest golden token in the frontal portion of plane
		a_th_gld (float): threshold for the frontal golden token, default: 1.2
	"""

	if(dist_front<a_th_gld):	#check if the frontal distance is lower than a_th_gld	
		
		if(dist_left<=dist_right): #checks if the distance of the left golden token is lower than the one of the right token 
			if(1.5*dist_left<dist_right): #in this case the the left distance (dist_left) is at least 1.5 times smaller than the right distance (dist_right), so i only need to turn to the right 
		    		turn(45,0.1)	
		    		print("right a bit...")
		    		#print("right a bit because left= "+str(dist_left)+" and right= "+str(dist_right)) 		
			else:	 		#the two lateral distances are too similar, better to go forward while turning
		    		drive(20,0.1)
				turn(20,0.1)
				print("slightly turn to the right...")	
		elif(1.5*dist_right<dist_left): #if the cycle arrives here, it means that dist_right<dist_left
		    	print("left a bit...")
		    	#print("left a bit because left= "+str(dist_left)+" and right= "+str(dist_right))
		   	turn(-45,0.1)
		else:
			drive(20,0.1)
			turn(-35,0.1)
			print("slightly turn to the left...")	
	else:				#if none of the previous conditions occured, then go forward
		drive(80,0.15)
		print("going forward...")   	
	  	  	

##############################################################################################################

def main():
	lap=0;
	
	while 1:
		print("Lap number: "+str(int(math.floor(lap/7)))) #counts the number of laps, just for fun
		
		
		#Updating information about the gold and silver tokens in the specified areas of the robot view (i.e. frontal and lateral for golden tokens, frontal for silver tokens)
		dist_svr, rot_y_svr= find_silver_token()
		dist_front_gld,dist_left_gld,dist_right_gld= find_obstacles() #notice that i could have put this line in the else statement
		
		#If the distance of the silver token (dist) is lower than the specified threshold (a_th_svr) and within the range of (+- d_th_svr), then grab_silver()
		if(dist_svr<a_th_svr and dist_svr!=-1 and rot_y_svr>-d_th_svr and rot_y_svr<d_th_svr):
			lap=lap+1
			grab_silver()	
		else:
			drive_around(dist_front_gld,dist_left_gld,dist_right_gld) #If the silver token is too far, then drive around!
			  	
		print("---------------------------------------")   
	
			
main()

