import sqlite3
import pandas as pd
import random
import os
import sys

# 读取character_voice_info.txt文件并生成character_info字典
def load_character_info(file_path):
    character_info = {}
    with open(file_path, 'r', encoding='utf-8') as file:
        lines = file.readlines()
        for line in lines:
            if line.strip():  # 跳过空行
                parts = line.strip().split()
                if len(parts) >= 4:
                    character, name, gender, description = parts[0], parts[1], parts[2], ' '.join(parts[3:])
                    character_info[character] = {"name": name, "gender": gender, "description": description}
    return character_info

# 从数据库中取回示例文件路径
def retrieve_sample_file(character):
    db_path = os.path.join(os.path.dirname(__file__), '../static/voice_files.db')
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("SELECT file_path FROM voice_files WHERE character = ? AND sentiment = 3", (character,))
    result = cursor.fetchone()
    conn.close()
    return result[0] if result else 'N/A'

# 从BGM_files.db数据库中取回BGM文件信息
def retrieve_bgm_files(sentiment):
    db_path = os.path.join(os.path.dirname(__file__), '../static/BGM_files.db')
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("SELECT music_name, file_path FROM BGM_files WHERE sentiment = ?", (sentiment,))
    results = cursor.fetchall()
    conn.close()
    return results if results else []

# 处理输入的文本
def process_input(script_text):
    # 根据指定的分隔符将脚本文本拆分为角色和音乐部分
    split_point = script_text.find("##小说台词本")
    roles = script_text[:split_point]
    script = script_text[split_point:]
    return roles, script

# 提取角色和性别信息
def extract_roles(roles_text):
    roles_list = []
    lines = roles_text.strip().split('\n')
    for line in lines:
        if "###" in line:
            role_info = line.split('：')[1] if '：' in line else line.split(':')[1]
            role_name, role_gender = role_info.split('，') if '，' in role_info else role_info.split(',')
            roles_list.append((role_name.strip(), role_gender.strip()[0:1]))  # 去掉“声”字
    return roles_list

# 提取场景信息和情感值
def extract_scenes(script_text):
    scenes = []
    lines = script_text.strip().split('\n')
    for line in lines:
        if line.startswith("### 场景"):
            scene_text = line.strip()
            # 提取情感值，处理中英文括号
            sentiment_start = scene_text.find("(") + 1
            if sentiment_start == 0:
                sentiment_start = scene_text.find("（") + 1
            sentiment_end = scene_text.find(")") if ")" in scene_text else scene_text.find("）")
            sentiment = int(scene_text[sentiment_start:sentiment_end])
            scenes.append((scene_text, sentiment))
    return scenes

# 分配角色
def assign_characters(roles_list, character_info):
    assigned_characters = []
    used_characters = set()

    # 用于在可用角色用完时循环使用已分配的角色
    gender_based_characters = {
        "男": [char for char, info in character_info.items() if info["gender"] == "男"],
        "女": [char for char, info in character_info.items() if info["gender"] == "女"]
    }

    for role_name, role_gender in roles_list:
        available_characters = [char for char in gender_based_characters[role_gender] if char not in used_characters]
        if available_characters:
            selected_char = random.choice(available_characters)
            used_characters.add(selected_char)
        else:
            # 如果没有新的角色可用，从已使用的角色中重新分配
            selected_char = random.choice(gender_based_characters[role_gender])

        selected_info = character_info[selected_char]
        sample_file = retrieve_sample_file(selected_char)
        assigned_characters.append((role_name, selected_char, selected_info["gender"], selected_info["description"], sample_file))

    return assigned_characters

# 生成角色音源的 HTML 内容
def generate_html(df, character_info):
    html_content = """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>角色音源</title>
        <link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/bootstrap/4.5.2/css/bootstrap.min.css">
        <style>
            body, .container {
                margin: 1px; /* 调整页面的外边距 */
                padding: 0;
            }
            table {
                margin: 1px;
                width: 100%;
                border-collapse: collapse; /* 去掉表格单元格之间的间隙 */
            }
            th, td {
                padding: 1px; /* 减小单元格内边距 */
            }

        </style>
        <script>
            function updateSampleFile(selectElement, audioId) {
                var selectedOption = selectElement.options[selectElement.selectedIndex];
                var audioElement = document.getElementById(audioId);
                if (audioElement) {
                    audioElement.src = selectedOption.getAttribute('data-file');
                    audioElement.load();
                }
            }
        </script>
    </head>
    <body>
        <div class="container">
            <!-- <h1 class="text-center">角色音源表</h1> -->
            <table class="table table-bordered" id=table_voice>
                <thead>
                    <tr>
                        <th>角色</th>
                        <th>音源</th>
                        <th>声音样本</th>
                    </tr>
                </thead>
                <tbody>
    """
    for index, row in df.iterrows():
        role_name, character, gender, description, sample_file = row
        html_content += f"<tr><td>{role_name}</td>"
        html_content += f"""
            <td>
                <select class="form-control" onchange="updateSampleFile(this, 'audio-{index}')">
        """
        for char, info in character_info.items():
            char_info = f"{info['name']} {info['gender']} {info['description']}"
            selected = "selected" if char == character else ""
            file_path = retrieve_sample_file(char)
            static_file_path = file_path
            html_content += f'<option value="{char}" data-file="{static_file_path}" {selected}>{char_info}</option>'
        html_content += """
                </select>
            </td>
        """

        static_file_url = sample_file

        html_content += f"""
            <td>
                <audio id="audio-{index}" controls>
                    <source src="{static_file_url}" type="audio/mpeg">
                    您的浏览器不支持 audio 元素。
                </audio>
            </td>
        """
        html_content += "</tr>"

    html_content += """
                </tbody>
            </table>
        </div>
    </body>
    </html>
    """
    return html_content

