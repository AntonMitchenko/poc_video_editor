# POC Video Editor

POC (Proof of Concept) for a video editor web application.

## Description

This project aims to develop a web application for manipulating video files. The application allows users to:

- Upload a video file.
- Specify the number of clips to divide the video file into.
- Input a prompt for generating an audio track.
- Indicate which clip to add the generated audio track to.
- Specify the number of columns for displaying the clips (to avoid long scrolling).

The output provides the user with N video files, one of which contains the generated audio track instead of the original. Users can also download all video files as an archive.

## Development guide

Here the [guide](./docs/development_guide.md)

## Features

- Video file manipulation using `ffmpeg` or `moviepy`.
- Audio track generation using [riffusion](https://github.com/riffusion/riffusion) (preferably running on GPU if possible).
- Ensures the generated audio track duration matches the clip duration.
- Optional additional settings for riffusion.
- User interface built with Streamlit.
- Docker support for easy deployment.

## Installation

1. Clone the repository:
```shell
git clone https://github.com/yourusername/poc_video_editor.git
cd poc_video_editor
```

2. Install the required dependencies:
```shell
conda create -n poc_video_editor python=3.11
conda activate poc_video_editor
pip install pip-tools
python -m pip install --upgrade pip
pip-compile --output-file requirements.txt requirements.in
pip install --user -r requirements.txt
```

## Usage

1. Run the application:
```shell
python -m streamlit run main.py
```

2. Open your web browser and navigate to the provided local URL (typically http://localhost:8501).

## Project Structure

- `app.py`: Main application script.
- `requirements.in`: List of dependencies to be installed.
- `requirements.txt`: Compiled list of dependencies.
- `Dockerfile`: Docker configuration file for containerization.

## Deployment

To run the service in Docker:

1. Build the Docker image:
```shell
docker build -t poc_video_editor .
```

2. Run the Docker container:
```shell
docker run -p 8501:8501 poc_video_editor
```
