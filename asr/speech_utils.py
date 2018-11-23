# !/usr/bin/env python3

import wave
import pyaudio
from pyaudio import PyAudio, paInt16
from aip import AipSpeech
import io, os, subprocess, wave
import io


CUID = '93489083242'
DEV_PID = 1537

def audio_record_rt(rec_time):
    CHUNK = 1024
    FORMAT = pyaudio.paInt16 #16bit编码格式
    CHANNELS = 1 #单声道
    RATE = 16000 #16000采样频率
    p = pyaudio.PyAudio()
    # 创建音频流
    stream = p.open(format=FORMAT, # 音频流wav格式
                    channels=CHANNELS, # 单声道
                    rate=RATE, # 采样率16000
                    input=True,
                    frames_per_buffer=CHUNK)
    print("Start Recording...")
    frames = [] # 录制的音频流
    # 录制音频数据
    for i in range(0, int(RATE / CHUNK * rec_time)):
        data = stream.read(CHUNK)
        frames.append(data)
    # 录制完成
    stream.stop_stream()
    stream.close()
    p.terminate()
    print("Recording Done...")
    # 保存音频文件
    with io.BytesIO() as wav_file:
        wf = wave.open(wav_file, 'wb')
        wf.setnchannels(CHANNELS)
        wf.setsampwidth(p.get_sample_size(FORMAT))
        wf.setframerate(RATE)
        wf.writeframes(b''.join(frames))
        wf.close()
        wav_data = wav_file.getvalue()
    return wav_data

def shutil_which(pgm):
    """
    python2 backport of python3's shutil.which()
    """
    path = os.getenv('PATH')
    for p in path.split(os.path.pathsep):
        p = os.path.join(p, pgm)
        if os.path.exists(p) and os.access(p, os.X_OK):
            return p

def play_mp3(mp3_data):
    import platform, os, stat
    # determine which player executable to use
    system = platform.system()
    path = os.path.dirname(os.path.abspath(
        __file__))  # directory of the current module file, where all the FLAC bundled binaries are stored
    player = shutil_which("mpg123")  # check for installed version first
    if player is None:  # flac utility is not installed
        if system == "Windows" and platform.machine() in ["i386", "x86", "x86_64",
                                                          "AMD64"]:  # Windows NT, use the bundled FLAC conversion utility
            player = os.path.join(path, "player", "mpg123-win32.exe")
        elif system == "Linux" and platform.machine() in ["i386", "x86", "x86_64", "AMD64"]:
            player = os.path.join(path, "player", "mpg123-linux")
        elif system == 'Darwin' and platform.machine() in ["i386", "x86", "x86_64", "AMD64"]:
            player = os.path.join(path, "player", "mpg123-mac")
        else:
            raise OSError(
                "MP3 player utility not available - consider installing the MPG123 command line application using `brew install mpg123` or your operating system's equivalent")

    try:
        stat_info = os.stat(player)
        os.chmod(player, stat_info.st_mode | stat.S_IEXEC)
    except OSError:
        pass

    process = subprocess.Popen("\"%s\" -q -" % player, stdin=subprocess.PIPE, stdout=subprocess.PIPE, shell=True)
    play_info, stderr = process.communicate(mp3_data)
    return play_info

sp_client = AipSpeech('14922410', 'NSChZHWWVwa1BSwZ36Oaya4C', '1dd0sxs2LXYRWETZ4gZSSDYDQvM6aROv')