# 生成场景背景音乐的 HTML 内容
def generate_scene_html(scenes, bgm_info):
    html_content = """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>场景背景音乐</title>
        <link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/bootstrap/4.5.2/css/bootstrap.min.css">
        <style>
            body, .container {
                margin: 1px; /* 调整页面的外边距*/
                padding: 0;
            }
            table {
                margin: 1px;
                width: 100%;
                border-collapse: collapse; /* 去掉表格单元格之间的间隙 */
            }
            th, td {
                padding: 1px; /* 减小单元格内边距 */
            }

        </style>
        <script>
            function updateBGM(selectElement, audioId) {
                var selectedOption = selectElement.options[selectElement.selectedIndex];
                var audioElement = document.getElementById(audioId);
                if (audioElement) {
                    audioElement.src = selectedOption.getAttribute('data-file');
                    audioElement.load();
                }
            }
        </script>
    </head>
    <body>
        <div class="container">
            <!-- <h1 class="text-center">场景背景音乐</h1> -->
            <table class="table table-bordered" id=table_bgm>
                <thead>
                    <tr>
                        <th>场景</th>
                        <th>背景音乐</th>
                        <th>试听</th>
                    </tr>
                </thead>
                <tbody>
    """
    for index, (scene_text, sentiment) in enumerate(scenes):
        # 获取对应情感值的BGM列表
        bgm_list = bgm_info.get(sentiment, [])
        if not bgm_list:
            bgm_list = [("N/A", "N/A")]
        selected_bgm = random.choice(bgm_list)  # 随机选择一个BGM

        html_content += f"<tr><td>{scene_text}</td>"
        html_content += f"""
            <td>
                <select class="form-control" onchange="updateBGM(this, 'bgm-{index}')">
        """
        for music_name, file_path in bgm_list:
            selected = "selected" if music_name == selected_bgm[0] else ""
            html_content += f'<option value="{music_name}" data-file="{file_path}" {selected}>{music_name}</option>'
        html_content += """
                </select>
            </td>
        """

        bgm_file_path = selected_bgm[1]  # 默认选择随机选中的BGM

        html_content += f"""
            <td>
                <audio id="bgm-{index}" controls>
                    <source src="{bgm_file_path}" type="audio/mpeg">
                    您的浏览器不支持 audio 元素。
                </audio>
            </td>
        """
        html_content += "</tr>"

    html_content += """
                </tbody>
            </table>
        </div>
    </body>
    </html>
    """
    return html_content

if __name__ == "__main__":
    script = """
##登场角色

###角色1：旁白，男声
###角色2：夏侯琢，男声
###角色3：燕青之，男声
###角色4：李丢丢，男声
###角色5：高希宁，女声

##小说台词本

### 场景一:(3）[轻松愉快的背景音乐]教习小食堂

**旁白**:(3)第49章.两小无猜一大傻.书名.不让江山.作者名.知白.本章字数.3332字.更新时间.2020-09-12 13:28:31.

**旁白**:(3)羽亲王殿下亲自到了教习小食堂那边去请教食堂师傅们饭菜做法.以他的身份.自然不会有谁阻拦.倒是把那些食堂师傅吓着了.一个个脸色惶恐不安.

**旁白**:(3)夏侯琢很开心.他这样的人对他父亲说两三句狠话.便是最后的骄傲和自尊.也是他对亲人狠厉的极限.

### 场景二:(2）[紧张场景]教习小食堂

**旁白**:(2)可实际上.在他父亲面前.他的伪装并不好.身份带来了诸多便利.别人苦求都办不到的事.亲王一言就可轻松做到.

**旁白**:(2)比如夏侯琢说他想看父亲做饭是什么样子.而羽亲王觉得夏侯琢现在身上有伤.进厨房会被油烟呛着.所以问了一句能不能把炊具之类的东西搬到燕青之的小院里.他问一句.哪有人会说不行的.

**旁白**:(2)于是小厨房那边的人全都忙活起来.锅碗瓢盆油盐酱醋.一股脑的往燕青之的小院里搬.还用最短的时间搭起来一个土灶.大铁锅已经刷的干干净净.

**旁白**:(2)燕青之和李丢丢拎着修好的木桶回来.看到小院里这热闹的样子两个人都懵了一下.

**燕青之**:(5)我的菜！
   """
    script = sys.argv[1] if len(sys.argv) > 1 else ''
    roles, script = process_input(script)

    # 提取角色列表
    roles_list = extract_roles(roles)

    # 读取character_info
    character_info = load_character_info('../static/voice_data_sentiment/character_voice_info.txt')

    # 分配角色
    assigned_characters = assign_characters(roles_list, character_info)

    # 创建角色音源表格
    df = pd.DataFrame(assigned_characters, columns=["角色", "character", "gender", "description", "sample_file"])

    # 生成并保存角色音源HTML文件
    html_content = generate_html(df, character_info)
    with open('../static/character_voice.html', 'w', encoding='utf-8') as f:
        f.write(html_content)

    # 提取场景列表和情感值
    scenes = extract_scenes(script)

    # 获取每个情感值对应的BGM列表
    bgm_info = {}
    for _, sentiment in scenes:
        if sentiment not in bgm_info:
            bgm_info[sentiment] = retrieve_bgm_files(sentiment)

    # 生成并保存场景背景音乐HTML文件
    scene_html_content = generate_scene_html(scenes, bgm_info)
    with open('../static/scene_bgm.html', 'w', encoding='utf-8') as f:
        f.write(scene_html_content)

    print("HTML 文件已生成：character_voice.html 和 scene_bgm.html")
