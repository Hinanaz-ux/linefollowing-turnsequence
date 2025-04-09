import cv2
import numpy as np
import serial
import time

# Initialize serial communication with Arduino
try:
    arduino = serial.Serial('COM6', 9600)  # Replace with the correct port
    time.sleep(2)  # Allow time for Arduino to initialize
except Exception as e:
    print(f"Error: Unable to connect to Arduino: {e}")
    exit()

# Open the camera
cap = cv2.VideoCapture(0)

# Check if the camera is opened correctly
if not cap.isOpened():
    print("Error: Unable to open the camera.")
    exit()

# Define the ArUco dictionary and detector parameters
dictionary = cv2.aruco.getPredefinedDictionary(cv2.aruco.DICT_4X4_250)  # Use your dictionary type
parameters = cv2.aruco.DetectorParameters()
detector = cv2.aruco.ArucoDetector(dictionary, parameters)

# Prompt the user to input marker IDs
try:
    target_markers = input("Enter the ArUco marker IDs (0 to 3) to stop the robot, separated by commas: ")
    target_markers = [int(marker.strip()) for marker in target_markers.split(",")]
    if any(marker not in [0, 1, 2, 3] for marker in target_markers):
        raise ValueError("Invalid marker ID(s). Please enter numbers from 0 to 3.")
    print(f"Target markers: {target_markers}")
except ValueError as ve:
    print(f"Error: {ve}")
    exit()

# Variables to track detection state
robot_busy = False

try:
    while True:
        # Capture a frame from the camera
        ret, frame = cap.read()

        if not ret:
            print("Error: Unable to read the frame.")
            break

        # Detect markers in the frame
        markerCorners, markerIds, rejectedCandidates = detector.detectMarkers(frame)

        if markerIds is not None:
            # Extract detected marker IDs
            detected_ids = markerIds.flatten()
            print(f"Detected marker IDs: {detected_ids}")

            # Check if any target marker is detected
            for marker in target_markers:
                if marker in detected_ids and not robot_busy:
                    print(f"Target marker {marker} detected!")

                    # Notify Arduino to perform the stop, turn, wait, and return sequence
                    arduino.write(b'TURN_SEQUENCE\n')
                    robot_busy = True
                    print("Sent TURN_SEQUENCE command to Arduino.")

                    break  # Prevent multiple commands in one loop iteration

        # Display the frame with detected markers
        cv2.imshow("Frame", frame)

        # Check if Arduino is ready to continue line following
        # if robot_busy and arduino.in_waiting > 0:
        #     # response = arduino.readline().decode().strip()
        #     response = arduino.readline().decode('utf-8').strip()  # Use 'utf-8' for standard encoding0,1
        #     if response == "READY":
        #         robot_busy = False
        #         print("Arduino ready. Resuming line following.")  

        # if robot_busy and arduino.in_waiting > 0:
        #     try:
        #         response = arduino.readline().decode('utf-8').strip()
        #         print(f"Response from Arduino: {response}")  # Debugging line
        #         if response == "READY":
        #             robot_busy = False
        #             print("Arduino ready. Resuming line following.")
        #     except Exception as e:
        #         print(f"Error reading Arduino response: {e}")

        if robot_busy:
            print(f"robot_busy: {robot_busy}, arduino.in_waiting: {arduino.in_waiting}")
            if arduino.in_waiting > 0:
                try:
                    response = arduino.readline().decode('utf-8').strip()
                    print(f"Response from Arduino: {response}")
                    if response == "READY":
                        robot_busy = False
                        print("Arduino ready. Resuming line following.")
                except Exception as e:
                    print(f"Error reading Arduino response: {e}")
            else:
                print("No data waiting in Arduino buffer.")

        # Exit if 'q' key is pressed
        if cv2.waitKey(1) & 0xFF == ord('q'):
            print("Exiting...")
            break

except KeyboardInterrupt:
    print("Interrupted by user.")

finally:
    # Release resources and close connections
    print("Releasing resources...")
    cap.release()
    cv2.destroyAllWindows()
    arduino.close()
    print("Arduino connection closed.")
