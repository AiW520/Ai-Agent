# AI Agent 客服系统 - 前端

基于 React 18 + TypeScript + Tailwind CSS 的智能客服前端应用。

## 功能特性

- 💬 **实时对话**: 支持流式响应，实时展示AI回复
- 🎨 **优雅界面**: 现代UI设计，响应式布局
- ⌨️ **快捷输入**: 支持Enter发送，Shift+Enter换行
- 🔄 **状态管理**: 完整的加载状态、错误处理
- 📱 **移动适配**: 良好的移动端体验

## 快速开始

### 1. 安装依赖

```bash
cd frontend
npm install
```

### 2. 配置环境变量

创建 `.env.local` 文件：

```env
VITE_API_URL=http://localhost:8000
```

### 3. 启动开发服务器

```bash
npm run dev
```

访问 http://localhost:5173

### 4. 构建生产版本

```bash
npm run build
```

## 项目结构

```
frontend/
├── src/
│   ├── components/        # React 组件
│   │   ├── ChatInterface.tsx   # 聊天主界面
│   │   ├── MessageBubble.tsx   # 消息气泡
│   │   └── LoadingDots.tsx     # 加载动画
│   ├── hooks/             # 自定义 Hooks
│   │   └── useChatStream.ts   # 流式聊天逻辑
│   ├── api/               # API 请求
│   │   └── chat.ts        # 聊天接口封装
│   ├── App.tsx            # 根组件
│   ├── main.tsx           # 入口文件
│   └── index.css           # 全局样式
├── package.json
├── vite.config.ts
├── tailwind.config.js
└── README.md
```

## 技术栈

- **框架**: React 18.2.0
- **语言**: TypeScript 5.3.3
- **构建**: Vite 5.0.12
- **样式**: Tailwind CSS 3.4.1
- **状态管理**: React Hooks

## 组件说明

### ChatInterface

聊天主界面组件，包含消息列表和输入框。

```tsx
import { ChatInterface } from './components/ChatInterface'

<ChatInterface
  messages={messages}
  streamingContent={streamingContent}
  isLoading={isLoading}
  error={error}
  onSendMessage={sendMessage}
  onCancel={cancel}
  onClearMessages={clearMessages}
/>
```

### useChatStream

处理流式聊天的自定义 Hook。

```tsx
import { useChatStream } from './hooks/useChatStream'

const {
  messages,
  streamingContent,
  isLoading,
  error,
  sendMessage,
  cancel,
  clearMessages,
} = useChatStream()
```

## API 接口

前端通过以下端点与后端通信：

| 端点 | 方法 | 描述 |
|------|------|------|
| `/api/chat/stream` | GET | 流式聊天 (SSE) |
| `/api/chat/stream` | POST | 流式聊天 (SSE) |
| `/api/history/{id}` | GET | 获取对话历史 |
| `/api/history/{id}` | DELETE | 清除对话历史 |
| `/health` | GET | 健康检查 |

## 开发指南

### 添加新组件

1. 在 `src/components/` 目录创建组件文件
2. 导出组件
3. 在需要的地方引入使用

### 添加新接口

1. 在 `src/api/` 目录添加接口文件
2. 封装请求方法
3. 在组件中引入使用

### 修改样式

使用 Tailwind CSS 类名进行样式调整，无需编写额外 CSS。

## 常见问题

### 1. 无法连接到后端

确保：
- 后端服务已启动 (http://localhost:8000)
- `.env.local` 中的 `VITE_API_URL` 配置正确
- 浏览器允许跨域请求

### 2. 流式响应不工作

检查：
- 浏览器是否支持 EventSource
- 网络连接是否正常
- 后端 SSE 配置是否正确

## License

MIT License
