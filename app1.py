import streamlit as st
from ultralytics import YOLO
import cv2
import tempfile
import pandas as pd
import hashlib
import os

#Updated
#{


import base64
from pathlib import Path

def load_css():
    css_file = Path("styles/style.css").read_text()
    st.markdown(f"<style>{css_file}</style>", unsafe_allow_html=True)
def load_bg_image(image_path):
    with open(image_path, "rb") as f:
        return base64.b64encode(f.read()).decode()

bg_image = load_bg_image("assets/bg-tech.png")

st.markdown(
    f"""
    <style>
    .stApp {{
        background:
            url("data:image/png;base64,{bg_image}");
        background-size: cover;
        background-position: center;
        background-repeat: no-repeat;
        background-attachment: fixed;
    }}
    </style>
    """,
    unsafe_allow_html=True
)

load_css()
#load_bg_image()

#}

# def load_css():
#    css_path = os.path.join("styles", "style.css")
#    if os.path.exists(css_path):
#       with open(css_path) as f:
#            st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
#   else:
#        st.error("CSS file not found!")

#load_css()




# ================= PAGE CONFIG =================
st.set_page_config(
    page_title="AI Park Surveillance System",
    layout="wide"
)

# ================= SESSION STATE =================
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if "user_email" not in st.session_state:
    st.session_state.user_email = None

if "page" not in st.session_state:
    st.session_state.page = "login"

USERS_FILE = "users.csv"

# ================= UTILS =================
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def load_users():
    if not os.path.exists(USERS_FILE):
        return pd.DataFrame(columns=["email", "password"])
    return pd.read_csv(USERS_FILE)

def save_user(email, password):
    df = load_users()
    df.loc[len(df)] = [email, hash_password(password)]
    df.to_csv(USERS_FILE, index=False)

# ================= LOAD YOLO =================
@st.cache_resource
def load_model():
    return YOLO("best.pt")

model = load_model()

# ================= SIDEBAR =================
with st.sidebar:
    st.title("📌 Navigation")

    if not st.session_state.logged_in:
        if st.button("🔐 Login"):
            st.session_state.page = "login"
        if st.button("📝 Register"):
            st.session_state.page = "register"
    else:
        if st.button("🏠 Home"):
            st.session_state.page = "home"
        if st.button("⚙️ Workflow"):
            st.session_state.page = "workflow"
        if st.button("🎥 Video Analysis"):
            st.session_state.page = "dashboard"
        if st.button("🛡️ Admin Review"):
            st.session_state.page = "admin"
        if st.button("📥 Downloads"):
            st.session_state.page = "downloads"
        if st.button("🚪 Logout"):
            st.session_state.logged_in = False
            st.session_state.user_email = None
            st.session_state.page = "login"
            st.rerun()

# ================= PAGES =================
def login_page():

    st.markdown(
    """
    <style>
    .fade-title {
        font-size: 42px;
        font-weight: 700;
        text-align: center;  
        color: #000000;
        animation: fadeIn 1.5s ease;
    }
    .subtitle {
        text-align: center;
        font-size: 15px;
        color: #cfeff3;
        animation: fadeIn 2.2s ease;
    }
    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(15px); }
        to { opacity: 1; transform: translateY(0); }
    }
    </style>

    <div class="fade-title">Welcome to the AI-Powered Park Surveillance System🎥</div>
    
    """,
    unsafe_allow_html=True
)

    
    st.subheader("🔐 Login")

    email = st.text_input("Email", key="login_email")
    password = st.text_input("Password", type="password", key="login_pass")

    if st.button("Login"):
        users = load_users()
        hashed = hash_password(password)

        user = users[
            (users["email"] == email) &
            (users["password"] == hashed)
        ]

        if user.empty:
            st.error("Invalid email or password")
        else:
            st.session_state.logged_in = True
            st.session_state.user_email = email
            st.session_state.page = "home"
            st.success("Login successful")
            st.rerun()

