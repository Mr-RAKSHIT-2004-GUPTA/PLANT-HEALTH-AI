from elevenlabs import ElevenLabs
import os

client = ElevenLabs(api_key=os.getenv("ELEVEN_API_KEY"))

def generate_tts(text, out_path):
    audio_stream = client.text_to_speech.convert(
        voice_id="pNInz6obpgDQGcFmaJgB",
        model_id="eleven_turbo_v2",
        text=text
    )

    with open(out_path, "wb") as f:
        for chunk in audio_stream:
            f.write(chunk)

    return out_path
