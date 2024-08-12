import subprocess
import re

# TODO
language = "auto"  # "en", "zh", "auto"...
WHISPER_STREAM_PATH = "C:/Users/angellachen/whisper.cpp-master/whisper.cpp-master/examples/stream" #"...your_path.../whisper.cpp/stream"
WHISPER_MODEL_PATH = "C:/Users/angellachen/whisper.cpp-master/whisper.cpp-master/models/ggml-base.bin" #"...your_path.../whisper.cpp/models/ggml-base.bin"
WHISPER_LOG_FILE_PATH = "C:/Users/angellachen/whisper.cpp-master/my_log_file_path"


def start_whisper():
    global process
    process = subprocess.Popen([WHISPER_STREAM_PATH, "-m", WHISPER_MODEL_PATH, "-l", language, "-t", "8", "--step", "500", "--length", "5000"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)

def get_output():
    raw_output = process.stdout.readline()
    if raw_output == b'' and process.poll() is not None:
        return None
    if raw_output:
        ansi_string = raw_output.decode().strip()
        ansi_escape_pattern = re.compile(r'\x1B\[[0-?9;]*[mK]')
        output = ansi_escape_pattern.sub('', ansi_string)
        return output
    return None

def get_error():
    log_file = open(WHISPER_LOG_FILE_PATH, "w")
    stderr_output = process.stderr.read().decode().strip()
    log_file.write(stderr_output)
    log_file.close()
