import os
from elevenlabs import ElevenLabs

def get_tts_client():
    key = os.getenv("ELEVEN_API_KEY")
    if not key:
        raise RuntimeError("❌ ELEVEN_API_KEY missing in environment!")
    return ElevenLabs(api_key=key)

def generate_tts_audio(text: str, plant_name: str, disease: str):
    """
    Generates an MP3 audio file for diary text using ElevenLabs TTS.
    Returns the saved audio file path.
    """
    client = get_tts_client()

    # Clean filenames
    pname = plant_name.lower().replace(" ", "_")
    dname = disease.lower().replace(" ", "_")
    out_path = f"audio_{pname}_{dname}.mp3"

    # Call ElevenLabs TTS
    # FIX: correct function call → eleventlabs.text_to_speech
    try:
        audio_stream = client.text_to_speech.convert(
            text=text,
            voice_id="pNInz6obpgDQGcFmaJgB",  # Emily Voice
            model_id="eleven_turbo_v2"
        )

        with open(out_path, "wb") as f:
            for chunk in audio_stream:
                f.write(chunk)

        return out_path

    except Exception as e:
        raise RuntimeError(f"TTS generation failed: {str(e)}")
