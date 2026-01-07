import cv2
from ultralytics import YOLO
import time

VIDEO_FILE = "traffic_final_video.mp4"
model = YOLO("yolov8n.pt")

lanes = ["Lane A", "Lane B", "Lane C", "Lane D"]
GREEN_TIME = 6
PANEL_WIDTH = 360

cap = cv2.VideoCapture(VIDEO_FILE)
if not cap.isOpened():
    print("Error: Cannot open video!")
    exit()

current_lane_index = 0
remaining_time = GREEN_TIME
last_time = time.time()

while True:
    ret, frame = cap.read()
    if not ret:
        break

    frame_h, frame_w = frame.shape[:2]
    results = model(frame, verbose=False)
    detections = results[0].boxes

    laneA = len(detections)
    laneB = laneA + 2
    laneC = laneA + 4
    laneD = laneA + 1

    lane_counts = [laneA, laneB, laneC, laneD]

    if time.time() - last_time >= 1:
        remaining_time -= 1
        last_time = time.time()
        if remaining_time == 0:
            current_lane_index = (current_lane_index + 1) % 4
            remaining_time = GREEN_TIME

    current_lane = lanes[current_lane_index]

    frame = cv2.resize(frame, (960, 540))
    canvas = cv2.copyMakeBorder(frame, 0, 0, PANEL_WIDTH, 0,
                                cv2.BORDER_CONSTANT, value=(0, 0, 0))

    cv2.putText(canvas, "AI TRAFFIC CONTROLLER", (20, 50),
                cv2.FONT_HERSHEY_SIMPLEX, 1, (0,255,0), 3)

    y = 120
    for i, lc in enumerate(lane_counts):
        color = (0,255,0) if i == current_lane_index else (255,255,255)
        cv2.putText(canvas, f"{lanes[i]}: {lc} vehicles", (20, y),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.9, color, 2)
        y += 60

    cv2.putText(canvas, f"GREEN ---> {current_lane}", (20, 400),
                cv2.FONT_HERSHEY_SIMPLEX, 1, (0,255,255), 3)

    cv2.putText(canvas, f"Timer: {remaining_time}s", (20, 480),
                cv2.FONT_HERSHEY_SIMPLEX, 1, (255,255,0), 3)

    cv2.imshow("AI Traffic Controller", canvas)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
