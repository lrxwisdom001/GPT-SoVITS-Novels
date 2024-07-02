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

## 项目Repository里面有什么？
包括代码，1个小说《不让江山》的片段，及合成的后的声音样本。

合成样本需要用到，5个原神角色声音（派蒙，久岐忍，五郎，班尼特，艾尔海森）的样本及对应的GPT-SoVITS配置文件。
由于Github容量限制，传到Baidu网盘和Hugging Face,链接见快速上手教程 [1. 这是一个目录跳转示例](#1)



更多声音样本和配置文件请转到：
特看科技的滚石 
【原神全角色GPT-sovits音色模型克隆，八重神子的声音太酥了啊啊啊啊】 
https://www.bilibili.com/video/BV1rA4m157aw/?share_source=copy_web&vd_source=e8e5bbbe8195c50ca4a9ea44fdd8843c
目前只找到中文的，其他语言还请自行寻找，或用GPT-SoVITS自行训练：

## 快速上手
创建python 环境
 ```bash
conda env creat -n Novels python=3.10
conda activate Novels
pip install git-lfs
  ```
git-lfs 用brew,apt-get等工具安装也可，但必须安装，否则后面GPT-SoVITS会报错。

 ```bash
git clone https://github.com/lrxwisdom001/GPT-SoVITS-Novels.git
cd GPT-SoVITS-Novels
mkdir pretrained_models && cd pretrained_models && git lfs clone https://huggingface.co/lj1995/GPT-SoVITS
  ```
下载Baidu网盘或者Google Drive里面的样本声音和配置文件，解压之后放入Voice_data文件夹（若使用自己的声音样本，此步可跳过。但需要修改 voice_server_config.json）

<p id="1">"Voice_data.zip"下载地址</p> 
Baidu网盘：链接: https://pan.baidu.com/s/1EmfepzvqtYnWbxtEpxcylQ?pwd=ry63 提取码: ry63 

Hugging Face：https://huggingface.co/datasets/lrxwisdom001/GPT-SoVITS-Novels/blob/main/Voice_data.zip

下载GPT-SoVITS
 ```bash
git clone https://github.com/lrxwisdom001/GPT-SoVITS-Novels.git
cd GPT-SoVITS-Novels
  ```

需要输入自己的openai api_key
运行
 ```bash
python main.py
  ```
程序会先将小说文本转换成带角色标注的md文档，然后利用GPT-SoVITS-Novels合成音频，合成音频前有一部开启合成服务，耗时较长（30s-1min视电脑速度而定），中间会有几步确认操作，需输入“Y“或”N“回车后方可继续。

## 视频简介、教学、及效果展示
待制作

## 后续工作
- [ ]加入更多语言和角色的samples
- [ ]加入情绪分析
- [ ]基于情绪分析自动插入音乐

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
