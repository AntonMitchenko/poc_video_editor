# Standard library imports
import os
import datetime

# Third-party library imports
from tqdm import tqdm
from moviepy.editor import VideoFileClip


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
    """
    Generates a list of string ranges based on the total number of clips and the number of columns.

    Parameters:
    num_clips (int): The total number of clips.
    num_col (int): The size of each range or the number of columns.

    Returns:
    list of str: A list containing ranges in the format "start-end".

    Example:
    >>> generate_ranges(10, 3)
    ['1-3', '4-6', '7-9', '10-12']
    """
    ranges = []
    start = 1

    # Loop until the starting point exceeds the total number of clips
    while start <= num_clips:
        end = start + num_col
        ranges.append(f"{start}-{end-1}")
        start += num_col

    return ranges


def split_list(lst, n):
    """
    Splits a list into smaller sublists of specified size.

    Parameters:
    lst (list): The list to be split.
    n (int): The size of each sublist.

    Returns:
    generator: A generator yielding sublists of size n.

    Example:
    list(split_list([1, 2, 3, 4, 5, 6], 2))
    [[1, 2], [3, 4], [5, 6]]
    """
    for i in range(0, len(lst), n):
        yield lst[i:i + n]

