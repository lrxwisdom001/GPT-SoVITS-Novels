from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
import subprocess
import os,time
from threading import Thread

def index(request):
    return render(request, 'voice_synthesis/index.html')
# 存储任务状态的全局字典
task_results = {}

@csrf_exempt
def novel_to_GPT(request):
    if request.method == 'POST':
      
        data = json.loads(request.body)
        api_key = data.get('api_key')
        novel_origin = data.get('novel_origin')
        task_id = str(time.time())  # Generate a unique task ID using a timestamp

        task_results[task_id] = {'status': 'running', 'output': []}
        
        # 使用线程启动任务
        thread = Thread(target=novel_to_script, args=(task_id, api_key, novel_origin))
        thread.start()

        return JsonResponse({'task_id': task_id})

    return JsonResponse({'error': 'Invalid request'}, status=400)

def novel_to_script(task_id, api_key, novel_origin):
    try:
        script_directory = os.path.join(os.path.dirname(__file__))
        process = subprocess.Popen(
            ['python3', '-u', 'novel_to_GPT.py', api_key, novel_origin], 
            cwd=script_directory,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            bufsize=1
        )

        # 初始化输出列表
        task_results[task_id] = {'status': 'running', 'output': []}

        # 逐行读取标准输出和标准错误
        for line in process.stdout:
            task_results[task_id]['output'].append(line)
        for line in process.stderr:
            task_results[task_id]['output'].append(line)
        
        process.wait()  # 等待进程结束

        if process.returncode == 0:
            task_results[task_id]['status'] = 'success'
        else:
            task_results[task_id]['status'] = 'error'
    except Exception as e:
        task_results[task_id] = {
            'status': 'error',
            'output': [str(e)]
        }


@csrf_exempt
def initialize_audio_library(request):
    try:
        script_directory = os.path.join(os.path.dirname(__file__), '../static')
        result = subprocess.run(
            ['python3', 'build_audio_sql.py'],
            cwd=script_directory,
            check=True
        )
        return JsonResponse({'status': 'success'})
    except subprocess.CalledProcessError as e:
        return JsonResponse({'status': 'error', 'message': str(e)})
    except Exception as e:
        return JsonResponse({'status': 'error', 'message': str(e)})


def process_input(request):
    if request.method == 'POST':
        user_input = request.POST.get('user_input')
        response_data = {'result': f'Processed: {user_input}'}
        return JsonResponse(response_data)
    return JsonResponse({'error': 'Invalid request'}, status=400)

@csrf_exempt
def process_script(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        novel_script = data.get('document_content', '')
        # print(novel_script)
        
        # 调用外部Python脚本处理数据
        match_novel_script_to_sound_sources(novel_script)

        return JsonResponse({}) #JsonResponse 必须是一个json dict 

def match_novel_script_to_sound_sources(script):
    try:
        script_directory = os.path.join(os.path.dirname(__file__))
        result = subprocess.run(
            ['python3', 'match_novel_script_to_sound_sources.py', script],
            cwd=script_directory,
            check=True
        )
    except subprocess.CalledProcessError as e:
        print(f"Error occurred: {e}")



@csrf_exempt
def generate_audiobook(request):
    if request.method == 'POST':
        json_get = json.loads(request.body)
        task_id = str(time.time())  # 使用时间戳作为唯一任务ID

        task_results[task_id] = {'status': 'running', 'output': []}
        
        # 使用线程启动任务
        thread = Thread(target=create_audiobook, args=(task_id, json_get))
        thread.start()

        return JsonResponse({'task_id': task_id})

    return JsonResponse({'error': 'Invalid request'}, status=400)

def create_audiobook(task_id, json_get):
    try:
        script_directory = os.path.join(os.path.dirname(__file__))
        process = subprocess.Popen(
            ['python3', '-u', 'generate_audiobook.py', json.dumps(json_get)], 
            cwd=script_directory,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            bufsize=1
        )

        # 初始化输出列表
        task_results[task_id] = {'status': 'running', 'output': []}

        # 逐行读取标准输出和标准错误
        for line in process.stdout:
            task_results[task_id]['output'].append(line)
        for line in process.stderr:
            task_results[task_id]['output'].append(line)
        
        process.wait()  # 等待进程结束

        if process.returncode == 0:
            task_results[task_id]['status'] = 'success'
        else:
            task_results[task_id]['status'] = 'error'
    except Exception as e:
        task_results[task_id] = {
            'status': 'error',
            'output': [str(e)]
        }
        

def check_task_status(request, task_id):
    result = task_results.get(task_id, {'status': 'unknown'})
    return JsonResponse(result, status=200)