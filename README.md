**Read this in other languages: [English](README.md), [中文](README_zh.md).**

# GPT-SoVITS-Novels
Let Genshin characters read novels for you!

## Important Notice: The sample audio sources and texts provided by this project are for learning and reference only. Please do not use them for commercial purposes.
<img src="https://github.com/lrxwisdom001/GPT-SoVITS-Novels/assets/106758196/69cb3a68-9f6e-4211-bc9b-9222efdac845" height="100">
<img src="https://github.com/lrxwisdom001/GPT-SoVITS-Novels/assets/106758196/69cb3a68-9f6e-4211-bc9b-9222efdac845" height="125">
<img src="https://github.com/lrxwisdom001/GPT-SoVITS-Novels/assets/106758196/69cb3a68-9f6e-4211-bc9b-9222efdac845" height="150">

<img src="https://github.com/lrxwisdom001/GPT-SoVITS-Novels/assets/106758196/69cb3a68-9f6e-4211-bc9b-9222efdac845" height="150">
<img src="https://github.com/lrxwisdom001/GPT-SoVITS-Novels/assets/106758196/69cb3a68-9f6e-4211-bc9b-9222efdac845" height="125">
<img src="https://github.com/lrxwisdom001/GPT-SoVITS-Novels/assets/106758196/69cb3a68-9f6e-4211-bc9b-9222efdac845" height="100">

## What is GPT-SoVITS-Novels?
This project uses ChatGPT's OpenAI API and GPT-SoVITS to quickly convert any novel text into a multi-character audio book.

## What’s in the Project Repository?
The repository includes the code, a segment from the novel "Bù Ràng Jiāngshān," and the synthesized audio samples.

The synthesis samples require the voice samples of five Genshin Impact characters (Paimon, Kujou Sara, Gorou, Bennett, Alhaitham) and the corresponding GPT-SoVITS configuration files. Due to GitHub's capacity limitations, they are uploaded to Baidu Netdisk and Hugging Face. Links are provided in the Quick Start guide ["Voice_data.zip" download link](#1).

For more voice samples and configuration files, please refer to:
TeKanTech's Rolling Stone
[Genshin Impact full character GPT-SoVITS voice model clone, Yae Miko's voice is too cute!](https://www.bilibili.com/video/BV1rA4m157aw/?share_source=copy_web&vd_source=e8e5bbbe8195c50ca4a9ea44fdd8843c)
Currently, only Chinese versions are available. For other languages, please find or train them using GPT-SoVITS:

## Quick Start
Create a Python environment:
```bash
conda create --name Novels python=3.10 ffmpeg
conda activate Novels
pip install git-lfs
```
Git-lfs must be installed. You can use tools like brew, apt-get, etc., otherwise, GPT-SoVITS will report errors.

Download project files, install dependencies, and create Voice_data and Output_temp folders.
```bash
git clone https://github.com/lrxwisdom001/GPT-SoVITS-Novels.git
cd GPT-SoVITS-Novels
mkdir Output_temp
mkdir Voice_data
pip install -r requirements.txt
```
Download the sample voices and configuration files from Baidu Netdisk or Google Drive, and extract the files into the Voice_data folder (skip this step if using your own voice samples, but you need to modify the voice_server_config.json).

<p id="1">"Voice_data.zip" download link</p> 

```bash
Baidu Netdisk: https://pan.baidu.com/s/1EmfepzvqtYnWbxtEpxcylQ?pwd=ry63 (Password: ry63)

Hugging Face: https://huggingface.co/datasets/lrxwisdom001/GPT-SoVITS-Novels/blob/main/Voice_data.zip
```

Download GPT-SoVITS
```bash
git clone https://github.com/RVC-Boss/GPT-SoVITS.git
cd GPT-SoVITS/GPT_SoVITS/pretrained_models && git lfs clone https://huggingface.co/lj1995/GPT-SoVITS
mv GPT-SoVITS/* .
rm -rf GPT-SoVITS
cd ../../..
```

Enter your OpenAI API key in gpt_script.py or set it in the system environment.

Copy the novel text to novel_original.txt.

Run the script:
```bash
python main.py
```
The program will first convert the novel text into a markdown document with character annotations, then use GPT-SoVITS-Novels to synthesize the audio. There is a step to start the synthesis service, which takes some time (30 seconds to 1 minute depending on the computer's speed). There are several confirmation steps in between, and the GPT-converted text (novel_modified4tts.md) may have some issues, so check it before continuing. Adjust the character-to-voice mapping (characters2voice.json) as per your preference. Press "Y" or "N" and enter to continue.

The final output will be combined.mp3.

## Video Introduction, Tutorials, and Demonstrations
bilibili: [GPT-SoVITS-Novels Let Genshin characters read novels for you](https://www.bilibili.com/video/BV1Q3heeHE2k/?share_source=copy_web&vd_source=e8e5bbbe8195c50ca4a9ea44fdd8843c)
YouTube: [Eng sub+ CN sub] [GPT-SoVITS-Novels] Let Genshin characters read novels for you!](https://youtu.be/yryOkQoHb5M?si=dGyerWanyJHLPoDD)

## Future Work
- [ ] Add more language and character samples
- [ ] Add emotion analysis
- [ ] Automatically insert music based on emotion analysis

## References and Learning
```code
No particular order
GPT-SoVITS original project
https://github.com/RVC-Boss/GPT-SoVITS

OpenAI API
https://openai.com/index/openai-api/

TeKanTech's Rolling Stone [Genshin Impact full character GPT-SoVITS voice model clone, Yae Miko's voice is too cute!](https://www.bilibili.com/video/BV1rA4m157aw/?share_source=copy_web&vd_source=e8e5bbbe8195c50ca4a9ea44fdd8843c)

Bilibili chatbot
https://github.com/linyiLYi/bilibot

GPT-SoVITS audio synthesis online demo
https://openbayes.com/console/GraceXiii/containers/3AB3h9950IN
```
