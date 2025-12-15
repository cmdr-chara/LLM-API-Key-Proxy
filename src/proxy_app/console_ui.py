"""
Console UI helper module for beautiful terminal output using Rich.
"""

from rich.console import Console, Group
from rich.panel import Panel
from rich.table import Table
from rich.text import Text
from rich.box import ROUNDED, SIMPLE, DOUBLE, MINIMAL
from rich.style import Style
from rich.columns import Columns
from rich.align import Align
from rich.rule import Rule
from datetime import datetime
from typing import Dict, List, Optional, Tuple
import logging


console = Console()

# Color scheme for consistency
COLORS = {
    "primary": "bright_cyan",
    "secondary": "bright_magenta",
    "success": "bright_green",
    "warning": "bright_yellow",
    "error": "bright_red",
    "accent": "bright_blue",
    "muted": "dim",
}

# Simple text banner
MINI_LOGO = "⚡ LLM API Key Proxy"


def print_startup_banner(host: str, port: int, proxy_api_key: Optional[str] = None, github_url: str = ""):
    """Print a beautiful startup banner."""
    console.print()
    
    # Modern styled header
    title = Text()
    title.append("⚡ ", style="bright_yellow")
    title.append("LLM API Key Proxy", style="bold bright_white")
    
    console.print(Panel(
        Align.center(title),
        border_style="bright_blue",
        box=DOUBLE,
        padding=(0, 3),
        expand=False
    ))


def print_config_summary(
    host: str,
    port: int,
    proxy_api_key: Optional[str],
    env_files: List[str],
    github_url: str = ""
):
    """Print configuration summary in a clean panel."""
    lines = []
    
    # Server URL - prominent
    lines.append(f"  [bright_cyan]●[/bright_cyan] [bold]Server[/bold]    [white]http://{host}:{port}[/white]")
    
    # API Key status - show full key, no censorship
    if proxy_api_key:
        lines.append(f"  [bright_green]●[/bright_green] [bold]API Key[/bold]   [green]{proxy_api_key}[/green]")
    else:
        lines.append(f"  [bright_yellow]●[/bright_yellow] [bold]API Key[/bold]   [yellow]Open Access[/yellow] [dim](no auth)[/dim]")
    
    # GitHub
    if github_url:
        lines.append(f"  [dim]●[/dim] [bold]GitHub[/bold]    [dim cyan]{github_url}[/dim cyan]")
    
    console.print(Panel(
        "\n".join(lines),
        title="[bold bright_white]Configuration[/bold bright_white]",
        title_align="left",
        border_style="bright_blue",
        padding=(1, 1),
        box=ROUNDED,
    ))


def print_providers_summary(
    api_credentials: Dict[str, List[str]],
    oauth_credentials: Dict[str, List[str]],
    total_providers: int
):
    """Print a summary of configured providers and credentials."""
    if not api_credentials and not oauth_credentials:
        console.print(Panel(
            "[bright_yellow]⚠️  No provider credentials configured[/bright_yellow]\n"
            "[dim]Run with --add-credential to add API keys or OAuth credentials[/dim]",
            border_style="yellow",
            box=ROUNDED,
            padding=(1, 2),
        ))
        return
    
    # Modern styled table
    table = Table(
        box=ROUNDED,
        show_header=True,
        header_style="bold bright_white",
        border_style="bright_green",
        padding=(0, 1),
        expand=False,
    )
    table.add_column("Provider", style="bright_cyan", min_width=12)
    table.add_column("Type", style="dim white", min_width=8)
    table.add_column("Count", justify="center", style="bright_white", min_width=6)
    table.add_column("Tier", style="dim", min_width=8)
    
    # Combine and sort providers
    all_providers = set(api_credentials.keys()) | set(oauth_credentials.keys())
    
    for provider in sorted(all_providers):
        api_count = len(api_credentials.get(provider, []))
        oauth_count = len(oauth_credentials.get(provider, []))
        
        if api_count > 0:
            table.add_row(
                provider,
                "[blue]API[/blue]",
                f"[bright_green]{api_count}[/bright_green]",
                "[dim]–[/dim]"
            )
        if oauth_count > 0:
            table.add_row(
                provider,
                "[magenta]OAuth[/magenta]",
                f"[bright_green]{oauth_count}[/bright_green]",
                "[magenta]OAuth[/magenta]"
            )
    
    total_count = sum(len(v) for v in api_credentials.values()) + sum(len(v) for v in oauth_credentials.values())
    
    # Print table with title
    console.print()
    title_text = Text()
    title_text.append("Providers ", style="bold bright_white")
    title_text.append(f"({total_providers} plugins, {total_count} credentials)", style="dim")
    console.print(title_text)
    console.print(table)


def print_models_loaded(models_by_source: Dict[str, int]):
    """Print models loaded summary."""
    if not models_by_source:
        return
    
    parts = []
    for source, count in models_by_source.items():
        parts.append(f"[bright_cyan]{source}[/bright_cyan]:[bright_green]{count}[/bright_green]")
    
    console.print(f"  [dim]📊[/dim] Models: {' [dim]│[/dim] '.join(parts)}")


