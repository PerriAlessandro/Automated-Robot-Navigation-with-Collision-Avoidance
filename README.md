Python Robotics Simulator
================================

This is a simple, portable robot simulator developed by [Student Robotics](https://studentrobotics.org).
Some of the arenas and the exercises have been modified for the Research Track I course

Installing and running
----------------------

The simulator requires a Python 2.7 installation, the [pygame](http://pygame.org/) library, [PyPyBox2D](https://pypi.python.org/pypi/pypybox2d/2.1-r331), and [PyYAML](https://pypi.python.org/pypi/PyYAML/).

Pygame, unfortunately, can be tricky (though [not impossible](http://askubuntu.com/q/312767)) to install in virtual environments. If you are using `pip`, you might try `pip install hg+https://bitbucket.org/pygame/pygame`, or you could use your operating system's package manager. Windows users could use [Portable Python](http://portablepython.com/). PyPyBox2D and PyYAML are more forgiving, and should install just fine using `pip` or `easy_install`.

## Troubleshooting

When running `python run.py <file>`, you may be presented with an error: `ImportError: No module named 'robot'`. This may be due to a conflict between sr.tools and sr.robot. To resolve, symlink simulator/sr/robot to the location of sr.tools.

On Ubuntu, this can be accomplished by:
* Find the location of srtools: `pip show sr.tools`
* Get the location. In my case this was `/usr/local/lib/python2.7/dist-packages`
* Create symlink: `ln -s path/to/simulator/sr/robot /usr/local/lib/python2.7/dist-packages/sr/`


Robot API
---------

The API for controlling a simulated robot is designed to be as similar as possible to the [SR API][sr-api].

### Motors ###

The simulated robot has two motors configured for skid steering, connected to a two-output [Motor Board](https://studentrobotics.org/docs/kit/motor_board). The left motor is connected to output `0` and the right motor to output `1`.

The Motor Board API is identical to [that of the SR API](https://studentrobotics.org/docs/programming/sr/motors/), except that motor boards cannot be addressed by serial number. So, to turn on the spot at one quarter of full power, one might write the following:

```python
R.motors[0].m0.power = 25
R.motors[0].m1.power = -25
```

### The Grabber ###

The robot is equipped with a grabber, capable of picking up a token which is in front of the robot and within 0.4 metres of the robot's centre. To pick up a token, call the `R.grab` method:

```python
success = R.grab()
```

The `R.grab` function returns `True` if a token was successfully picked up, or `False` otherwise. If the robot is already holding a token, it will throw an `AlreadyHoldingSomethingException`.

To drop the token, call the `R.release` method.

Cable-tie flails are not implemented.

### Vision ###

To help the robot find tokens and navigate, each token has markers stuck to it, as does each wall. The `R.see` method returns a list of all the markers the robot can see, as `Marker` objects. The robot can only see markers which it is facing towards.

Each `Marker` object has the following attributes:

* `info`: a `MarkerInfo` object describing the marker itself. Has the following attributes:
  * `code`: the numeric code of the marker.
  * `marker_type`: the type of object the marker is attached to (either `MARKER_TOKEN_GOLD`, `MARKER_TOKEN_SILVER` or `MARKER_ARENA`).
  * `offset`: offset of the numeric code of the marker from the lowest numbered marker of its type. For example, token number 3 has the code 43, but offset 3.
  * `size`: the size that the marker would be in the real game, for compatibility with the SR API.
* `centre`: the location of the marker in polar coordinates, as a `PolarCoord` object. Has the following attributes:
  * `length`: the distance from the centre of the robot to the object (in metres).
  * `rot_y`: rotation about the Y axis in degrees.
* `dist`: an alias for `centre.length`
* `res`: the value of the `res` parameter of `R.see`, for compatibility with the SR API.
* `rot_y`: an alias for `centre.rot_y`
* `timestamp`: the time at which the marker was seen (when `R.see` was called).

For example, the following code lists all of the markers the robot can see:

```python
markers = R.see()
print "I can see", len(markers), "markers:"

for m in markers:
    if m.info.marker_type in (MARKER_TOKEN_GOLD, MARKER_TOKEN_SILVER):
        print " - Token {0} is {1} metres away".format( m.info.offset, m.dist )
    elif m.info.marker_type == MARKER_ARENA:
        print " - Arena marker {0} is {1} metres away".format( m.info.offset, m.dist )
```

[sr-api]: https://studentrobotics.org/docs/programming/sr/



How to run and aim of the project 
----------------------
It is possible to start the program by simply running the command:
```bash
$ python2 run.py assignment.py
```
where __assignment.py__  is the Python code that I implemented in order to complete the assigned task and that will be described in the following paragraphs.

This assignment aimed to make the robot move inside a maze made out of golden boxes. In the path, the robot will come into contact with some silver boxes, with which it will have to grab and put them behind itself (with a 180 degrees rotation), finally turn back to the initial position and keep going on. Here's a short clip of the desired behavior I just described.

The hardest part of the assignment was to implement a logic with which the robot should be able to detect the walls made out of golden boxes and to avoid them by simply turning left or right, depending on the information about the distance and the orientation of the golden tokens close to it.

Functions 
----------------------
Here's a list of all the functions in __assignment.py__ code, with their descriptions: 


### drive() ###
This function sets the linear velocity of the robot. The parameters are the speed and the time with which the robot has to drive forward.
- Arguments 
  - `speed` _(float)_, the amount of linear velocity that we want our robot to assume.
  - `seconds` _(float)_, the amount of time (in seconds) we want our robot to drive.
- Returns
  - None.
- Code
```python
def drive(speed, seconds):
    R.motors[0].m0.power = speed
    R.motors[0].m1.power = speed
    time.sleep(seconds)
    R.motors[0].m0.power = 0
    R.motors[0].m1.power = 0
```

### turn() ###
This function permits the robot to turn on itself, therefore there is no linear velocity but only an angular one.
- Arguments 
  - `speed` (float), the amount of angular velocity that we want our robot to assume.
  - `seconds`(float), the amount of time (in seconds) we want our robot to drive.
- Returns
  - None.
- Code
```python
def turn(speed, seconds):
    R.motors[0].m0.power = speed
    R.motors[0].m1.power = -speed
    time.sleep(seconds)
    R.motors[0].m0.power = 0
    R.motors[0].m1.power = 0
```


### find_silver_token() ###
This function permits to get information about the distance and the angle between the robot and the closest silver token. To do that, the robot checks all the silver tokens that it can see thanks to 'R.see()' method (that returns a list of all the markers the robot can see as `Marker` objects).
- Arguments 
  - None
- Returns
  - `dist` _(float)_: distance of the closest silver token (-1 if no silver token is detected)
  - `rot_y` _(float)_: angle between the robot and the silver token (-1 if no silver token is detected)
- Code
```python
def find_silver_token():
   dist = 100
   for token in R.see():
       if token.dist < dist and token.info.marker_type is MARKER_TOKEN_SILVER:
           dist = token.dist
    rot_y = token.rot_y
   if dist == 100:
    return -1, -1
   else:
    return dist, rot_y
```

### grab_silver() ###
This function permits you to move forward to the closest silver token and grab it. After these steps, the robot will turn behind himself, release the token and turn back to the initial position.
- Arguments 
  - None
- Returns
  - None
- Code
```python
def grab_silver():
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
```

### find_frontal_token() ###
Function to find the closest golden token in a angle between the specified range(i.e. the frontal portion of the robot view)
- Arguments 
  - `range` _(float)_, positive range in which we want to find the token, _default_: 30 
- Returns
  - `dist` _(float)_: distance of the closest golden token in the specified range(-1 if no golden token is detected)
- Code
```python
def find_frontal_token(range=30): 
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
```
### find_lateral_token() ###
Function to find the mean of the distances of the two closest golden token on the left and the right portions of the robot view
- Arguments 
  - `range` _(float[])_, list of the two positive angles in which the robot will search for, _default_:[80,100]
- Returns
  - `mean_l` _(float)_: mean distance of the two closest golden token on the left
  - `mean_r` _(float)_: mean distance of the two closest golden token on the right
- Code
```python
def find_lateral_token(range=[80,100]):    
	dist_l_1 = dist_l_2 = dist_r_1 =dist_r_2= 100

	for token in R.see():
		if(token.info.marker_type is MARKER_TOKEN_GOLD and token.dist < 2.5):
			if token.dist < dist_l_1 and -range[1] < token.rot_y < -range[0] :
			    dist_l_1 = token.dist
			    dist_l_2 = dist_l_1
			if token.dist < dist_r_1 and range[0] < token.rot_y < range[1] :
			    dist_r_1 = token.dist
			    dist_r_2 = dist_r_1
	mean_l = np.mean((dist_l_1, dist_l_2))  #mean of the two closest left token distances, mean() function from Numpy library
	mean_r = np.mean((dist_r_1, dist_r_2))  #mean of the two closest right token distances

	return mean_l,mean_r
```

### navigation_logic() ###
Function that implements the logic with which the robot will decide to navigate in 2D space, it is essentially based on the distance values obtained by find_frontal_token() and
	find_lateral_token() functions. This function is called whenever the conditions for grabbing a silver token (specified in the main()) are not respected.
- Arguments 
  - `mean_l` _(float)_: mean distance of the two closest golden token on the left
  - `mean_r` _(float)_: mean distance of the two closest golden token on the right
  - `front_d` _(float)_: distance of the closest golden token in the frontal portion of plane(-1 if no golden token is detected)
  
- Returns
  - None
- Code
```python
def navigation_logic(mean_l,mean_r,front_d):
 a_th_gld=1.2 #linear distance threshold of golden token
	if(front_d<a_th_gld):	#check if the frontal distance is lower than a_th_gld	
		if(mean_l<=mean_r): #checks if the distance of the left golden token is lower than the one of the right token 
			if(1.5*mean_l<mean_r): #in this case the the left distance (mean_l) is at least 1.5 times smaller than the right distance (mean_r), so i only need to turn to the right 
		    		turn(45,0.1)	
		    		print("right a bit because left= "+str(mean_l)+" and right= "+str(mean_r)) 		
			else:	 		#the two lateral distances are too similar, better to go forward while turning
		    		drive(20,0.1)
				turn(20,0.1)
				print("slightly turn to the right...")	
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
```

main () function 
----------------------
The `main()` function is pretty simple and synthetic.
The first thing to do is to initialize the variables that set the threshold values of linear distance and orientation for the silver tokens:
```python
a_th_svr=1.4 #linear distance threshold of silver token
d_th_svr=70 #orientation threshold of silver token
```
After that, there is an endless loop cycle (_while 1_) in which data are updated and used to tell the robot what to do in that specific moment by using an _if statement_ that will call `grab_silver()` function or `navigation_logic()` function:
```python
a_th_svr=1.4 #linear distance threshold of silver token
d_th_svr=70 #orientation threshold of silver token
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
```












