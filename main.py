import streamlit as st
import streamlit_ext as ste
import ffmpeg
import moviepy.editor as mp
import requests
import os
import replicate
from dotenv import load_dotenv
import subprocess
import zipfile



from video_split import (
    generate_ranges,
    split_video,
    split_list
)

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
zip_file_path = './video/all_clips.zip'

# Define the URL for the POST request
url = 'http://localhost:5000/predictions'

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
num_columns = st.sidebar.number_input(
    label="Enter number of columns for displaying clips",
    min_value=1,
    step=1,
    value=3
)

st.write("Riffusion additional settings:")
# Input number of epochs for music generation
num_epochs = st.sidebar.slider(
    label="Enter number of epochs for music generation",
    min_value=1,
    max_value=100,
    step=1,
    value=33
)

#Seed spectrogram to use
selected_option = st.sidebar.selectbox(
    label="Seed spectrogram to use",
    options=("vibes", "agile", "marim", "motorway", "og_beat")
)

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

    chosen_clip = created_clips[clip_number - 1]
    # Get video duration
    video_duration = get_video_duration(chosen_clip)
    st.write(f"Clip duration: {video_duration} seconds")

    # Generate music based on prompt
    if os.getenv("LOCAL_INFERENCE"):
        print("Running locally")



        # Define the payload for the POST request
        payload = {
            "input": {
              "alpha": 0,
              "prompt_a": audio_prompt,
              "denoising": 0.75,
              "seed_image_id": "vibes",
              "num_inference_steps": num_epochs
            }
          }

        # Make the POST request
        response = requests.post(url, json=payload)
        response_dict = response.json()
        print(response_dict)
        import base64

        # Base64-encoded audio string
        audio_base64 = response_dict['output']['audio']

        # Remove the data URL scheme (if present)
        if audio_base64.startswith("data:audio/mpeg;base64,"):
            audio_base64 = audio_base64.replace("data:audio/mpeg;base64,", "")

        # Decode the Base64 string to binary data
        audio_data = base64.b64decode(audio_base64)

        # Write the binary data to a .wav file
        directory_path = "./audio"
        file_name = "gen_sound.wav"
        file_path = os.path.join(directory_path, file_name)
        with open(file_path, "wb") as audio_file:
            audio_file.write(audio_data)

        print("Audio file saved as output.wav")

    else:
        print("Running on Replicate")
        gened_music_url = music_generation(audio_prompt, num_epochs, selected_option)
        download_music(gened_music_url)

    # Loop audio to match video duration
    loop_audio(audio_file, video_duration, looped_audio_file)

    # Replace audio track in video
    remove_audio_from_video(chosen_clip, video_without_audio)
    add_audio_to_video(video_without_audio, looped_audio_file, output_file)

    st.success("Video processed successfully")

    if created_clips:
        st.write("Created clips:")
        tabs = st.tabs(generate_ranges(num_clips, num_columns))
        clips_per_tab = list(split_list(created_clips, num_columns))

        for tab, clip_group in zip(tabs, clips_per_tab):
            with tab:
                clip_columns = st.columns([1] * num_columns)
                for i, clip_path in enumerate(clip_group):

                    with clip_columns[i]:
                        output_video_container, _ = st.columns([0.67,   0.33])
                        output_video_container.video(clip_path,
                                                     format="video/mp4",
                                                     start_time=0,
                                                     subtitles=None,
                                                     end_time=None,
                                                     loop=False,
                                                     autoplay=False,
                                                     muted=False)
                        ste.download_button(
                            label="Download " + os.path.basename(clip_path),
                            data=clip_path,
                            file_name=os.path.basename(clip_path),
                            mime="video/mp4"
                        )

        created_clips.append(output_file)

        # Provide download link for the final video
        output_video_container = st.container(border=True)
        with output_video_container:
            video_col, button_col = st.columns([0.7, 0.3])

        with video_col:
            st.write("Created clip with generated music:")
            output_video_container, _ = st.columns([0.33, 0.67])
            output_video_container.video(output_file,
                                         format="video/mp4",
                                         start_time=0,
                                         subtitles=None,
                                         end_time=None,
                                         loop=False,
                                         autoplay=False,
                                         muted=False)

        with button_col:
            ste.download_button(
                label="Download Final Video",
                data=output_file,
                file_name=os.path.basename(output_file),
                mime="video/mp4"
            )


            with zipfile.ZipFile(zip_file_path, 'w') as zipf:
                for clip_path in created_clips:
                    zipf.write(clip_path, os.path.basename(clip_path))

            ste.download_button(
                label="Download All Clips as ZIP",
                data=zip_file_path,
                file_name=os.path.basename(zip_file_path),
                mime="clips/zip"
            )



