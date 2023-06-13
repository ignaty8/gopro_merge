import os
import re
import subprocess
import sys

def has_audio(video_path):
    cmd = ['ffprobe', '-i', video_path, '-show_streams', '-select_streams', 'a', '-loglevel', 'error']
    result = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    return result.stdout != b''

def group_files(directory):
    pattern = r'^GX[0-9]{6}.MP4'
    grouped_files = {}
    for filename in os.listdir(directory):
        if re.match(pattern, filename):
            key = filename[4:8]
            if key not in grouped_files:
                grouped_files[key] = []
            grouped_files[key].append(filename)
    return grouped_files

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print('Usage: python script.py DIRECTORY')
        sys.exit(1)
    directory = sys.argv[1]
    grouped_files = group_files(directory)
    for key in sorted(grouped_files.keys(), key=int):
        files = grouped_files[key]
        has_audio_file = any(has_audio(os.path.join(directory, file)) for file in files)
        print(f'Group {key}: {"has" if has_audio_file else "does not have"} an audio file')
