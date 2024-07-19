import streamlit as st
import ffmpeg
import moviepy.editor as mp
import requests
import os
import replicate
from dotenv import load_dotenv
import subprocess
from tqdm import tqdm
import time

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


def split_video(input_file, num_clip):
    # Инициализация команды PowerShell
    command = ["powershell", "-File", "./video_split.ps1", str(input_file), str(num_clip)]
    result = subprocess.run(command, capture_output=True, text=True)

    # Инициализация списка файлов
    output_files = []

    # Проверка кода возврата процесса
    if result.returncode != 0:
        raise subprocess.CalledProcessError(result.returncode, result.args, output=result.stdout,
                                            stderr=result.stderr)

    output_files = []

    # Используем tqdm для отображения прогресса
    with tqdm(total=num_clip, desc="Processing clips", unit="clip") as pbar:
        for line in result.stdout.splitlines():
            print(line.strip())  # Печатаем каждую строку вывода
            if "Processing clip" in line:
                pbar.update(1)
            elif "Completed clip" in line:
                clip_path = line.split(":")[-1].strip()
                output_files.append(clip_path)

    print(output_files)


# Обработка видео и создание клипов
if st.button("Process Video"):
    if uploaded_file is not None:
        # Сохранение загруженного файла
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


        # Process video to create clips
        # (You need to implement the logic to split the video into clips and generate audio track)
        output = replicate.run(
            "riffusion/riffusion:8cf61ea6c56afd61d8f5b9ffd14d7c216c0a93844ce2d82ac1c9ecc9c7f24e05",
            input={
                "alpha": 0.5,
                "prompt_a": "funky synth solo",
                "prompt_b": "90's rap",
                "denoising": 0.75,
                "seed_image_id": "vibes",
                "num_inference_steps": 50
            }
        )
        print(output)

        st.success("Video processed successfully")

        # Provide download link for the clips (you need to generate the clips first)
        # st.download_button("Download Clips", data="path_to_clips_archive.zip")

    else:
        st.error("Please upload a video file")
