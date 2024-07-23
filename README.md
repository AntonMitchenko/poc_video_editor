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

## Riffusion usage

### Local
To use it locally, you need a video card, which unfortunately I don’t have.

If GPU exists, you can use the following command to generate tracks:
```shell
docker run -d -p 5000:5000 --gpus=all r8.im/riffusion/riffusion@sha256:8cf61ea6c56afd61d8f5b9ffd14d7c216c0a93844ce2d82ac1c9ecc9c7f24e05
curl -s -X POST \
  -H "Content-Type: application/json" \
  -d $'{
    "input": {
      "alpha": 0.5,
      "prompt_a": "funky synth solo",
      "prompt_b": "90\'s rap",
      "denoising": 0.75,
      "seed_image_id": "agile",
      "num_inference_steps": 50
    }
  }' \
  http://localhost:5000/predictions
```
All information was taken from this [site](https://replicate.com/riffusion/riffusion?input=docker)

### Api
I chose to use the API to generate music.To do this, we need an API key that needs to be written to the env in the following way:
```shell
export REPLICATE_API_TOKEN=<paste-your-token-here>
```
Run riffusion using Replicate’s API:
```shell
output = replicate.run(
    "riffusion/riffusion:8cf61ea6c56afd61d8f5b9ffd14d7c216c0a93844ce2d82ac1c9ecc9c7f24e05",
    input={
        "alpha": 0.5,
        "prompt_a": "funky synth solo",
        "prompt_b": "90's rap",
        "denoising": 0.75,
        "seed_image_id": "agile",
        "num_inference_steps": 50
    }
)
print(output)
```
All information how use Replicate`s API was taken from this [site](https://replicate.com/riffusion/riffusion?input=python)


## Project Structure

- `main.py`: Main application script.
- `requirements.in`: List of dependencies to be installed.
- `requirements.txt`: Compiled list of dependencies.
- `Dockerfile`: Docker configuration file for containerization.
- `utils`: A folder that contains all the main functions
- `docs`: A folder that contains the necessary installation guides
- `video_for_exampls`: A folder that contains video for test 

## Deployment

To run the service in Docker:

1. Build the Docker image:
```shell
docker build -t poc_video_editor .
```

2. Run the Docker container:
```shell
docker run -p 80:80 poc_video_editor
```
