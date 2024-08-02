**Other Language Versions: [English](README.md), [中文](README_zh.md).**

# GPT-SoVITS-Novels
Let Genshin characters read novels for you!

## Important Note: The sample audio and text provided by this project are for learning and reference only. Please do not use them for commercial purposes.
<img src="https://github.com/lrxwisdom001/GPT-SoVITS-Novels/assets/106758196/69cb3a68-9f6e-4211-bc9b-9222efdac845" height="100">
<img src="https://github.com/lrxwisdom001/GPT-SoVITS-Novels/assets/106758196/69cb3a68-9f6e-4211-bc9b-9222efdac845" height="125">
<img src="https://github.com/lrxwisdom001/GPT-SoVITS-Novels/assets/106758196/69cb3a68-9f6e-4211-bc9b-9222efdac845" height="150">

<img src="https://github.com/lrxwisdom001/GPT-SoVITS-Novels/assets/106758196/69cb3a68-9f6e-4211-bc9b-9222efdac845" height="150">
<img src="https://github.com/lrxwisdom001/GPT-SoVITS-Novels/assets/106758196/69cb3a68-9f6e-4211-bc9b-9222efdac845" height="125">
<img src="https://github.com/lrxwisdom001/GPT-SoVITS-Novels/assets/106758196/69cb3a68-9f6e-4211-bc9b-9222efdac845" height="100">

## What is GPT-SoVITS-Novels?
This project utilizes the OpenAI API and GPT-SoVITS to quickly convert any novel text into an audiobook featuring multiple characters.

## What's New?
The new version adds a web-based UI, emotion analysis, and the ability to adjust tones based on the emotional context of character dialogues and assign background music to different scene types.

## Getting Started
Create a Python environment
 ```bash
conda create --name Novels python=3.10 ffmpeg
conda activate Novels
pip install git-lfs
 ```

git-lfs must be installed. You can use tools like brew or apt-get, otherwise GPT-SoVITS will throw an error later.

Download project files.
 ```bash
git clone https://github.com/lrxwisdom001/GPT-SoVITS-Novels.git
 ```

Due to GitHub space limitations, this repository contains only the necessary code. For the full package, please visit Hugging Face or Baidu Netdisk.
 ```bash
https://huggingface.co/datasets/lrxwisdom001/GPT-SoVITS-Novels/blob/main/GPT_SoVITS_Novels_v1.0_full_pack.zip

https://pan.baidu.com/s/1zXSA-VVHhb9TfFoQ9QVPGQ?pwd=reas Code: reas 
 ```
Install dependencies.
 ```bash
cd GPT-SoVITS-Novels
pip install -r requirements.txt
 ```
Open the web client
 ```bash
python manage.py runserver
 ```
Enter the following URL in the browser address bar. It is recommended to use Safari or Incognito mode to prevent plugins from causing page loading errors!
 ```bash
http://127.0.0.1:8000
 ```
Follow the five steps on the web page to complete the process:

Step 1: Input your openai_key and the original novel text, then send it to ChatGPT for processing.

Step 2: Organize the script processed by ChatGPT (you can also generate it with other tools and paste it directly into the Step 2 window).

Steps 3 and 4: Select character voices and background music.

Finally, generate the final_combined_audio.mp3, with the download link displayed in the information bar at the top of the web page.

The script format, character dialogues, and the emotional numbers representing tone refer to the following GPT prompt:
 ```prompt
The user will provide a piece of a novel. First, identify the characters who have dialogues (including the narrator, but not characters mentioned without dialogues) and guess the gender of each character.
The format is:
##Characters

###Character 1: Narrator, Male voice
###Character 2: Female 1, Female voice
###Character 3: Male 1, Male voice

After listing the characters, leave a blank line and output the following line:
##Novel Script

Then convert the novel into a script format, with the title and author information as the narrator's dialogue. Each line of dialogue should be labeled with a tone:
1 = light urgency, for sudden realizations, self-talk, etc.;
2 = light and slow, for weakness, exhaustion, contemplation, etc.;
3 = neutral, for neutral tone;
4 = heavy and slow, for questioning, threatening, emphasizing, mocking, etc.;
5 = heavy urgency, for emergencies, anxiety, impatience, etc.
The narrator's tone should mostly be 3, with occasional use of other tones. The tones for other characters should be assigned normally. Each line of dialogue should follow the format:
**Character Name**:(Tone Number) Dialogue
Replace spaces and line breaks within a line of dialogue with periods. If a line of dialogue exceeds three sentences, split it into multiple lines.

Divide the story into several scenes, no more than five, and label the type of background music suitable for each scene. The types of background music are:
1 = light urgency, for relaxed and happy scenes;
2 = light and slow, for sad scenes;
3 = neutral, for general scenes;
4 = heavy and slow, for tense scenes before a climax or horror;
5 = heavy urgency, for car chases, battle climaxes, etc.
The format for scenes is:
### Scene One:(Tone Number) [Background Music Type] Small Dining Hall

Only complete the tasks above. Do not continue the novel's content!!
Answer in plain text.
 ```
Background music and character voices are located in the static/BGMs and static/Voice_data_sentiment folders, respectively. You can refer to the files within and add new ones if needed.
If the format is correct, every time you refresh the web page, static/build_audio_sql.py will automatically load newly added files.

## Video Introduction, Tutorial, and Demonstration
[【Brand New Version】 GPT-SoVITS-Novels: Let Genshin Characters Read Novels for You] https://www.bilibili.com/video/BV11iiNegEGP/?share_source=copy_web&vd_source=e8e5bbbe8195c50ca4a9ea44fdd8843c

## References and Learning
 ```code
Listed in no particular order
GPT-SoVITS Original Project
https://github.com/RVC-Boss/GPT-SoVITS

OpenAI API
https://openai.com/index/openai-api/

Tekkon Technology's Rolling Stone [All Genshin Characters GPT-sovits Voice Model Cloning, Yae Miko's Voice is So Soft Ahhhh]
https://www.bilibili.com/video/BV1rA4m157aw/?share_source=copy_web&vd_source=e8e5bbbe8195c50ca4a9ea44fdd8843c

Bilibili Chatbot
https://github.com/linyiLYi/bilibot

GPT-SoVITS Audio Synthesis Online Demo
https://openbayes.com/console/GraceXiii/containers/3AB3h9950IN
 ```
