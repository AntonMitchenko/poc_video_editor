import ffmpeg
import moviepy.editor as mp
import requests
import os
import replicate
import subprocess
from tqdm import tqdm
import datetime

def split_video(input_file, num_clip):
    """
    Splits a video into a specified number of clips using a PowerShell script.

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
    # Initialize PowerShell command
    command = ["powershell", "-File", "./video_split.ps1", str(input_file), str(num_clip), directory]
    print("start subprocess")
    result = subprocess.run(command, capture_output=True, text=True)

    # Initialize list of output files
    output_files = []

    # Check the return code of the process
    if result.returncode != 0:
        raise subprocess.CalledProcessError(result.returncode,
                                            result.args,
                                            output=result.stdout,
                                            stderr=result.stderr)

    # Use tqdm to display progress
    with tqdm(total=num_clip, desc="Processing clips", unit="clip") as pbar:
        for line in result.stdout.splitlines():
            print(line.strip())  # Print each line of output
            if "Processing clip" in line:
                pbar.update(1)
            elif "Completed clip" in line:
                clip_path = line.split(":")[-1].strip()
                output_files.append(clip_path)

    return output_files