 Research Track 1  -  First assignment <img src="https://raw.githubusercontent.com/jmnote/z-icons/master/svg/python.svg" width="30" height="30">
================================

This assignment is based on a simple, portable robot simulator developed by [Student Robotics](https://studentrobotics.org).


Aim of the project
----------------------
The project aimed to write a Python script in which we had to manage the behaviour of the robot using this kind of logic:
- constantly drive the robot around the circuit in the counter-clockwise direction
- avoid touching the golden boxes
- when the robot is close to a silver box, it should:
	- grab the token
	- put it behind itself (with a 180 degrees rotation)
	- Turn back to the initial position (with the same orientation but negative)
- keep driving the robot around. 



Here's a short clip of the desired behavior I just described.
<p align="center">
	<img src="https://github.com/PerriAlessandro/Assignment1/blob/main/images%20and%20videos/grab_token_gif.gif" height=320 width=256>
</p>

The hardest part of the assignment was to implement a logic with which the robot should be able to detect the walls made out of golden boxes and to avoid them by simply turning left or right, depending on the information about the distance and the orientation of the golden tokens close to it. As it'll be described better in the next paragraphs, my code is mainly based on the comparison between left and right golden token distances. In such a way, the robot will properly turn in the right direction, here's a GIF that shows the desired behavior:
<p align="center">
	<img src="https://github.com/PerriAlessandro/Assignment1/blob/main/images%20and%20videos/corner_gif.gif" height=234 width=600>
</p>


Installing and running the simulator
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



How to run
----------------------
It is possible to start the program by simply running the command:
```bash
$ python2 run.py assignment.py
```
where __assignment.py__  is the Python code that I implemented in order to complete the assigned task and that will be described in the following paragraphs.

Imported libraries
----------------------
The Python libraries needed are:
- [print_function](https://www.python.org/dev/peps/pep-3105/) (from __future__)
- [time](https://docs.python.org/3/library/time.html?highlight=time#module-time)
- [sr.robot](https://studentrobotics.org/docs/programming/sr/)


Functions
----------------------
Here's a list of all the functions in __assignment.py__ code:
- [drive(speed,seconds)](https://github.com/PerriAlessandro/Assignment1/blob/main/README.md#drivespeedseconds)
- [turn(speed,seconds)](https://github.com/PerriAlessandro/Assignment1/blob/main/README.md#turnspeedseconds)
- [find_silver_token()](https://github.com/PerriAlessandro/Assignment1/blob/main/README.md#find_silver_token)
- [grab_silver()](https://github.com/PerriAlessandro/Assignment1/blob/main/README.md#grab_silver)
- [find_obstacles(range_front, range_lat)](https://github.com/PerriAlessandro/Assignment1/blob/main/README.md#find_obstaclesrange_front-range_lat)
- [drive_around(dist_left,dist_right,dist_front)](https://github.com/PerriAlessandro/Assignment1/blob/main/README.md#drive_arounddist_frontdist_left-dist_right)



### drive(speed,seconds) ###
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

### turn(speed,seconds) ###
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
- Flowchart
  
  Here's a flowchart that illustrates the way of how `grab_silver()` works:
  
![immagine](https://github.com/PerriAlessandro/Assignment1/blob/main/images%20and%20videos/grab_silver_flowchart.png)
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


### find_obstacles(range_front, range_lat) ###
Function to find the mean of the distances of the two closest golden token on the left and the right portions of the robot view
- Arguments 
  - `range_front` (float): positive range in which we want to find the frontal token, default: 30 degrees
  - `range_lat` _(float[])_, list of the two positive angles (that correspond to the lateral areas) in which the robot will search for, default: [80,100] degrees
- Returns
  - `dist_front` _(float)_: distance of the closest golden token on the front
  - `dist_left` _(float)_: distance of the two closest golden token on the left
  - `dist_right` _(float)_: distance of the two closest golden token on the right
- Robot's Field of View

The robot will have this kind of field of view:
<p align="center">
	<img src="https://github.com/PerriAlessandro/Assignment1/blob/main/images%20and%20videos/thresholds.jpg" height=465 width=640>
</p>

	
- Code
```python
def find_obstacles(range_front=30,range_lat=[80,100]):
    
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

```

### drive_around(dist_front,dist_left, dist_right) ###
Function that implements the logic with which the robot will decide to navigate in 2D space, it is essentially based on the (frontal and lateral) 
	distance values of the golden tokens obtained by find_obstacles(). This function is called whenever the conditions for grabbing a silver token (specified in the main()) are not respected.
- Arguments 
  - `dist_front` _(float)_: distance of the closest golden token on the front
  - `dist_left` _(float)_: distance of the closest golden token on the left
  - `dist_right` _(float)_: distance of the closest golden token on the right

  
- Returns
  - None
- Code
```python
def drive_around(dist_front,dist_left,dist_right,a_th_gld=1.2):

	if(dist_front<a_th_gld):	#check if the frontal distance is lower than a_th_gld	
		
		if(dist_left<=dist_right): #checks if the distance of the left golden token is lower than the one of the right token 
			if(1.5*dist_left<dist_right): #in this case the the left distance (dist_left) is at least 1.5 times smaller than the right distance (dist_right), so i only need to turn to the right 
		    		turn(45,0.1)	
		    		print("right a bit...")	
			else:	 		#the two lateral distances are too similar, better to go forward while turning
		    		drive(20,0.1)
				turn(20,0.1)
				print("slightly turn to the right...")	
		elif(1.5*dist_right<dist_left): #if the cycle arrives here, it means that dist_right<dist_left
		    	print("left a bit...")
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

There is an endless loop cycle (_while 1_) in which data are updated and used to tell the robot what to do in that specific moment by using an _if statement_ that will call `grab_silver()` function or `drive_around()` one. The _if statement_ checks if the distance of the silver token (dist svr) is lower than the specified threshold (a_th_svr) and within the range of (+- d_th_svr). The robot will only see the silver tokens that are in the blue portion of the plane illustrated in the "Robot's Field of view" section of [`find_obstacles()`](https://github.com/PerriAlessandro/Assignment1/blob/main/README.md#find_obstaclesrange_front-range_lat).
```python
def main():
		
	while 1:
		
		#Updating information about the gold and silver tokens in the specified areas of the robot view (i.e. frontal and lateral for golden tokens, frontal for silver tokens)
		dist_svr, rot_y_svr= find_silver_token()
		dist_front_gld,dist_left_gld,dist_right_gld= find_obstacles()
		
		#If the distance of the silver token (dist_svr) is lower than the specified threshold (a_th_svr) and within the range of (+- d_th_svr), then grab_silver()
		if(dist_svr<a_th_svr and dist_svr!=-1 and rot_y_svr>-d_th_svr and rot_y_svr<d_th_svr):
			grab_silver()	
		else:
			drive_around(dist_front_gld,dist_left_gld,dist_right_gld) #If the silver token is too far, then drive around!
		
```

In order to have a more intuitive idea of what I just explained, I created a simple __flowchart__ concerning the logic of my entire Python code:

![immagine](https://github.com/PerriAlessandro/Assignment1/blob/main/images%20and%20videos/main_flowchart.jpeg)

In this way, it's possible to understand my work clearly and concisely. Moreover, I specified which function is called in each significative block (i.e. the writings in yellow) so that you can see how my code works point by point during the execution of the program. You can also find the flowchart for the `grab_silver()` function [here](https://github.com/PerriAlessandro/Assignment1/blob/main/README.md#grab_silver).

Results
----------------------

### Overall work ###
Overall, I'm genuinely satisfied with the work I've done because it allowed me to learn a lot about Python programming and, regarding to the concepts that are in this kind of work, I started to learn something about the logic with which a robot has to decide to move itself in a 2D environment. I have worked both on my own and with some of my classmates and it's been fun collaborating in order to find a smart solution to the task requested.

I spent most of the time on the first part of the project because at a first sight I didn't know which could be the best way to make the robot take a decision. The first code I implemented was based on letting the robot avoid golden tokens by just checking the angle between them and the robot, but I had noticed that it couldn't have worked in a deterministic way because there were some moments in which the robot decided to turn on the wrong way and eventually go back instead of going on. Things started working better when I decided to base the main logic on comparing the distances between right and left tokens. 
Here's a short video of the final result (sped up to 2x):
https://github.com/PerriAlessandro/Assignment1/blob/main/images%20and%20videos/full_lap.mp4

In the last days before the assignment deadline, I implemented a new version of the code in which I put `find_obstacles()` function inside `drive around()`, using inner functions. In this way it is no more necessary to update infos (about golden tokens) in `main()` but it is directly managed by `drive around()`, you can find [here] (https://github.com/PerriAlessandro/Assignment1/blob/main/extra/assignment_extra.py) the code.


### Personal comments & Possible improvements ###
During the whole time spent implementing the code, I preferred focusing more on developing a conceptually simple code rather than a more intricated one. However, there are several ways to improve the work done, one of them is letting the robot make decisions about where to turn in the proximity of a wall using silver tokens info about relative orientation. In this way, the robot could be able to turn itself and point directly to the token rather than just going on and searching for the silver token at a later time. This is actually quite simple to implement, but I decided against it because I took as my priority the ability to allow the robot to move through the circuit regardless of the presence of silver tokens, as if the two tasks were implemented by two stand-alone _modules_.









