import cv2
from collections import defaultdict
from ultralytics import YOLO  # Corrected import

# Initialize the YOLOv8 model
model = YOLO("best1.pt")  # Ensure the path to the model is correct

# Define signal time thresholds based on vehicle count
signal_time_thresholds = {
    0: 10,    # 0 vehicles -> 10 seconds
    1: 15,    # 1 vehicle -> 15 seconds
    2: 20,    # 2 vehicles -> 20 seconds
    3: 30,    # 3 vehicles -> 30 seconds
    4: 40,    # 4 vehicles -> 40 seconds
    5: 50,    # 5 vehicles -> 50 seconds
    6: 60,    # 6+ vehicles -> 60 seconds
}

def calculate_signal_time(vehicle_count):
    """ Calculate signal time based on vehicle count """
    if vehicle_count <= 0:
        return signal_time_thresholds[0]
    elif vehicle_count == 1:

        return signal_time_thresholds[1]
    elif vehicle_count == 2:
        return signal_time_thresholds[2]
    elif vehicle_count == 3:
        return signal_time_thresholds[3]
    elif vehicle_count == 4:
        return signal_time_thresholds[4]
    elif vehicle_count == 5:
        return signal_time_thresholds[5]
    else:
        return signal_time_thresholds[6]

def process_video(video_path, frame_interval=3):
    """ Process a video and count vehicles per lane, capturing frames every 'frame_interval' seconds """
    cap = cv2.VideoCapture(video_path)
    fps = cap.get(cv2.CAP_PROP_FPS)  # Get the frames per second of the video
    frame_skip = int(fps * frame_interval)  # Calculate how many frames to skip for 3 seconds
    lane_vehicle_count = defaultdict(int)  # Dictionary to track vehicle counts for each lane

    frame_count = 0  # Frame counter

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        # Capture frame every 'frame_interval' seconds
        if frame_count % frame_skip == 0:
            results = model(frame)  # Perform inference on the frame
            detections = results[0].boxes  # Get detected bounding boxes

            # For simplicity, assume detections are split by lane (this should be adjusted based on the video setup)
            for box in detections:
                x_min, y_min, x_max, y_max = box.xywh[0]  # Get coordinates of the bounding box
                # Assume that the frame is divided into lanes and we are counting cars per lane
                # Implement lane assignment based on x-coordinate or region of interest

                lane = get_lane_from_x(x_min)  # This function determines the lane based on x_min
                lane_vehicle_count[lane] += 1  # Increment vehicle count in the appropriate lane

        frame_count += 1  # Increment frame counter

    cap.release()
    return lane_vehicle_count

def get_lane_from_x(x_min):
    """ Dummy function to determine lane based on x_min value (adjust this logic based on your setup) """
    if x_min < 320:
        return 1  # Lane 1
    elif x_min < 640:
        return 2  # Lane 2
    else:
        return 3  # Lane 3

def adjust_traffic_signals(lane_vehicle_count):
    """ Adjust traffic signal timing based on vehicle counts """
    for lane, count in lane_vehicle_count.items():
        signal_time = calculate_signal_time(count)
        print(f"Lane {lane}: {count} vehicles -> Adjusted Signal Time: {signal_time}s")
        # Here, implement actual traffic signal control to adjust the light timing dynamically.
        # This can be a function that interfaces with the traffic
        # signal system.

if __name__ == "__main__":
    video_paths = [
        "/Users/gauravtalele/PycharmProjects/PythonProject/video1.mp4",
        "/Users/gauravtalele/PycharmProjects/PythonProject/video2.mp4",
        "/Users/gauravtalele/PycharmProjects/PythonProject/video3.mp4",
        "/Users/gauravtalele/PycharmProjects/PythonProject/video4.mp4"
    ]

    # Process each video and adjust signals
    for video_path in video_paths:
        print(f"Processing {video_path}...")
        lane_vehicle_count = process_video(video_path)
        adjust_traffic_signals(lane_vehicle_count)
        input("Press Enter to continue to the next video...")  # Pause before next video
