import streamlit as st
import streamlit_ext as ste
import ffmpeg
import moviepy.editor as mp
import requests
import os
import replicate
from dotenv import load_dotenv
import subprocess

from video_split import split_video
from audio_gen import (
    music_generation,
    download_music,
    add_audio_to_video,
    get_video_duration,
    loop_audio,
    remove_audio_from_video
)

# Define file paths
video_path = None
audio_file = "./audio/gen_sound.wav"
looped_audio_file = "./audio/looped_audio.wav"
video_without_audio = "./video/video_no_audio.mp4"
output_file = "./video/output_video.mp4"

# Load environment variables
if os.getenv("REPLICATE_API_TOKEN") is None:
    load_dotenv('.env')

# Set up the Streamlit interface
st.title('POC Video Editor')

# Upload video file
uploaded_file = st.sidebar.file_uploader("Choose a video file", type=["mp4", "mov", "avi"])

# Input number of clips
num_clips = st.sidebar.number_input(
    label="Enter number of clips",
    min_value=1,
    step=1,
    value=3
)

# Input prompt for generating audio track
audio_prompt = st.text_input(
    label="Enter prompt for audio generation",
    value="Lofi beats, chill, relax"
)

# Input which clip to add the generated audio track to
clip_number = st.sidebar.number_input(
    label="Enter the clip number to add the generated audio track to",
    min_value=1,
    step=1,
    value=2
)

# Input number of columns to display clips
# num_columns = st.sidebar.number_input("Enter number of columns for displaying clips", min_value=1, step=1)

# Process video and create clips
if st.button("Process Video"):
    if uploaded_file:
        # Save the uploaded file
        os.makedirs("video", exist_ok=True)
        video_path = "video/uploaded_video.mp4"
        with open(video_path, "wb") as f:
            f.write(uploaded_file.getbuffer())
    else:
        st.error("Please upload a video file")

if video_path:
    st.write("Processing video...")
    created_clips = split_video(video_path, num_clips)

    if created_clips:
        st.write("Created clips:")
        clip_columns = st.columns([1] * num_clips)
        for i, clip_path in enumerate(created_clips):
            clip_columns[i].write(clip_path)

            with clip_columns[i]:
                ste.download_button(
                    label="Download " + os.path.basename(clip_path),
                    data=clip_path,
                    file_name=os.path.basename(clip_path),
                    mime="video/mp4"
                )

        chosen_clip = created_clips[clip_number - 1]
        # Get video duration
        video_duration = get_video_duration(chosen_clip)
        st.write(f"Video duration: {video_duration} seconds")

        # Generate music based on prompt
        gened_music_url = music_generation(audio_prompt)
        download_music(gened_music_url)

        # Loop audio to match video duration
        loop_audio(audio_file, video_duration, looped_audio_file)

        # Replace audio track in video
        remove_audio_from_video(chosen_clip, video_without_audio)
        add_audio_to_video(video_without_audio, looped_audio_file, output_file)

        st.success("Video processed successfully")

        # Provide download link for the final video
        # with open(output_file, "rb") as file:
        st.download_button(
            label="Download Final Video",
            data=output_file,
            file_name=os.path.basename(output_file),
            mime="video/mp4"
        )
        output_video_container, _ = st.columns([0.33, 0.67])
        output_video_container.video(output_file, format="video/mp4", start_time=0, subtitles=None, end_time=None, loop=False,
                 autoplay=False, muted=False)

