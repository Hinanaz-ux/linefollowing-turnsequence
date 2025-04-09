# linefollowing-turnsequence
This contains the code to move a robotic agent using line following and the ability to stop at certain stops and initiate turn sequence when an marker indicating the stop has been detected.

turn sequence: the robot turns almost 90 degrees or so , the degree is set by the seconds given to the robot to turn.

the ino files are arduino files, used to control the movement of the robot , when a turn sequence command is recieved by robot it initiates turn sequence that is to turn left, the degree is controlled by the seconds taken to turn . i have also uploaded an ino file containing camera control , my robot contains a camera mounted to it for vision , the whole time camera faces downwards to detect aruco marker placed on ground and upon detection of a marker and a turn sequence command has been received , the servo motor turn the camera to face forward and then the robot initiated turn sequence. 

**The robot is built on a cuboidal base with a sleek, functional design. Key components include:
**
Mobility System:
The base features four DC motors mounted underneath to drive the wheels, allowing smooth and controlled navigation along a predefined path.

Inbuilt Cart:
The cuboidal base includes a hollow section designed to function as an inbuilt cart, where collected items are securely placed during the shopping process. This makes SARA compact and self-contained, without the need for an external basket.

Robotic Arm:
Centrally placed on top of the base, the 4-DOF robotic arm includes:

Two servo motors to control the vertical motion of the arm joints

One servo motor to extend or retract the arm horizontally

One servo motor at the end-effector to operate the gripper for item pickup and placement into the cart

Camera Mount:
A vertical pillar located at one corner of the base supports a rotating camera, controlled by a servo motor. This setup allows SARA to detect items, follow paths, and recognize shelf positions using real-time computer vision.
