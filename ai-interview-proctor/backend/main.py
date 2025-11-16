# backend/main.py
from fastapi import FastAPI, UploadFile, File, Form
from fastapi.responses import FileResponse, JSONResponse
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
import os, tempfile
from db import init_db, SessionLocal, Candidate, SessionLog
from utils import text_to_speech, transcribe_audio_stub
from cv_proctor import decode_base64_image, detect_faces_simple, estimate_blink
from datetime import datetime

app = FastAPI(title="AI Interview Prototype")
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])

init_db()
db = SessionLocal()

@app.post("/candidate/register")
def register_candidate(name: str = Form(...), email: str = Form(...)):
    cand = Candidate(name=name, email=email)
    db.add(cand); db.commit(); db.refresh(cand)
    return {"candidate_id": cand.id, "name": cand.name, "email": cand.email}

@app.get("/generate_questions")
def generate_questions(domain: str = "software", count: int = 5):
    # Simple static questions for prototype
    questions = [
        "Tell me about a challenging bug you fixed.",
        "Explain the difference between HTTP and HTTPS.",
        "Describe a project where you used teamwork.",
        "How do you prioritize tasks under tight deadlines?",
        "Explain a data structure you often use and why."
    ]
    return {"questions": questions[:count]}

@app.post("/tts")
def tts_endpoint(text: str = Form(...)):
    mp3_path = text_to_speech(text)
    return FileResponse(mp3_path, media_type="audio/mpeg", filename="question.mp3")

@app.post("/upload_audio")
async def upload_audio(file: UploadFile = File(...), candidate_id: int = Form(...)):
    tmp = tempfile.NamedTemporaryFile(delete=False, suffix=".webm")
    content = await file.read()
    tmp.write(content); tmp.close()
    transcript = transcribe_audio_stub(tmp.name)
    # Save into DB
    session = SessionLocal()
    log = SessionLog(candidate_id=candidate_id, transcript=transcript, proctoring_flags=[])
    session.add(log); session.commit(); session.refresh(log)
    return {"transcript": transcript, "log_id": log.id}

@app.post("/frame_proctor")
async def frame_proctor(frame_b64: str = Form(...), candidate_id: int = Form(...)):
    frame = decode_base64_image(frame_b64)
    face_count = detect_faces_simple(frame)
    bl = estimate_blink(frame)
    flags = {"num_faces": face_count, "liveness": bl}
    session = SessionLocal()
    latest = session.query(SessionLog).filter(SessionLog.candidate_id == int(candidate_id)).order_by(SessionLog.created_at.desc()).first()
    if latest:
        pf = latest.proctoring_flags or []
        pf.append({"timestamp": datetime.utcnow().isoformat(), "flags": flags})
        latest.proctoring_flags = pf
        session.commit()
    return {"ok": True, "flags": flags}

@app.get("/report/{candidate_id}")
def get_report(candidate_id: int):
    session = SessionLocal()
    logs = session.query(SessionLog).filter(SessionLog.candidate_id == candidate_id).all()
    if not logs:
        return JSONResponse(status_code=404, content={"detail": "No session logs"})
    return {"candidate_id": candidate_id, "sessions": [{"id": l.id, "transcript": l.transcript, "proctoring_flags": l.proctoring_flags} for l in logs]}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
