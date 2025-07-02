# src/audio_generator.py
import os
import io
import re
from pydub import AudioSegment
from . import config

# Correct imports for the new ElevenLabs v1.x library
from elevenlabs.client import ElevenLabs

# Initialize the client using the API key from your config
try:
    client = ElevenLabs(api_key=config.ELEVENLABS_API_KEY)
except TypeError:
    raise ValueError("ElevenLabs API key not found. Please set ELEVENLABS_API_KEY in your .env file.")

def create_podcast_audio(script: str, output_filename: str) -> str:
    """
    Generates a single audio file from a podcast script with two speakers
    using the ElevenLabs v1.x client.
    """
    print("Generating audio with ElevenLabs client...")
    
    lines = script.strip().split('\n')
    
    final_audio = AudioSegment.silent(duration=0)
    silence = AudioSegment.silent(duration=config.SILENCE_BETWEEN_SPEAKERS_MS)

    for line in lines:
        line = line.strip()
        if not line:
            continue
            
        speaker_text = ""
        current_voice_id = ""
        
        # This robust matching logic is kept from our debugging session
        if line.startswith('[Host]:') or line.startswith('[Host]::'):
            speaker_text = re.sub(r'\[Host\]::?', '', line, 1).strip()
            current_voice_id = config.VOICE_ID_HOST
        elif line.startswith('[Guest]:') or line.startswith('[Guest]::'):
            speaker_text = re.sub(r'\[Guest\]::?', '', line, 1).strip()
            current_voice_id = config.VOICE_ID_GUEST
        else:
            continue

        if not speaker_text:
            continue

        print(f"Generating audio for: {line[:60]}...")
        
        try:
            # --- THE FINAL FIX IS HERE ---
            # The parameter for the model is 'model_id', not 'model'.
            audio_stream = client.text_to_speech.stream(
                text=speaker_text,
                voice_id=current_voice_id,
                model_id="eleven_multilingual_v2" # CORRECTED PARAMETER NAME
            )
            
            audio_bytes = b"".join(chunk for chunk in audio_stream)

            if audio_bytes:
                audio_segment = AudioSegment.from_file(io.BytesIO(audio_bytes), format="mp3")
                final_audio += audio_segment + silence
            
        except Exception as e:
            print(f"ERROR generating audio for line '{line}': {e}")
            continue

    output_path = os.path.join(config.OUTPUT_DIR, f"{output_filename}.mp3")
    final_audio.export(output_path, format="mp3")
    print(f"Full podcast audio saved to: {output_path} (Duration: {len(final_audio)/1000.0}s)")
    return output_path