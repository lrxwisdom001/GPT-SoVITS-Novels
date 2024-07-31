#%%
import sqlite3
import os

BGM_root_dir = 'BGMs/'
voice_root_dir = 'Voice_data_sentiment/'
# 连接到SQLite数据库（如果数据库不存在，会自动创建）

db_name = 'BGM_files.db'
# if os.path.exists(db_name):
#     if input(f"Database '{db_name}' already exists. Overwrite? (y/n) ") == 'y':
#         os.remove(db_name)
db = sqlite3.connect(db_name)

# 创建一个表来存储MP3文件的信息
create_table_query = """
CREATE TABLE IF NOT EXISTS BGM_files (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    sentiment INTEGER,
    music_name TEXT,
    file_path TEXT
);
"""
db.execute(create_table_query)
#%%
# 获取文件夹中的所有MP3和WAV文件
files = [file for file in os.listdir(BGM_root_dir) if file.endswith(('.mp3', '.wav'))]

# 遍历每个文件并插入数据库
for file in files:
    # 假设文件名格式为：数字_音乐名字.mp3 或 数字_音乐名字.wav
    parts = file.split('_', 1)
    if len(parts) == 2:
        sentiment = int(parts[0])    
        music_name = parts[1].rsplit('.', 1)[0]  # 去掉文件扩展名
        file_path = BGM_root_dir+file
        # 插入数据到数据库
        insert_query = "INSERT INTO BGM_files (sentiment ,music_name, file_path) VALUES (?, ?, ?)"
        db.execute(insert_query, (sentiment, music_name, file_path))

# 提交更改
db.commit()

# 查询所有MP3和WAV文件信息
query = "SELECT * FROM BGM_files"
results = db.execute(query).fetchall()

# 打印结果
# for row in results:
#     print(row)

# 关闭数据库连接
db.close()
# %%


# 搜索文件夹，去除隐藏文件夹
sub_dirs = [item for item in os.listdir(voice_root_dir) if os.path.isdir(os.path.join(voice_root_dir, item)) and not item.startswith('.')]
# print(sub_dirs)
# %%
db_name = 'voice_files.db'
# if os.path.exists(db_name):
#     if input(f"Database '{db_name}' already exists. Overwrite? (y/n) ") == 'y':
#         os.remove(db_name)
db = sqlite3.connect(db_name)

# 创建一个表来存储MP3文件的信息
create_table_query = """
CREATE TABLE IF NOT EXISTS voice_files (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    character TEXT,
    sentiment TEXT,
    text TEXT,
    file_path TEXT
);
"""
db.execute(create_table_query)

for sub_dir in sub_dirs:
    files = [file for file in os.listdir(voice_root_dir+sub_dir) if file.endswith(('.mp3', '.wav'))]
    for file in files:
        parts = file.split('_', 2) #文件名被两个'_'分段
        if len(parts) == 3:
            character = parts[0]
            sentiment = int(parts[1])
            text = parts[2].rsplit('.', 1)[0]  # 去掉文件扩展名
            file_path = voice_root_dir+sub_dir+'/'+file
            # 插入数据到数据库
            insert_query = "INSERT INTO voice_files (character, sentiment, text, file_path) VALUES (?, ?, ?, ?)"
            db.execute(insert_query, (character, sentiment, text, file_path))

# 提交更改
db.commit()
# 查询所有MP3和WAV文件信息
query = "SELECT * FROM voice_files"
results = db.execute(query).fetchall()

# 打印结果
# for row in results:
#     print(row)
# %%
# 创建一个表来存储MP3文件的信息
create_table_query = """
CREATE TABLE IF NOT EXISTS config_files (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    character TEXT,
    sovitsweight TEXT,
    gptweight TEXT
);
"""
db.execute(create_table_query)

for sub_dir in sub_dirs:
    sovits_file = [file for file in os.listdir(voice_root_dir+sub_dir) if file.endswith(('.pth'))]
    gpt_file = [file for file in os.listdir(voice_root_dir+sub_dir) if file.endswith(('.ckpt'))]
    if (len(sovits_file)>0) & (len(gpt_file)>0):
        character = sub_dir
        insert_query = "INSERT INTO config_files (character, sovitsweight, gptweight) VALUES (?, ?, ?)"
        db.execute(insert_query, (character, voice_root_dir+sub_dir+'/'+sovits_file[0], voice_root_dir+sub_dir+'/'+gpt_file[0]))
        
# 提交更改
db.commit()
# 查询所有MP3和WAV文件信息
query = "SELECT * FROM config_files"
results = db.execute(query).fetchall()
# 打印结果
# for row in results:
#     print(row)
# %%
db.close()