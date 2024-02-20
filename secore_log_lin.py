# cash program on system


import daemon
import os
import csv
import time
import json
from datetime import datetime
from multiprocessing import Process
import cv2


#save pach for locations

log_file_path = "logs/logs.csv"
json_log_file_path = "logs/logs.json"




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
        
        # Optionally, you can wait for the process to finish
        # process.join()