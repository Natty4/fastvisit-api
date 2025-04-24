from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware
import re

class BotDetectionMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        # Get User-Agent header
        user_agent = request.headers.get("user-agent", "")
        
        # List of common bot user agents
        bot_patterns = [
            r'bot', r'crawler', r'spider', r'slurp', r'baiduspider',
            r'yandex', r'googlebot', r'bingbot', r'semrushbot'
        ]
        
        # Check if the User-Agent matches any bot pattern
        is_bot = any(re.search(pattern, user_agent, re.IGNORECASE) for pattern in bot_patterns)
        
        # Add is_bot to request state
        request.state.is_bot = is_bot
        
        # Continue processing the request
        response = await call_next(request)
        return response
