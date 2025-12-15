import json
import os
from datetime import datetime
from pathlib import Path
import uuid
from typing import Literal, Dict, Optional
import logging

from rotator_library.model_info_service import get_model_info_service
from .provider_urls import get_provider_endpoint

# Try to import Rich console for beautiful output
try:
    from rich.console import Console
    from rich.text import Text
    _console = Console()
    _has_rich = True
except ImportError:
    _has_rich = False
    _console = None

# Store pending requests for response correlation
_pending_requests: Dict[str, dict] = {}


def _get_provider_color(provider: str) -> str:
    """Get a consistent color for each provider."""
    provider_colors = {
        "openai": "green",
        "anthropic": "bright_magenta",
        "gemini": "blue",
        "gemini_cli": "blue",
        "openrouter": "cyan",
        "groq": "yellow",
        "mistral": "bright_red",
        "cohere": "bright_blue",
        "nvidia": "bright_green",
        "antigravity": "bright_cyan",
        "qwen_code": "bright_yellow",
        "chutes": "magenta",
        "brave": "bright_white",
        "iflow": "bright_magenta",
    }
    return provider_colors.get(provider.lower(), "white")


def _truncate_model_name(model_name: str, max_length: int = 30) -> str:
    """Truncate model name for display, keeping the most significant parts."""
    if len(model_name) <= max_length:
        return model_name
    
    # If it has multiple slashes (like openai/gpt-5.2-chat), keep just the last part
    if '/' in model_name:
        parts = model_name.split('/')
        # Keep just the actual model name (last part)
        model_name = parts[-1]
    
    if len(model_name) <= max_length:
        return model_name
    
    return model_name[:max_length - 3] + "..."


def log_request_to_console(url: str, headers: dict, client_info: tuple, request_data: dict) -> str:
    """
    Logs a concise, single-line summary of an incoming request to the console.
    Uses Rich formatting when available for beautiful output.
    
    Returns:
        A request ID that can be used to correlate with response logging.
    """
    request_id = str(uuid.uuid4())[:8]
    time_str = datetime.now().strftime("%H:%M:%S")
    model_full = request_data.get("model", "N/A")
    is_streaming = request_data.get("stream", False)
    
    provider = "unknown"
    model_name = model_full

    if '/' in model_full:
        parts = model_full.split('/')
        provider = parts[0]  # First identifier only (e.g., "openrouter", not "openrouter/openai")
        # For display, show the actual model name (last part)
        model_name = parts[-1] if len(parts) > 1 else parts[0]

    # Store request info for response correlation
    _pending_requests[request_id] = {
        "time": time_str,
        "provider": provider,
        "model": model_name,
        "client": client_info[0],
        "streaming": is_streaming,
        "start_time": datetime.now()
    }

    # Truncate model name for display
    model_display = _truncate_model_name(model_name)
    
    if _has_rich and _console:
        # Beautiful Rich-formatted output
        provider_color = _get_provider_color(provider)
        stream_indicator = "[dim italic]⟳[/]" if is_streaming else "[dim]→[/]"
        
        _console.print(
            f"[dim]{time_str}[/] "
            f"{stream_indicator} "
            f"[bold {provider_color}]{provider}[/][dim]/[/][white]{model_display}[/]"
        )
    else:
        # Fallback to standard logging
        stream_marker = "~" if is_streaming else "→"
        log_message = f"{time_str} {stream_marker} {provider}/{model_display}"
        logging.info(log_message)
    
    return request_id


def log_response_to_console(
    request_id: str,
    status_code: int = 200,
    error: Optional[str] = None,
    tokens_used: Optional[int] = None
):
    """
    Logs the response status for a completed request.
    
    Args:
        request_id: The request ID returned by log_request_to_console
        status_code: HTTP status code of the response
        error: Error message if the request failed
        tokens_used: Total tokens used (if available)
    """
    request_info = _pending_requests.pop(request_id, None)
    
    if not request_info:
        return
    
    time_str = datetime.now().strftime("%H:%M:%S")
    provider = request_info["provider"]
    model_name = request_info["model"]
    
    # Calculate duration
    duration = (datetime.now() - request_info["start_time"]).total_seconds()
    
    # Truncate model name for display
    model_display = _truncate_model_name(model_name)
    
    if _has_rich and _console:
        provider_color = _get_provider_color(provider)
        
        if status_code >= 200 and status_code < 300:
            status_icon = "[green]✓[/]"
            status_style = "green"
        elif status_code >= 400 and status_code < 500:
            status_icon = "[yellow]⚠[/]"
            status_style = "yellow"
        else:
            status_icon = "[red]✗[/]"
            status_style = "red"
        
        # Build the log line
        duration_str = f"[dim]{duration:.1f}s[/]"
        tokens_str = f" [dim]({tokens_used} tok)[/]" if tokens_used else ""
        
        if error:
            error_display = f"{error[:50]}..." if len(error) > 50 else error
            _console.print(
                f"[dim]{time_str}[/] "
                f"{status_icon} "
                f"[bold {provider_color}]{provider}[/][dim]/[/][white]{model_display}[/] "
                f"[{status_style}]{status_code}[/] "
                f"{duration_str} "
                f"[dim red]{error_display}[/]"
            )
        else:
            _console.print(
                f"[dim]{time_str}[/] "
                f"{status_icon} "
                f"[bold {provider_color}]{provider}[/][dim]/[/][white]{model_display}[/] "
                f"[{status_style}]{status_code}[/] "
                f"{duration_str}{tokens_str}"
            )
    else:
        # Fallback to standard logging
        status_symbol = "✓" if status_code < 400 else "✗"
        log_message = f"{time_str} {status_symbol} {provider}/{model_name} {status_code} ({duration:.1f}s)"
        if error:
            log_message += f" - {error}"
        logging.info(log_message)


def log_simple_request(provider: str, model: str, status_code: int, duration: float):
    """
    Simple one-line request log showing both request and response info.
    Used for non-streaming requests where we can log everything at once.
    """
    time_str = datetime.now().strftime("%H:%M:%S")
    
    # Truncate model name for display
    model_display = _truncate_model_name(model)
    
    if _has_rich and _console:
        provider_color = _get_provider_color(provider)
        
        if status_code >= 200 and status_code < 300:
            status_icon = "[green]✓[/]"
            status_text = f"[green]{status_code}[/]"
        elif status_code >= 400 and status_code < 500:
            status_icon = "[yellow]⚠[/]"
            status_text = f"[yellow]{status_code}[/]"
        else:
            status_icon = "[red]✗[/]"
            status_text = f"[red]{status_code}[/]"
        
        _console.print(
            f"[dim]{time_str}[/] "
            f"{status_icon} "
            f"[bold {provider_color}]{provider}[/][dim]/[/][white]{model_display}[/] "
            f"{status_text} "
            f"[dim]{duration:.1f}s[/]"
        )
    else:
        status_symbol = "✓" if status_code < 400 else "✗"
        log_message = f"{time_str} {status_symbol} {provider}/{model_display} {status_code} ({duration:.1f}s)"
        logging.info(log_message)

