#%%
import sys
import subprocess
import time
import sqlite3
import re
import json
import random
import shutil
import os
import glob
from merge_audios import merge_temp

time_ckpt = time.time()
db_voice_name = '../static/voice_files.db'
db_voice = sqlite3.connect(db_voice_name)
cursor_voice = db_voice.cursor()

# 处理输入的文本
def process_input(script_text):
    # 根据指定的分隔符将脚本文本拆分为角色和音乐部分
    split_point = script_text.find("##小说台词本")
    roles = script_text[:split_point]
    script = script_text[split_point:]
    return roles, script

# 定义数据库连接和查询函数
def get_voice_info(character, sentiment, cursor):
    query = """
    SELECT text, file_path FROM voice_files
    WHERE character = ? AND sentiment = ?
    """
    cursor.execute(query, (character, sentiment))
    result = cursor.fetchone()
    if result:
        return result
    return ("Unknown text", "Unknown file_path")

def get_config_info(character, cursor):
    query = """
    SELECT sovitsweight, gptweight FROM config_files
    WHERE character = ?
    """
    cursor.execute(query, (character,))
    result = cursor.fetchone()
    if result:
        return result
    return ("Unknown sovitsweight", "Unknown gptweight")

# 读取配置文件
def process_bold_line(line,ii):
    # 在此处处理以**开头的行，是**角色**:(语气)台词格式
    match = re.match(r'\*\*(.*?)\*\*:\((\d+)\)(.*)', line)
    if match:
        character = match.group(1).strip()
        sentiment = match.group(2).strip()
        dialogue = match.group(3).strip()
        
        # 在table_voice中查找对应的cell_1值
        voice = None
        for entry in json_get['table_voice']:
            if entry['cell_0'] == character:
                voice = entry['cell_1']
                break
                # 从数据库中获取角色和情绪对应的文本和文件路径

        sample_text, sample_voice = get_voice_info(voice, sentiment, cursor_voice)
        # 从数据库中获取角色对应的 sovitsweight 和 gptweight
        sovitsweight, gptweight = get_config_info(voice, cursor_voice)
        # print(f"Character: {character}, Sentiment: {sentiment}, Dialogue: {dialogue}")
        static_dir = '../static/'
        cmd = [
            "python", "synthesize_audio.py",
            "-s", static_dir+sovitsweight,
            "-g", static_dir+gptweight,
            "-dr", static_dir+sample_voice,
            "-dt", sample_text,
            "-t", dialogue,
            "-p", str(port_init+ii),
            "-i", str(ii)] #输出文件的序号
        # print(cmd)

        process = subprocess.Popen(
        cmd,
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        universal_newlines=True,
        encoding='utf8',
        bufsize=1
        )
        return process
    # else:
    #     print(f"Line does not match pattern: {line}")


def process_scene_line(line, ii):
    # 在此处处理以### 场景开头的行
    # 查找table_bgm中的匹配项
    bgm_file = None
    for entry in json_get['table_bgm']:
        if entry['cell_0'] == line:
            bgm_file = entry['cell_1']
            break

    # # 输出结果
    # if bgm_file:
    #     print(f"The BGM file for the scene is: {bgm_file}")
    # else:
    #     print("No matching BGM file found.")

    # 复制文件并重命名
    new_music_path = os.path.join(f"../Output_temp/{ii}_music_{os.path.basename(bgm_file)}")
    shutil.copy("../static/"+bgm_file, new_music_path)
    
    # 还是建一个subprocess方便后面函数判断是否处理完成
    process = subprocess.Popen(
        ['echo', 'music copied!'],
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        universal_newlines=True,
        encoding='utf8',
        bufsize=1
    )
    return process

    return None, None

def sythesize_line(line, ii):
    print('开始合成',ii,line)
    if line.startswith('**'):
        process = process_bold_line(line,ii)
       
    elif line.startswith('### 场景'):
        process = process_scene_line(line,ii)
    return process

