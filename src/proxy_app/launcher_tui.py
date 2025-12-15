"""
Interactive TUI launcher for the LLM API Key Proxy.
Provides a beautiful Rich-based interface for configuration and execution.
"""

import json
import os
import sys
from pathlib import Path
from rich.console import Console, Group
from rich.prompt import IntPrompt, Prompt
from rich.panel import Panel
from rich.text import Text
from rich.table import Table
from rich.layout import Layout
from rich import box
from rich.align import Align
from rich.columns import Columns
from rich.style import Style
from rich.rule import Rule
from dotenv import load_dotenv, set_key

console = Console()

# Modern color scheme
COLORS = {
    "primary": "bright_cyan",
    "secondary": "bright_magenta",
    "success": "bright_green",
    "warning": "bright_yellow",
    "error": "bright_red",
    "accent": "bright_blue",
    "muted": "dim white",
    "text": "white",
    "highlight": "bold bright_white",
}


def clear_screen():
    """
    Cross-platform terminal clear that works robustly on both
    classic Windows conhost and modern terminals (Windows Terminal, Linux, Mac).

    Uses native OS commands instead of ANSI escape sequences:
    - Windows (conhost & Windows Terminal): cls
    - Unix-like systems (Linux, Mac): clear
    """
    os.system("cls" if os.name == "nt" else "clear")


class LauncherConfig:
    """Manages launcher_config.json (host, port, logging only)"""

    def __init__(self, config_path: Path = Path("launcher_config.json")):
        self.config_path = config_path
        self.defaults = {
            "host": "127.0.0.1",
            "port": 8000,
            "enable_request_logging": False,
        }
        self.config = self.load()

    def load(self) -> dict:
        """Load config from file or create with defaults."""
        if self.config_path.exists():
            try:
                with open(self.config_path, "r") as f:
                    config = json.load(f)
                # Merge with defaults for any missing keys
                for key, value in self.defaults.items():
                    if key not in config:
                        config[key] = value
                return config
            except (json.JSONDecodeError, IOError):
                return self.defaults.copy()
        return self.defaults.copy()

    def save(self):
        """Save current config to file."""
        import datetime

        self.config["last_updated"] = datetime.datetime.now().isoformat()
        try:
            with open(self.config_path, "w") as f:
                json.dump(self.config, f, indent=2)
        except IOError as e:
            console.print(f"[red]Error saving config: {e}[/red]")

    def update(self, **kwargs):
        """Update config values."""
        self.config.update(kwargs)
        self.save()

    @staticmethod
    def update_proxy_api_key(new_key: str):
        """Update PROXY_API_KEY in .env only"""
        env_file = Path.cwd() / ".env"
        set_key(str(env_file), "PROXY_API_KEY", new_key)
        load_dotenv(dotenv_path=env_file, override=True)


