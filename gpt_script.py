from openai import OpenAI
import re
import json
import os

def generate_gpt_response(config, novel_content):
    client = OpenAI(api_key="")

    prompt1 = "以下Json中包含几个声音的信息，包括name，male，p等："
    prompt2 = '''
    以下是一段小说，先找出有几个角色有台词（包括旁白）。然后猜测每个角色的性别。旁白使用"aierhaisen"的信息，男性角色使用"wulang"或者"bannite"的信息，女性角色使用"paimeng"或者"jiuqiren"的信息。输出一个新的Json表。格式为 {"character":旁白,"name":"aierhaisen","p":9881}。然后把小说改成台词本的形式，不用分场景，开头的标题、作者也属于旁白内容，如果角色的台词带有表情动作，不要使用“**角色**：（表情动作）”的形式输出，而是改成旁白的台词。
    生成的json部分以“```json”开头。台词本部分使用md输出，以“```markdown”开头，每一段都用“**角色**：台词”的形式。
    小说内容：
    '''
    prompt = prompt1 + config + prompt2 + novel_content
    response0 = client.chat.completions.create(
        model="gpt-4o",
        messages=[{"role": "user", "content": prompt}],
        stream=False,
    )
    return response0.choices[0].message.content

def extract_info_from_gpt(response,characters_file_path,md_file_path):
    content = response
    # 使用正则表达式提取json和markdown内容
    json_match = re.search(r'```json\n(.*?)\n```', content, re.DOTALL)
    md_match = re.search(r'```markdown\n(.*?)\n```', content, re.DOTALL)

    if json_match and md_match:
        json_part = json_match.group(1)
        md_part = md_match.group(1)

        # 将JSON部分解析为字典
        json_data = json.loads(json_part)

        if os.path.exists(characters_file_path):
            while True:
                user_input = input(characters_file_path + "（角色声音对应表） 已经存在，是否更新，请输入 'Y' 更新，或 'n' 不更新：").strip().lower()
                if user_input == 'y':
                    # 保存为json文件
                    with open(characters_file_path, 'w', encoding='utf-8') as json_file:
                        json.dump(json_data, json_file, ensure_ascii=False, indent=4)
                        print("文件已更新。")
                    break
                elif user_input == 'n':
                    print("保留原始文件。")
                    break
                else:
                    print("无效输入，请重新输入。")
        else:
            # 保存为json文件
            with open(characters_file_path, 'w', encoding='utf-8') as json_file:
                json.dump(json_data, json_file, ensure_ascii=False, indent=4)
                print(characters_file_path +" 文件已保存。")
        
        if os.path.exists(md_file_path):
            while True:
                user_input = input(md_file_path + "（修改过的小说台本） 已经存在，是否更新，请输入 'Y' 更新，或 'n' 不更新：").strip().lower()
                if user_input == 'y':
                    # 保存为json文件
                    # 保存为markdown文件
                    with open(md_file_path, 'w', encoding='utf-8') as md_file:
                        md_file.write(md_part)
                        print("文件已更新。")
                    break
                elif user_input == 'n':
                    print("保留原始文件。")
                    break
                else:
                    print("无效输入，请重新输入。")
        else:
            # 保存为markdown文件
            with open(md_file_path, 'w', encoding='utf-8') as md_file:
                md_file.write(md_part)
                print(md_file_path + " 文件已保存。")

    else:
        print("无法找到JSON或Markdown内容")