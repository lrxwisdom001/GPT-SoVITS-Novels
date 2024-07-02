import json,glob
import re
from pydub import AudioSegment
import subprocess
import os
import psutil
import time
import requests
import wave
import io
import simpleaudio as sa
from pydub import AudioSegment

def find_process_using_port(port):
    """找到使用指定端口的进程"""
    for proc in psutil.process_iter(['pid', 'name']):
        try:
            connections = proc.connections(kind='inet')
            for conn in connections:
                if conn.laddr.port == port:
                    return proc
        except (psutil.AccessDenied, psutil.NoSuchProcess):
            continue
    return None

def release_port(port):
    """释放指定端口"""
    process = find_process_using_port(port)
    if process:
        print(f"终止占用端口 {port} 的进程: PID {process.pid}, 名称 {process.info['name']}")
        process.terminate()  # 终止进程
        process.wait(timeout=5)  # 等待进程终止
        print(f"端口 {port} 已释放。")
    # else:
    #     print(f"未找到占用端口 {port} 的进程。")

def continue_or_not(hint=''):
    while True:
        user_input = input(hint+"\n请输入 'Y' 继续 ctrl (control) + c 退出: ").strip().lower()
        if user_input == 'y':
            print("继续执行程序...")
            break

        else:
            print("无效输入，请重新输入。")

def start_GPT_SoVITS(config,voice_data_path):
    # 读取 JSON 文件
    with open('./voice_server_config.json', 'r', encoding='utf-8') as f:
        commands = json.load(f)

    print('即将开启 GPT-SoVITS服务，若开启成功会显示：\nINFO:     Uvicorn running on http://127.0.0.1:988X (Press CTRL+C to quit)\n请耐心等待，开启成功请按回车Enter继续。。。\n\n')
    time.sleep(3)
    # 存储所有子进程
    processes = []

    # 遍历每条命令并构建命令行参数字符串
    os.chdir('./GPT-SoVITS')
    #print(os.getcwd())

    for p in range(9880,9990):
        # 释放端口,好开启GPT-SoVITS
        release_port(p)

    # GPT-SoVITS api必须在这个文件夹下启动，不然报错
    for command in commands:
        cmd = [
            "python", "api.py",
            "-s", f"{voice_data_path}/{command['s']}",
            "-g", f"{voice_data_path}/{command['g']}",
            "-dr", f"{voice_data_path}/{command['dr']}",
            "-dt", f"{command['dt']}",
            "-dl", f"{command['dl']}",
            "-a", f"{command['a']}",
            "-p", f"{command['p']}"
        ]
        
        # 启动子进程
        process = subprocess.Popen(cmd)
        processes.append(process)
    #因为开启服务需要一段时间，加一个input，就暂时不显示后面的提示。
    input()

    os.chdir('../')
    # print(os.getcwd())
    #
    # 这一段没用
    # # 检查所有子进程是否成功启动
    # all_started = all(process.poll() is None for process in processes)

    # if all_started:
    #     print("所有服务已成功启动。")


    continue_or_not('请检查,角色声音对应表(novel_modified4tts.md),确认无误后，')
    continue_or_not('即将开始语音合成，本操作将先删除Output_temp文件夹中的临时文件，请确认已保留必要备份！！！')
    #清空临时文件夹
    files = glob.glob('./Output_temp/*')
    for file in files:
        try:
            os.remove(file)
        except Exception as e:
            print(f"Error deleting file {file}: {e}")



def read_and_split_md(md_file_path):
    with open(md_file_path, 'r', encoding='utf-8') as file:
        content = file.read()
    paragraphs = content.split('\n\n')
    return paragraphs

def load_characters(characters_file_path):
    with open(characters_file_path, 'r', encoding='utf-8') as file:
        characters_info = json.load(file)
    return characters_info

def parse_paragraph(paragraph, characters_info):
    paragraph = paragraph.replace('\n', '，')
    paragraph = paragraph.replace(' ', '，')
    # if paragraph.startswith('**') and '：' in paragraph:
    if '：' in paragraph:
        character, text = paragraph.split('：', 1)
        character = character.strip('*')
        for info in characters_info:
            if info["character"] == character:
                return {
                    "character": character,
                    "name": info["name"],
                    "p": info["p"],
                    "text": text.strip()
                }
    return {
        "character": "未知",
        "name": "",
        "p": "",
        "text": paragraph
    }

def generate_speech(text, port,play_after_done=False):
    time_ckpt = time.time()
    data={
        "text": text,
        "text_language": "zh"
    }
    response = requests.post("http://127.0.0.1:{}".format(port), json=data)
    if response.status_code == 400:
        raise Exception(f"GPT-SoVITS ERROR: {response.message}")
    audio_data = io.BytesIO(response.content)
    with wave.open(audio_data, 'rb') as wave_read:
        audio_frames = wave_read.readframes(wave_read.getnframes())
        audio_wave_obj = sa.WaveObject(audio_frames, wave_read.getnchannels(), wave_read.getsampwidth(), wave_read.getframerate())
    if play_after_done:
        print("start playing...")
        play_obj = audio_wave_obj.play()
        play_obj.wait_done()
    print("Audio Generation Time: %d ms\n" % ((time.time() - time_ckpt) * 1000))
    return audio_wave_obj, wave_read.getnchannels(), wave_read.getsampwidth(), wave_read.getframerate(), audio_frames

def save_audio_as_mp3(filename, channels, sampwidth, framerate, frames):
    """保存音频数据到 MP3 文件"""
    # 将音频帧转换为 AudioSegment
    audio_segment = AudioSegment(
        data=frames,
        sample_width=sampwidth,
        frame_rate=framerate,
        channels=channels
    )
    # 保存为 MP3 文件
    audio_segment.export(filename, format="mp3")
    print(f"Audio saved as {filename}")



def synthesize_voice(md_file_path, characters_file_path,config,voice_data_path):
    start_GPT_SoVITS(config,voice_data_path)
    paragraphs = read_and_split_md(md_file_path)
    characters_info = load_characters(characters_file_path)

    results = [parse_paragraph(para, characters_info) for para in paragraphs]

    mp3_files = []
    for i, entry in enumerate(results):
        text = entry['text']
        port = entry['p']
        try:
            audio_wave_obj, channels, sampwidth, framerate, frames = generate_speech(text, port)
            filename = f"./Output_temp/audio_{i}.mp3"
            mp3_files.append(filename)
            save_audio_as_mp3(filename, channels, sampwidth, framerate, frames)
        except Exception as e:
            print(f"Error generating speech for text '{text}': {e}")

    combined = AudioSegment.empty()
    for mp3_file in mp3_files:
        audio = AudioSegment.from_mp3(mp3_file)
        combined += audio

    combined.export("combined.mp3", format="mp3")
    print("合成后的音频已保存为 combined.mp3")