def register_page():

    st.markdown(
    """
    <style>
    .fade-title {
        font-size: 42px;
        font-weight: 700;
        text-align: center;
        color: #000000;
        animation: fadeIn 1.5s ease;
    }
    .subtitle {
        text-align: center;
        font-size: 15px;
        color: #cfeff3;
        animation: fadeIn 2.2s ease;
    }
    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(15px); }
        to { opacity: 1; transform: translateY(0); }
    }
    </style>

    <div class="fade-title">Welcome to the AI-Powered Park Surveillance System🎥</div>
    
    """,
    unsafe_allow_html=True
)

    st.subheader("📝 Register")

    username = st.text_input("Username", key="reg_name")
    email = st.text_input("Email", key="reg_email")
    password = st.text_input("Password", type="password", key="reg_pass")
    confirm = st.text_input("Confirm Password", type="password", key="reg_confirm")

    if st.button("Create Account"):
        users = load_users()

        if not email or not password:
            st.error("All fields required")
        elif password != confirm:
            st.error("Passwords do not match")
        elif email in users["email"].values:
            st.error("User already exists")
        else:
            save_user(email, password)
            st.success("Registration successful. Please login.")
            st.session_state.page = "login"
            st.rerun()

def home_page():

    st.markdown("""
    <style>
    @keyframes fadeIn {
        from {
            opacity: 0;
            transform: translateY(20px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }

    .fade-title {
        font-size: 42px;
        font-weight: 700;
        text-align: center;
        color: #000000;
        animation: fadeIn 2s ease forwards;
        margin-bottom: 12px;
    }

    .fade-subtitle {
        text-align: center;
        font-size: 16px;
        color: #cfeff3;
        animation: fadeIn 2.4s ease forwards;
        animation-delay: 0.2s;
        opacity: 0;
        margin-bottom: 28px;
    }
    </style>

    <div class="fade-title">🌳 AI Park Surveillance System 🎥</div>
    <div class="fade-subtitle">
        Welcome to AI-powered intelligent park monitoring and safety system
    </div>
    """, unsafe_allow_html=True)
    #st.title("🌳 AI Park Surveillance System")

    st.markdown("""
    **Welcome to AI-Powered Park Surveillance System
This system is an intelligent video surveillance solution designed to monitor park activities in real time using YOLO-based deep learning models. It automatically analyzes uploaded video footage to detect, classify, and highlight human activities such as authorized movement and unauthorized behavior.

    ### 🔑 Key Features
    - Real-time activity detection
    - Authorized vs Unauthorized classification
    - Color-coded bounding boxes
    - Video analytics & reporting
    - Secure login system
    """)

def workflow_page():
    st.markdown(
    """
    <style>
    .fade-title {
        font-size: 42px;
        font-weight: 700;
        text-align: center;
        color: #000000;
        animation: fadeIn 1.5s ease;
    }
    .subtitle {
        text-align: center;
        font-size: 15px;
        color: #cfeff3;
        animation: fadeIn 2.2s ease;
    }
    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(15px); }
        to { opacity: 1; transform: translateY(0); }
    }
    </style>

    <div class="fade-title">⚙️ System Workflow 🎥</div>
    
    """,
    unsafe_allow_html=True
)
    

    st.markdown("""
                🔄 System Workflow
The AI-Powered Park Surveillance System follows a structured and secure workflow to ensure accurate activity monitoring and reliable results.
                User Authentication
                
- Users must log in using valid credentials. This ensures secure access and role-based system usage.
Video Upload
                
- Authorized users upload a recorded park surveillance video in supported formats. The system validates the file before processing.

                AI Model Processing
                
- The uploaded video is analyzed frame-by-frame using a custom-trained YOLO model. The model detects individuals and classifies activities based on trained categories.
Activity Classification
                
- Detected persons are labeled as Authorized or Unauthorized.
🟢 Green bounding boxes indicate authorized activity
🔴 Red bounding boxes indicate unauthorized or suspicious activity
                
                Result Visualization
- The processed video with detection overlays and activity statistics is displayed directly in the application without using GUI-based rendering.

                Admin Review
- Administrators can review flagged activities, verify detections, and assess security concerns.

                Report & Download
                
Final results, logs, and processed videos can be downloaded for documentation and further analysis.
   
                Summary
    1️⃣ User uploads park surveillance video  
    2️⃣ YOLO model processes video frame-by-frame  
    3️⃣ Activities are detected and classified  
    4️⃣ Green boxes → Authorized activities  
    5️⃣ Red boxes → Unauthorized activities  
    6️⃣ Analytics and reports generated  
    """)

