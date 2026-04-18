"""
数据模型定义
定义聊天请求、响应和消息的数据结构
"""

from pydantic import BaseModel, Field
from typing import Optional, List, Literal
from datetime import datetime


class Message(BaseModel):
    """消息模型"""
    role: Literal["user", "assistant", "system"] = Field(..., description="消息角色")
    content: str = Field(..., description="消息内容")
    timestamp: datetime = Field(default_factory=datetime.now, description="时间戳")


class ChatRequest(BaseModel):
    """聊天请求模型"""
    message: str = Field(..., description="用户消息", min_length=1)
    conversation_id: Optional[str] = Field(default=None, description="对话ID，用于追踪对话历史")


class ChatResponse(BaseModel):
    """聊天响应模型"""
    message: str = Field(..., description="AI回复消息")
    conversation_id: str = Field(..., description="对话ID")
    timestamp: datetime = Field(default_factory=datetime.now, description="时间戳")
    sources: Optional[List[str]] = Field(default=None, description="信息来源")


class HealthResponse(BaseModel):
    """健康检查响应模型"""
    status: str = Field(default="healthy", description="服务状态")
    version: str = Field(default="1.0.0", description="版本号")
    timestamp: datetime = Field(default_factory=datetime.now, description="检查时间")


class ErrorResponse(BaseModel):
    """错误响应模型"""
    error: str = Field(..., description="错误信息")
    detail: Optional[str] = Field(default=None, description="错误详情")
    timestamp: datetime = Field(default_factory=datetime.now, description="错误发生时间")
