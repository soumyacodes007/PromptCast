# src/audiogram_generator.py
import os
import numpy as np
from PIL import Image, ImageDraw, ImageFont
from moviepy.editor import *
from moviepy.audio.fx.all import audio_normalize
from scipy.io import wavfile

def create_background_image(title: str, output_path: str):
    """Creates a simple background image with text."""
    try:
        title_font = ImageFont.truetype("assets/Montserrat-Bold.ttf", 70)
        subtitle_font = ImageFont.truetype("assets/Montserrat-Regular.ttf", 35)
    except IOError:
        print("Custom fonts not found in 'assets/'. Using default font.")
        title_font = ImageFont.load_default()
        subtitle_font = ImageFont.load_default()

    img = Image.new('RGB', (1920, 1080), color=(25, 25, 25))
    d = ImageDraw.Draw(img)
    
    # Wrap title text if too long
    words = title.split()
    lines = []
    current_line = ""
    for word in words:
        if d.textlength(current_line + word, font=title_font) < 1600:
            current_line += word + " "
        else:
            lines.append(current_line)
            current_line = word + " "
    lines.append(current_line)

    y_text = 400
    for line in lines:
        d.text((960, y_text), line.strip(), font=title_font, fill=(255, 255, 255), anchor="ms")
        y_text += 80

    d.text((960, 560), "Podcast Powered by AI", font=subtitle_font, fill=(150, 150, 150), anchor="ms")
    img.save(output_path)

def generate_waveform_animation(audio_path: str, video_duration: float, bars: int = 70):
    """Creates a moviepy clip of an animated waveform."""
    samplerate, data = wavfile.read(audio_path)
    if data.ndim > 1: data = data[:, 0]
    
    data_max = np.max(np.abs(data)) or 1

    def make_frame(t):
        frame_img = Image.new('RGBA', (1920, 1080), (0, 0, 0, 0))
        draw = ImageDraw.Draw(frame_img)
        
        start_index = int(t * samplerate)
        segment = data[start_index : start_index + int(samplerate / 24)] # 24 fps
        
        if not segment.any(): return np.array(frame_img)

        rms = np.sqrt(np.mean(segment.astype(float)**2))
        normalized_rms = rms / data_max
        
        bar_width = 12
        gap_width = 8
        
        for i in range(bars):
            dist_from_center = abs(i - bars//2)
            damping = 1 - (dist_from_center / (bars//2))**2
            bar_height = max(5, normalized_rms * 600 * damping)
            
            x0 = (1920/2) + (i - bars//2) * (bar_width + gap_width)
            y0 = 1080/2 - bar_height/2 + 250
            x1 = x0 + bar_width
            y1 = 1080/2 + bar_height/2 + 250
            
            draw.rectangle([x0, y0, x1, y1], fill=(255, 255, 255, 180))
            
        return np.array(frame_img)

    return VideoClip(make_frame, duration=video_duration)

def create_audiogram_video(audio_path: str, title: str, output_path: str):
    """Generates a full audiogram video."""
    print("Generating audiogram video...")
    
    audio_clip = AudioFileClip(audio_path)
    normalized_audio = audio_normalize(audio_clip)
    temp_wav_path = audio_path.replace(".mp3", ".wav")
    normalized_audio.write_audiofile(temp_wav_path, codec='pcm_s16le')

    background_image_path = "output/background.png"
    create_background_image(title, background_image_path)
    background_clip = ImageClip(background_image_path).set_duration(normalized_audio.duration)

    waveform_clip = generate_waveform_animation(temp_wav_path, normalized_audio.duration)

    final_clip = CompositeVideoClip([background_clip, waveform_clip])
    final_clip = final_clip.set_audio(normalized_audio)
    
    final_clip.write_videofile(output_path, fps=24, codec="libx264", audio_codec="aac")
    
    os.remove(temp_wav_path)
    os.remove(background_image_path)
    print("Audiogram video generated successfully.")