**其他语言版本: [English](README.md), [中文](README_zh.md).**

# GPT-SoVITS-Novels
Let Genshin characters read novels for you!

## 郑重声明：本项目提供的样本音源和文本仅供学习参考使用，请勿用于商业用途
<img src="https://github.com/lrxwisdom001/GPT-SoVITS-Novels/assets/106758196/69cb3a68-9f6e-4211-bc9b-9222efdac845" height="100">
<img src="https://github.com/lrxwisdom001/GPT-SoVITS-Novels/assets/106758196/69cb3a68-9f6e-4211-bc9b-9222efdac845" height="125">
<img src="https://github.com/lrxwisdom001/GPT-SoVITS-Novels/assets/106758196/69cb3a68-9f6e-4211-bc9b-9222efdac845" height="150">

<img src="https://github.com/lrxwisdom001/GPT-SoVITS-Novels/assets/106758196/69cb3a68-9f6e-4211-bc9b-9222efdac845" height="150">
<img src="https://github.com/lrxwisdom001/GPT-SoVITS-Novels/assets/106758196/69cb3a68-9f6e-4211-bc9b-9222efdac845" height="125">
<img src="https://github.com/lrxwisdom001/GPT-SoVITS-Novels/assets/106758196/69cb3a68-9f6e-4211-bc9b-9222efdac845" height="100">

## 什么是GPT-SoVITS-Novels？
本项目利用ChatGPT的openai api和GPT-SoVITS，快速将任意的小说文本转换成多角色联播的有声读物。

## 更新了什么？
新版本，增加网页版UI，情绪分析，可以根据角色台词感情调整语气，场景类型分配音乐。

## 快速上手
创建python 环境
 ```bash
conda create --name Novels python=3.10 ffmpeg
conda activate Novels
pip install git-lfs

  ```
git-lfs 必须安装，用brew，apt-get等工具安装也可，否则后面GPT-SoVITS会报错。

下载项目文件。
 ```bash
git clone https://github.com/lrxwisdom001/GPT-SoVITS-Novels.git
  ```
因为GitHub空间限制，本repo只有必要代码，完整包请移步Hugging Face或者百度网盘下载。
 ```bash
https://huggingface.co/datasets/lrxwisdom001/GPT-SoVITS-Novels/blob/main/GPT_SoVITS_Novels_v1.0_full_pack.zip

链接: https://pan.baidu.com/s/1zXSA-VVHhb9TfFoQ9QVPGQ?pwd=reas 提取码: reas 
  ```

安装依赖库。
 ```bash
cd GPT-SoVITS-Novels
pip install -r requirements.txt
  ```


打开网页客户端
 ```bash
python manage.py runserver
  ```
在浏览器地址栏输入， 最好使用**隐身模式**防止插件导致网页错误加载！
 ```md
http://127.0.0.1:8000
  ```

跟着网页5个步骤依次完成：

**第一步**：输入openai_key和小说原文，发送给chatGPT处理。

**第二步**：整理chatGPT处理过的台词本化的小说（**也可以用其他工具生成直接粘贴到第二步窗口开始**）

**第三步和第四步**：选择角色音源和场景音乐。

最终生成 final_combined_audio.mp3，在网页上部的信息栏显示下载链接。

台词本格式，角色台词以及场景音乐的数字代表的**情绪**，参照以下gpt prompt：
 ```prompt
 用户会提供一段小说，先找出有几个角色有台词（包括旁白，提到名字的人物但没有台词的不算）并猜测每个角色的性别。
格式为：
##登场角色

###角色1：旁白，男声
###角色2：女1，女声
###角色3：男1，男声

列举完成后空一行，输出以下一行：
##小说台词本

然后把小说改成台词本的形式，开头的标题、作者信息是属于旁白的台词。每段台词都标注语气：
1=轻急，用于恍然大悟，自言自语等语气；
2=轻缓，用于虚弱、无力、沉吟等语气；
3=中性，用于中性语气；
4=重缓，用于质问，威胁，强调、调侃等语气；
5=重急，用于危急，焦急，不耐烦等语气。
旁白的语气多数用3，可以少量用其他语气。其他角色的语气请正常分配。每一段台词的格式：
**角色名字**:(语气数字)台词
一段台词中间的空格和换行符都替换成句号。如果一段台词超过3句话，请拆拆成多段。

分个几个场景，不要超过5个，标注每个场景适合什么类型背景音乐。场景音乐类型：
1=轻急，用于轻松愉快的场景；
2=轻缓，用于悲凉的场景；
3=中性，用于一般场景；
4=重缓，用于高潮来临前，恐怖来袭的紧张场景；
5=重急，用于飙车、战斗高潮等场景。
场景的格式：
### 场景一:(语气数字)[轻松愉快的背景音乐]教习小食堂

你只需完成以上任务，不要续写小说内容！！
以纯文本形式回答。
  ```
背景音乐和角色音源分别在 static/BGMs 和 static/Voice_data_sentiment文件夹中，可参考其中的文件格式自行添加文件。
如果格式正确，每次刷新网页，static/build_audio_sql.py都会自动加载新加入的文件。





## 视频简介、教学、及效果展示
待制作


## 参考与学习
 ```code
排名不分先后
GPT-SoVITS原始项目
https://github.com/RVC-Boss/GPT-SoVITS

OpenAI API
https://openai.com/index/openai-api/

特看科技的滚石【原神全角色GPT-sovits音色模型克隆，八重神子的声音太酥了啊啊啊啊】 
https://www.bilibili.com/video/BV1rA4m157aw/?share_source=copy_web&vd_source=e8e5bbbe8195c50ca4a9ea44fdd8843c

哔哩哔哩聊天机器人
https://github.com/linyiLYi/bilibot

GPT-SoVITS 音频合成在线 Demo
https://openbayes.com/console/GraceXiii/containers/3AB3h9950IN
  ```
