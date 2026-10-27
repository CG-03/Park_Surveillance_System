import stream as st
import pandas as pd
import hashlib
import os
import tempfile
import cv2
import numpy as np
# ----------------- OPENCV FULL PATCH FOR STREAMLIT + YOLO -----------------





from ultralytics import YOLO

# -------------------------------------------------
# PAGE CONFIG
# -------------------------------------------------
st.set_page_config(page_title="AI Park Surveillance", layout="wide")

# -------------------------------------------------
# LOAD CSS
# -------------------------------------------------
def load_css():
    with open("styles/neumorphism.css") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

load_css()

# -------------------------------------------------
# CONSTANTS
# -------------------------------------------------
USERS_FILE = "users.csv"
MODEL_PATH = "yolov8n.pt"

# -------------------------------------------------
# SESSION STATE
# -------------------------------------------------
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "page" not in st.session_state:
    st.session_state.page = "login"

# -------------------------------------------------
# UTILS
# -------------------------------------------------
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def load_users():
    if os.path.exists(USERS_FILE):
        return pd.read_csv(USERS_FILE)
    return pd.DataFrame(columns=["name", "email", "password"])

def save_user(name, email, password):
    df = load_users()
    df.loc[len(df)] = [name, email, hash_password(password)]
    df.to_csv(USERS_FILE, index=False)

# -------------------------------------------------
# AUTH PAGES
# -------------------------------------------------
def register_page():
    st.markdown('<div class="neu-card">', unsafe_allow_html=True)
    st.title("📝 Registration")

    name = st.text_input("Full Name", key="reg_name")
    email = st.text_input("Email", key="reg_email")
    password = st.text_input("Password", type="password", key="reg_password")
    confirm = st.text_input("Confirm Password", type="password", key="reg_confirm")

    if st.button("Create Account", key="reg_btn"):
        users = load_users()
        if not name or not email or not password:
            st.error("All fields required")
        elif password != confirm:
            st.error("Passwords do not match")
        elif email in users["email"].values:
            st.error("Email already exists")
        else:
            save_user(name, email, password)
            st.success("Registration successful")
            st.session_state.page = "login"
            st.rerun()

    st.markdown("</div>", unsafe_allow_html=True)

def login_page():
    st.markdown('<div class="neu-card">', unsafe_allow_html=True)
    st.title("🔐 Login")

    email = st.text_input("Email", key="login_email")
    password = st.text_input("Password", type="password", key="login_password")

    if st.button("Login", key="login_btn"):
        users = load_users()
        hashed = hash_password(password)
        user = users[(users.email == email) & (users.password == hashed)]

        if user.empty:
            st.error("Invalid credentials")
        else:
            st.session_state.logged_in = True
            st.session_state.username = user.iloc[0]["name"]
            st.session_state.page = "dashboard"
            st.rerun()

    st.markdown("</div>", unsafe_allow_html=True)

# -------------------------------------------------
# YOLO VIDEO PROCESSING
# -------------------------------------------------
def process_video(video_path):
    model = YOLO(MODEL_PATH)
    cap = cv2.VideoCapture(video_path)

    fps = int(cap.get(cv2.CAP_PROP_FPS))
    w = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    h = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

    out_path = tempfile.NamedTemporaryFile(delete=False, suffix=".mp4").name
    out = cv2.VideoWriter(out_path, cv2.VideoWriter_fourcc(*"mp4v"), fps, (w, h))

    stats = {"Authorized": 0, "Unauthorized": 0}

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        results = model(frame, conf=0.5)

        for box in results[0].boxes:
            x1, y1, x2, y2 = map(int, box.xyxy[0])
            cls = int(box.cls[0])
            conf = float(box.conf[0])

            if cls == 0:  # person
                color = (0, 255, 0)
                label = f"Authorized {conf:.2f}"
                stats["Authorized"] += 1
            else:
                color = (0, 0, 255)
                label = f"Unauthorized {conf:.2f}"
                stats["Unauthorized"] += 1

            cv2.rectangle(frame, (x1, y1), (x2, y2), color, 2)
            cv2.putText(frame, label, (x1, y1 - 10),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.6, color, 2)

        out.write(frame)

    cap.release()
    out.release()
    return out_path, stats

# -------------------------------------------------
# DASHBOARD
# -------------------------------------------------
def dashboard():
    st.sidebar.success(f"👤 {st.session_state.username}")

    if st.sidebar.button("Logout"):
        st.session_state.clear()
        st.session_state.page = "login"
        st.rerun()

    st.markdown('<div class="neu-card">', unsafe_allow_html=True)
    st.title("🎥 AI Park Surveillance Dashboard")
    st.write("Upload a park surveillance video to analyze activities.")
    st.markdown("</div>", unsafe_allow_html=True)

    uploaded = st.file_uploader("Upload Video (.mp4 / .avi)", type=["mp4", "avi"])

    if uploaded:
        with tempfile.NamedTemporaryFile(delete=False) as tmp:
            tmp.write(uploaded.read())
            video_path = tmp.name

        if st.button("▶️ Start Processing"):
            with st.spinner("Analyzing video frames..."):
                output_video, stats = process_video(video_path)

            col1, col2 = st.columns([2, 1])

            with col1:
                st.markdown('<div class="neu-card">', unsafe_allow_html=True)
                st.subheader("Processed Video")
                st.video(output_video)
                st.markdown("</div>", unsafe_allow_html=True)

            with col2:
                st.markdown('<div class="neu-card">', unsafe_allow_html=True)
                st.subheader("📊 Activity Analytics")
                total = sum(stats.values())
                for k, v in stats.items():
                    pct = (v / total * 100) if total else 0
                    st.metric(k, v, f"{pct:.1f}%")
                st.markdown("</div>", unsafe_allow_html=True)

# -------------------------------------------------
# SIDEBAR NAV
# -------------------------------------------------
if not st.session_state.logged_in:
    nav = st.sidebar.radio("Navigation", ["Login", "Register"])
    st.session_state.page = nav.lower()

# -------------------------------------------------
# ROUTER
# -------------------------------------------------
if st.session_state.page == "login":
    login_page()
elif st.session_state.page == "register":
    register_page()
elif st.session_state.page == "dashboard" and st.session_state.logged_in:
    dashboard()