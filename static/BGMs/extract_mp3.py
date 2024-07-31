#%%
# 从mp4文件中，使用 ffmpeg 提取音频并保存为 mp3
import ffmpeg
import os

def extract_audio(input_file, output_file):
    try:
        # 使用 ffmpeg 提取音频
        (
            ffmpeg
            .input(input_file)
            .output(output_file, format='mp3')
            .run(overwrite_output=True)
        )
        print(f"Audio extracted successfully to {output_file}")
    except ffmpeg.Error as e:
        print(f"An error occurred: {e}")

def process_folder(input_folder, output_folder):
    # 确保输出文件夹存在
    os.makedirs(output_folder, exist_ok=True)

    # 遍历输入文件夹中的所有文件
    for root, _, files in os.walk(input_folder):
        for file in files:
            if file.endswith('.mp4'):
                input_file = os.path.join(root, file)
                output_file = os.path.join(output_folder, os.path.splitext(file)[0] + '.mp3')
                extract_audio(input_file, output_file)

# 示例用法
input_folder = './'
output_folder = './'
process_folder(input_folder, output_folder)

# %%
