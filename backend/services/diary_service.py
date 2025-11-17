# services/diary_service.py
import os
import json
import time

BASE_DIR = "storage"
LOG_DIR = os.path.join(BASE_DIR, "diary_logs")
IMG_DIR = os.path.join(BASE_DIR, "images")
AUDIO_DIR = os.path.join(BASE_DIR, "audio")

# Ensure folders exist
os.makedirs(LOG_DIR, exist_ok=True)
os.makedirs(IMG_DIR, exist_ok=True)
os.makedirs(AUDIO_DIR, exist_ok=True)


def save_diary_entry(plant_name, disease, diary_text, image_filename, audio_filename):
    entry_id = str(int(time.time() * 1000))

    entry = {
        "id": entry_id,
        "plant_name": plant_name,
        "disease": disease,
        "diary_text": diary_text,
        "image_url": f"/storage/images/{image_filename}",
        "audio_url": f"/storage/audio/{audio_filename}",
        "timestamp": time.time()
    }

    file_path = os.path.join(LOG_DIR, f"{entry_id}.json")
    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(entry, f, indent=2)

    return entry


def load_all_diaries():
    entries = []
    for filename in os.listdir(LOG_DIR):
        if filename.endswith(".json"):
            with open(os.path.join(LOG_DIR, filename), "r", encoding="utf-8") as f:
                entries.append(json.load(f))
    return sorted(entries, key=lambda x: x["timestamp"], reverse=True)


def load_diary(entry_id):
    file_path = os.path.join(LOG_DIR, f"{entry_id}.json")
    if not os.path.exists(file_path):
        return None
    with open(file_path, "r", encoding="utf-8") as f:
        return json.load(f)


def delete_diary(entry_id):
    path = os.path.join(LOG_DIR, f"{entry_id}.json")
    if os.path.exists(path):
        os.remove(path)
        return True
    return False