class SettingsDetector:
    """Detects settings from .env for display"""

    @staticmethod
    def _load_local_env() -> dict:
        """Load environment variables from all .env files in cwd"""
        env_dict = {}
        cwd = Path.cwd()
        
        # Find all .env files (main .env and any *.env files)
        env_files = []
        main_env = cwd / ".env"
        if main_env.exists():
            env_files.append(main_env)
        
        # Add any additional *.env files (combined env files)
        for env_file in cwd.glob("*.env"):
            if env_file not in env_files:
                env_files.append(env_file)
        
        # Parse all env files
        for env_file in env_files:
            try:
                with open(env_file, "r", encoding="utf-8") as f:
                    for line in f:
                        line = line.strip()
                        if not line or line.startswith("#"):
                            continue
                        if "=" in line:
                            key, _, value = line.partition("=")
                            key, value = key.strip(), value.strip()
                            if value and value[0] in ('"', "'") and value[-1] == value[0]:
                                value = value[1:-1]
                            # Don't override existing values (first file wins)
                            if key not in env_dict:
                                env_dict[key] = value
            except (IOError, OSError):
                pass
        
        return env_dict

    @staticmethod
    def get_all_settings() -> dict:
        """Returns comprehensive settings overview"""
        return {
            "credentials": SettingsDetector.detect_credentials(),
            "custom_bases": SettingsDetector.detect_custom_api_bases(),
            "model_definitions": SettingsDetector.detect_model_definitions(),
            "concurrency_limits": SettingsDetector.detect_concurrency_limits(),
            "model_filters": SettingsDetector.detect_model_filters(),
            "provider_settings": SettingsDetector.detect_provider_settings(),
        }

    @staticmethod
    def detect_credentials() -> dict:
        """Detect API keys and OAuth credentials"""
        from pathlib import Path

        providers = {}

        # Scan for API keys
        env_vars = SettingsDetector._load_local_env()
        for key, value in env_vars.items():
            if "_API_KEY" in key and key != "PROXY_API_KEY":
                provider = key.split("_API_KEY")[0].lower()
                if provider not in providers:
                    providers[provider] = {"api_keys": 0, "oauth": 0, "custom": False}
                providers[provider]["api_keys"] += 1

        # Scan for OAuth credentials
        oauth_dir = Path("oauth_credentials")
        if oauth_dir.exists():
            for file in oauth_dir.glob("*_oauth_*.json"):
                provider = file.name.split("_oauth_")[0]
                if provider not in providers:
                    providers[provider] = {"api_keys": 0, "oauth": 0, "custom": False}
                providers[provider]["oauth"] += 1

        # Mark custom providers (have API_BASE set)
        for provider in providers:
            if os.getenv(f"{provider.upper()}_API_BASE"):
                providers[provider]["custom"] = True

        return providers

    @staticmethod
    def detect_custom_api_bases() -> dict:
        """Detect custom API base URLs (not in hardcoded map)"""
        from proxy_app.provider_urls import PROVIDER_URL_MAP

        bases = {}
        env_vars = SettingsDetector._load_local_env()
        for key, value in env_vars.items():
            if key.endswith("_API_BASE"):
                provider = key.replace("_API_BASE", "").lower()
                # Only include if NOT in hardcoded map
                if provider not in PROVIDER_URL_MAP:
                    bases[provider] = value
        return bases

    @staticmethod
    def detect_model_definitions() -> dict:
        """Detect provider model definitions"""
        models = {}
        env_vars = SettingsDetector._load_local_env()
        for key, value in env_vars.items():
            if key.endswith("_MODELS"):
                provider = key.replace("_MODELS", "").lower()
                try:
                    parsed = json.loads(value)
                    if isinstance(parsed, dict):
                        models[provider] = len(parsed)
                    elif isinstance(parsed, list):
                        models[provider] = len(parsed)
                except (json.JSONDecodeError, ValueError):
                    pass
        return models

    @staticmethod
    def detect_concurrency_limits() -> dict:
        """Detect max concurrent requests per key"""
        limits = {}
        env_vars = SettingsDetector._load_local_env()
        for key, value in env_vars.items():
            if key.startswith("MAX_CONCURRENT_REQUESTS_PER_KEY_"):
                provider = key.replace("MAX_CONCURRENT_REQUESTS_PER_KEY_", "").lower()
                try:
                    limits[provider] = int(value)
                except (json.JSONDecodeError, ValueError):
                    pass
        return limits

    @staticmethod
    def detect_model_filters() -> dict:
        """Detect active model filters (basic info only: defined or not)"""
        filters = {}
        env_vars = SettingsDetector._load_local_env()
        for key, value in env_vars.items():
            if key.startswith("IGNORE_MODELS_") or key.startswith("WHITELIST_MODELS_"):
                filter_type = "ignore" if key.startswith("IGNORE") else "whitelist"
                provider = key.replace(f"{filter_type.upper()}_MODELS_", "").lower()
                if provider not in filters:
                    filters[provider] = {"has_ignore": False, "has_whitelist": False}
                if filter_type == "ignore":
                    filters[provider]["has_ignore"] = True
                else:
                    filters[provider]["has_whitelist"] = True
        return filters

    @staticmethod
    def detect_provider_settings() -> dict:
        """Detect provider-specific settings (Antigravity, Gemini CLI)"""
        try:
            from proxy_app.settings_tool import PROVIDER_SETTINGS_MAP
        except ImportError:
            # Fallback for direct execution or testing
            from .settings_tool import PROVIDER_SETTINGS_MAP

        provider_settings = {}
        env_vars = SettingsDetector._load_local_env()

        for provider, definitions in PROVIDER_SETTINGS_MAP.items():
            modified_count = 0
            for key, definition in definitions.items():
                env_value = env_vars.get(key)
                if env_value is not None:
                    # Check if value differs from default
                    default = definition.get("default")
                    setting_type = definition.get("type", "str")

                    try:
                        if setting_type == "bool":
                            current = env_value.lower() in ("true", "1", "yes")
                        elif setting_type == "int":
                            current = int(env_value)
                        else:
                            current = env_value

                        if current != default:
                            modified_count += 1
                    except (ValueError, AttributeError):
                        pass

            if modified_count > 0:
                provider_settings[provider] = modified_count

        return provider_settings


