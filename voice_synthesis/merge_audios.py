#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Jul  8 01:43:51 2024

@author: lrxwisdom001
"""
#%%
import os
import re
from pydub import AudioSegment

#本script的逻辑是先把台词部分合成，算出音乐插入点时间，在建立另一套音轨，在对应时间点上加入音乐
#可以有另一套逻辑，可以用于将来有多个音轨的情况。按序号依次扫码文件，如果是对话就加到第一音轨
#如果是音乐就加到第二音轨，其他音轨如果内容不够就加入空白片段，如果需要太长了就截取。

def merge_temp(temp_directory = '../Output_temp/', merge_file_name = 'final_combined_audio.mp3'):
    # 获取文件列表并按编号排序
    files = os.listdir(temp_directory)
    # 过滤并排序文件列表
    filtered_files = [f for f in files if re.search(r'^(\d+)', f)]
    sorted_files = sorted(filtered_files, key=lambda x: int(re.search(r'^(\d+)', x).group(1)))

    # 分离音乐和语音文件
    music_files = [f for f in sorted_files if '_music_' in f]
    voice_files = [f for f in sorted_files if '_voice_' in f]

    # 定义1秒的静音
    silence_1s = AudioSegment.silent(duration=1000)

    # 加载音频文件并替换空文件为3秒的静音
    def load_audio(file_path):
        try:
            audio = AudioSegment.from_file(file_path)
            return audio
        except:

            print(file_path,"fail to load. Replacing with 3-second silence...")
            return silence_1s
        

    # 加载音频文件
    music_audios = [load_audio(os.path.join(temp_directory, f)) for f in music_files]
    voice_audios = [load_audio(os.path.join(temp_directory, f)) for f in voice_files]

    # 获取音乐文件的序号
    music_indices = [int(re.search(r'^(\d+)', f).group(1)) for f in music_files]

    #%%
    # 创建一个空白音频段，用于合并
    combined_music_audio = AudioSegment.silent(duration=0)
    combined_voice_audio = AudioSegment.silent(duration=0)

    # 定义2秒的静音
    silence = AudioSegment.silent(duration=2000)

    # 处理语音文件，并在音乐文件序号+1的voice前面加2秒的空白
    total_audio_length = 0
    music_in_times = []

    #防止出现第一个文件就是音乐的情况
    if 0 in [index for index in music_indices]:
        # print(0, "音乐插入点",0)
        combined_voice_audio = combined_voice_audio+silence
        music_in_times.append(total_audio_length)

    for i in range(len(voice_audios)):
        combined_voice_audio += voice_audios[i]
        total_audio_length = len(combined_voice_audio)
        if i+1 in [index for index in music_indices]:
            # print(i+1, "音乐插入点",total_audio_length)
            combined_voice_audio = combined_voice_audio+silence
            music_in_times.append(total_audio_length)
        
    #音乐要在所有voice结束后5秒结束
    music_in_times.append(total_audio_length+5000)  
    #%%
    # 处理音乐文件
    combined_music_audio += AudioSegment.silent(duration=music_in_times[0])

    for i in range(len(music_audios)):
        music_length_max = music_in_times[i+1]-music_in_times[i]
        music_audio = music_audios[i]
        # fade_to_half_duration = 3000  # 3秒内降低到原来音量的一半
        # hold_half_volume_duration = 30000 - initial_play_time - fade_to_half_duration  # 保持一半音量到30秒
        fade_out_duration = 50000  # 最后五秒逐渐减弱

        music_audio = (music_audio[:music_length_max-5000] + 
                    music_audio[music_length_max-5000:music_length_max].fade_out(fade_out_duration))
        music_audio -= 20 #音量减20分贝
        combined_music_audio += music_audio


    #%%
    # # 确保音频片段为单声道
    # combined_music_audio = combined_music_audio.set_channels(1)
    # combined_voice_audio = combined_voice_audio.set_channels(1)

    # #%% from_mono_audiosegments 方法不知道为什么就是没法让两个部分等长，导致合并失败
    # # 确保两个音频片段长度相等
    # max_length = max(len(combined_music_audio), len(combined_voice_audio))
    # if len(combined_music_audio) < max_length:
    #     combined_music_audio = combined_music_audio + AudioSegment.silent(duration=max_length - len(combined_music_audio))
    # if len(combined_voice_audio) < max_length:
    #     combined_voice_audio = combined_voice_audio + AudioSegment.silent(duration=max_length - len(combined_voice_audio))

    # 将音乐音频与文字稿音频合并成一个立体声音频
    if len(combined_music_audio) > len(combined_voice_audio):
        final_combined_audio = combined_music_audio.overlay(combined_voice_audio) 
    elif len(combined_music_audio) < len(combined_voice_audio):
        final_combined_audio = combined_voice_audio.overlay(combined_music_audio)


    # 保存合并后的音频
    final_combined_audio.export('../static/'+merge_file_name, format="mp3")

    # print(f"音频合并完成,请查看{merge_file_name}")
# %%
if __name__ == "__main__":
    merge_temp()