# DroneCrashValidationGUI
Flask GUI to collect ground truth data on test videos to get accuracy on a drone crash detection model's predictions.

# Run with Docker
- docker build -t validation-gui:1.0 .
- docker run --shm-size=8g -it -d -p 5000:5000 -v ${PWD}:/app validation-gui:1.0
# GUI Walkthrough
https://youtu.be/UIpUHJdKJRw?si=CPHqHoq4zDrpEE08