class LauncherTUI:
    """Main launcher interface"""

    def __init__(self):
        self.console = Console()
        self.config = LauncherConfig()
        self.running = True
        self.env_file = Path.cwd() / ".env"
        self._cached_settings = None
        self._settings_cache_valid = False
        # Load .env file to ensure environment variables are available
        load_dotenv(dotenv_path=self.env_file, override=True)

    def needs_onboarding(self) -> bool:
        """Check if onboarding is needed"""
        return not self.env_file.exists() or not os.getenv("PROXY_API_KEY")

    def _invalidate_settings_cache(self):
        """Invalidate the settings cache to force a refresh"""
        self._settings_cache_valid = False
        self._cached_settings = None

    def _get_settings(self, force_refresh: bool = False):
        """Get settings with caching to avoid repeated file scans"""
        if force_refresh or not self._settings_cache_valid or self._cached_settings is None:
            self._cached_settings = SettingsDetector.get_all_settings()
            self._settings_cache_valid = True
        return self._cached_settings

    def run(self):
        """Main TUI loop"""
        while self.running:
            self.show_main_menu()

    def _create_header(self):
        """Create a modern styled header"""
        title = Text()
        title.append("⚡ ", style="bright_yellow")
        title.append("LLM API Key Proxy", style="bold bright_white")
        
        subtitle = Text("Centralized Control for LLM Providers & Access", style="dim italic")
        
        header_content = Group(
            Align.center(title),
            Align.center(subtitle),
        )
        
        return Panel(
            header_content,
            border_style="bright_blue",
            box=box.DOUBLE,
            padding=(1, 4),
            expand=False
        )

    def _create_server_info_card(self):
        """Create a compact server info card"""
        host = self.config.config['host']
        port = self.config.config['port']
        logging_enabled = self.config.config['enable_request_logging']
        proxy_key = os.getenv("PROXY_API_KEY")
        
        lines = []
        lines.append(f"[bright_cyan]●[/bright_cyan] [bold]Server[/bold]  [white]http://{host}:{port}[/white]")
        
        if proxy_key:
            # Show full API key without censorship
            lines.append(f"[bright_green]●[/bright_green] [bold]API Key[/bold] [green]{proxy_key}[/green]")
        else:
            lines.append(f"[bright_red]●[/bright_red] [bold]API Key[/bold] [red]Not Set[/red] [dim](insecure)[/dim]")
        
        log_status = "[green]ON[/green]" if logging_enabled else "[dim]OFF[/dim]"
        lines.append(f"[bright_blue]●[/bright_blue] [bold]Logging[/bold] {log_status}")
        
        return Panel(
            "\n".join(lines),
            title="[bold bright_white]⚙️  Server Config[/bold bright_white]",
            title_align="left",
            border_style="bright_blue",
            box=box.ROUNDED,
            padding=(1, 2),
        )

    def _create_status_card(self, settings, credentials, custom_bases):
        """Create a status summary card"""
        provider_count = len(credentials)
        custom_count = len(custom_bases)
        total_creds = sum(c.get("api_keys", 0) + c.get("oauth", 0) for c in credentials.values())
        
        provider_settings = settings.get("provider_settings", {})
        has_advanced = bool(
            settings["model_definitions"]
            or settings["concurrency_limits"]
            or settings["model_filters"]
            or provider_settings
        )
        
        lines = []
        if provider_count > 0:
            # Show providers with their names (truncated to first identifier)
            provider_names = ", ".join(sorted(credentials.keys())[:4])
            if len(credentials) > 4:
                provider_names += f"... +{len(credentials) - 4}"
            lines.append(f"[bright_green]●[/bright_green] [bold]Providers[/bold] [white]{provider_count}[/white] [dim]({provider_names})[/dim]")
        else:
            lines.append(f"[bright_yellow]○[/bright_yellow] [bold]Providers[/bold] [dim]None detected[/dim]")
        
        if custom_count > 0:
            lines.append(f"[bright_green]●[/bright_green] [bold]Custom APIs[/bold] [white]{custom_count}[/white]")
        else:
            lines.append(f"[dim]○[/dim] [bold]Custom APIs[/bold] [dim]None[/dim]")
        
        if has_advanced:
            lines.append(f"[bright_magenta]●[/bright_magenta] [bold]Advanced[/bold] [magenta]Configured[/magenta]")
        else:
            lines.append(f"[dim]○[/dim] [bold]Advanced[/bold] [dim]Default[/dim]")
        
        return Panel(
            "\n".join(lines),
            title="[bold bright_white]📊 Status[/bold bright_white]",
            title_align="left",
            border_style="bright_green",
            box=box.ROUNDED,
            padding=(1, 2),
        )

    def _create_menu(self, show_warning: bool):
        """Create the main menu with modern styling"""
        menu_items = [
            ("1", "▶", "Run Proxy Server", "bright_green", None),
            ("2", "⚙", "Configure Settings", "bright_blue", None),
            ("3", "🔑", "Manage Credentials", "bright_yellow", "⬅ Start here!" if show_warning else None),
            ("4", "📊", "Provider & Advanced", "bright_magenta", None),
            ("5", "🔄", "Reload Config", "bright_cyan", None),
            ("6", "ℹ", "About", "dim", None),
            ("7", "✖", "Exit", "dim red", None),
        ]
        
        lines = []
        for num, icon, label, color, hint in menu_items:
            hint_text = f" [bold yellow]{hint}[/bold yellow]" if hint else ""
            lines.append(f"  [{color}]{num}[/{color}]  {icon}  {label}{hint_text}")
        
        return Panel(
            "\n".join(lines),
            title="[bold bright_white]📋 Menu[/bold bright_white]",
            title_align="left",
            border_style="bright_magenta",
            box=box.ROUNDED,
            padding=(1, 2),
        )

    def show_main_menu(self):
        """Display main menu and handle selection"""
        clear_screen()

        # Use cached settings for faster menu display
        settings = self._get_settings()
        credentials = settings["credentials"]
        custom_bases = settings["custom_bases"]

        # Check if setup is needed
        show_warning = self.needs_onboarding()

        # Display Header
        self.console.print()
        self.console.print(Align.center(self._create_header()))
        self.console.print()
        
        # GitHub link - subtle
        github_text = Text()
        github_text.append("    GitHub: ", style="dim")
        github_text.append("github.com/Mirrowel/LLM-API-Key-Proxy", style="dim cyan underline")
        self.console.print(github_text)
        self.console.print()

        # Create cards
        server_card = self._create_server_info_card()
        status_card = self._create_status_card(settings, credentials, custom_bases)
        
        # Show cards side-by-side with better spacing
        self.console.print(Columns([server_card, status_card], padding=2, expand=False))
        self.console.print()

        # Warnings
        if show_warning:
            warning_content = Group(
                Text("⚠️  Initial Setup Required", style="bold yellow"),
                Text(""),
                Text("The proxy needs configuration before first use:", style="white"),
                Text("  • No .env file detected", style="dim"),
                Text("  • Select option 3 to begin setup", style="dim"),
            )
            self.console.print(
                Panel(
                    warning_content,
                    border_style="yellow",
                    box=box.ROUNDED,
                    padding=(1, 2),
                )
            )
            self.console.print()
        elif not os.getenv("PROXY_API_KEY"):
            warning_content = Group(
                Text("⚠️  Security Warning", style="bold red"),
                Text(""),
                Text("PROXY_API_KEY is not set - proxy is unsecured!", style="white"),
                Text("Set via option 2 or 3 to secure your proxy.", style="dim"),
            )
            self.console.print(
                Panel(
                    warning_content,
                    border_style="red",
                    box=box.ROUNDED,
                    padding=(1, 2),
                )
            )
            self.console.print()

        # Menu
        self.console.print(self._create_menu(show_warning))
        self.console.print()

        choice = Prompt.ask(
            "[bright_cyan]›[/bright_cyan] Select option",
            choices=["1", "2", "3", "4", "5", "6", "7"],
            show_choices=False,
        )

        if choice == "1":
            self.run_proxy()
        elif choice == "2":
            self.show_config_menu()
        elif choice == "3":
            self.launch_credential_tool()
        elif choice == "4":
            self.show_provider_settings_menu()
        elif choice == "5":
            with self.console.status("[bright_cyan]Reloading configuration...[/bright_cyan]", spinner="dots"):
                load_dotenv(dotenv_path=Path.cwd() / ".env", override=True)
                self.config = LauncherConfig()  # Reload config
                self._invalidate_settings_cache()  # Force settings refresh
                self._get_settings(force_refresh=True)  # Pre-load settings
            self.console.print("\n[green]✅ Configuration reloaded![/green]")
        elif choice == "6":
            self.show_about()
        elif choice == "7":
            self.running = False
            sys.exit(0)

    def confirm_setting_change(self, setting_name: str, warning_lines: list) -> bool:
        """
        Display a warning and require Y/N (case-sensitive) confirmation.
        Re-prompts until user enters exactly 'Y' or 'N'.
        Returns True only if user enters 'Y'.
        """
        clear_screen()
        self.console.print()
        self.console.print(
            Panel(
                Text.from_markup(
                    f"[bold yellow]⚠️  WARNING: You are about to change the {setting_name}[/bold yellow]\n\n"
                    + "\n".join(warning_lines)
                    + "\n\n[bold]If you are not sure about changing this - don't.[/bold]"
                ),
                border_style="yellow",
                expand=False,
            )
        )

        while True:
            response = Prompt.ask(
                "Enter [bold]Y[/bold] to confirm, [bold]N[/bold] to cancel (case-sensitive)"
            )
            if response == "Y":
                return True
            elif response == "N":
                self.console.print("\n[dim]Operation cancelled.[/dim]")
                return False
            else:
                self.console.print(
                    "[red]Please enter exactly 'Y' or 'N' (case-sensitive)[/red]"
                )

    def show_config_menu(self):
        """Display configuration sub-menu"""
        while True:
            clear_screen()
            
            self.console.print()
            self.console.print(Panel(
                "[bold bright_white]⚙️  Configuration Settings[/bold bright_white]",
                border_style="bright_blue",
                box=box.DOUBLE,
                expand=False
            ))
            self.console.print()

            # Current Settings - modern card style
            host = self.config.config['host']
            port = self.config.config['port']
            logging_enabled = self.config.config['enable_request_logging']
            api_key_set = bool(os.getenv("PROXY_API_KEY"))
            
            settings_lines = [
                f"  [bright_cyan]Host[/bright_cyan]           {host}",
                f"  [bright_cyan]Port[/bright_cyan]           {port}",
                f"  [bright_cyan]Logging[/bright_cyan]        {'[green]Enabled[/green]' if logging_enabled else '[dim]Disabled[/dim]'}",
                f"  [bright_cyan]API Key[/bright_cyan]        {'[green]✓ Set[/green]' if api_key_set else '[red]✗ Not Set[/red]'}",
            ]

            self.console.print(Panel(
                "\n".join(settings_lines),
                title="[bold bright_white]Current Settings[/bold bright_white]",
                title_align="left",
                border_style="bright_cyan",
                box=box.ROUNDED,
                padding=(1, 2)
            ))
            self.console.print()

            # Menu - modern style
            menu_lines = [
                "  [bright_blue]1[/bright_blue]  🌐  Set Host IP",
                "  [bright_blue]2[/bright_blue]  🔌  Set Port",
                "  [bright_blue]3[/bright_blue]  🔑  Set Proxy API Key",
                "  [bright_blue]4[/bright_blue]  📝  Toggle Request Logging",
                "  [bright_blue]5[/bright_blue]  🔄  Reset to Defaults",
                "",
                "  [dim]6[/dim]  ↩   Back to Main Menu",
            ]

            self.console.print(Panel(
                "\n".join(menu_lines),
                title="[bold bright_white]Options[/bold bright_white]",
                title_align="left",
                border_style="bright_magenta",
                box=box.ROUNDED,
                padding=(1, 2)
            ))
            self.console.print()

            choice = Prompt.ask(
                "[bright_cyan]›[/bright_cyan] Select option",
                choices=["1", "2", "3", "4", "5", "6"],
                show_choices=False,
            )

            if choice == "1":
                # Show warning and require confirmation
                confirmed = self.confirm_setting_change(
                    "Host IP",
                    [
                        "Changing the host IP affects which network interfaces the proxy listens on:",
                        "  • [cyan]127.0.0.1[/cyan] = Local access only (recommended for development)",
                        "  • [cyan]0.0.0.0[/cyan] = Accessible from all network interfaces",
                        "",
                        "Applications configured to connect to the old host may fail to connect.",
                    ],
                )
                if not confirmed:
                    continue

                new_host = Prompt.ask(
                    "Enter new host IP", default=self.config.config["host"]
                )
                self.config.update(host=new_host)
                self.console.print(f"\n[green]✅ Host updated to: {new_host}[/green]")
            elif choice == "2":
                # Show warning and require confirmation
                confirmed = self.confirm_setting_change(
                    "Port",
                    [
                        "Changing the port will affect all applications currently configured",
                        "to connect to your proxy on the existing port.",
                        "",
                        "Applications using the old port will fail to connect.",
                    ],
                )
                if not confirmed:
                    continue

                new_port = IntPrompt.ask(
                    "Enter new port", default=self.config.config["port"]
                )
                if 1 <= new_port <= 65535:
                    self.config.update(port=new_port)
                    self.console.print(
                        f"\n[green]✅ Port updated to: {new_port}[/green]"
                    )
                else:
                    self.console.print("\n[red]❌ Port must be between 1-65535[/red]")
            elif choice == "3":
                # Show warning and require confirmation
                confirmed = self.confirm_setting_change(
                    "Proxy API Key",
                    [
                        "This is the authentication key that applications use to access your proxy.",
                        "",
                        "[bold red]⚠️  Changing this will BREAK all applications currently configured",
                        "   with the existing API key![/bold red]",
                        "",
                        "[bold cyan]💡 If you want to add provider API keys (OpenAI, Gemini, etc.),",
                        '   go to "3. 🔑 Manage Credentials" in the main menu instead.[/bold cyan]',
                    ],
                )
                if not confirmed:
                    continue

                current = os.getenv("PROXY_API_KEY", "")
                new_key = Prompt.ask(
                    "Enter new Proxy API Key (leave empty to disable authentication)",
                    default=current,
                )

                if new_key != current:
                    # If setting to empty, show additional warning
                    if not new_key:
                        self.console.print(
                            "\n[bold red]⚠️  Authentication will be DISABLED - anyone can access your proxy![/bold red]"
                        )
                        Prompt.ask("Press Enter to continue", default="")

                    LauncherConfig.update_proxy_api_key(new_key)

                    if new_key:
                        self.console.print(
                            "\n[green]✅ Proxy API Key updated successfully![/green]"
                        )
                        self.console.print("   Updated in .env file")
                    else:
                        self.console.print(
                            "\n[yellow]⚠️  Proxy API Key cleared - authentication disabled![/yellow]"
                        )
                        self.console.print("   Updated in .env file")
                else:
                    self.console.print("\n[yellow]No changes made[/yellow]")
            elif choice == "4":
                current = self.config.config["enable_request_logging"]
                self.config.update(enable_request_logging=not current)
                self.console.print(
                    f"\n[green]✅ Request Logging {'enabled' if not current else 'disabled'}![/green]"
                )
            elif choice == "5":
                # Reset to Default Settings
                # Define defaults
                default_host = "127.0.0.1"
                default_port = 8000
                default_logging = False
                default_api_key = "VerysecretKey"

                # Get current values
                current_host = self.config.config["host"]
                current_port = self.config.config["port"]
                current_logging = self.config.config["enable_request_logging"]
                current_api_key = os.getenv("PROXY_API_KEY", "")

                # Build comparison table
                warning_lines = [
                    "This will reset ALL proxy settings to their defaults:",
                    "",
                    "[bold]   Setting              Current Value         →  Default Value[/bold]",
                    "   " + "─" * 62,
                    f"   Host IP              {current_host:20} →  {default_host}",
                    f"   Port                 {str(current_port):20} →  {default_port}",
                    f"   Request Logging      {'Enabled':20} →  Disabled"
                    if current_logging
                    else f"   Request Logging      {'Disabled':20} →  Disabled",
                    f"   Proxy API Key        {current_api_key[:20]:20} →  {default_api_key}",
                    "",
                    "[bold red]⚠️  This may break applications configured with current settings![/bold red]",
                ]

                confirmed = self.confirm_setting_change(
                    "Settings (Reset to Defaults)", warning_lines
                )
                if not confirmed:
                    continue

                # Apply defaults
                self.config.update(
                    host=default_host,
                    port=default_port,
                    enable_request_logging=default_logging,
                )
                LauncherConfig.update_proxy_api_key(default_api_key)

                self.console.print(
                    "\n[green]✅ All settings have been reset to defaults![/green]"
                )
                self.console.print(f"   Host:             {default_host}")
                self.console.print(f"   Port:             {default_port}")
                self.console.print(f"   Request Logging:  Disabled")
                self.console.print(f"   Proxy API Key:    {default_api_key}")
            elif choice == "6":
                break

    def show_provider_settings_menu(self):
        """Display provider/advanced settings (read-only + launch tool)"""
        clear_screen()
        
        self.console.print()
        self.console.print(Panel(
            "[bold bright_white]📊 Provider & Advanced Settings[/bold bright_white]",
            border_style="bright_blue",
            box=box.DOUBLE,
            expand=False
        ))
        self.console.print()

        settings = SettingsDetector.get_all_settings()
        credentials = settings["credentials"]
        custom_bases = settings["custom_bases"]
        model_defs = settings["model_definitions"]
        concurrency = settings["concurrency_limits"]
        filters = settings["model_filters"]
        provider_settings = settings.get("provider_settings", {})

        # Providers Table - modern styling
        prov_table = Table(
            box=box.ROUNDED,
            show_header=True,
            header_style="bold bright_white",
            border_style="bright_blue",
            padding=(0, 1),
            expand=False,
        )
        prov_table.add_column("Provider", style="bright_cyan", min_width=15)
        prov_table.add_column("API", justify="center", style="white", min_width=6)
        prov_table.add_column("OAuth", justify="center", style="white", min_width=6)
        prov_table.add_column("Custom", justify="center", min_width=8)
        prov_table.add_column("Models", justify="center", min_width=8)

        all_providers = set(credentials.keys()) | set(custom_bases.keys()) | set(model_defs.keys())

        if not all_providers:
            prov_table.add_row("[dim]No providers configured[/dim]", "-", "-", "-", "-")
        else:
            for p in sorted(all_providers):
                cred = credentials.get(p, {"api_keys": 0, "oauth": 0})
                base = "[green]✓[/green]" if p in custom_bases else "[dim]–[/dim]"
                models = str(model_defs.get(p, "[dim]–[/dim]")) if p in model_defs else "[dim]–[/dim]"
                api_count = f"[green]{cred['api_keys']}[/green]" if cred["api_keys"] > 0 else "[dim]–[/dim]"
                oauth_count = f"[green]{cred['oauth']}[/green]" if cred["oauth"] > 0 else "[dim]–[/dim]"
                
                prov_table.add_row(
                    p.title(),
                    api_count,
                    oauth_count,
                    base,
                    models
                )

        self.console.print(prov_table)
        self.console.print()

        # Advanced Settings Table - modern styling
        adv_providers = set(concurrency.keys()) | set(filters.keys()) | set(provider_settings.keys())
        
        if adv_providers:
            adv_table = Table(
                box=box.ROUNDED,
                show_header=True,
                header_style="bold bright_white",
                border_style="bright_magenta",
                padding=(0, 1),
                expand=False,
            )
            adv_table.add_column("Provider", style="bright_cyan", min_width=15)
            adv_table.add_column("Concurrency", justify="center", min_width=12)
            adv_table.add_column("Filters", justify="center", min_width=15)
            adv_table.add_column("Custom Settings", justify="center", min_width=15)

            for p in sorted(adv_providers):
                limit = str(concurrency.get(p)) if p in concurrency else "[dim]default[/dim]"
                
                filt = filters.get(p, {"has_whitelist": False, "has_ignore": False})
                filt_parts = []
                if filt["has_whitelist"]: filt_parts.append("[green]whitelist[/green]")
                if filt["has_ignore"]: filt_parts.append("[yellow]ignore[/yellow]")
                filt_str = ", ".join(filt_parts) if filt_parts else "[dim]–[/dim]"

                mod_settings = provider_settings.get(p, 0)
                mod_str = f"[magenta]{mod_settings} modified[/magenta]" if mod_settings > 0 else "[dim]–[/dim]"

                adv_table.add_row(p.title(), limit, filt_str, mod_str)

            self.console.print(adv_table)
        else:
            self.console.print(Panel(
                "[dim]No advanced settings configured[/dim]",
                border_style="dim",
                box=box.ROUNDED,
            ))
        
        self.console.print()

        # Actions Menu - modern style
        menu_lines = [
            "  [bright_blue]1[/bright_blue]  🔧  Launch Settings Tool",
            "",
            "  [dim]2[/dim]  ↩   Back to Main Menu",
        ]
        
        self.console.print(Panel(
            "\n".join(menu_lines),
            title="[bold bright_white]Actions[/bold bright_white]",
            title_align="left",
            border_style="bright_cyan",
            box=box.ROUNDED,
            padding=(1, 2)
        ))
        
        self.console.print("[dim]ℹ️  Use the Settings Tool to configure advanced options interactively.[/dim]")
        self.console.print()

        choice = Prompt.ask("[bright_cyan]›[/bright_cyan] Select option", choices=["1", "2"], show_choices=False)

        if choice == "1":
            self.launch_settings_tool()
        # choice == "2" returns to main menu

    def launch_credential_tool(self):
        """Launch credential management tool"""
        import time

        # CRITICAL: Show full loading UI to replace the 6-7 second blank wait
        clear_screen()

        _start_time = time.time()

        # Show the same header as standalone mode
        self.console.print("━" * 70)
        self.console.print("Interactive Credential Setup Tool")
        self.console.print("GitHub: https://github.com/Mirrowel/LLM-API-Key-Proxy")
        self.console.print("━" * 70)
        self.console.print("Loading credential management components...")

        # Now import with spinner (this is where the 6-7 second delay happens)
        with self.console.status("Initializing credential tool...", spinner="dots"):
            from rotator_library.credential_tool import (
                run_credential_tool,
                _ensure_providers_loaded,
            )

            _, PROVIDER_PLUGINS = _ensure_providers_loaded()
        self.console.print("✓ Credential tool initialized")

        _elapsed = time.time() - _start_time
        self.console.print(
            f"✓ Tool ready in {_elapsed:.2f}s ({len(PROVIDER_PLUGINS)} providers available)"
        )

        # Small delay to let user see the ready message
        time.sleep(0.5)

        # Run the tool with from_launcher=True to skip duplicate loading screen
        run_credential_tool(from_launcher=True)
        # Reload environment after credential tool
        load_dotenv(dotenv_path=Path.cwd() / ".env", override=True)
        self._invalidate_settings_cache()  # Force settings refresh after credential changes

    def launch_settings_tool(self):
        """Launch settings configuration tool"""
        from proxy_app.settings_tool import run_settings_tool

        run_settings_tool()
        # Reload environment after settings tool
        load_dotenv(dotenv_path=Path.cwd() / ".env", override=True)
        self._invalidate_settings_cache()  # Force settings refresh after settings changes

    def show_about(self):
        """Display About page with project information"""
        clear_screen()

        self.console.print()
        self.console.print(Panel(
            "[bold bright_white]ℹ️  About LLM API Key Proxy[/bold bright_white]",
            border_style="bright_blue",
            box=box.DOUBLE,
            expand=False
        ))
        self.console.print()

        # Project Info Card
        project_info = Group(
            Text("A lightweight, high-performance proxy server for managing", style="white"),
            Text("LLM API keys with automatic rotation and OAuth support.", style="white"),
            Text(""),
            Text("GitHub: github.com/Mirrowel/LLM-API-Key-Proxy", style="dim cyan underline"),
        )
        
        self.console.print(Panel(
            project_info,
            title="[bold bright_white]📦 Project[/bold bright_white]",
            title_align="left",
            border_style="bright_cyan",
            box=box.ROUNDED,
            padding=(1, 2)
        ))
        self.console.print()

        # Features - compact grid style
        features = [
            ("🔄", "Smart Rotation", "Auto-rotate across API keys"),
            ("🔐", "OAuth Support", "Automated OAuth flows"),
            ("🌐", "Multi-Provider", "10+ LLM providers"),
            ("🔧", "Custom APIs", "OpenAI-compatible integration"),
            ("🎯", "Filtering", "Model whitelists/ignore lists"),
            ("⚡", "Concurrency", "Per-key rate limiting"),
            ("💰", "Tracking", "Usage and cost monitoring"),
            ("🎨", "Modern UI", "Beautiful terminal interface"),
        ]
        
        feature_lines = []
        for i in range(0, len(features), 2):
            left = features[i]
            right = features[i + 1] if i + 1 < len(features) else None
            
            left_text = f"  {left[0]} [bright_green]{left[1]}[/bright_green] [dim]{left[2]}[/dim]"
            if right:
                right_text = f"  {right[0]} [bright_green]{right[1]}[/bright_green] [dim]{right[2]}[/dim]"
                feature_lines.append(f"{left_text:<45}{right_text}")
            else:
                feature_lines.append(left_text)
        
        self.console.print(Panel(
            "\n".join(feature_lines),
            title="[bold bright_white]✨ Features[/bold bright_white]",
            title_align="left",
            border_style="bright_green",
            box=box.ROUNDED,
            padding=(1, 2)
        ))
        self.console.print()

        # Credits
        self.console.print(Panel(
            "  Made with [red]❤️[/red]  by the community\n  [dim]Open source - contributions welcome![/dim]",
            title="[bold bright_white]📝 Credits[/bold bright_white]",
            title_align="left",
            border_style="bright_magenta",
            box=box.ROUNDED,
            padding=(1, 2)
        ))
        self.console.print()

        Prompt.ask("[dim]Press Enter to return[/dim]", default="")

    def run_proxy(self):
        """Prepare and launch proxy in same window"""
        # Check if forced onboarding needed
        if self.needs_onboarding():
            clear_screen()
            self.console.print(
                Panel(
                    Text.from_markup(
                        "⚠️  [bold yellow]Setup Required[/bold yellow]\n\n"
                        "Cannot start without .env.\n"
                        "Launching credential tool..."
                    ),
                    border_style="yellow",
                )
            )

            # Force credential tool
            from rotator_library.credential_tool import (
                ensure_env_defaults,
                run_credential_tool,
            )

            ensure_env_defaults()
            load_dotenv(dotenv_path=Path.cwd() / ".env", override=True)
            run_credential_tool()
            load_dotenv(dotenv_path=Path.cwd() / ".env", override=True)

            # Check again after credential tool
            if not os.getenv("PROXY_API_KEY"):
                self.console.print(
                    "\n[red]❌ PROXY_API_KEY still not set. Cannot start proxy.[/red]"
                )
                return

        # Clear console and modify sys.argv
        clear_screen()
        self.console.print(
            f"\n[bold green]🚀 Starting proxy on {self.config.config['host']}:{self.config.config['port']}...[/bold green]\n"
        )

        # Clear console again to remove the starting message before main.py shows loading details
        import time

        time.sleep(0.5)  # Brief pause so user sees the message
        clear_screen()

        # Reconstruct sys.argv for main.py
        sys.argv = [
            "main.py",
            "--host",
            self.config.config["host"],
            "--port",
            str(self.config.config["port"]),
        ]
        if self.config.config["enable_request_logging"]:
            sys.argv.append("--enable-request-logging")

        # Exit TUI - main.py will continue execution
        self.running = False


def run_launcher_tui():
    """Entry point for launcher TUI"""
    # Show loading screen immediately
    console.print()
    
    title = Text()
    title.append("⚡ ", style="bright_yellow")
    title.append("LLM API Key Proxy", style="bold bright_white")
    
    console.print(Panel(
        Align.center(title),
        border_style="bright_blue",
        box=box.DOUBLE,
        padding=(0, 3),
        expand=False
    ))
    console.print()
    
    # Load with visual feedback
    with console.status("[bright_cyan]Loading launcher...[/bright_cyan]", spinner="dots"):
        tui = LauncherTUI()
        # Pre-load settings during startup
        tui._get_settings(force_refresh=True)
    
    tui.run()
