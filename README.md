# AI-Based Intelligent Video Surveillance Platform for Activity Recognition and Security Management in Parks

## 📌 Project Overview
This project implements an AI-powered video surveillance system designed for public parks.  
It detects, classifies, and visualizes human activities such as walking, running, cycling, and unauthorized behavior using computer vision and deep learning techniques.

The system is built as part of an academic AI project and demonstrates real-time and recorded video analysis using modern object detection pipelines.

---

## 🎯 Key Features
- Activity recognition using object detection
- Supports recorded video input
- Bounding box visualization with labels
- Object counting and classification
- Roboflow-hosted inference workflow
- Modular and scalable project structure
- Ready for dashboard integration (Streamlit)

---

## 🧠 Technologies Used
- Python
- OpenCV
- Roboflow
- YOLO (Object Detection)
- Inference Pipelines
- NumPy
- Streamlit

---

## 📁 Project Structure
Park_Surveillance_System/
│
├── data/
│   ├── raw_videos/                # Original input videos (NOT on GitHub)
│   │   ├── walking/
│   │   │   
│   │   ├── running/
│   │   ├── cycling/
│   │   └── unauthorized/
│   │
│   ├── frames/                    # Extracted frames (auto-generated)
│   │   ├── walking/
│   │   │   
│   │   ├── running/
│   │   ├── cycling/
│   │   └── unauthorized/
│   │
│   └── annotated/                 # Roboflow dataset (LOCAL ONLY)
│       ├── train/
│       │   ├── images/
│       │   └── labels/
│       ├── valid/
│       │   ├── images/
│       │   └── labels/
│       ├── test/
│       │   ├── images/
│       │   └── labels/
│       └── data.yaml
│
├── models/                        # Trained YOLO models (optional)
│   └── best.pt
│
├── runs/                          # YOLO training outputs (auto)
│
├── src/                           # Core Python logic
│   ├── annotate.py
│   ├── preprocess.py
│   ├── utils.py
│
├── app/
│   └── streamlit_app.py           # Streamlit dashboard
│
├── run_surveillance.py            # InferencePipeline execution (MAIN)
│
├── yolov8n.pt                     # Base YOLO model
│
├── requirements.txt
├── README.md
├── README_dataset.md              # Dataset explanation (optional)
├── .gitignore
└── venv/                          # Virtual environment (NOT on GitHub)

Milestone 2 

📌 Milestone 2: Detection Model Training & Evaluation
Objective

The objective of Milestone 2 was to train, fine-tune, and evaluate an object detection model capable of identifying authorized and unauthorized activities in park surveillance videos. This milestone focuses on improving detection quality, validating model performance using standard metrics, and enabling real-time video testing.

🔧 Model Training

Trained a YOLOv8 object detection model using a custom annotated dataset.

Used pre-trained YOLOv8 weights to leverage transfer learning.

Training was performed for ~50 epochs to ensure stable convergence.

Dataset included multiple activity classes such as:

Authorized (e.g., walking, cycling)

Unauthorized (e.g., crowding, restricted activities)

🎯 Data Augmentation

To improve generalization and robustness across different park conditions:

Applied built-in YOLO augmentations including:

Horizontal flipping

Brightness and lighting variations

These augmentations help handle real-world scenarios such as:

Different camera angles

Changing daylight conditions

Crowd density variations

📊 Model Evaluation & Metrics

Model performance was evaluated using the test dataset and YOLO’s built-in validation pipeline.

Final Model Performance 

From the last epoch 

Precision: 86.56%

Recall: 85.41%

mAP@0.5: 91.13%



✅ This meets and exceeds your milestone requirement of
mAP@0.5 > 0.85 for authorized class

Key observations:

Authorized activity detection achieved strong precision and recall.

Unauthorized class showed higher sensitivity, with some false positives under crowded scenes.

Overall detection performance improved compared to initial baseline training.

📉 Confusion Matrix & Error Analysis

Generated a confusion matrix to analyze class-wise predictions.

Identified common misclassification patterns:

Overlapping people causing confusion between authorized and unauthorized.

Background elements occasionally triggering false positives.

These insights will guide further dataset balancing and future model improvements.

🎥 Video Testing (detect.py)

Implemented a detect.py script for real-time testing on recorded videos.

Features:

Bounding boxes with class labels and confidence scores

Green boxes for authorized activities

Red boxes + alert message for unauthorized detections

Successfully tested on multiple park-like video scenarios.

🛠️ Project Structure Considerations

Heavy training artifacts (runs/, .pt files, datasets) are excluded using .gitignore.

Code, configuration files, metrics, and scripts are tracked for reproducibility.

Repository is kept clean and mentor-review friendly.



✅ Milestone 2 Conclusion

Milestone 2 has been successfully completed with the following outcomes:

✔ YOLOv8 detection model trained and fine-tuned

✔ Data augmentation applied for real-world robustness

✔ Model evaluated using standard metrics (mAP, Precision, Recall)

✔ Confusion matrix generated and analyzed

✔ Real-time video detection implemented and validated