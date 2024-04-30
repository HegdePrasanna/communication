from starlette.middleware.base import BaseHTTPMiddleware
import time
from fastapi import Request


class ResponseTimeMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        start_time = time.time()
        response = await call_next(request)
        execution_time_ms = int((time.time() - start_time) * 1000)
        response.headers["X-Response-Time"] = str(execution_time_ms)
        return response
