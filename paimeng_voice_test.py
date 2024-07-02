#%%
import time
import wave
import requests
import io
import simpleaudio as sa


def generate_speech(text, port):
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
    print("start playing...")
    play_obj = audio_wave_obj.play()
    play_obj.wait_done()
    print("Audio Generation Time: %d ms\n" % ((time.time() - time_ckpt) * 1000))
    return audio_wave_obj


text = "这糖果总得取个名字吧。不如叫棍糖，棍棍糖，或者你看形状像是个大锤，叫大锤糖，锤子糖，咱们出去就卖个锤子糖......"
text = '''
旁白：夏侯琢完全没有醒悟到自己和这两个小家伙认真商量事情的时候真的变幼稚了，根本就没有去想，反而跟着融入进去。

夏侯琢：要不然叫竹糖？

李丢丢：名字还行。

高希宁：这个就叫竹竹糖？

李丢丢：谐音不好听。

夏侯琢：那就叫棍糖，棍棍糖，或者你看形状像是个大锤，叫大锤糖，锤子糖，咱们出去就卖个锤子糖......

高希宁：棒棒糖！
'''

audio = generate_speech(text, port=9880)
# %%
# print('Paimeng:',text)
# audio.play()
#%%
import json
import os

base_path = os.path.expanduser('/Users/lei/L2Pproject/GPT-SoVITS/Voice_data')
# 读取 JSON 文件
with open('/Users/lei/L2Pproject/GPT-SoVITS/voice_server_config.ini', 'r', encoding='utf-8') as f:
    commands = json.load(f)

# 遍历每条命令并构建命令行参数字符串
for command in commands:
    cmd = (
        f"python api.py "
        f"-s {base_path}/{command['s']} "
        f"-g {base_path}/{command['g']} "
        f"-dr {base_path}/{command['dr']} "
        f"-dt \"{command['dt']}\" "
        f"-dl {command['dl']} "
        f"-a {command['a']} "
        f"-p {command['p']}"
    )
    
    # 打印还原的命令行参数
    print(cmd)
# %%
text = "这糖果总得取个名字吧。不如叫棍糖，棍棍糖，或者你看形状像是个大锤，叫大锤糖，锤子糖，咱们出去就卖个锤子糖......"
audio = generate_speech(text, port=9885)
# %%
import json

def read_and_split_md(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        content = file.read()

    # 分割内容为段落
    paragraphs = content.split('\n\n')

    # 过滤掉空段落
    paragraphs = [para.strip() for para in paragraphs if para.strip()]

    return paragraphs

def load_characters(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        return json.load(file)


def parse_paragraph(paragraph, characters_info):
    paragraph = paragraph.replace('\n', ' ')
    if paragraph.startswith('**') and '：' in paragraph:
        character, text = paragraph.split('：', 1)
        character = character.strip('**')
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
    
md_file_path = 'novel_modified4tts.md'
characters_file_path = 'characters2voice.json'

paragraphs = read_and_split_md(md_file_path)
characters_info = load_characters(characters_file_path)

result = [parse_paragraph(para, characters_info) for para in paragraphs]

# 输出为 JSON 格式
json_output = json.dumps(result, ensure_ascii=False, indent=4)
print(json_output)
# %%
# 定义一个函数来处理用户输入
def continue_or_not():
    while True:
        user_input = input("请输入 'Y' 继续，或 'n' 退出: ").strip().lower()
        if user_input == 'y':
            print("继续执行程序...")
            # 这里可以放置程序继续执行的代码
            break
        elif user_input == 'n':
            print("程序已退出。")
            # 这里可以放置程序终止执行的代码
            break
        else:
            print("无效输入，请重新输入。")

# 调用函数来等待用户输入
continue_or_not()
# %%
