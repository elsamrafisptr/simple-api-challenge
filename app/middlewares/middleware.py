from functools import wraps
from dependency_injector.wiring import inject as di_inject
from loguru import logger
from typing import Callable, Any

def inject(func: Callable[..., Any]) -> Callable[..., Any]:
    @di_inject
    @wraps(func)
    async def wrapper(*args: Any, **kwargs: Any) -> Any:
        result = func(*args, **kwargs)
        for service in kwargs.values():
            if hasattr(service, "close_scoped_session") and callable(service.close_scoped_session):
                try:
                    service.close_scoped_session()
                except Exception as e:
                    logger.error(f"Error closing scoped session: {e}")
        return result
    return wrapper
