from astrbot.api.event import filter, AstrMessageEvent
from astrbot.api.star import Context, Star, register
from astrbot.api.provider import ProviderRequest
from astrbot.api import AstrBotConfig
from astrbot.api import logger
from astrbot.api.message_components import Plain
import json
import re

@register(
    "astrbot_plugin_openclaw_helper",
    "OpenClaw Helper",
    "OpenClaw session helper - whitelist protection for dangerous commands",
    "v0.0.1-beta"
)
class OpenClawHelper(Star):
    def __init__(self, context: Context, config: AstrBotConfig):
        super().__init__(context)
        # 从配置读取白名单
        whitelist_str = config.get("whitelist", "")
        self.whitelist = [uid.strip() for uid in whitelist_str.split(",") if uid.strip()]
        
        # 内置危险关键词（不展示给用户）
        built_in_keywords = {"删除", "rm ", "rm -rf", "exec", "sudo", "shutdown", "reboot", "kill", "format", "del ", "drop "}
        
        # 从配置读取用户添加的关键词
        keywords_str = config.get("dangerous_keywords", "")
        user_keywords = set(k.strip() for k in keywords_str.split(",") if k.strip())
        
        # 合并并去重
        self.dangerous_keywords = list(built_in_keywords | user_keywords)
        
        # 警告消息（支持自定义）
        self.warning_message = config.get("warning_message", "").strip()
        if not self.warning_message:
            # 默认糖浆风格警告
            self.warning_message = "抱歉呀～这个操作有点危险，我不能执行呢 😣 如果真的需要，请联系管理员开通权限哦～"
    
    @filter.command(" whitelist")
    async def whitelist_cmd(self, event: AstrMessageEvent):
        """白名单管理命令"""
        args = event.message_str.strip().split()
        
        if not args:
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
        user_id = str(event.get_sender_id())
        
        # 检查是否在白名单
        if user_id in self.whitelist:
            return
        
        # 检查危险关键词
        message_text = req.prompt or ""
        
        # 使用更精确的匹配
        is_dangerous = False
        matched_keyword = ""
        for keyword in self.dangerous_keywords:
            # 精确匹配整个词或前后有空格
            pattern = r'(^|\s)' + re.escape(keyword) + r'(\s|$)'
            if re.search(pattern, message_text):
                is_dangerous = True
                matched_keyword = keyword
                break
        
        if is_dangerous:
            logger.info(f"[OpenClaw Helper] 危险操作被拦截 - 用户: {user_id}, 关键词: {matched_keyword}")
            # 拦截：清空请求，替换为警告消息
            req.prompt = self.warning_message
            # 可选：添加上下文说明被拦截了
            req.system_prompt = (req.system_prompt or "") + "\n\n[系统] 用户刚才尝试执行危险操作，已被拦截并替换为警告消息。"