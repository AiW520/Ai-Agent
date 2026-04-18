"""
LLM封装模块
配置和使用OpenAI的ChatGPT模型
"""

import os
from typing import Optional
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv

# 加载环境变量
load_dotenv()


class LLMManager:
    """LLM管理器，负责模型的配置和初始化"""
    
    def __init__(
        self,
        model: Optional[str] = None,
        temperature: float = 0.7,
        api_key: Optional[str] = None,
        max_tokens: int = 2000,
        streaming: bool = True
    ):
        """
        初始化LLM管理器
        
        Args:
            model: 模型名称，默认从环境变量读取或使用 gpt-3.5-turbo
            temperature: 温度参数，控制输出的随机性（0-1）
            api_key: OpenAI API密钥，默认从环境变量读取
            max_tokens: 最大生成的token数
            streaming: 是否支持流式输出
        """
        self.model = model or os.getenv("OPENAI_MODEL", "gpt-3.5-turbo")
        self.temperature = temperature
        self.api_key = api_key or os.getenv("OPENAI_API_KEY")
        self.max_tokens = max_tokens
        self.streaming = streaming
        
        # 检查API密钥
        if not self.api_key:
            raise ValueError(
                "未设置OpenAI API密钥！\n"
                "请设置环境变量 OPENAI_API_KEY 或在 .env 文件中配置"
            )
        
        # 创建LLM实例
        self.llm = self._create_llm()
    
    def _create_llm(self) -> ChatOpenAI:
        """
        创建ChatOpenAI实例
        
        Returns:
            ChatOpenAI: 配置好的LLM实例
        """
        return ChatOpenAI(
            model=self.model,
            temperature=self.temperature,
            api_key=self.api_key,
            max_tokens=self.max_tokens,
            streaming=self.streaming,
            callbacks=[]  # 可在此处添加回调用于监控
        )
    
    def get_llm(self) -> ChatOpenAI:
        """
        获取LLM实例
        
        Returns:
            ChatOpenAI: LLM实例
        """
        return self.llm
    
    def update_temperature(self, temperature: float) -> None:
        """
        更新温度参数
        
        Args:
            temperature: 新的温度值（0-1）
        """
        if not 0 <= temperature <= 2:
            raise ValueError("温度参数必须在0到2之间")
        self.temperature = temperature
        self.llm = self._create_llm()
    
    def update_model(self, model: str) -> None:
        """
        更新模型
        
        Args:
            model: 新的模型名称
        """
        self.model = model
        self.llm = self._create_llm()


# 全局LLM实例（延迟初始化）
_llm_manager: Optional[LLMManager] = None


def get_llm_manager() -> LLMManager:
    """
    获取全局LLM管理器实例
    
    Returns:
        LLMManager: LLM管理器实例
    """
    global _llm_manager
    if _llm_manager is None:
        _llm_manager = LLMManager()
    return _llm_manager


def get_llm() -> ChatOpenAI:
    """
    获取LLM实例的便捷函数
    
    Returns:
        ChatOpenAI: LLM实例
    """
    return get_llm_manager().get_llm()
