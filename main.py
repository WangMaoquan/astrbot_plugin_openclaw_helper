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
    "v0.0.3-beta"
)
class OpenClawHelper(Star):
    def __init__(self, context: Context, config: AstrBotConfig):
        super().__init__(context)
        # 从配置读取管理员ID
        admin_str = config.get("admin_ids", "")
        self.admin_ids = [uid.strip() for uid in admin_str.split(",") if uid.strip()]
        
        # 白名单通过 /whitelist add 命令添加，不从配置读取
        self.whitelist = []
        
        # 内置危险关键词（不展示给用户）- 只保留最明确的危险操作
        built_in_keywords = {
            # 文件删除
            "删除", "rm ", "rm -rf", "del ", "drop ", "unlink",
            # 系统操作
            "exec", "sudo", "shutdown", "reboot", "kill", "pkill",
            # 明确获取敏感信息
            "获取密码", "获取token", "读取密码", "查看密码",
            "读取credentials", "获取credentials", "读取token",
            "给我密码", "给我token", "show me password",
            # 网络下载执行
            "curl ", "wget ", "curl -", "wget -",
            # 其他危险操作
            "format", "chmod 777", "chown "
        }
        
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
    
    def is_admin(self, user_id: str) -> bool:
        """检查是否为管理员"""
        return user_id in self.admin_ids
    
    @filter.command(" whitelist")
    async def whitelist_cmd(self, event: AstrMessageEvent):
        user_id = str(event.get_sender_id())
        args = event.message_str.strip().split()
        
        # 需要管理员权限才能执行任何操作
        if not self.is_admin(user_id):
            yield event.plain_result("抱歉，你没有权限执行此操作哦 😣")
            return
        
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
    async def on_llm_request_handler(self, event: AstrMessageEvent, req: ProviderRequest):
        """Hook into LLM requests to check whitelist for dangerous commands."""
        user_id = str(event.get_sender_id())
        
        # 打印收到的 prompt
        logger.info(f"[OpenClaw Helper] prompt: {req.prompt[:200] if req.prompt else 'None'}")
        
        # 只有管理员能通过，其他人一概拦截，不调用 LLM
        if not self.is_admin(user_id):
            logger.info(f"[OpenClaw Helper] 非管理员用户危险操作被拦截 - 用户: {user_id}")
            yield event.plain_result(self.warning_message)
            event.stop_event()
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