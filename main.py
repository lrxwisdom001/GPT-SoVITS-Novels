#!/usr/bin/python
# -*- coding: UTF-8 -*-
import json,os
from gpt_script import generate_gpt_response,extract_info_from_gpt
from voice_script import synthesize_voice

def main():
    # 示例提示词
    
    config_file = 'voice_server_config.json'
    novel_file = 'novel_original.txt'
    md_file_path = 'novel_modified4tts.md'
    characters_file_path = 'characters2voice.json'
    voice_data_path = os.path.expanduser('../Voice_data')


    # 读取配置文件
    with open(config_file, 'r', encoding='utf-8') as file:
        config = file.read()

    # 读取小说内容
    with open(novel_file, 'r', encoding='utf-8') as file:
        novel_content = file.read()

    # 让GPT改写小说格式，生成角色语音对应表

    response = generate_gpt_response(config, novel_content)

    # 如何你没有openai的api_key,这里提供一个openai返回的response样本，以供测试其他部分
    # response = '首先，我需要找出小说中的所有角色以及他们的性别，然后将这些角色的信息填充到指定的Json格式中。接下来，会把小说改写成台词本。\n\n根据小说内容，以下是出现的角色及其性别：\n- 旁白：未知（使用aierhaisen)\n- 羽亲王：男性\n- 夏侯琢：男性\n- 燕青之：男性\n- 李丢丢：男性\n- 高希宁：女性\n\n下面是生成的JSON信息：\n```json\n[\n  {"character": "旁白", "name": "aierhaisen", "p": 9881},\n  {"character": "羽亲王", "name": "wulang", "p": 9882},\n  {"character": "夏侯琢", "name": "bannite", "p": 9883},\n  {"character": "燕青之", "name": "wulang", "p": 9882},\n  {"character": "李丢丢", "name": "bannite", "p": 9883},\n  {"character": "高希宁", "name": "paimeng", "p": 9884}\n]\n```\n\n接下来，把小说改写成台词本的形式：\n```markdown\n**旁白**：第四十八章 两小无猜一大傻\n书名： 不让江山 作者： 知白 \n\n**旁白**：羽亲王殿下亲自到了教习小食堂那边去请教食堂师傅们饭菜做法，以他的身份，自然不会有谁阻拦，倒是把那些食堂师傅吓着了，一个个脸色惶恐不安。\n\n**羽亲王**：羽亲王很开心，他这样的人对他父亲说两三句狠话，便是最后的骄傲和自尊，也是他对亲人狠厉的极限。\n\n**旁白**：可实际上，在他父亲面前，他的伪装并不好。\n\n**旁白**：身份带来了诸多便利，别人苦求都办不到的事，亲王一言就可轻松做到。比如夏侯琢说他想看父亲做饭是什么样子，而羽亲王觉得夏侯琢现在身上有伤，进厨房会被油烟呛着，所以问了一句能不能把炊具之类的东西搬到燕青之的小院里。\n\n**羽亲王**：他问一句，哪有人会说不行的。\n\n**旁白**：于是小厨房那边的人全都忙活起来，锅碗瓢盆油盐酱醋，一股脑的往燕青之的小院里搬，还用最短的时间搭起来一个土灶，大铁锅已经刷的干干净净。\n\n**旁白**：燕青之和李丢丢拎着修好的木桶回来，看到小院里这热闹的样子两个人都懵了一下。\n\n**燕青之**：我的菜！\n\n**旁白**：燕青之脸色大变，冲回小院里后才松了口气，虽然人多，好在人们都刻意避开他种的菜苗，不然的话这乱七八糟的，早就被踩没了。\n\n**旁白**：燕青之长长的松了口气，看向夏侯琢，夏侯琢朝着他微笑着说了三个字。\n\n**夏侯琢**：不客气。\n\n**旁白**：燕青之一笑，想着原来是他帮忙守着。\n\n**旁白**：夏侯琢一脸你该怎么谢我的表情，虽然没说话，可是眼神里已经足够表达清楚了，燕青之回了一个你要是不来有这屁事的眼神，夏侯琢随即把邪恶的手伸向了他身边稚嫩的幼苗。\n\n**燕青之**：住手！\n\n**旁白**：燕青之看了看那菜苗：“苗在人在，苗亡你亡。”\n\n**旁白**：夏侯琢的手还是伸了出去，不过是从地上捡起来一个小土块，用很娘的姿势打在燕青之身上，用很娘的语气说了一声讨厌。\n\n**旁白**：燕青之打了个寒颤......\n\n**旁白**：在一边的李丢丢看到这一幕后都惊了，自言自语似的说道。\n\n**李丢丢**：这才睡了先生床一晚，他怎么就这样了？\n\n**旁白**：所有人的视线都因为这句话而看过来，夏侯琢和燕青之同时朝着李丢丢走过去，李丢丢转身就跑，在那一刻仿若飞升成了神话故事里的陆地剑仙，如贴地飞行一样。\n\n**旁白**：羽亲王在燕青之那小院里学习怎么做菜，高院长也要在一边陪着，还得夸着，比哄孩子还累。\n\n**旁白**：李丢丢不喜欢这样的场面，借机逃离小院后就到了树林那边，果然看到高希宁坐在那边矮墙上，如以往一样晃着那两条小长腿，一边的腮帮子鼓鼓的，也不知道嘴里有什么东西。\n\n**李丢丢**：你在吃什么？\n\n**旁白**：高希宁张开嘴给他看了看：“硬糖，可甜。”\n\n**旁白**：她从腰畔挂着的可爱至极的小荷包里取出来两块递给李丢丢，李丢丢打开糖纸看了看，瞧着黑了吧唧的，放进嘴里后一股特别浓厚的蔗糖味道就溢了出来。\n\n**高希宁**：甜吧。\n\n**高希宁**：我自己做的。\n```'
    #提取chatGPT的response信息
    extract_info_from_gpt(response,characters_file_path,md_file_path)
    synthesize_voice(md_file_path, characters_file_path, config,voice_data_path)

if __name__ == "__main__":
    main()
