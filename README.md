# AI Agent 客服系统

基于 LangChain Agent 的智能客服系统，支持多轮对话、工具调用和流式响应。

## 项目简介

这是一个完整的 AI 客服系统项目，包含：
- 🤖 **Python 后端**: FastAPI + LangChain Agent
- 💻 **React 前端**: React 18 + TypeScript + Tailwind CSS

```
┌─────────────────────────────────────────────────────────────┐
│                        前端 (React)                          │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────────────┐  │
│  │ ChatInterface│  │MessageBubble│  │    LoadingDots     │  │
│  └─────────────┘  └─────────────┘  └─────────────────────┘  │
│         │                                    │               │
│         └────────────── useChatStream ──────┘               │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼ SSE 流式请求
┌─────────────────────────────────────────────────────────────┐
│                        后端 (FastAPI)                        │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────────────┐  │
│  │    main.py   │  │   agent.py  │  │      tools.py       │  │
│  │   API入口    │  │  Agent核心  │  │  8个工具(天气/计算等) │  │
│  └─────────────┘  └─────────────┘  └─────────────────────┘  │
│         │                                    │               │
│  ┌──────┴──────┐                    ┌───────┴────────┐       │
│  │   memory.py  │                    │  LangChain LLM │       │
│  │  对话记忆    │                    │   OpenAI API   │       │
│  └─────────────┘                    └────────────────┘       │
└─────────────────────────────────────────────────────────────┘
```

## 功能列表

### 后端功能
- ✅ FastAPI RESTful API
- ✅ LangChain Agent 核心
- ✅ 8个实用工具（天气、计算器、时间、订单查询等）
- ✅ SSE 流式响应
- ✅ 对话历史持久化
- ✅ 多轮对话支持
- ✅ CORS 跨域支持

### 前端功能
- ✅ 现代化聊天界面
- ✅ 实时流式输出
- ✅ 消息气泡动画
- ✅ 加载状态指示
- ✅ 错误提示
- ✅ 快捷问题按钮
- ✅ 响应式布局

## 快速启动

### 环境要求

- Python 3.9+
- Node.js 18+
- OpenAI API Key

### 1. 启动后端

```bash
# 进入后端目录
cd backend

# 创建虚拟环境（推荐）
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# 安装依赖
pip install -r requirements.txt

# 配置环境变量
cp .env.example .env
# 编辑 .env，填入 OPENAI_API_KEY

# 启动服务
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### 2. 启动前端

```bash
# 新开终端，进入前端目录
cd frontend

# 安装依赖
npm install

# 启动开发服务器
npm run dev
```

### 3. 访问应用

- 前端: http://localhost:5173
- 后端 API 文档: http://localhost:8000/docs

## 项目结构

```
ai-customer-service/
├── backend/                    # Python 后端
│   ├── app/
│   │   ├── main.py           # FastAPI 入口
│   │   ├── llm.py            # LLM 配置
│   │   ├── agent.py          # Agent 核心
│   │   ├── tools.py          # 工具定义
│   │   ├── memory.py         # 对话记忆
│   │   └── schemas.py        # 数据模型
│   ├── requirements.txt
│   └── README.md
├── frontend/                  # React 前端
│   ├── src/
│   │   ├── components/
│   │   │   ├── ChatInterface.tsx
│   │   │   ├── MessageBubble.tsx
│   │   │   └── LoadingDots.tsx
│   │   ├── hooks/
│   │   │   └── useChatStream.ts
│   │   ├── api/
│   │   │   └── chat.ts
│   │   ├── App.tsx
│   │   └── main.tsx
│   ├── package.json
│   ├── vite.config.ts
│   ├── tailwind.config.js
│   └── README.md
├── README.md                   # 项目总览
└── LICENSE
```

## 可用工具

| 工具名称 | 功能 | 示例问题 |
|---------|------|---------|
| `get_weather` | 查询天气 | "北京今天天气怎么样" |
| `calculate` | 数学计算 | "帮我算一下 123*456" |
| `get_current_time` | 获取时间 | "现在几点了" |
| `search_knowledge` | 知识库搜索 | "退款政策是什么" |
| `get_order_status` | 订单查询 | "我的订单 ORD2024001 到哪了" |
| `FAQ_answer` | 常见问题 | "如何修改密码" |
| `get_user_info` | 用户信息 | "查一下用户 U001 的信息" |
| `create_ticket` | 创建工单 | "我要投诉" |

## 技术亮点

### 后端
- **LangChain Agent**: 使用 `create_openai_functions_agent` 创建函数调用型 Agent
- **工具调用**: 8个实用工具，涵盖客服常见场景
- **对话记忆**: 基于 `ConversationBufferMemory` 的多轮对话
- **流式响应**: SSE 实现实时打字机效果
- **持久化存储**: 对话历史保存到 JSON 文件

### 前端
- **TypeScript**: 完整的类型定义
- **Tailwind CSS**: 原子化 CSS，快速样式开发
- **SSE 流式**: EventSource 处理流式响应
- **自定义 Hooks**: `useChatStream` 封装聊天逻辑
- **响应式设计**: 适配桌面和移动端

## API 文档

### 聊天接口

```bash
# 流式聊天
GET /api/chat/stream?message=你好&conversation_id=xxx

# 或 POST
POST /api/chat/stream
{
    "message": "你好",
    "conversation_id": "xxx"
}
```

### 对话历史

```bash
# 获取历史
GET /api/history/{conversation_id}

# 清除历史
DELETE /api/history/{conversation_id}
```

## 开发指南

### 添加新工具

1. 在 `backend/app/tools.py` 中定义工具函数
2. 使用 `@tool` 装饰器
3. 在 `get_all_tools()` 中注册

```python
@tool
def my_new_tool(param: str) -> str:
    """工具描述"""
    return f"结果: {param}"
```

### 添加新页面

1. 在 `frontend/src/components/` 创建组件
2. 在 `App.tsx` 中引入使用

## 注意事项

1. ⚠️ 请妥善保管 OpenAI API Key，不要提交到代码仓库
2. ⚠️ 生产环境请配置正确的 CORS 策略
3. 💡 对话历史存储在 `backend/conversation_history/` 目录

## License

MIT License
