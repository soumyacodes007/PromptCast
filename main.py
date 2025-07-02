# app.py
import streamlit as st
import os
import re
from datetime import datetime

# Import all processing modules
from src.input_processor import process_pdf, process_url, process_prompt
from src.script_generator import generate_podcast_script
from src.audio_generator import create_podcast_audio
from src.video_producer import merge_audio_to_video
from src.audiogram_generator import create_audiogram_video
from src.config import (
    OUTPUT_DIR, VIDEO_TEMPLATE_PATH, PROMPT_FLIRTY_COUPLE, 
    PROMPT_HUMOROUS_BROS, PROMPT_PROFESSIONAL
)

# --- Streamlit Page Configuration ---
st.set_page_config(
    page_title="AI Podcast Generator",
    page_icon="🎙️",
    layout="wide"
)

# --- Pre-flight Check: Ensure assets exist ---
if not os.path.exists(VIDEO_TEMPLATE_PATH):
    st.error(f"FATAL ERROR: The video template 'pre_recorded_video.mp4' could not be found in the 'assets' folder.")
    st.stop()

# Create output directory if it doesn't exist
if not os.path.exists(OUTPUT_DIR):
    os.makedirs(OUTPUT_DIR)

# --- UI Components ---
st.title("🎙️ AI Podcast Generator")
st.markdown("Turn any topic, URL, or PDF into a polished podcast video with just a few clicks!")

# --- Sidebar Controls ---
st.sidebar.title("Generation Controls")

st.sidebar.header("1. Choose Input")
input_method = st.sidebar.radio("Input method:", ("Topic Prompt", "URL", "PDF File"))

st.sidebar.header("2. Choose Personality")
personality_choice = st.sidebar.selectbox(
    "Podcast style:",
    ("Two Friends (Humorous)", "Flirty Couple (Playful)", "Professional Interview")
)

st.sidebar.header("3. Choose Video Style")
video_choice = st.sidebar.selectbox(
    "Video type:",
    ("Generate Waveform Video", "Use Pre-recorded Template")
)

# --- Main Page Input Area ---
source_text = ""
output_filename_base = ""
user_prompt = ""
user_url = ""
uploaded_file = None
temp_pdf_path = None

if input_method == "Topic Prompt":
    user_prompt = st.text_area("Enter the podcast topic or a detailed prompt:", height=150)
    if user_prompt:
        output_filename_base = re.sub(r'\W+', '_', user_prompt.lower()[:30])
elif input_method == "URL":
    user_url = st.text_input("Enter the URL to scrape:")
    if user_url:
        output_filename_base = "url_scrape_" + datetime.now().strftime("%Y%m%d%H%M%S")
elif input_method == "PDF File":
    uploaded_file = st.file_uploader("Upload your PDF file:", type="pdf")
    if uploaded_file is not None:
        temp_pdf_path = os.path.join(OUTPUT_DIR, uploaded_file.name)
        with open(temp_pdf_path, "wb") as f:
            f.write(uploaded_file.getbuffer())
        output_filename_base = os.path.splitext(os.path.basename(uploaded_file.name))[0]

# --- Generation Button and Process ---
if st.button("🚀 Generate Podcast!", type="primary", use_container_width=True):
    if (input_method == "URL" and user_url) or (input_method == "Topic Prompt" and user_prompt) or (input_method == "PDF File" and uploaded_file):
        with st.container(border=True):
            try:
                # STEP 1: Process Input
                with st.status("Step 1/4: Processing Input...", expanded=True) as status:
                    if input_method == "Topic Prompt": source_text = process_prompt(user_prompt)
                    elif input_method == "URL": source_text = process_url(user_url)
                    elif input_method == "PDF File": source_text = process_pdf(temp_pdf_path)
                    st.write("✅ Input processed."); status.update(label="Input Processed!", state="complete")

                # STEP 2: Generate Script
                with st.status("Step 2/4: Generating Podcast Script...", expanded=True) as status:
                    if personality_choice == "Two Friends (Humorous)": selected_prompt = PROMPT_HUMOROUS_BROS
                    elif personality_choice == "Flirty Couple (Playful)": selected_prompt = PROMPT_FLIRTY_COUPLE
                    else: selected_prompt = PROMPT_PROFESSIONAL
                    podcast_script = generate_podcast_script(source_text, selected_prompt)
                    st.write("✅ Script generated."); status.update(label="Script Generation Complete!", state="complete")
                with st.expander("View Generated Script"):
                    st.text_area(label="script", value=podcast_script, height=300, label_visibility="collapsed")

                # STEP 3: Generate Audio
                with st.status("Step 3/4: Generating Podcast Audio...", expanded=True) as status:
                    audio_path = create_podcast_audio(podcast_script, output_filename_base)
                    st.write("✅ Audio generated."); status.update(label="Audio Generation Complete!", state="complete")
                st.subheader("Preview the Generated Audio"); st.audio(audio_path)

                # STEP 4: Produce Final Video
                with st.status("Step 4/4: Producing Final Video...", expanded=True) as status:
                    final_video_path = os.path.join(OUTPUT_DIR, f"{output_filename_base}.mp4")
                    if video_choice == "Generate Waveform Video":
                        video_title = user_prompt if user_prompt else os.path.basename(output_filename_base).replace("_", " ").title()
                        create_audiogram_video(audio_path, video_title, final_video_path)
                    else:
                        merge_audio_to_video(audio_path, output_filename_base)
                    st.write("✅ Final video produced!"); status.update(label="Video Production Complete!", state="complete")

                # Final Output
                st.success("🎉 Your podcast video has been generated successfully!")
                st.subheader("Watch Your Final Podcast Video")
                video_file = open(final_video_path, 'rb')
                video_bytes = video_file.read()
                st.video(video_bytes)
                st.download_button(label="Download Video (MP4)", data=video_bytes, file_name=f"{output_filename_base}.mp4", mime="video/mp4", use_container_width=True)

            except Exception as e:
                st.error(f"An error occurred: {e}")
                import traceback
                st.code(traceback.format_exc())
    else:
        st.warning("Please provide an input source before generating.")