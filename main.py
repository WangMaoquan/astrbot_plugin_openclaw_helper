from astrbot.api.event import filter, AstrMessageEvent
from astrbot.api.star import Context, Star, register
from astrbot.api.provider import ProviderRequest
from astrbot.api import logger
from astrbot.api.message_components import Plain
import json

@register(
    "astrbot_plugin_openclaw_helper",
    "OpenClaw Helper",
    "OpenClaw session helper - whitelist protection for dangerous commands",
    "v0.0.1-beta"
)
class OpenClawHelper(Star):
    def __init__(self, context: Context):
        super().__init__(context)
        # 白名单用户ID列表
        self.whitelist = []
        # 危险关键词列表
        self.dangerous_keywords = [
            "删除", "删除文件", "rm ", "rm -rf", 
            "format", "执行命令", "exec", "sudo",
            "shutdown", "reboot", "kill"
        ]
    
    @filter.command(" whitelist")
    async def whitelist_cmd(self, event: AstrMessageEvent):
        """白名单管理命令"""
        args = event.message_str.strip().split()
        
        if not args:
            # 显示白名单
            yield event.plain_result(f"当前白名单: {self.whitelist}")
            return
        
        action = args[0]
        
        if action == "add" and len(args) > 1:
            user_id = args[1]
            if user_id not in self.whitelist:
                self.whitelist.append(user_id)
            yield event.plain_result(f"已添加 {user_id} 到白名单")
        
        elif action == "remove" and len(args) > 1:
            user_id = args[1]
            if user_id in self.whitelist:
                self.whitelist.remove(user_id)
            yield event.plain_result(f"已从白名单移除 {user_id}")
        
        elif action == "list":
            yield event.plain_result(f"当前白名单: {self.whitelist}")
        
        else:
            yield event.plain_result("用法: /whitelist add|remove|list [user_id]")
    
    @filter.on_llm_request()
    async def on_llm_request(self, event: AstrMessageEvent, req: ProviderRequest):
        """Hook into LLM requests to check whitelist for dangerous commands."""
        user_id = event.get_sender_id()
        message_text = req.prompt or ""
        
        is_dangerous = any(keyword in message_text for keyword in self.dangerous_keywords)
        
        if is_dangerous and str(user_id) not in self.whitelist:
            logger.info(f"[OpenClaw Helper] 危险操作检测 - 用户: {user_id}, 内容: {message_text[:50]}")
            # 注意：这里是检测危险操作，可以选择警告或拦截
