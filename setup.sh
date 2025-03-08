#!/bin/bash

# 安装Python
sudo apt-get update
sudo apt-get install -y python3.10 python3.10-venv python3.10-dev

# 安装PostgreSQL
sudo apt-get install -y postgresql postgresql-contrib

# 安装Redis
sudo apt-get install -y redis-server

# 创建数据库用户
sudo -u postgres psql -c "CREATE USER game_user WITH PASSWORD 'game_password';"
sudo -u postgres psql -c "CREATE DATABASE game_platform OWNER game_user;"

# 创建虚拟环境
python3.10 -m venv venv
source venv/bin/activate

# 安装项目依赖
pip install --upgrade pip
pip install --ignore-installed -r requirements.txt

echo "安装完成！请执行以下命令启动项目："
echo "source venv/bin/activate"
echo "flask run"
