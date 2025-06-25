import cv2
from ultralytics import YOLO

# Load the model
model = YOLO('/Users/gauravtalele/PycharmProjects/PythonProject/best1.pt')

# Load the video
video_path = "/Users/gauravtalele/PycharmProjects/PythonProject1/4K Road traffic video for object detection and tracking - free download now! - Karol Majek (720p, h264).mp4"
cap = cv2.VideoCapture(video_path)

# Check if the video opened successfully
if not cap.isOpened():
    print("Error: Could not open video.")
    exit()

# Get video properties
frame_width = int(cap.get(3))
frame_height = int(cap.get(4))
fps = int(cap.get(cv2.CAP_PROP_FPS))

# Define the codec and create a VideoWriter object (optional, for saving output)
output_path = "/Users/gauravtalele/PycharmProjects/PythonProject/output.mp4"
fourcc = cv2.VideoWriter_fourcc(*'mp4v')  # Codec for MP4 format
out = cv2.VideoWriter(output_path, fourcc, fps, (frame_width, frame_height))

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break  # Exit if video ends

    # Run inference
    results = model(frame)

    # Process and display results
    for result in results:
        annotated_frame = result.plot()  # Draw detections

    # Show the frame
    cv2.imshow("YOLO Detection", annotated_frame)

    # Write the frame to output video
    out.write(annotated_frame)

    # Press 'q' to exit
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release resources
cap.release()
out.release()
cv2.destroyAllWindows()
