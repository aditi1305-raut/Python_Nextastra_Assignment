# 🤖 AI Automated Interview & Proctoring System

A full-stack AI-powered system designed to conduct automated interviews, record candidate responses, monitor user presence using real-time proctoring, and generate a structured interview report.  
This project demonstrates AI integration, computer-vision proctoring, backend API development, and a multi-page frontend.

---

## 📌 Features

### 🔹 Interview Automation
- Auto-generates interview questions  
- Text-to-Speech (TTS) for audio-based questioning  
- Records candidate responses via microphone  
- Stores sessions and transcripts  

### 🔹 Real-Time Proctoring
- Face detection (MediaPipe)  
- Blink detection (EAR-based liveness)  
- Multi-face detection  
- Periodic video frame capture (every 2.5 seconds)  
- Proctoring flags for suspicious behavior  

### 🔹 Backend (FastAPI)
- Clean REST API architecture  
- Candidate registration  
- Audio upload & processing  
- Webcam frame processing  
- JSON-based final report  

### 🔹 Frontend (HTML/CSS/JS)
- Registration page  
- Interview dashboard  
- Proctoring page  
- Question page (TTS + recording)  
- Beautiful final report page  

---

Frontend (Browser)
├── Webcam → /frame_proctor (FastAPI)
├── Microphone → /upload_audio
├── Question Request → /generate_questions
└── TTS Request → /tts

Backend (FastAPI)
├── OpenCV + MediaPipe (Face / Blink Detection)
├── gTTS (Audio Generation)
├── SQLite Database
└── API Endpoints

Database (SQLite)
## 🧠 System Architecture

## 📁 Project Structure

ai-interview-proctor/
│
├── backend/
│ ├── main.py
│ ├── db.py
│ ├── utils.py
│ ├── cv_proctor.py
│ └── ai_interview.db
│
├── frontend/
│ ├── register.html
│ ├── interview.html
│ ├── proctor.html
│ ├── questions.html
│ ├── report.html
│ └── styles.css
│
└── README.md

---

## 🛠️ Technologies Used

- **FastAPI** (Backend)  
- **OpenCV + MediaPipe** (Proctoring)  
- **gTTS** (Text-to-Speech)  
- **SQLite** (Database)  
- **HTML, CSS, JavaScript** (Frontend UI)  
- **MediaRecorder API**  
- **Uvicorn** (Server)

---

## ⚙️ Installation

### 1. Clone the repository

bash
git clone https://github.com/<your-username>/ai-interview-proctor.git
cd ai-interview-proctor

###2. Create a virtual environment
python -m venv venv


Activate it:

Windows:

venv\Scripts\activate


Linux/Mac:

source venv/bin/activate

3. Install dependencies
pip install -r requirements.txt

🚀 Running the Application
Start Backend
cd backend
uvicorn main:app --reload --port 8001


API Docs:
👉 http://127.0.0.1:8001/docs

Start Frontend
cd ../frontend
python -m http.server 5500


Frontend:
👉 http://localhost:5500/register.html

📡 API Endpoints Overview
Method	Endpoint	Description
POST	/candidate/register	Register candidate
GET	/generate_questions	Fetch questions
POST	/tts	Convert text to audio
POST	/frame_proctor	Process webcam frames
POST	/upload_audio	Upload answer audio
GET	/report/{candidate_id}	Get final interview report

📄 Final Interview Report Includes
- Candidate details
- Timestamp
- List of questions (if added)
- Transcripts of answers
- Proctoring flags
- Professional card-styled layout

🔮 Future Enhancements
- Real Speech-to-Text (Whisper API)
- Gaze tracking & phone detection
- Identity verification using face recognition
- More question categories
- PDF export for reports
- AI scoring of responses

👨‍💻 Author
Aditi Raut
AI & Full Stack Developer
GitHub: https://github.com/aditi1305-raut
Email: aditiraut306@gmail.com

📄 License
This project is licensed under the MIT License.
