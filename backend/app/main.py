"""
FastAPI 主入口文件
AI Agent 客服系统后端服务
"""

import asyncio
import uuid
from typing import AsyncGenerator, Optional
from datetime import datetime
from contextlib import asynccontextmanager

from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse, StreamingResponse
from sse_starlette.sse import EventSourceResponse

from .agent import get_or_create_agent, CustomerServiceAgent
from .schemas import (
    ChatRequest, ChatResponse, HealthResponse, 
    ErrorResponse, Message
)
from .memory import get_memory_manager


# 全局Agent存储
_active_agents: dict[str, CustomerServiceAgent] = {}


@asynccontextmanager
async def lifespan(app: FastAPI):
    """应用生命周期管理"""
    print("🚀 AI Agent 客服系统启动中...")
    yield
    print("👋 AI Agent 客服系统已关闭")


# 创建FastAPI应用
app = FastAPI(
    title="AI Agent 客服系统",
    description="基于LangChain的智能客服系统，支持多轮对话和多种工具调用",
    version="1.0.0",
    lifespan=lifespan,
    docs_url="/docs",
    redoc_url="/redoc"
)

# 配置CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://localhost:3000",
        "http://127.0.0.1:5173",
        "http://127.0.0.1:3000",
        "*"  # 生产环境应限制具体域名
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/health", response_model=HealthResponse, tags=["健康检查"])
async def health_check():
    """
    健康检查端点
    
    返回服务状态和版本信息
    """
    return HealthResponse(
        status="healthy",
        version="1.0.0",
        timestamp=datetime.now()
    )


@app.post("/api/chat", response_model=ChatResponse, tags=["聊天"])
async def chat(request: ChatRequest):
    """
    聊天接口（非流式）
    
    接收用户消息，返回AI响应
    """
    try:
        # 获取或创建Agent
        conversation_id = request.conversation_id or str(uuid.uuid4())
        agent = get_or_create_agent(conversation_id)
        
        # 调用Agent
        result = agent.invoke(request.message)
        
        if result.get("success"):
            return ChatResponse(
                message=result["message"],
                conversation_id=result["conversation_id"],
                timestamp=datetime.now()
            )
        else:
            raise HTTPException(status_code=500, detail=result.get("error", "处理失败"))
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/chat/stream", tags=["聊天"])
async def chat_stream(
    message: str,
    conversation_id: Optional[str] = None
):
    """
    流式聊天接口 (SSE)
    
    使用Server-Sent Events实现流式响应
    """
    if not message or not message.strip():
        raise HTTPException(status_code=400, detail="消息不能为空")
    
    conversation_id = conversation_id or str(uuid.uuid4())
    
    async def event_generator():
        """SSE事件生成器"""
        try:
            # 获取或创建Agent
            agent = get_or_create_agent(conversation_id)
            
            # 先发送conversation_id
            yield {
                "event": "conversation",
                "data": conversation_id
            }
            
            # 流式处理
            full_response = ""
            tool_used = []
            
            # 使用流式调用
            for chunk in agent.stream(message):
                if chunk:
                    full_response += chunk
                    yield {
                        "event": "message",
                        "data": chunk
                    }
                    # 小延迟以避免过快的流式输出
                    await asyncio.sleep(0.01)
            
            # 发送完成信号
            yield {
                "event": "done",
                "data": "stream_complete"
            }
        
        except Exception as e:
            yield {
                "event": "error",
                "data": str(e)
            }
    
    return EventSourceResponse(event_generator())


@app.post("/api/chat/stream", tags=["聊天"])
async def chat_stream_post(request: ChatRequest):
    """
    POST方式的流式聊天接口 (SSE)
    
    使用POST方法接收消息
    """
    if not request.message or not request.message.strip():
        raise HTTPException(status_code=400, detail="消息不能为空")
    
    conversation_id = request.conversation_id or str(uuid.uuid4())
    
    async def event_generator():
        """SSE事件生成器"""
        try:
            # 获取或创建Agent
            agent = get_or_create_agent(conversation_id)
            
            # 先发送conversation_id
            yield {
                "event": "conversation",
                "data": conversation_id
            }
            
            # 流式处理
            full_response = ""
            
            for chunk in agent.stream(request.message):
                if chunk:
                    full_response += chunk
                    yield {
                        "event": "message",
                        "data": chunk
                    }
                    await asyncio.sleep(0.01)
            
            # 发送完成信号
            yield {
                "event": "done",
                "data": "stream_complete"
            }
        
        except Exception as e:
            yield {
                "event": "error",
                "data": str(e)
            }
    
    return EventSourceResponse(event_generator())


@app.get("/api/history/{conversation_id}", tags=["对话历史"])
async def get_history(conversation_id: str):
    """
    获取对话历史
    
    Args:
        conversation_id: 对话ID
    
    Returns:
        消息历史列表
    """
    try:
        memory_manager = get_memory_manager()
        history = memory_manager.get_history(conversation_id)
        
        return {
            "conversation_id": conversation_id,
            "messages": history,
            "count": len(history)
        }
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.delete("/api/history/{conversation_id}", tags=["对话历史"])
async def clear_history(conversation_id: str):
    """
    清除对话历史
    
    Args:
        conversation_id: 对话ID
    """
    try:
        memory_manager = get_memory_manager()
        success = memory_manager.clear_memory(conversation_id)
        
        return {
            "success": success,
            "conversation_id": conversation_id,
            "message": "对话历史已清除" if success else "对话历史不存在"
        }
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/conversations", tags=["对话管理"])
async def list_conversations():
    """
    获取所有对话列表
    """
    try:
        memory_manager = get_memory_manager()
        conversations = memory_manager.get_all_conversations()
        
        return {
            "count": len(conversations),
            "conversations": conversations
        }
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    """HTTP异常处理器"""
    return JSONResponse(
        status_code=exc.status_code,
        content=ErrorResponse(
            error=exc.detail,
            timestamp=datetime.now()
        ).model_dump()
    )


@app.exception_handler(Exception)
async def general_exception_handler(request: Request, exc: Exception):
    """通用异常处理器"""
    return JSONResponse(
        status_code=500,
        content=ErrorResponse(
            error="服务器内部错误",
            detail=str(exc),
            timestamp=datetime.now()
        ).model_dump()
    )


# 欢迎页面
@app.get("/", tags=["首页"])
async def root():
    """欢迎页面"""
    return {
        "message": "🎉 欢迎使用 AI Agent 客服系统",
        "version": "1.0.0",
        "docs": "/docs",
        "health": "/health"
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )
