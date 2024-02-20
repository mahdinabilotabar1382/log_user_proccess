Face Recognition Attendance System
Introduction

This Python script implements a simple Face Recognition Attendance System using the OpenCV and Face Recognition libraries. The system captures video from a webcam or a specified video file, detects faces, recognizes them, and maintains attendance records in a CSV file.
Prerequisites

    Python 3.x
    Required Python packages: cv2, face_recognition, numpy, PyQt5, dlib

Setup

    Install the required Python packages:

    bash

    pip install opencv-python face_recognition numpy PyQt5 dlib

    Ensure you have a webcam connected or provide a video file path when prompted.

Usage

    Run the script:

    bash

    python your_script_name.py

    The system will prompt you to select a video file (supports formats: mp4, avi, mkv).

    Detected faces will be framed with a green rectangle, and recognized names will be displayed.

    The attendance records will be saved in a CSV file with the current date (e.g., YY-MM-DD.csv).

Notes

    The system uses a predefined image encoding for face recognition. You can extend the code to include more faces as needed.
    Adjust the threshold variable to fine-tune the face recognition accuracy.

Feel free to modify the code to suit your specific requirements. For any questions or issues, contact the script owner.

Please replace "your_script_name.py" with the actual name of your script. Feel free to add or modify sections based on the specifics of your implementation.
User



#save image to captured_images .............

class WebcamCapture:
    def __init__(self):
        self.capture = cv2.VideoCapture(0)  # 0 indicates the default camera (you may need to adjust this)
        self.face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

    def capture_frame(self):
        ret, frame = self.capture.read()
        if ret:
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            faces = self.face_cascade.detectMultiScale(gray, scaleFactor=1.3, minNeighbors=5, minSize=(30, 30))

            if len(faces) > 0:
                # Save the captured frame
                timestamp = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
                image_filename = f"captured_images/{timestamp}.png"
                cv2.imwrite(image_filename, frame)
                print(f"Captured image saved: {image_filename}")

    def release(self):
        self.capture.release()


#create json file for api  .............

class Logger:
    def __init__(self):
        self.log_data = []

    def add_log_entry(self, username):
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        log_entry = {"timestamp": timestamp, "username": username}
        self.log_data.append(log_entry)

    def write_logs_to_csv(self):
        with open(log_file_path, 'w', newline='') as csvfile:
            csv_writer = csv.writer(csvfile)
            csv_writer.writerow(["Timestamp", "Username"])
            for log in self.log_data:
                csv_writer.writerow([log["timestamp"], log["username"]])

    def write_logs_to_json(self):
        with open(json_log_file_path, 'w') as json_file:
            json.dump(self.log_data, json_file, indent=2)





# read log for write logs.csv 
def read_logs():
    try:
        with open(log_file_path, 'r') as log_file:
            log_data = log_file.readlines()
            return log_data
    except FileNotFoundError:
        print(f"Error: Log file '{log_file_path}' not found.")
        return []

def write_log_entry(username):
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    log_entry = f"{timestamp},{username}\n"
    
    with open(log_file_path, 'a') as log_file:
        log_file.write(log_entry)

def write_logs_to_csv(logs):
    with open(log_file_path, 'w', newline='') as csvfile:
        csv_writer = csv.writer(csvfile)
        csv_writer.writerow(["Timestamp", "Username"])
        for log in logs:
            timestamp, username = log.strip().split(',')
            csv_writer.writerow([timestamp, username])

def main():
    while True:
        try:
            log_data = read_logs()
            if log_data:
                last_entry = log_data[-1].split(",")[-1].strip()
                print(f"Last log entry: {last_entry}")
                write_logs_to_csv(log_data)
        except Exception as e:
            print(f"Error in main loop: {e}")
        
        time.sleep(5)


        
if __name__ == '__main__':
    # Create a new process and run the main function
    with daemon.DaemonContext():
        process = Process(target=main)
        process.start()

        # You can continue with other code here if needed
        print("Program is running in the background.")
   


This Python program captures images using a webcam, detects faces, and logs user entries. The captured frames are saved in the "captured_images" directory, and logs are recorded in both CSV and JSON formats.
File Paths

    CSV Log File: "logs/logs.csv"
    JSON Log File: "logs/logs.json"
    Captured Images Directory: "captured_images/"

Usage

    Webcam Capture:
        The program captures frames from the default webcam.
        Detected faces trigger the saving of the captured frame in the "captured_images" directory with a timestamped filename.

    Logging:
        User entries are logged with timestamps in both CSV and JSON formats.
        CSV log file: "logs/logs.csv"
        JSON log file: "logs/logs.json"

    Background Process:
        The program runs in the background, continuously reading logs and updating the CSV file every 5 seconds.

Setup

    Dependencies:

        Ensure you have Python 3.x installed.

        Install required packages: cv2, daemon
    pip install opencv-python daemon

Run the Program:

    Execute the program:
        python your_script_name.py

        The program will run in the background, continuously updating the CSV log file.

Notes

    Adjust the face detection parameters in the WebcamCapture class as needed.
    Customize file paths and directories based on your preferences.
    Modify the main loop and logging functions to suit specific requirements.
