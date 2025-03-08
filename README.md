# 游戏平台后端系统

## 项目概述
这是一个基于Flask的游戏平台后端系统，提供用户认证、物品管理、任务管理和交易管理等功能。

## 环境要求
- Python 3.8+
- PostgreSQL 12+
- Redis 6+（用于JWT令牌黑名单）

## 安装步骤

1. 克隆项目：
```bash
git clone https://github.com/your-repo/game-platform.git
cd game-platform
```

2. 创建虚拟环境：
```bash
python -m venv venv
source venv/bin/activate  # Linux/macOS
venv\Scripts\activate  # Windows
```

3. 安装依赖：
```bash
pip install -r requirements.txt
```

## 配置文件
复制示例配置文件并修改：
```bash
cp game_platform/config.example.py game_platform/config.py
```

主要配置项：
- `SQLALCHEMY_DATABASE_URI`: 数据库连接字符串
- `JWT_SECRET_KEY`: JWT加密密钥
- `JWT_ACCESS_TOKEN_EXPIRES`: 访问令牌有效期
- `JWT_REFRESH_TOKEN_EXPIRES`: 刷新令牌有效期

## 数据库初始化
1. 创建数据库：
```bash
createdb game_platform
```

2. 初始化数据库：
```bash
flask db upgrade
```

## API文档
启动服务后访问：
```
http://localhost:5000/api/docs
```

## 运行项目
```bash
flask run
```

## 依赖库
主要依赖库：
- Flask
- Flask-SQLAlchemy
- Flask-Migrate
- Flask-JWT-Extended
- psycopg2-binary
- redis
- python-dotenv

完整依赖见requirements.txt