def print_server_ready(elapsed_time: float, provider_count: int, provider_time: float):
    """Print server ready message."""
    console.print()
    
    # Success message with details
    ready_text = Text()
    ready_text.append("✓ ", style="bold bright_green")
    ready_text.append("Server Ready", style="bold bright_green")
    ready_text.append(f" in {elapsed_time:.2f}s", style="dim white")
    
    details = Text()
    details.append(f"  {provider_count} providers discovered in {provider_time:.2f}s", style="dim")
    
    content = Group(
        Align.center(ready_text),
        Align.center(details),
    )
    
    console.print(Panel(
        content,
        border_style="bright_green",
        box=ROUNDED,
        padding=(0, 4),
    ))
    console.print()


def print_loading_step(step: str, status: str = "loading"):
    """Print a loading step with spinner-like appearance."""
    if status == "loading":
        console.print(f"  [bright_blue]⟳[/bright_blue] [dim]{step}...[/dim]", end="\r")
    elif status == "done":
        console.print(f"  [bright_green]✓[/bright_green] {step}    ")  # Extra spaces to clear line
    elif status == "error":
        console.print(f"  [bright_red]✗[/bright_red] {step}    ")


def format_request_log(
    time_str: str,
    client_ip: str,
    client_port: int,
    provider: str,
    model: str,
    status_code: int = 200
) -> str:
    """Format a request log line with colors."""
    # Determine status color and icon
    if status_code < 300:
        status_style = "bright_green"
        status_icon = "●"
    elif status_code < 400:
        status_style = "bright_yellow"
        status_icon = "●"
    else:
        status_style = "bright_red"
        status_icon = "●"
    
    # Truncate model name if too long
    model_display = model if len(model) <= 30 else model[:27] + "..."
    
    return (
        f"[dim]{time_str}[/dim] "
        f"[{status_style}]{status_icon}[/{status_style}] "
        f"[bright_cyan]{provider}[/bright_cyan][dim]/[/dim][white]{model_display}[/white] "
        f"[{status_style}]{status_code}[/{status_style}] "
        f"[dim]← {client_ip}[/dim]"
    )


def log_request(
    client_info: Tuple[str, int],
    provider: str,
    model: str,
    status_code: int = 200
):
    """Log a request with beautiful formatting."""
    time_str = datetime.now().strftime("%H:%M:%S")
    formatted = format_request_log(
        time_str=time_str,
        client_ip=client_info[0],
        client_port=client_info[1],
        provider=provider,
        model=model,
        status_code=status_code
    )
    console.print(formatted)


def print_credential_acquired(credential: str, model: str, tried: int, total: int, tier: Optional[str] = None):
    """Print credential acquisition info (for debug/verbose mode only)."""
    cred_display = mask_credential(credential)
    tier_info = f" [dim magenta]({tier})[/dim magenta]" if tier else ""
    console.print(
        f"  [dim]🔄[/dim] [dim]Acquired[/dim] [bright_cyan]{cred_display}[/bright_cyan]{tier_info} "
        f"[dim]for[/dim] [white]{model}[/white] [dim]({tried}/{total})[/dim]"
    )


def mask_credential(credential: str) -> str:
    """Format credential for display (show filename for paths, full key for API keys)."""
    if "/" in credential or "\\" in credential:
        # It's a path - show just the filename
        import os
        return os.path.basename(credential)
    else:
        # Show full API key (no masking per user preference)
        return credential


class ConsoleLogHandler(logging.Handler):
    """Custom log handler that uses Rich console for beautiful output."""
    
    def __init__(self, level=logging.INFO):
        super().__init__(level)
        self.console = console
        
    def emit(self, record):
        try:
            msg = self.format(record)
            
            # Skip certain verbose messages
            if self._should_skip(msg):
                return
            
            # Format based on level with modern styling
            if record.levelno >= logging.ERROR:
                self.console.print(f"[bright_red]✗[/bright_red] [red]{msg}[/red]")
            elif record.levelno >= logging.WARNING:
                self.console.print(f"[bright_yellow]⚠[/bright_yellow] [yellow]{msg}[/yellow]")
            elif record.levelno >= logging.INFO:
                # Make info messages more concise with subtle styling
                self.console.print(f"  [dim]›[/dim] {msg}")
            else:
                self.console.print(f"  [dim]{msg}[/dim]")
                
        except Exception:
            self.handleError(record)
    
    def _should_skip(self, msg: str) -> bool:
        """Determine if a message should be skipped for cleaner output."""
        skip_patterns = [
            "Started server process",
            "Waiting for application startup",
            "ASGI 'lifespan'",
            "Uvicorn running on",
            "Application startup complete",
        ]
        return any(pattern in msg for pattern in skip_patterns)


def print_dashboard_link(host: str, port: int):
    """Print a clickable dashboard link."""
    url = f"http://{host}:{port}"
    console.print(f"  [bright_cyan]→[/bright_cyan] Dashboard: [bright_blue underline]{url}[/bright_blue underline]")


def print_shutdown_message():
    """Print a clean shutdown message."""
    console.print()
    console.print(Panel(
        "[dim]Server stopped gracefully[/dim]",
        border_style="dim",
        box=ROUNDED,
        padding=(0, 2),
    ))


def setup_console_logging():
    """Set up console logging with the custom handler."""
    # Remove default handlers from uvicorn
    for logger_name in ["uvicorn", "uvicorn.error", "uvicorn.access"]:
        logger = logging.getLogger(logger_name)
        logger.handlers = []
        logger.propagate = False
    
    return ConsoleLogHandler()