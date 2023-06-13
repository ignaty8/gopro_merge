import os
import re
import sys
import subprocess

def group_files(directory):
    pattern = r'^GX[0-9]{6}.[Mm][Pp]4$'
    grouped_files = {}
    for filename in os.listdir(directory):
        if re.match(pattern, filename):
            key = filename[4:8]
            if key not in grouped_files:
                grouped_files[key] = []
            grouped_files[key].append(filename)
    return grouped_files

def has_audio(video_path):
    cmd = ['ffprobe', '-i', video_path, '-show_streams', '-select_streams', 'a', '-loglevel', 'error']
    result = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    return result.stdout != b''

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print('Usage: python script.py DIRECTORY')
        sys.exit(1)
    directory = sys.argv[1]
    grouped_files = group_files(directory)
    print(grouped_files)


'''
STITCHER NO AUDIO:
import sys, subprocess, os

print (sys.argv)
assert(len(sys.argv[1:]) >= 2)
args = sys.argv[1:-1]

inputs = ""
for i in args:
    inputs += "-i " + i + " "

cmd = "-hwaccel_output_format cuda " + inputs + "-filter_complex \""
for i in range(len(args)):
    cmd += "[" + str(i) + ":v] "
cmd += "concat=n=" + str(len(args)) + ":v=1 [v]\" -map \"[v]\" -c:v h264_nvenc -b:v 50M -maxrate:v 100M -metadata:s:v:0 rotate=180 " + sys.argv[-1]
print("Final cmd: " + cmd)
os.system("ffmpeg.exe " + cmd)
#process = subprocess.Popen(["ffmpeg.exe",cmd], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
#stdout, stderr = process.communicate()
#stdout, stderr

STITCHER AUDIO:
import sys, subprocess, os

print (sys.argv)
assert(len(sys.argv[1:]) >= 3)
args = sys.argv[1:-2]

inputs = ""
for i in args:
    inputs += "-i " + sys.argv[-2] + i + " "

cmd = "-hwaccel_output_format cuda " + inputs + "-filter_complex \""
for i in range(len(args)):
    cmd += "[" + str(i) + ":v] " + "[" + str(i) + ":a] "
cmd += "concat=n=" + str(len(args)) + ":v=1:a=1 [v] [a]\" -map \"[v]\" -map \"[a]\" -c:v h264_nvenc -b:v 50M -maxrate:v 100M " + sys.argv[-1]
print("Final cmd: " + cmd)
os.system("ffmpeg.exe " + cmd)
#process = subprocess.Popen(["ffmpeg.exe",cmd], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
#stdout, stderr = process.communicate()
#stdout, stderr
'''