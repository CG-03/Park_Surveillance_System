from ultralytics import YOLO
import cv2

# Load trained model
model = YOLO("runs/detect/train16/weights/best.pt")

video_path = r"data\raw_videos\running\running.mp4"
cap = cv2.VideoCapture(video_path)

if not cap.isOpened():
    print("Error: Cannot open video file")
    exit()

while True:
    ret, frame = cap.read()
    if not ret:
        break

    results = model(frame, conf=0.5)

    unauthorized_count = 0

    for box in results[0].boxes:
        x1, y1, x2, y2 = map(int, box.xyxy[0])
        cls_id = int(box.cls[0])
        conf = float(box.conf[0])

        # Class names (same order as dataset.yaml)
        label = "authorized" if cls_id == 0 else "unauthorized"

        # 🎨 Color logic
        if cls_id == 0:
            color = (0, 255, 0)      # GREEN for authorized
        else:
            color = (0, 0, 255)      # RED for unauthorized
            unauthorized_count += 1

        # Draw box
        cv2.rectangle(frame, (x1, y1), (x2, y2), color, 2)

        # Draw label
        cv2.putText(
            frame,
            f"{label} {conf:.2f}",
            (x1, y1 - 10),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.6,
            color,
            2
        )

    # 🚨 Alert text
    if unauthorized_count > 0:
        cv2.putText(
            frame,
            f"ALERT: Unauthorized detected ({unauthorized_count})",
            (30, 40),
            cv2.FONT_HERSHEY_SIMPLEX,
            1,
            (0, 0, 255),
            2
        )

    cv2.imshow("AI Park Surveillance - Video Test", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
