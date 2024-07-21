import streamlit as st
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
uploaded_file = st.file_uploader("Choose a video file", type=["mp4", "mov", "avi"])

# Input number of clips
num_clips = st.number_input("Enter number of clips", min_value=1, step=1)

# Input prompt for generating audio track
audio_prompt = st.text_input("Enter prompt for audio generation")

# Input which clip to add the generated audio track to
clip_number = st.number_input("Enter the clip number to add the generated audio track to", min_value=1, step=1)

# Input number of columns to display clips
num_columns = st.number_input("Enter number of columns for displaying clips", min_value=1, step=1)

# Process video and create clips
if st.button("Process Video"):
    if uploaded_file is not None:
        # Save the uploaded file
        os.makedirs("video", exist_ok=True)
        video_path = "video/uploaded_video.mp4"
        with open(video_path, "wb") as f:
            f.write(uploaded_file.getbuffer())

        st.write("Processing video...")
        created_clips = split_video(video_path, num_clips)

        if created_clips:
            st.write("Created clips:")
            for clip in created_clips:
                st.write(clip)
                with open(clip, "rb") as file:
                    btn = st.download_button(
                        label="Download " + os.path.basename(clip),
                        data=file,
                        file_name=os.path.basename(clip),
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
            with open(output_file, "rb") as file:
                st.download_button(
                    label="Download Final Video",
                    data=file,
                    file_name=os.path.basename(output_file),
                    mime="video/mp4"
                )
    else:
        st.error("Please upload a video file")
