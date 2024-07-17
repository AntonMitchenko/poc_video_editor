# Development Guide for poc_video_editor

This document provides a step-by-step guide to develop the POC video editor web application.

## Prerequisites

- Conda environment configured (see main README.md for setup instructions)
- Basic understanding of Python, Streamlit, and video/audio processing libraries

## Step-by-Step Development Guide

### Step 1: Install Required Libraries

Ensure the following libraries are included in your `requirements.in` file:

```
streamlit
ffmpeg-python
moviepy
riffusion
requests
```

To update your `requirements.in` file, add the following lines:

```plaintext
streamlit
ffmpeg-python
moviepy
requests
# Add riffusion dependency as necessary, typically a custom or specific repo URL
```

### Step 2: Setup Streamlit Application

1. Create a new file named `app.py` in the root directory of your project.

2. Add the following code to `app.py` to set up a basic Streamlit interface:

```python
import streamlit as st
import ffmpeg
import moviepy.editor as mp
import requests
import os

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

# Process the video and generate clips
if st.button("Process Video"):
    if uploaded_file is not None:
        # Save uploaded file
        with open("uploaded_video.mp4", "wb") as f:
            f.write(uploaded_file.getbuffer())

        # Process video to create clips
        # (You need to implement the logic to split the video into clips and generate audio track)
        st.success("Video processed successfully")

        # Provide download link for the clips (you need to generate the clips first)
        # st.download_button("Download Clips", data="path_to_clips_archive.zip")

    else:
        st.error("Please upload a video file")
```

### Step 3: Implement Video Processing Logic

Update the `app.py` file to include the logic for:

- Splitting the video into clips using `moviepy`.
- Generating an audio track using `riffusion`.
- Replacing the audio track in one of the clips.
- Creating a downloadable archive of the clips.

Here's an example implementation:

```python
def split_video_into_clips(video_path, num_clips):
    video = mp.VideoFileClip(video_path)
    duration = video.duration
    clip_duration = duration / num_clips

    clips = []
    for i in range(num_clips):
        start_time = i * clip_duration
        end_time = start_time + clip_duration
        clip = video.subclip(start_time, end_time)
        clip_path = f"clip_{i + 1}.mp4"
        clip.write_videofile(clip_path)
        clips.append(clip_path)

    return clips

def generate_audio(prompt, duration):
    # Call riffusion API or run locally to generate audio
    # This is a placeholder implementation
    audio_url = "https://riffusion.example.com/api/generate_audio"
    response = requests.post(audio_url, json={"prompt": prompt, "duration": duration})
    audio_path = "generated_audio.mp3"
    with open(audio_path, "wb") as f:
        f.write(response.content)
    return audio_path

def replace_audio_in_clip(clip_path, audio_path):
    clip = mp.VideoFileClip(clip_path)
    audio = mp.AudioFileClip(audio_path).set_duration(clip.duration)
    new_clip = clip.set_audio(audio)
    new_clip_path = clip_path.replace(".mp4", "_with_audio.mp4")
    new_clip.write_videofile(new_clip_path)
    return new_clip_path

if st.button("Process Video"):
    if uploaded_file is not None:
        with open("uploaded_video.mp4", "wb") as f:
            f.write(uploaded_file.getbuffer())

        clips = split_video_into_clips("uploaded_video.mp4", num_clips)
        audio_path = generate_audio(audio_prompt, clip_duration)
        updated_clip_path = replace_audio_in_clip(clips[clip_number - 1], audio_path)

        # Archive clips
        archive_path = "clips_archive.zip"
        with ZipFile(archive_path, 'w') as archive:
            for clip in clips:
                archive.write(clip)
            archive.write(updated_clip_path)

        st.success("Video processed successfully")
        st.download_button("Download Clips", data=archive_path)

    else:
        st.error("Please upload a video file")
```

### Step 4: Run the Application

1. Run the Streamlit application:
```shell
streamlit run app.py
```

2. Open your web browser and navigate to the provided local URL (typically http://localhost:8501).

### Step 5: Containerize the Application (Optional)

1. Create a `Dockerfile` in the root directory:
```dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY . .

RUN pip install pip-tools
RUN pip-compile --output-file requirements.txt requirements.in
RUN pip install -r requirements.txt

EXPOSE 8501

CMD ["streamlit", "run", "app.py"]
```

2. Build the Docker image:
```shell
docker build -t poc_video_editor .
```

3. Run the Docker container:
```shell
docker run -p 8501:8501 poc_video_editor
```

## Conclusion

Follow these steps to develop, run, and optionally containerize your POC video editor web application. Make sure to customize the placeholder implementations for splitting videos and generating audio according to your project's requirements.

For any issues or contributions, please refer to the main `README.md` file.
