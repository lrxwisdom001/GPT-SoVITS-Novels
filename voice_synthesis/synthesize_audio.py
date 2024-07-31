#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Jul  7 13:40:51 2024

@author: lrxwisdom001
"""
#%%
import argparse
from pydub import AudioSegment
import os
import time
import requests
import wave
import io
import simpleaudio as sa
import json
from start_GPT_SoVITS_service import start_GPT_SoVITS_service

# 输入 台词，配置 先开启一个线程启动GPT-SoVITS 监测到成功开启后， 合成语音
# 合成结束后，关闭线程

def generate_speech(text, port,play_after_done=False):
    time_ckpt = time.time()
    data={
        "text": text,
        "text_language": "zh"
    }
    response = requests.post("http://127.0.0.1:{}".format(port), json=data)
    # 构建对应的curl命令
    # curl_command = "curl -X POST http://127.0.0.1:{} -H 'Content-Type: application/json' -d '{}'".format(port, json.dumps(data))

    # 打印curl命令
    # print(curl_command)

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


#%%

if __name__ == "__main__":
    cwd = print(os.getcwd())
    voice_dir = '../static/Voice_data_sentiment/aierhaisen/'
    
    parser = argparse.ArgumentParser(description="合成音频")
    parser.add_argument('-s', default=voice_dir+'aierhaisen_e8_s136.pth', help="参数s")
    parser.add_argument('-g', default=voice_dir+'aierhaisen-e15.ckpt', help="参数g")
    parser.add_argument('-dr', default=voice_dir+'aierhaisen_5_动作快，东西掉远就难捡了。.mp3', help="参数dr")
    parser.add_argument('-dt', default='动作快，东西掉远就难捡了。', help="参数dt")
    parser.add_argument('-p', '--port', type=int, default=9885, help="端口号")
    parser.add_argument('--GPT_SoVITS_dir', default='../GPT-SoVITS/', help="GPT_SoVITS 目录")
    parser.add_argument('--dl', default='zh', help="参数dl")
    parser.add_argument('-a', default='127.0.0.1', help="参数a")
    parser.add_argument('-t', default='好吧。。。你的监测方式是正确的，它会实时读取子进程的输出。', help="参数a")
    parser.add_argument('-i', default='0', help="输出文件的序号")
    args = parser.parse_args()

    process, port = start_GPT_SoVITS_service(
        args.s,
        args.g,
        args.dr,
        args.dt,
        args.port,
        args.GPT_SoVITS_dir,
        args.dl,
        args.a
    )

    audio_wave_obj, channels, sampwidth, framerate, frames = generate_speech(args.t, args.port,play_after_done=False)
    filename = f"../Output_temp/{args.i}_voice_"+args.t+".mp3"
    save_audio_as_mp3(filename, channels, sampwidth, framerate, frames)
    #关闭GPT-SoVITs服务
    process.terminate()
    print(f"端口{port} 服务关闭！")
    print(f"端口{port} 合成完成！")
