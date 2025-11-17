import os
os.environ["TRANSFORMERS_NO_TF"] = "1"

import torch
from PIL import Image
from transformers import AutoImageProcessor, AutoModelForImageClassification

# Model ID (NO config.py required)
MODEL_ID = "linkanjarad/mobilenet_v2_1.0_224-plant-disease-identification"

# Load once on startup
processor = AutoImageProcessor.from_pretrained(MODEL_ID)
model = AutoModelForImageClassification.from_pretrained(MODEL_ID)

device = "cuda" if torch.cuda.is_available() else "cpu"
model.to(device)

def predict_disease(image_path: str):
    """
    Predict plant disease from an image file path.
    Returns: (label: str, confidence: float)
    """

    try:
        img = Image.open(image_path).convert("RGB")
    except Exception as e:
        raise ValueError(f"Invalid image file: {e}")

    # Preprocess
    inputs = processor(images=img, return_tensors="pt")
    inputs = {k: v.to(device) for k, v in inputs.items()}

    # Model inference
    with torch.no_grad():
        logits = model(**inputs).logits

    probs = torch.softmax(logits, dim=-1).cpu().squeeze(0)
    pred_id = int(probs.argmax().item())
    confidence = float(probs[pred_id].item())
    
    # HF model stores mapping internally
    label = model.config.id2label[pred_id]

    return label.lower(), confidence
