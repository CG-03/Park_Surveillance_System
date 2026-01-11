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

## 🚧 Project Status
This project is currently under active development.

- Dataset integration: ⏳ in progress
- Model training: ⏳ planned
- Inference on recorded videos: ✅ implemented
- Real-time deployment: 🔜 upcoming

The repository currently focuses on system design, pipeline setup,
and inference workflow integration.
