import cv2
import os

print("🚀 Frame extraction started...")

# ===============================
# CONFIGURATION
# ===============================

# How many frames to skip (5 = take 1 frame every 5 frames)
FRAME_SKIP = 5

# Resize all frames to same size
RESIZE_SIZE = (640, 480)

# Video source folders grouped by FINAL CLASS
ACTIVITIES = {
    "authorized": [
        "data/raw_videos/walking",
        "data/raw_videos/running",
        "data/raw_videos/cycling"
    ],
    "unauthorized": [
        "data/raw_videos/unauthorized"
    ]
}

# Output base folder
FRAME_BASE_DIR = "data/frames"

# ===============================
# FRAME EXTRACTION LOGIC
# ===============================

for label, video_folders in ACTIVITIES.items():

    output_dir = os.path.join(FRAME_BASE_DIR, label)
    os.makedirs(output_dir, exist_ok=True)

    for folder in video_folders:
        if not os.path.exists(folder):
            print(f"⚠️ Folder not found: {folder}")
            continue

        for video_file in os.listdir(folder):
            if not video_file.lower().endswith((".mp4", ".avi", ".mov")):
                continue

            video_path = os.path.join(folder, video_file)
            cap = cv2.VideoCapture(video_path)

            if not cap.isOpened():
                print(f"❌ Could not open video: {video_file}")
                continue

            print(f"🎥 Processing {video_file} → {label}")

            frame_count = 0
            saved_count = 0
            video_name = os.path.splitext(video_file)[0]

            while True:
                ret, frame = cap.read()
                if not ret:
                    break

                if frame_count % FRAME_SKIP == 0:
                    frame = cv2.resize(frame, RESIZE_SIZE)
                    frame_name = f"{video_name}_frame_{saved_count}.jpg"
                    frame_path = os.path.join(output_dir, frame_name)
                    cv2.imwrite(frame_path, frame)
                    saved_count += 1

                frame_count += 1

            cap.release()
            print(f"✅ Saved {saved_count} frames from {video_file}\n")

print("🎉 Frame extraction completed for ALL videos.")
