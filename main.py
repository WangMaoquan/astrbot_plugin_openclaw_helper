from astrbot.api.event import filter, AstrMessageEvent
from astrbot.api.star import Context, Star, register
from astrbot.api.provider import ProviderRequest

@register("astrbot_plugin_openclaw_helper", "OpenClaw Helper", "v1.0.0")
class OpenClawHelper(Star):
    def __init__(self, context: Context):
        super().__init__(context)
    
    @filter.on_llm_request()
    async def on_llm_request(self, event: AstrMessageEvent, req: ProviderRequest):
        """Hook into LLM requests to add user parameter for session continuity."""
        # Get user/group info
        user_id = event.get_sender_id()
        group_id = event.get_group_id()
        
        # Set user parameter
        if group_id:
            req.user = f"group_{group_id}"
        else:
            req.user = str(user_id)
