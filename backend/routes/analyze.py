from fastapi import APIRouter, UploadFile, File, Form
import os
import uuid

from models.prediction_model import predict_disease
from ai.groq_client import generate_diary_text
from ai.tts_client import generate_tts_audio

router = APIRouter(prefix="/api")

UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)


@router.post("/analyze")
async def analyze_image(
    plant_name: str = Form(...),
    file: UploadFile = File(...)
):
    # Save uploaded image temporarily
    file_ext = file.filename.split(".")[-1]
    temp_path = f"{UPLOAD_DIR}/{uuid.uuid4()}.{file_ext}"

    with open(temp_path, "wb") as f:
        f.write(await file.read())

    # Run disease prediction
    disease, confidence = predict_disease(temp_path)

    # Generate diary text
    diary_text = generate_diary_text(plant_name, disease)

    # Generate voice audio file
    audio_path = generate_tts_audio(diary_text, plant_name, disease)

    return {
        "plant_name": plant_name,
        "predicted_disease": disease,
        "confidence": confidence,
        "diary_text": diary_text,
        "audio_url": audio_path,
    }
