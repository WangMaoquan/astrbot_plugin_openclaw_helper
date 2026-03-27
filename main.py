from astrbot.api.event import filter, AstrMessageEvent
from astrbot.api.star import Context, Star, register
from astrbot.api.provider import ProviderRequest
from astrbot.api import logger

@register(
    "astrbot_plugin_openclaw_helper",
    "OpenClaw Helper",
    "OpenClaw session helper - maintains independent sessions per user/group",
    "v0.0.1-beta"
)
class OpenClawHelper(Star):
    def __init__(self, context: Context):
        super().__init__(context)
    
    @filter.on_llm_request()
    async def on_llm_request(self, event: AstrMessageEvent, req: ProviderRequest):
        """Hook into LLM requests to add user parameter for session continuity."""
        # Get user/group info
        user_id = event.get_sender_id()
        group_id = event.get_group_id()
        
        # Log for debugging
        logger.info(f"[OpenClaw Helper] user_id={user_id}, group_id={group_id}")
        
        # Set user and session_id parameter first
        if group_id:
            session_key = f"group_{group_id}"
        else:
            session_key = str(user_id)
        
        req.user = session_key
        req.session_id = session_key
        
        # Log after setting
        logger.info(f"[OpenClaw Helper] req.user set to: {req.user}")
        logger.info(f"[OpenClaw Helper] req.session_id set to: {req.session_id}")
        logger.info(f"[OpenClaw Helper] req attributes after: {dir(req)}")
