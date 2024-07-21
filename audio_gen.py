import replicate
import os
from dotenv import load_dotenv
from moviepy.editor import VideoFileClip
import ffmpeg
import subprocess
import requests

if os.getenv("REPLICATE_API_TOKEN") is None:
    load_dotenv('.env')


def music_generation(prompt):
    """
    Generates music based on a given text prompt using a specific AI model.

    Args:
        prompt (str): The text prompt for generating music.

    Returns:
        str: URL of the generated music.
    """
    audio_prompt = prompt

    output = replicate.run(
        "riffusion/riffusion:8cf61ea6c56afd61d8f5b9ffd14d7c216c0a93844ce2d82ac1c9ecc9c7f24e05",
        input={
            "alpha": 0,
            "prompt_a": audio_prompt,
            "denoising": 0.75,
            "seed_image_id": "vibes",
            "num_inference_steps": 33
        }
    )
    music_url = output.get('audio')

    return music_url


def download_music(url):
    """
    Downloads music from a given URL and saves it to a local directory.

    Args:
        url (str): URL of the music file to be downloaded.

    Returns:
        None
    """
    directory_path = "./audio"
    file_name = "gen_sound.wav"
    file_path = os.path.join(directory_path, file_name)

    os.makedirs(directory_path, exist_ok=True)

    response = requests.get(url)

    if response.status_code == 200:
        with open(file_path, "wb") as file:
            file.write(response.content)
        print(f"File successfully saved as {file_path}")
    else:
        print(f"Failed to download file. Status code: {response.status_code}")


def get_video_duration(file_path):
    """
    Retrieves the duration of a video file.

    Args:
        file_path (str): Path to the video file.

    Returns:
        float: Duration of the video in seconds, or None if an error occurs.
    """
    try:
        probe = ffmpeg.probe(file_path)
        video_info = next(stream for stream in probe['streams'] if stream['codec_type'] == 'video')
        duration = float(video_info['duration'])
        return duration
    except Exception as e:
        print(f"Error retrieving video duration: {e}")
        return None


def get_media_duration(file_path):
    """
    Retrieves the duration of a media file.

    Args:
        file_path (str): Path to the media file.

    Returns:
        float: Duration of the media file in seconds.
    """
    result = subprocess.run(
        ["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "default=noprint_wrappers=1:nokey=1", file_path],
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT
    )
    return float(result.stdout)


def loop_audio(input_audio, duration, output_audio):
    """
    Loops an audio file to a specified duration.

    Args:
        input_audio (str): Path to the input audio file.
        duration (float): Duration to loop the audio.
        output_audio (str): Path to save the output audio file.

    Returns:
        None
    """
    try:
        probe = ffmpeg.probe(input_audio)
        audio_streams = [stream for stream in probe['streams'] if stream['codec_type'] == 'audio']
        if not audio_streams:
            print(f"File {input_audio} does not contain audio streams.")
            return
        (
            ffmpeg
            .input(input_audio, stream_loop=-1)
            .output(output_audio, t=duration, acodec='pcm_s16le', format='wav')
            .overwrite_output()
            .run()
        )
        print(f"Looped audio saved as {output_audio}")
    except Exception as e:
        print(f"Error looping audio: {e}")


def remove_audio_from_video(video_path, video_without_audio_path):
    """
    Removes audio from a video file.

    Args:
        video_path (str): Path to the input video file.
        video_without_audio_path (str): Path to save the video file without audio.

    Returns:
        None
    """
    try:
        (
            ffmpeg
            .input(video_path)
            .output(video_without_audio_path, an=None, format='mp4')
            .overwrite_output()
            .run()
        )
        print(f"Video without audio saved as {video_without_audio_path}")
    except Exception as e:
        print(f"Error removing audio from video: {e}")


def add_audio_to_video(video_path, audio_path, output_video_path):
    """
    Adds an audio track to a video file.

    Args:
        video_path (str): Path to the input video file.
        audio_path (str): Path to the input audio file.
        output_video_path (str): Path to save the output video file with the new audio track.

    Returns:
        None
    """
    try:
        (
            ffmpeg
            .concat(
                ffmpeg.input(video_path),
                ffmpeg.input(audio_path),
                v=1, a=1
            )
            .output(output_video_path, acodec='aac', strict='experimental', format='mp4')
            .overwrite_output()
            .run()
        )
        print(f"Video with new audio track saved as {output_video_path}")
    except Exception as e:
        print(f"Error adding audio to video: {e}")
