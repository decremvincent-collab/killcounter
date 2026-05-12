import sounddevice as sd
import numpy as np
import queue
import time
from openai import OpenAI

# Mets ta clé API ici
client = OpenAI(api_key="TA_CLE_API_ICI")

# File pour stocker l'audio
audio_queue = queue.Queue()

# Callback audio
def audio_callback(indata, frames, time_info, status):
    audio_queue.put(indata.copy())

# Choisis l'ID du périphérique VB-Cable
DEVICE_ID = 3  # À ajuster selon ta machine

stream = sd.InputStream(
    samplerate=16000,
    channels=1,
    dtype='float32',
    callback=audio_callback,
    device=DEVICE_ID
)

stream.start()

print("🎧 Traduction en direct... (Ctrl+C pour arrêter)")

buffer = []

while True:
    try:
        # Récupère un petit morceau d'audio
        data = audio_queue.get()
        buffer.append(data)

        # Toutes les 3 secondes → on transcrit
        if len(buffer) > 50:
            audio_chunk = np.concatenate(buffer, axis=0)
            buffer = []

            # Convertir en wav bytes
            audio_bytes = (audio_chunk * 32767).astype(np.int16).tobytes()

            # Transcription
            transcription = client.audio.transcriptions.create(
                model="gpt-4o-mini-transcribe",
                file=("audio.wav", audio_bytes, "audio/wav"),
                language="ko"
            ).text

            if transcription.strip():
                # Traduction
                traduction = client.chat.completions.create(
                    model="gpt-4o-mini",
                    messages=[
                        {"role": "system", "content": "Tu traduis du coréen au français, naturellement."},
                        {"role": "user", "content": transcription}
                    ]
                ).choices[0].message.content.strip()

                print("\n🟦 Coréen :", transcription)
                print("🟩 Français :", traduction)

    except KeyboardInterrupt:
        print("Arrêt.")
        break
