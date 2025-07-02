# src/video_producer.py
from moviepy.editor import VideoFileClip, AudioFileClip
from . import config

def merge_audio_to_video(audio_path: str, output_filename: str):
    """Merges the generated audio onto the video template."""
    print("Merging audio onto video template...")

    # Load the video and audio clips
    video_clip = VideoFileClip(config.VIDEO_TEMPLATE_PATH)
    audio_clip = AudioFileClip(audio_path)

    # Set the audio of the video clip to our generated audio
    final_clip = video_clip.set_audio(audio_clip)

    # If the audio is longer than the video, loop the video
    if audio_clip.duration > video_clip.duration:
        final_clip = video_clip.loop(duration=audio_clip.duration)
        final_clip = final_clip.set_audio(audio_clip)

    # Write the result to a file
    output_path = f"{config.OUTPUT_DIR}/{output_filename}.mp4"
    final_clip.write_videofile(output_path, codec="libx264", audio_codec="aac")
    
    print(f"Final video saved to: {output_path}")
    # Close clips to free up memory
    video_clip.close()
    audio_clip.close()
    final_clip.close()