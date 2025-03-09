# API 对接文档

## 1. 基础信息

- API版本：v1.0
- 认证方式：Bearer Token
- 请求格式：JSON
- 响应格式：JSON

## 2. 接口调用规范

### 2.1 请求头
```json
{
  "Content-Type": "application/json",
  "Authorization": "Bearer {access_token}"
}
```

### 2.2 响应格式
```json
{
  "code": 200,
  "message": "success",
  "data": {}
}
```

### 2.3 分页参数
- page: 当前页码
- per_page: 每页数量

## 3. 错误码说明

| 错误码 | 说明 |
|--------|------|
| 200    | 请求成功 |
| 400    | 请求参数错误 |
| 401    | 未授权 |
| 403    | 禁止访问 |
| 404    | 资源不存在 |
| 500    | 服务器内部错误 |

## 4. API接口说明

### 4.1 认证相关接口

#### 用户注册
```bash
POST /api/auth/register
{
  "username": "test",
  "email": "test@example.com",
  "password": "test123"
}
```

#### 用户登录
```bash
POST /api/auth/login
{
  "username": "test",
  "password": "test123"
}
```

#### 刷新令牌
```bash
POST /api/auth/refresh
{
  "refresh_token": "your_refresh_token"
}
```

### 4.2 物品管理接口

#### 创建物品
```bash
POST /api/items
{
  "name": "Test Item",
  "description": "Test Description",
  "price": 10.0,
  "stock": 5
}
```

#### 获取物品列表
```bash
GET /api/items?page=1&per_page=10
```

#### 获取物品详情
```bash
GET /api/items/{item_id}
```

#### 更新物品
```bash
PUT /api/items/{item_id}
{
  "name": "Updated Item",
  "description": "Updated Description",
  "price": 15.0,
  "stock": 10
}
```

#### 删除物品
```bash
DELETE /api/items/{item_id}
```

### 4.3 任务管理接口

#### 创建任务
```bash
POST /api/tasks
{
  "item_id": 1,
  "type": "task",
  "price": 5.0,
  "quantity": 1
}
```

#### 获取任务列表
```bash
GET /api/tasks?status=active&page=1&per_page=10
```

#### 接受任务
```bash
POST /api/tasks/{task_id}/accept
```

#### 完成任务
```bash
POST /api/tasks/{task_id}/complete
```

### 4.4 交易相关接口

#### 创建交易

```bash
POST /api/transactions
{
  "task_id": 1,
  "amount": 5.0,
  "type": "purchase"
}
```

#### 获取交易记录

```bash
GET /api/transactions?user_id=1&page=1&per_page=10
```

## 5. 安全规范

- 所有API请求必须使用HTTPS
- 敏感数据必须加密传输
- 访问令牌有效期：24小时
- 建议使用OAuth2.0进行授权
- 请求频率限制：100次/分钟
