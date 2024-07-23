import ffmpeg
import moviepy.editor as mp
import requests
import os
import replicate
import subprocess
from tqdm import tqdm
import datetime

import datetime
import subprocess
from moviepy.editor import VideoFileClip
from tqdm import tqdm

def split_video(input_file, num_clip):
    """
    Splits a video into a specified number of clips.

    Args:
        input_file (str): Path to the input video file.
        num_clip (int): Number of clips to split the video into.

    Returns:
        list: List of paths to the output clip files.
    """

    current_timestamp = datetime.datetime.now()
    formatted_timestamp = current_timestamp.strftime("%Y-%m-%d %H:%M:%S")
    print(formatted_timestamp)

    directory = str(int(current_timestamp.timestamp()))
    os.mkdir(directory)
    # Initialize list of output files
    output_files = []

    # Load the video
    video = VideoFileClip(input_file)
    duration = video.duration
    clip_duration = duration / num_clip

    # Use tqdm to display progress
    with tqdm(total=num_clip, desc="Processing clips", unit="clip") as pbar:
        for i in range(num_clip):
            start_time = i * clip_duration
            end_time = (i + 1) * clip_duration if i < num_clip - 1 else duration
            clip = video.subclip(start_time, end_time)
            clip_path = f"{directory}/clip_{i+1}.mp4"
            clip.write_videofile(clip_path, codec="libx264")
            output_files.append(clip_path)
            pbar.update(1)

    return output_files


def generate_ranges(num_clips, num_col):
    ranges = []
    start = 1

    while start <= num_clips:
        end = start + num_col
        ranges.append(f"{start}-{end-1}")
        start += num_col

    return ranges

def split_list(lst, n):
    for i in range(0, len(lst), n):
        yield lst[i:i + n]