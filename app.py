import cv2
import time
from collections import defaultdict
from flask import Flask, render_template, Response, jsonify, request
from ultralytics import YOLO

app = Flask(__name__)

# Load YOLOv8 model (ensure the model is in the correct path)
model = YOLO("/Users/gauravtalele/PycharmProjects/PythonProject1/best1.pt")  # Provide correct path to your model

# Video file paths
video_paths = [
    '/Users/gauravtalele/PycharmProjects/PythonProject/video1.mp4',
    '/Users/gauravtalele/PycharmProjects/PythonProject/video2.mp4',
    '/Users/gauravtalele/PycharmProjects/PythonProject/video3.mp4',
    '/Users/gauravtalele/PycharmProjects/PythonProject/video4.mp4'
]

# Function to simulate lane determination (use actual lane detection logic)
def determine_lane(x1, x2):
    middle = (x1 + x2) // 2
    if middle < 300:  # Left side
        return 1
    else:  # Right side
        return 2

# Signal time calculation function based on vehicle count
def calculate_signal_time(vehicle_count):
    if vehicle_count < 5:
        return 20
    elif vehicle_count < 10:
        return 40
    elif vehicle_count < 15:
        return 60
    else:
        return 80

# Video stream generator
def gen(video_path):
    cap = cv2.VideoCapture(video_path)
    fps = cap.get(cv2.CAP_PROP_FPS)  # Get the FPS of the video

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        # Run YOLOv8 model on the frame
        results = model.predict(frame)

        # Process detected vehicles
        detected_vehicles = results[0].boxes if results else []
        vehicle_count_per_lane = defaultdict(int)

        for box in detected_vehicles:
            x1, y1, x2, y2 = map(int, box.xyxy[0])

            # Simulate lane determination logic based on position
            lane = determine_lane(x1, x2)  # Replace with actual lane detection logic
            vehicle_count_per_lane[lane] += 1

            # Draw bounding box and vehicle count on the frame
            cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
            cv2.putText(frame, f"Vehicle", (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX,
                        0.5, (0, 255, 0), 2, cv2.LINE_AA)

        # Create vehicle count string for each lane
        vehicle_count_str = f"Lane 1: {vehicle_count_per_lane[1]} cars, Lane 2: {vehicle_count_per_lane[2]} cars"

        # Put vehicle count on frame
        cv2.putText(frame, vehicle_count_str, (10, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)

        # Encode the frame in JPEG format and yield it
        ret, buffer = cv2.imencode('.jpg', frame)
        frame = buffer.tobytes()

        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')

        # Sync with video FPS (instead of using sleep)
        time.sleep(1 / fps)

    cap.release()

# Route for serving the video stream and showing vehicle counts
@app.route('/')
def index():
    return render_template('front.html')

# Route for streaming video feed (dynamic video selection)
@app.route('/video_feed')
def video_feed():
    video_index = int(request.args.get('video_index', 0))  # Get video index from query params
    return Response(gen(video_paths[video_index]), mimetype='multipart/x-mixed-replace; boundary=frame')

# Route for fetching signal times based on vehicle counts
@app.route('/get_signal_times', methods=['GET'])
def get_signal_times():
    signal_times = defaultdict(dict)

    for video_path in video_paths:
        vehicle_count_per_lane = defaultdict(int)
        cap = cv2.VideoCapture(video_path)

        # Process video for signal times
        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                break

            # Run YOLOv8 model on the frame
            results = model.predict(frame)
            detected_vehicles = results[0].boxes if results else []

            for box in detected_vehicles:
                x1, y1, x2, y2 = map(int, box.xyxy[0])
                lane = determine_lane(x1, x2)
                vehicle_count_per_lane[lane] += 1

        cap.release()

        # Calculate signal time based on vehicle count per lane
        for lane, vehicle_count in vehicle_count_per_lane.items():
            signal_times[video_path][lane] = calculate_signal_time(vehicle_count)

    return jsonify(signal_times)

if __name__ == '__main__':
    app.run(debug=True)
