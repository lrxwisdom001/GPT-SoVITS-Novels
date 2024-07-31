# 第一阶段: 构建依赖
FROM python:3.10-slim as builder

WORKDIR /app

COPY . /app

# 安装构建所需的依赖
RUN apt-get update && apt-get install -y \
    build-essential \
    cmake \
    qt5-qmake \
    qtbase5-dev \
    && rm -rf /var/lib/apt/lists/*

# 升级 pip
RUN pip install --upgrade pip

# 分批安装 Python 依赖
COPY requirements_part1.txt .
RUN pip install --no-cache-dir -r requirements_part1.txt
COPY requirements_part2.txt .
RUN pip install --no-cache-dir -r requirements_part2.txt
# 添加其他部分依赖...

# 第二阶段: 运行
FROM python:3.10-slim

WORKDIR /app

COPY --from=builder /app /app
COPY --from=builder /usr/local/lib/python3.10/site-packages /usr/local/lib/python3.10/site-packages

EXPOSE 8000
CMD ["sh", "-c", "python manage.py runserver 0.0.0.0:8000 & python open_browser.py"]
