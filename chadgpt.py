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

def stitch_no_audio(args, prefix="", directory=""):
    inputs = ""
    if not prefix:
        for i in args:
            inputs += "-i " + os.path.join(directory, i) + " "
    else:
        for i in args:
            inputs += "-i " + prefix + i + " "

    cmd = "ffmpeg.exe -n -hwaccel_output_format cuda " + inputs + "-filter_complex \""
    for i in range(len(args)):
        cmd += "[" + str(i) + ":v] "
    cmd += "concat=n=" + str(len(args)) + ":v=1 [v]\" -map \"[v]\" -c:v h264_nvenc -b:v 50M -maxrate:v 100M -metadata:s:v:0 rotate=180 "
    output_file = args[0][:2] + "XX" + args[0][4:]
    cmd += os.path.join(directory, output_file)
    print("Final cmd: " + cmd)
    return cmd
    result = subprocess.run(list(cmd.split(" ")), stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    print(result.stdout)

def stitch_with_audio(args, prefix="", directory=""):
    inputs = ""
    if not prefix:
        for i in args:
            inputs += "-i " + os.path.join(directory, i) + " "
    else:
        for i in args:
            inputs += "-i " + prefix + i + " "

    cmd = "ffmpeg.exe -n -hwaccel_output_format cuda " + inputs + "-filter_complex \""
    for i in range(len(args)):
        cmd += "[" + str(i) + ":v] " + "[" + str(i) + ":a] "
    cmd += "concat=n=" + str(len(args)) + ":v=1:a=1 [v] [a]\" -map \"[v]\" -map \"[a]\" -c:v h264_nvenc -b:v 50M -maxrate:v 100M "
    output_file = args[0][:2] + "XX" + args[0][4:]
    cmd += os.path.join(directory, output_file)
    print("Final cmd: " + cmd)
    return cmd
    result = subprocess.run(list(cmd.split(" ")), stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    print(result.stdout)

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print('Usage: python script.py DIRECTORY')
        sys.exit(1)
    directory = sys.argv[1]
    grouped_files = group_files(directory)
    cmds = []
    for key in sorted(grouped_files.keys(), key=int):
        files = sorted(grouped_files[key])
        has_audio_file = any(has_audio(os.path.join(directory, file)) for file in files)
        if has_audio_file:
            cmds.append(stitch_with_audio(files, directory=directory))
        else:
            cmds.append(stitch_no_audio(files, directory=directory))
        print(f'Group {key}: {"has" if has_audio_file else "does not have"} an audio file')
    with open("commands.txt", "w") as f:
        f.write('\r\n'.join(cmds))