if __name__ == "__main__":
    
    
    #json_get sample for test
    json_get= {
  "table_bgm": [
    {
      "cell_0": "### 场景一:(3）[轻松愉快的背景音乐]教习小食堂",
      "cell_1": "BGMs/3_御剑江湖_OST.mp3"
    },
    {
      "cell_0": "### 场景二:(2）[紧张场景]教习小食堂",
      "cell_1": "BGMs/2_西游伏妖篇酒馆.mp3"
    }
  ],
  "table_voice": [
    {
      "cell_0": "旁白",
      "cell_1": "bannite"
    },
    {
      "cell_0": "夏侯琢",
      "cell_1": "wulang"
    },
    {
      "cell_0": "燕青之",
      "cell_1": "aierhaisen"
    },
    {
      "cell_0": "李丢丢",
      "cell_1": "sainuo"
    },
    {
      "cell_0": "高希宁",
      "cell_1": "qiqi"
    }
  ],
  "novel_script": """

##登场角色

###角色1：旁白，男声
###角色2：夏侯琢，男声
###角色3：燕青之，男声
###角色4：李丢丢，男声
###角色5：高希宁，女声

##小说台词本

**旁白**:(3)第49章.两小无猜一大傻.书名.不让江山.作者名.知白.本章字数.3332字.更新时间.2020-09-12 13:28:31.

### 场景一:(3）[轻松愉快的背景音乐]教习小食堂

**旁白**:(3)羽亲王殿下亲自到了教习小食堂那边去请教食堂师傅们饭菜做法.以他的身份.自然不会有谁阻拦.倒是把那些食堂师傅吓着了.一个个脸色惶恐不安.

**旁白**:(3)夏侯琢很开心.他这样的人对他父亲说两三句狠话.便是最后的骄傲和自尊.也是他对亲人狠厉的极限.

### 场景二:(2）[紧张场景]教习小食堂

**旁白**:(2)可实际上.在他父亲面前.他的伪装并不好.身份带来了诸多便利.别人苦求都办不到的事.亲王一言就可轻松做到.

**旁白**:(2)比如夏侯琢说他想看父亲做饭是什么样子.而羽亲王觉得夏侯琢现在身上有伤.进厨房会被油烟呛着.所以问了一句能不能把炊具之类的东西搬到燕青之的小院里.他问一句.哪有人会说不行的.

**旁白**:(2)于是小厨房那边的人全都忙活起来.锅碗瓢盆油盐酱醋.一股脑的往燕青之的小院里搬.还用最短的时间搭起来一个土灶.大铁锅已经刷的干干净净.

**旁白**:(2)燕青之和李丢丢拎着修好的木桶回来.看到小院里这热闹的样子两个人都懵了一下.

**燕青之**:(5)我的菜！

"""
}
    json_get = sys.argv[1] if len(sys.argv) > 1 else ''
    json_get = json.loads(json_get)
    #通过bash传递进来的json只能是字符串，要用son.loads转换成json
    # print(json_get) 
    roles, text = process_input(json_get['novel_script'])

    # 按行分割字符串
    lines = text.split('\n')

    # 统计非空行数
    non_empty_lines = [line for line in lines if line.strip()]
    num_non_empty_lines = len(non_empty_lines)-1 #剪掉首行的##小说台词本

    # print(f'非空行数: {num_non_empty_lines}')
    # 逐行处理文件内容
    port_init = 9880
    ii = 0 #输出文件的序号
    line_pause = 0
    batch_size = 6 #并行合成的段数
    processes = []

    temp_directory = '../Output_temp/'

    # 删除所有文件和文件夹
    for item in os.listdir(temp_directory):
        item_path = os.path.join(temp_directory, item)
        try:
            if os.path.isfile(item_path) or os.path.islink(item_path):
                os.remove(item_path)  # 删除文件或链接
            elif os.path.isdir(item_path):
                shutil.rmtree(item_path)  # 删除文件夹及其内容
        except Exception as e:
            print(f"Error deleting {item_path}: {e}")

    print('临时文件，已清空，开始合成。。。')

    #先启动batch_size数量的子进程，等有子进程完成后继续启动
    line_pause = 1 #剪掉首行的##小说台词本
    for line in lines[1:]: 
        # print(line) 
        if ii == batch_size:
            break
        line_pause += 1
        line = line.strip()  # 去除行首尾的空白字符   
        if not line or line == '\n':  # 跳过空行或只有换行符的行
            continue
        else:
            process_new = sythesize_line(line, ii)
            processes.append((ii, process_new))
            ii += 1


    # print('line pause:',line_pause)
    # print('sub_processes opened:',len(processes))
    # 监控并继续启动剩余的子进程
    # for ii in lines[batch_size:]:
    finished_processes = 0
    for line in lines[line_pause:]:
        # print(line)
        line = line.strip()  # 去除行首尾的空白字符  
        if not line or line == '\n':  # 跳过空行或只有换行符的行
            continue
        else:
            while True: #完成一段，更新一个subProcess
                for idx, (index, process) in enumerate(processes):
                    if process.poll() is not None:  # 检查子进程是否已完成
                        process_new = sythesize_line(line, ii)
                        processes[idx] = (ii, process_new)
                        finished_processes += 1
                        print('已完成合成：',finished_processes,'/',num_non_empty_lines)
                        print("Time passed: %d ms\n" % ((time.time() - time_ckpt) * 1000))
                        ii += 1
                        break
                else: #这else indent没错，这相当于只有for循环的最后一个if 有else
                    time.sleep(3)  # 如果没有子进程完成，等待一秒钟再检查
                    continue 
                break

    # 确保所有子进程完成
    for _, process in processes:
        process.wait()
        finished_processes += 1
        print('已完成合成：',finished_processes,'/',num_non_empty_lines)
        print("Time passed: %d ms\n" % ((time.time() - time_ckpt) * 1000))

    # for process in processes:
    #     has_process_done(process)
    print('所有音频合成完毕')
    print("Total Audio Generation Time: %d ms\n" % ((time.time() - time_ckpt) * 1000))

    #%%
    merge_temp(temp_directory = temp_directory)
    # print('All Done! Enjoy!')