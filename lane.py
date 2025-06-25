import cv2
import numpy as np
from ultralytics import YOLO

# Load YOLOv8 model (make sure the correct path to the model is specified)
model = YOLO("best1.pt")

# Video file paths
video_files = [
    "/Users/gauravtalele/PycharmProjects/PythonProject/video1.mp4",
    "/Users/gauravtalele/PycharmProjects/PythonProject/video2.mp4",
    "/Users/gauravtalele/PycharmProjects/PythonProject/video3.mp4",
    "/Users/gauravtalele/PycharmProjects/PythonProject/video4.mp4"
]

# Default signal times (seconds)
signal_times = {
    "Lane 1": 30,  # Starts with green
    "Lane 2": 10,
    "Lane 3": 10,
    "Lane 4": 10
}

# Process each video one by one
for i, video_file in enumerate(video_files):
    print(f"Processing {video_file}...")

    # Open video file
    cap = cv2.VideoCapture(video_file)
    if not cap.isOpened():
        print(f"Error: Could not open video {video_file}")
        continue

    frame_count = 0
    vehicle_counts = {"Lane 1": 0, "Lane 2": 0, "Lane 3": 0, "Lane 4": 0}  # Reset vehicle counts for each video

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        frame_count += 1

        # Skip frames to get 1 frame per second (frame rate is assumed to be 30 FPS, adjust as needed)
        if frame_count % 30 != 0:
            continue

        # Run YOLOv8 model on the frame
        results = model.predict(frame)

        # Count detected vehicles
        detected_vehicles = len(results[0].boxes) if results and results[0].boxes else 0
        vehicle_counts[f"Lane {i + 1}"] += detected_vehicles  # Increment the vehicle count for this lane

        # Draw bounding boxes for detected vehicles
        for box in results[0].boxes:
            x1, y1, x2, y2 = map(int, box.xyxy[0])
            cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
            cv2.putText(frame, "Vehicle", (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX,
                        0.5, (0, 255, 0), 2, cv2.LINE_AA)

        # Display the processed frame (if you want to visualize it)
        # cv2.imshow(f"Lane {i+1} - Frame {frame_count}", frame)

    cap.release()

    # Wait for user input to continue to the next video
    print(f"\nFinished processing {video_file}. Vehicle count: {vehicle_counts[f'Lane {i + 1}']}")
    input("Press Enter to continue to the next video...")

cv2.destroyAllWindows()

# 🚦 Adjusting Signal Times Based on Traffic Density 🚦
total_vehicles = sum([count for count in vehicle_counts.values()])

if total_vehicles > 0:
    # Compute new signal times dynamically for each lane
    for lane, count in vehicle_counts.items():
        adjusted_time = int(count * 2)  # Multiply by 2 to get a better scaling effect
        adjusted_time = max(10, min(adjusted_time, 60))  # Ensure it stays between 10 and 60 seconds

        # Special adjustment logic based on the lane (green light priority for Lane 1)
        if lane == "Lane 1":
            # For Lane 1 (green first), adjust depending on the vehicle count:
            if count < 5:
                adjusted_time = max(adjusted_time - 5, 10)  # Reduce time if vehicles are few
            elif count > 10:
                adjusted_time = min(adjusted_time + 5, 60)  # Increase time if vehicles are many

        # Adjust timing for other lanes based on traffic intensity:
        else:
            if count > 10:  # If more than 10 cars, give extra time
                adjusted_time = min(adjusted_time + 5, 60)  # Increase time if more cars are detected
            elif count <= 5:  # If fewer than 5 cars, reduce time
                adjusted_time = max(adjusted_time - 5, 10)  # Decrease time if few cars are detected

        signal_times[lane] = adjusted_time  # Update signal times

# 🔥 Print Results 🔥

print("\n🚦 **Final Traffic Analysis** 🚦")
for lane in vehicle_counts:
    print(f"{lane}: {vehicle_counts[lane]} vehicles -> Adjusted Signal Time: {signal_times[lane]}s")
