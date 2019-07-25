# go_2_goal
## Go to goal ROS challenge
This code make possible that you set a target coordinates and next the ***turtlesim*** it is going to go to the coordinates choiced. 

# Prerequisites

Firstly make sure that you already haved to maked the ros tutorials it can be find at [ROS Tutorials](http://wiki.ros.org/pt_BR/ROS/Tutorials) .

# Running the go_2_goal ROS Node
1. Copy the contents of the src folder into your catkin workspace 'src' folder. Make sure the permissions are set to o+rw on your files and directories.

2. in yout catkin_ws ($CATKIN) folder, execute
    ```sh
    $ catkin_make
    ```
3. Source the environment for each terminal you work in. If necessary, add the line to your .bashrc 
    ```sh
    $ . $CATKIN/devel/setup.bash
    ```
4. Inside the 'launch' folder you can find the file *launch_go_2_goal.launch* you can change e parametrs *velocity_constant* and *angular_constant* as exemple:
    ~~~python
    <param name = "velocity_constant" value = "1.5" type = "double"/>
        <param name = "angular_constant" value = "6.0" type = "double"/>  
    ~~~
5. To run the node
    ```sh
    $ roslaunch turtlesim_go2goal launch_go_2_goal.launch    
    ``` 
# Running the service
This service that use to insert the target coordinates.
1. Open a new terminal
    ```
    $ rosservice call /set_coordinates
    ```
        
    >As a tip use tab for autocomplet
    
    ```
    $ rosservice call /set_coordinates "x: 0.0 y: 0.0 tolerance: 0.0"
    ```

    

