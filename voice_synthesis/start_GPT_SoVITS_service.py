#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Jul  7 14:03:51 2024

@author: lrxwisdom001
"""
#%%
import time
import os
import psutil
import subprocess
def find_process_using_port(port):
    """找到使用指定端口的进程"""
    for proc in psutil.process_iter(['pid', 'name']):
        try:
            connections = proc.connections(kind='inet')
            for conn in connections:
                if conn.laddr.port == port:
                    return proc
        except (psutil.AccessDenied, psutil.NoSuchProcess):
            continue
    return None

def release_port(port):
    """释放指定端口"""
    process = find_process_using_port(port)
    if process:
        print(f"终止占用端口 {port} 的进程: PID {process.pid}, 名称 {process.info['name']}")
        process.terminate()  # 终止进程
        process.wait(timeout=5)  # 等待进程终止
        print(f"端口 {port} 已释放。")
    # else:
    #     print(f"未找到占用端口 {port} 的进程。")

def service_opened(process,port): #old way using PIPE, 不能让其他script读取状态
    while subprocess.Popen.poll(process) is None:
        stream = process.stdout.readline()
        print(stream)

        if f"Uvicorn running on http://127.0.0.1:{port}" in stream:
            print(f"启动GPT-SoVITS服务，端口 {port},开启成功!") 
            break   
            return True
            
        else:
            return False
        time.sleep(1) #减少频繁轮询进程状态

def service_opened2(process,port): #old way using PIPE, 不能让其他script读取状态
    print('-------------',os.getcwd())
    while True:
        time.sleep(1) #减少频繁轮询进程状态
        with open(f'server_status_{port}.txt', 'r') as f:
            lines = f.readlines()
            print('------------------',lines)
            # print(lines[-1])
            if f"Uvicorn running on http://127.0.0.1:{port}" in lines[-1]:
                break
                
        

def start_GPT_SoVITS_service(s,g,dr,dt,port,GPT_SoVITS_dir = '../GPT-SoVITS/',dl='zh',
                    a = '127.0.0.1'):
    
    cwd = os.getcwd()
    release_port(port)
    # 遍历每条命令并构建命令行参数字符串
    
    
    # GPT-SoVITS api必须在这个文件夹下启动，不然报错
    cmd = [
        "python","api.py",
        "-s", s,
        "-g", g,
        "-dr", dr,
        "-dt", dt,
        "-dl", dl,
        "-a", a,
        "-p", str(port)
    ]
    # cmd = [
    #     "python","api.py",
    #     "-s", voice_data_dir+s,
    #     "-g", voice_data_dir+g,
    #     "-dr", voice_data_dir+dr,
    #     "-dt", dt,
    #     "-dl", dl,
    #     "-a", a,
    #     "-p", str(port)
    # ]
    # print(cmd)
    # 构建 bash 命令字符串
    bash_command = " ".join(["python", "api.py", "-s", s, "-g", g, "-dr", dr, "-dt", dt, "-dl", dl, "-a", a, "-p", str(port)])

    # 打印 bash 命令
    print(bash_command)
    # 启动子进程 并显示状态
    os.chdir(GPT_SoVITS_dir)
    #注意监测文档的相对位置
    # open(f'../server_status_{port}.txt', 'w')
    # with open(f'../server_status_{port}.txt', 'r') as f:
    # 启动服务器并将输出重定向到文件
        
    process = subprocess.Popen(
    cmd,
    stdin=subprocess.PIPE,
    stdout=subprocess.PIPE,
    stderr=subprocess.STDOUT,
    universal_newlines=True,
    encoding='utf8',
    bufsize=1
    )
    os.chdir(cwd)
    print('等待服务开启。。。')

    #为了并行，每句话，必须开一个subprocess开启对应角色语气的服务，一个subprocess合成
    #同一个script 开一个subprocess 写入文件，另外一个函数读，读不出来，必须是另外一个script来读
    #但是那样每个subprocess必须再开一个subprocess监测，太麻烦了，
    #不如后面用一个开一个subprocess监测已经完成合成的句子数

    # log = open(f'../server_status_{port}', 'w')  
    # log = open(f'../server_status_{port}', 'a')   

    while subprocess.Popen.poll(process) is None:
        stream = process.stdout.readline()
        # print(stream)
        # log.write(stream)
        if f"Uvicorn running on http://127.0.0.1:{port}" in stream:
            print(f"启动GPT-SoVITS服务，端口 {port},开启成功!") 
            break   
        
            
        # else:
        #     print(f"端口{port} GPT-SoVITS服务尚未开启")
        time.sleep(3) #减少频繁轮询进程状态
    # log.close()

    return process,port

def main():
    voice_data_dir = '/Users/lei/L2Pproject/Voice_data/'
    port = 9880
    s= 'aierhaisen_e8_s136.pth'
    g= 'aierhaisen-e15.ckpt'
    dr='aierhaisen_希望室友不要半夜敲敲打打做模型…或者他不在家最好。我不想晚上睡觉还得戴着耳机。.mp3'
    dt='希望室友不要半夜敲敲打打做模型…或者他不在家最好。我不想晚上睡觉还得戴着耳机。'
    GPT_SoVITS_dir = '../GPT-SoVITS/'
    print(f"启动GPT-SoVITS服务，端口 {port}。")
    process,port = start_GPT_SoVITS_service(voice_data_dir+s,
                                            voice_data_dir+g,voice_data_dir+dr,
                                            dt,port,GPT_SoVITS_dir)
    

if __name__ == "__main__":
    main()  

# %%