def dashboard_page():
    st.markdown(
    """
    <style>
    .fade-title {
        font-size: 42px;
        font-weight: 700;
        text-align: center;
        color: #000000;
        animation: fadeIn 1.5s ease;
    }
    .subtitle {
        text-align: center;
        font-size: 15px;
        color: #cfeff3;
        animation: fadeIn 2.2s ease;
    }
    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(15px); }
        to { opacity: 1; transform: translateY(0); }
    }
    </style>

    <div class="fade-title">🎥 Video Analysis Dashboard 🎥</div>
    
    """,
    unsafe_allow_html=True
)
    

    confidence = st.slider("Confidence Threshold", 0.1, 0.9, 0.4, 0.05)

    uploaded_video = st.file_uploader(
        "Upload Park Surveillance Video",
        type=["mp4", "avi", "mov"]
    )

    if uploaded_video:
        temp_input = tempfile.NamedTemporaryFile(delete=False)
        temp_input.write(uploaded_video.read())

        cap = cv2.VideoCapture(temp_input.name)

        fps = int(cap.get(cv2.CAP_PROP_FPS))
        w = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        h = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

        output_path = tempfile.NamedTemporaryFile(delete=False, suffix=".mp4").name
        out = cv2.VideoWriter(
            output_path,
            cv2.VideoWriter_fourcc(*"mp4v"),
            fps,
            (w, h)
        )

        video_placeholder = st.empty()
        progress = st.progress(0)

        activity_count = {}
        frame_count = 0
        total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))

        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                break

            results = model(frame, conf=confidence)
            annotated = results[0].plot()

            for cls in results[0].boxes.cls:
                name = model.names[int(cls)]
                activity_count[name] = activity_count.get(name, 0) + 1

            out.write(annotated)

            annotated = cv2.cvtColor(annotated, cv2.COLOR_BGR2RGB)
            video_placeholder.image(
                annotated,
                channels="RGB",
                use_container_width=True
            )

            frame_count += 1
            progress.progress(min(frame_count / total_frames, 1.0))

        cap.release()
        out.release()

        st.session_state.output_video = output_path
        st.session_state.activity_df = pd.DataFrame(
            [
                [k, v]
                for k, v in activity_count.items()
            ],
            columns=["Activity", "Detections"]
        )

        st.success("Video processing completed")

def admin_page():
    st.markdown(
    """
    <style>
    .fade-title {
        font-size: 42px;
        font-weight: 700;
        text-align: center;
        color: #000000;
        animation: fadeIn 1.5s ease;
    }
    .subtitle {
        text-align: center;
        font-size: 15px;
        color: #cfeff3;
        animation: fadeIn 2.2s ease;
    }
    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(15px); }
        to { opacity: 1; transform: translateY(0); }
    }
    </style>

    <div class="fade-title">🛡️ Admin Review Panel 🎥</div>
    
    """,
    unsafe_allow_html=True
)
    

    st.dataframe(
        {
            "Time": ["00:01:12", "00:03:45"],
            "Activity": ["Unauthorized", "Vehicle"],
            "Confidence": [0.91, 0.87],
            "Status": ["RED", "RED"]
        },
        use_container_width=True
    )

def downloads_page():
    st.markdown(
    """
    <style>
    .fade-title {
        font-size: 42px;
        font-weight: 700;
        text-align: center;
        color: #000000;
        animation: fadeIn 1.5s ease;
    }
    .subtitle {
        text-align: center;
        font-size: 15px;
        color: #cfeff3;
        animation: fadeIn 2.2s ease;
    }
    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(15px); }
        to { opacity: 1; transform: translateY(0); }
    }
    </style>

    <div class="fade-title"> 📥 Downloads 🎥</div>
    
    """,
    unsafe_allow_html=True
)
   

    if "output_video" in st.session_state:
        with open(st.session_state.output_video, "rb") as f:
            st.download_button(
                "Download Processed Video",
                f,
                "processed_video.mp4",
                "video/mp4"
            )

    if "activity_df" in st.session_state:
        st.download_button(
            "Download Activity Report (CSV)",
            st.session_state.activity_df.to_csv(index=False),
            "activity_report.csv",
            "text/csv"
        )

# ================= ROUTER =================
if st.session_state.page == "login":
    login_page()
elif st.session_state.page == "register":
    register_page()
elif st.session_state.page == "home":
    home_page()
elif st.session_state.page == "workflow":
    workflow_page()
elif st.session_state.page == "dashboard":
    dashboard_page()
elif st.session_state.page == "admin":
    admin_page()
elif st.session_state.page == "downloads":
    downloads_page()