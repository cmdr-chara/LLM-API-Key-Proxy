<<<<<<< HEAD
# Universal LLM API Proxy & Resilience Library [![ko-fi](https://ko-fi.com/img/githubbutton_sm.svg)](https://ko-fi.com/C0C0UZS4P)
[![Ask DeepWiki](https://deepwiki.com/badge.svg)](https://deepwiki.com/Mirrowel/LLM-API-Key-Proxy) [![zread](https://img.shields.io/badge/Ask_Zread-_.svg?style=flat&color=00b0aa&labelColor=000000&logo=data%3Aimage%2Fsvg%2Bxml%3Bbase64%2CPHN2ZyB3aWR0aD0iMTYiIGhlaWdodD0iMTYiIHZpZXdCb3g9IjAgMCAxNiAxNiIgZmlsbD0ibm9uZSIgeG1sbnM9Imh0dHA6Ly93d3cudzMub3JnLzIwMDAvc3ZnIj4KPHBhdGggZD0iTTQuOTYxNTYgMS42MDAxSDIuMjQxNTZDMS44ODgxIDEuNjAwMSAxLjYwMTU2IDEuODg2NjQgMS42MDE1NiAyLjI0MDFWNC45NjAxQzEuNjAxNTYgNS4zMTM1NiAxLjg4ODEgNS42MDAxIDIuMjQxNTYgNS42MDAxSDQuOTYxNTZDNS4zMTUwMiA1LjYwMDEgNS42MDE1NiA1LjMxMzU2IDUuNjAxNTYgNC45NjAxVjIuMjQwMUM1LjYwMTU2IDEuODg2NjQgNS4zMTUwMiAxLjYwMDEgNC45NjE1NiAxLjYwMDFaIiBmaWxsPSIjZmZmIi8%2BCjxwYXRoIGQ9Ik00Ljk2MTU2IDEwLjM5OTlIMi4yNDE1NkMxLjg4ODEgMTAuMzk5OSAxLjYwMTU2IDEwLjY4NjQgMS42MDE1NiAxMS4wMzk5VjEzLjc1OTlDMS42MDE1NiAxNC4xMTM0IDEuODg4MSAxNC4zOTk5IDIuMjQxNTYgMTQuMzk5OUg0Ljk2MTU2QzUuMzE1MDIgMTQuMzk5OSA1LjYwMTU2IDE0LjExMzQgNS42MDE1NiAxMy43NTk5VjExLjAzOTlDNS42MDE1NiAxMC42ODY0IDUuMzE1MDIgMTAuMzk5OSA0Ljk2MTU2IDEwLjM5OTlaIiBmaWxsPSIjZmZmIi8%2BCjxwYXRoIGQ9Ik0xMy43NTg0IDEuNjAwMUgxMS4wMzg0QzEwLjY4NSAxLjYwMDEgMTAuMzk4NCAxLjg4NjY0IDEwLjM5ODQgMi4yNDAxVjQuOTYwMUMxMC4zOTg0IDUuMzEzNTYgMTAuNjg1IDUuNjAwMSAxMS4wMzg0IDUuNjAwMUgxMy43NTg0QzE0LjExMTkgNS42MDAxIDE0LjM5ODQgNS4zMTM1NiAxNC4zOTg0IDQuOTYwMVYyLjI0MDFDMTQuMzk4NCAxLjg4NjY0IDE0LjExMTkgMS42MDAxIDEzLjc1ODQgMS42MDAxWiIgZmlsbD0iI2ZmZiIvPgo8cGF0aCBkPSJNNCAxMkwxMiA0TDQgMTJaIiBmaWxsPSIjZmZmIi8%2BCjxwYXRoIGQ9Ik00IDEyTDEyIDQiIHN0cm9rZT0iI2ZmZiIgc3Ryb2tlLXdpZHRoPSIxLjUiIHN0cm9rZS1saW5lY2FwPSJyb3VuZCIvPgo8L3N2Zz4K&logoColor=ffffff)](https://zread.ai/Mirrowel/LLM-API-Key-Proxy)


## Detailed Setup and Features

This project provides a powerful solution for developers building complex applications, such as agentic systems, that interact with multiple Large Language Model (LLM) providers. It consists of two distinct but complementary components:

1.  **A Universal API Proxy**: A self-hosted FastAPI application that provides a single, OpenAI-compatible endpoint for all your LLM requests. Powered by `litellm`, it allows you to seamlessly switch between different providers and models without altering your application's code.
2.  **A Resilience & Key Management Library**: The core engine that powers the proxy. This reusable Python library intelligently manages a pool of API keys to ensure your application is highly available and resilient to transient provider errors or performance issues.

## Features

-   **Universal API Endpoint**: Simplifies development by providing a single, OpenAI-compatible interface for diverse LLM providers.
-   **High Availability**: The underlying library ensures your application remains operational by gracefully handling transient provider errors and API key-specific issues.
-   **Resilient Performance**: A global timeout on all requests prevents your application from hanging on unresponsive provider APIs.
-   **Advanced Concurrency Control**: A single API key can be used for multiple concurrent requests. By default, it supports concurrent requests to *different* models. With configuration (`MAX_CONCURRENT_REQUESTS_PER_KEY_<PROVIDER>`), it can also support multiple concurrent requests to the *same* model using the same key.
-   **Intelligent Key Management**: Optimizes request distribution across your pool of keys by selecting the best available one for each call.
-   **Automated OAuth Discovery**: Automatically discovers, validates, and manages OAuth credentials from standard provider directories (e.g., `~/.gemini/`, `~/.qwen/`, `~/.iflow/`).
-   **Stateless Deployment Support**: Deploy easily to platforms like Railway, Render, or Vercel. The new export tool converts complex OAuth credentials (Gemini CLI, Qwen, iFlow) into simple environment variables, removing the need for persistent storage or file uploads.
-   **Batch Request Processing**: Efficiently aggregates multiple embedding requests into single batch API calls, improving throughput and reducing rate limit hits.
-   **New Provider Support**: Full support for **iFlow** (API Key & OAuth), **Qwen Code** (API Key & OAuth), and **NVIDIA NIM** with DeepSeek thinking support, including special handling for their API quirks (tool schema cleaning, reasoning support, dedicated logging).
-   **Duplicate Credential Detection**: Intelligently detects if multiple local credential files belong to the same user account and logs a warning, preventing redundancy in your key pool.
-   **Escalating Per-Model Cooldowns**: If a key fails for a specific model, it's placed on a temporary, escalating cooldown for that model, allowing it to be used with others.
-   **Automatic Daily Resets**: Cooldowns and usage statistics are automatically reset daily, making the system self-maintaining.
-   **Detailed Request Logging**: Enable comprehensive logging for debugging. Each request gets its own directory with full request/response details, streaming chunks, and performance metadata.
-   **Provider Agnostic**: Compatible with any provider supported by `litellm`.
-   **OpenAI-Compatible Proxy**: Offers a familiar API interface with additional endpoints for model and provider discovery.
-   **Advanced Model Filtering**: Supports both blacklists and whitelists to give you fine-grained control over which models are available through the proxy.

-   **🆕 Antigravity Provider**: Full support for Google's internal Antigravity API, providing access to Gemini 3 and Claude models with advanced features:
    - **🚀 Claude Opus 4.5** - Anthropic's most powerful model (thinking mode only)
    - **Claude Sonnet 4.5** - Supports both thinking and non-thinking modes
    - **Gemini 3 Pro** - With thinkingLevel support (low/high)
    - Credential prioritization with automatic paid/free tier detection
    - Thought signature caching for multi-turn conversations
    - Tool hallucination prevention via parameter signature injection
    - Automatic thinking block sanitization for Claude models (with recovery strategies)
    - Note: Claude thinking mode requires careful conversation state management (see [Antigravity documentation](DOCUMENTATION.md#antigravity-claude-extended-thinking-sanitization) for details)
-   **🆕 Credential Prioritization**: Automatic tier detection and priority-based credential selection ensures paid-tier credentials are used for premium models that require them.
-   **🆕 Sequential Rotation Mode**: Choose between balanced (distribute load evenly) or sequential (use until exhausted) credential rotation strategies. Sequential mode maximizes cache hit rates for providers like Antigravity.
-   **🆕 Per-Model Quota Tracking**: Granular per-model usage tracking with authoritative quota reset timestamps from provider error responses. Each model maintains its own window with `window_start_ts` and `quota_reset_ts`.
-   **🆕 Model Quota Groups**: Group models that share quota limits (e.g., Claude Sonnet and Opus). When one model in a group hits quota, all receive the same cooldown timestamp.
-   **🆕 Priority-Based Concurrency**: Assign credentials to priority tiers (1=highest) with configurable concurrency multipliers. Paid-tier credentials can handle more concurrent requests than free-tier ones.
-   **🆕 Provider-Specific Quota Parsing**: Extended provider interface with `parse_quota_error()` method to extract precise retry-after times from provider-specific error formats (e.g., Google RPC format).
-   **🆕 Flexible Rolling Windows**: Support for provider-specific quota reset configurations (5-hour, 7-day, etc.) replacing hardcoded daily resets.
-   **🆕 Weighted Random Rotation**: Configurable credential rotation strategy - choose between deterministic (perfect balance) or weighted random (unpredictable, harder to fingerprint) selection.
-   **🆕 Enhanced Gemini CLI**: Improved project discovery, paid vs free tier detection, and Gemini 3 support with thoughtSignature caching.
-   **🆕 Temperature Override**: Global temperature=0 override option to prevent tool hallucination issues with low-temperature settings.
-   **🆕 Provider Cache System**: Modular caching system for preserving conversation state (thought signatures, thinking content) across requests.
-   **🆕 Refactored OAuth Base**: Shared [`GoogleOAuthBase`](src/rotator_library/providers/google_oauth_base.py) class eliminates code duplication across OAuth providers.

-   **🆕 Interactive Launcher TUI**: Beautiful, cross-platform TUI for configuration and management with an integrated settings tool for advanced configuration.


---

## 1. Quick Start

### Windows (Simplest)

1.  **Download the latest release** from the [GitHub Releases page](https://github.com/Mirrowel/LLM-API-Key-Proxy/releases/latest).
2.  Unzip the downloaded file.
3.  **Run the executable** (run without arguments). This launches the **interactive TUI launcher** which allows you to:
    -   🚀 Run the proxy server with your configured settings
    -   ⚙️ Configure proxy settings (Host, Port, PROXY_API_KEY, Request Logging)
    -   🔑 Manage credentials (add/edit API keys & OAuth credentials)
    -   📊 View provider status and advanced settings
    -   🔧 Configure advanced settings interactively (custom API bases, model definitions, concurrency limits)
    -   🔄 Reload configuration without restarting

> **Note:** The legacy `launcher.bat` is deprecated.

### macOS / Linux

**Option A: Using the Executable (Recommended)**
If you downloaded the pre-compiled binary for your platform, no Python installation is required.

1.  **Download the latest release** from the GitHub Releases page.
2.  Open a terminal and make the binary executable:
    ```bash
    chmod +x proxy_app
    ```
3.  **Run the Interactive Launcher**:
    ```bash
    ./proxy_app
    ```
    This launches the TUI where you can configure and run the proxy.

4.  **Or run directly with arguments** to bypass the launcher:
    ```bash
    ./proxy_app --host 0.0.0.0 --port 8000
    ```

**Option B: Manual Setup (Source Code)**
If you are running from source, use these commands:

**1. Install Dependencies**
```bash
# Ensure you have Python 3.10+ installed
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

**2. Launch the Interactive TUI**
```bash
export PYTHONPATH=$PYTHONPATH:$(pwd)/src
python src/proxy_app/main.py
```

**3. Or run directly with arguments to bypass the launcher**
```bash
export PYTHONPATH=$PYTHONPATH:$(pwd)/src
python src/proxy_app/main.py --host 0.0.0.0 --port 8000
```
*To enable logging, add `--enable-request-logging` to the command.*

---

## 2. Interactive TUI Launcher

The proxy now includes a powerful **interactive Text User Interface (TUI)** that makes configuration and management effortless.

### Features

- **🎯 Main Menu**:
  - Run proxy server with saved settings
  - Configure proxy settings (host, port, API key, logging)
  - Manage credentials (API keys & OAuth)
  - View provider & advanced settings status
  - Reload configuration
  
- **🔧 Advanced Settings Tool**:
  - Configure custom OpenAI-compatible providers
  - Define provider models (simple or advanced JSON format)
  - Set concurrency limits per provider
  - Configure rotation modes (balanced vs sequential)
  - Manage priority-based concurrency multipliers
  - Interactive numbered menus for easy selection
  - Pending changes system with save/discard options

- **📊 Status Dashboard**:
  - Shows configured providers and credential counts
  - Displays custom providers and API bases
  - Shows active advanced settings
  - Real-time configuration status

### How to Use

**Running without arguments launches the TUI:**
```bash
# Windows
proxy_app.exe

# macOS/Linux
./proxy_app

# From source
python src/proxy_app/main.py
```

**Running with arguments bypasses the TUI:**
```bash
# Direct startup (skips TUI)
proxy_app.exe --host 0.0.0.0 --port 8000
```

### Configuration Files

The TUI manages two configuration files:
- **`launcher_config.json`**: Stores launcher-specific settings (host, port, logging preference)
- **`.env`**: Stores all credentials and advanced settings (PROXY_API_KEY, provider credentials, custom settings)

All advanced settings configured through the TUI are stored in `.env` for compatibility with manual editing and deployment platforms.

---

## 3. Detailed Setup (From Source)

This guide is for users who want to run the proxy from the source code on any operating system.

### Step 1: Clone and Install

First, clone the repository and install the required dependencies into a virtual environment.

**Linux/macOS:**
```bash
# Clone the repository
git clone https://github.com/Mirrowel/LLM-API-Key-Proxy.git
cd LLM-API-Key-Proxy

# Create and activate a virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

**Windows:**
```powershell
# Clone the repository
git clone https://github.com/Mirrowel/LLM-API-Key-Proxy.git
cd LLM-API-Key-Proxy

# Create and activate a virtual environment
python -m venv venv
.\venv\Scripts\Activate.ps1

# Install dependencies
pip install -r requirements.txt
```

### Step 2: Configure API Keys

Create a `.env` file to store your secret keys. You can do this by copying the example file.

**Linux/macOS:**
```bash
cp .env.example .env
```

**Windows:**
```powershell
copy .env.example .env
```

Now, open the new `.env` file and add your keys.

**Refer to the `.env.example` file for the correct format and a full list of supported providers.**

The proxy supports two types of credentials:

1.  **API Keys**: Standard secret keys from providers like OpenAI, Anthropic, etc.
2.  **OAuth Credentials**: For services that use OAuth 2.0, like the Gemini CLI.

#### Automated Credential Discovery (Recommended)

For many providers, **no configuration is necessary**. The proxy automatically discovers and manages credentials from their default locations:
-   **API Keys**: Scans your environment variables for keys matching the format `PROVIDER_API_KEY_1` (e.g., `GEMINI_API_KEY_1`).
-   **OAuth Credentials**: Scans default system directories (e.g., `~/.gemini/`, `~/.qwen/`, `~/.iflow/`) for all `*.json` credential files.

You only need to create a `.env` file to set your `PROXY_API_KEY` and to override or add credentials if the automatic discovery doesn't suit your needs.

#### Interactive Credential Management Tool

The proxy includes a powerful interactive CLI tool for managing all your credentials. This is the recommended way to set up credentials:
=======
# Universal LLM API Proxy & Resilience Library 
[![ko-fi](https://ko-fi.com/img/githubbutton_sm.svg)](https://ko-fi.com/C0C0UZS4P)
[![Ask DeepWiki](https://deepwiki.com/badge.svg)](https://deepwiki.com/Mirrowel/LLM-API-Key-Proxy) [![zread](https://img.shields.io/badge/Ask_Zread-_.svg?style=flat&color=00b0aa&labelColor=000000&logo=data%3Aimage%2Fsvg%2Bxml%3Bbase64%2CPHN2ZyB3aWR0aD0iMTYiIGhlaWdodD0iMTYiIHZpZXdCb3g9IjAgMCAxNiAxNiIgZmlsbD0ibm9uZSIgeG1sbnM9Imh0dHA6Ly93d3cudzMub3JnLzIwMDAvc3ZnIj4KPHBhdGggZD0iTTQuOTYxNTYgMS42MDAxSDIuMjQxNTZDMS44ODgxIDEuNjAwMSAxLjYwMTU2IDEuODg2NjQgMS42MDE1NiAyLjI0MDFWNC45NjAxQzEuNjAxNTYgNS4zMTM1NiAxLjg4ODEgNS42MDAxIDIuMjQxNTYgNS42MDAxSDQuOTYxNTZDNS4zMTUwMiA1LjYwMDEgNS42MDE1NiA1LjMxMzU2IDUuNjAxNTYgNC45NjAxVjIuMjQwMUM1LjYwMTU2IDEuODg2NjQgNS4zMTUwMiAxLjYwMDEgNC45NjE1NiAxLjYwMDFaIiBmaWxsPSIjZmZmIi8%2BCjxwYXRoIGQ9Ik00Ljk2MTU2IDEwLjM5OTlIMi4yNDE1NkMxLjg4ODEgMTAuMzk5OSAxLjYwMTU2IDEwLjY4NjQgMS42MDE1NiAxMS4wMzk5VjEzLjc1OTlDMS42MDE1NiAxNC4xMTM0IDEuODg4MSAxNC4zOTk5IDIuMjQxNTYgMTQuMzk5OUg0Ljk2MTU2QzUuMzE1MDIgMTQuMzk5OSA1LjYwMTU2IDE0LjExMzQgNS42MDE1NiAxMy43NTk5VjExLjAzOTlDNS42MDE1NiAxMC42ODY0IDUuMzE1MDIgMTAuMzk5OSA0Ljk2MTU2IDEwLjM5OTlaIiBmaWxsPSIjZmZmIi8%2BCjxwYXRoIGQ9Ik0xMy43NTg0IDEuNjAwMUgxMS4wMzg0QzEwLjY4NSAxLjYwMDEgMTAuMzk4NCAxLjg4NjY0IDEwLjM5ODQgMi4yNDAxVjQuOTYwMUMxMC4zOTg0IDUuMzEzNTYgMTAuNjg1IDUuNjAwMSAxMS4wMzg0IDUuNjAwMUgxMy43NTg0QzE0LjExMTkgNS42MDAxIDE0LjM5ODQgNS4zMTM1NiAxNC4zOTg0IDQuOTYwMVYyLjI0MDFDMTQuMzk4NCAxLjg4NjY0IDE0LjExMTkgMS42MDAxIDEzLjc1ODQgMS42MDAxWiIgZmlsbD0iI2ZmZiIvPgo8cGF0aCBkPSJNNCAxMkwxMiA0TDQgMTJaIiBmaWxsPSIjZmZmIi8%2BCjxwYXRoIGQ9Ik00IDEyTDEyIDQiIHN0cm9rZT0iI2ZmZiIgc3Ryb2tlLXdpZHRoPSIxLjUiIHN0cm9rZS1saW5lY2FwPSJyb3VuZCIvPgo8L3N2Zz4K&logoColor=ffffff)](https://zread.ai/Mirrowel/LLM-API-Key-Proxy)

**One proxy. Any LLM provider. Zero code changes.**

A self-hosted proxy that provides a single, OpenAI-compatible API endpoint for all your LLM providers. Works with any application that supports custom OpenAI base URLs—no code changes required in your existing tools.

This project consists of two components:
1. **The API Proxy** — A FastAPI application providing a universal `/v1/chat/completions` endpoint
2. **The Resilience Library** — A reusable Python library for intelligent API key management, rotation, and failover

---

## Why Use This?

- **Universal Compatibility** — Works with any app supporting OpenAI-compatible APIs: Opencode, Continue, Roo/Kilo Code, JanitorAI, SillyTavern, custom applications, and more
- **One Endpoint, Many Providers** — Configure Gemini, OpenAI, Anthropic, and [any LiteLLM-supported provider](https://docs.litellm.ai/docs/providers) once. Access them all through a single API key
- **Built-in Resilience** — Automatic key rotation, failover on errors, rate limit handling, and intelligent cooldowns
- **Exclusive Provider Support** — Includes custom providers not available elsewhere: **Antigravity** (Gemini 3 + Claude Sonnet/Opus 4.5), **Gemini CLI**, **Qwen Code**, and **iFlow**

---

## Quick Start

### Windows

1. **Download** the latest release from [GitHub Releases](https://github.com/Mirrowel/LLM-API-Key-Proxy/releases/latest)
2. **Unzip** the downloaded file
3. **Run** `proxy_app.exe` — the interactive TUI launcher opens

<!-- TODO: Add TUI main menu screenshot here -->

### macOS / Linux

```bash
# Download and extract the release for your platform
chmod +x proxy_app
./proxy_app
```

### From Source

```bash
git clone https://github.com/Mirrowel/LLM-API-Key-Proxy.git
cd LLM-API-Key-Proxy
python3 -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
python src/proxy_app/main.py
```

> **Tip:** Running with command-line arguments (e.g., `--host 0.0.0.0 --port 8000`) bypasses the TUI and starts the proxy directly.

---

## Connecting to the Proxy

Once the proxy is running, configure your application with these settings:

| Setting | Value |
|---------|-------|
| **Base URL / API Endpoint** | `http://127.0.0.1:8000/v1` |
| **API Key** | Your `PROXY_API_KEY` |

### Model Format: `provider/model_name`

**Important:** Models must be specified in the format `provider/model_name`. The `provider/` prefix tells the proxy which backend to route the request to.

```
gemini/gemini-2.5-flash          ← Gemini API
openai/gpt-4o                    ← OpenAI API
anthropic/claude-3-5-sonnet      ← Anthropic API
openrouter/anthropic/claude-3-opus  ← OpenRouter
gemini_cli/gemini-2.5-pro        ← Gemini CLI (OAuth)
antigravity/gemini-3-pro-preview ← Antigravity (Gemini 3, Claude Opus 4.5)
```

### Usage Examples

<details>
<summary><b>Python (OpenAI Library)</b></summary>

```python
from openai import OpenAI

client = OpenAI(
    base_url="http://127.0.0.1:8000/v1",
    api_key="your-proxy-api-key"
)

response = client.chat.completions.create(
    model="gemini/gemini-2.5-flash",  # provider/model format
    messages=[{"role": "user", "content": "Hello!"}]
)
print(response.choices[0].message.content)
```

</details>

<details>
<summary><b>curl</b></summary>

```bash
curl -X POST http://127.0.0.1:8000/v1/chat/completions \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer your-proxy-api-key" \
  -d '{
    "model": "gemini/gemini-2.5-flash",
    "messages": [{"role": "user", "content": "What is the capital of France?"}]
  }'
```

</details>

<details>
<summary><b>JanitorAI / SillyTavern / Other Chat UIs</b></summary>

1. Go to **API Settings**
2. Select **"Proxy"** or **"Custom OpenAI"** mode
3. Configure:
   - **API URL:** `http://127.0.0.1:8000/v1`
   - **API Key:** Your `PROXY_API_KEY`
   - **Model:** `provider/model_name` (e.g., `gemini/gemini-2.5-flash`)
4. Save and start chatting

</details>

<details>
<summary><b>Continue / Cursor / IDE Extensions</b></summary>

In your configuration file (e.g., `config.json`):

```json
{
  "models": [{
    "title": "Gemini via Proxy",
    "provider": "openai",
    "model": "gemini/gemini-2.5-flash",
    "apiBase": "http://127.0.0.1:8000/v1",
    "apiKey": "your-proxy-api-key"
  }]
}
```

</details>

### API Endpoints

| Endpoint | Description |
|----------|-------------|
| `GET /` | Status check — confirms proxy is running |
| `POST /v1/chat/completions` | Chat completions (main endpoint) |
| `POST /v1/embeddings` | Text embeddings |
| `GET /v1/models` | List all available models with pricing & capabilities |
| `GET /v1/models/{model_id}` | Get details for a specific model |
| `GET /v1/providers` | List configured providers |
| `POST /v1/token-count` | Calculate token count for a payload |
| `POST /v1/cost-estimate` | Estimate cost based on token counts |

> **Tip:** The `/v1/models` endpoint is useful for discovering available models in your client. Many apps can fetch this list automatically. Add `?enriched=false` for a minimal response without pricing data.

---

## Managing Credentials

The proxy includes an interactive tool for managing all your API keys and OAuth credentials.

### Using the TUI

<!-- TODO: Add TUI credentials menu screenshot here -->

1. Run the proxy without arguments to open the TUI
2. Select **"🔑 Manage Credentials"**
3. Choose to add API keys or OAuth credentials

### Using the Command Line
>>>>>>> origin/main

### Credential Types

| Type | Providers | How to Add |
|------|-----------|------------|
| **API Keys** | Gemini, OpenAI, Anthropic, OpenRouter, Groq, Mistral, NVIDIA, Cohere, Chutes | Enter key in TUI or add to `.env` |
| **OAuth** | Gemini CLI, Antigravity, Qwen Code, iFlow | Interactive browser login via credential tool |

### The `.env` File

Credentials are stored in a `.env` file. You can edit it directly or use the TUI:

```env
# Required: Authentication key for YOUR proxy
PROXY_API_KEY="your-secret-proxy-key"

# Provider API Keys (add multiple with _1, _2, etc.)
GEMINI_API_KEY_1="your-gemini-key"
GEMINI_API_KEY_2="another-gemini-key"
OPENAI_API_KEY_1="your-openai-key"
ANTHROPIC_API_KEY_1="your-anthropic-key"
```

> Copy `.env.example` to `.env` as a starting point.

---

## The Resilience Library

The proxy is powered by a standalone Python library that you can use directly in your own applications.

### Key Features

- **Async-native** with `asyncio` and `httpx`
- **Intelligent key selection** with tiered, model-aware locking
- **Deadline-driven requests** with configurable global timeout
- **Automatic failover** between keys on errors
- **OAuth support** for Gemini CLI, Antigravity, Qwen, iFlow
- **Stateless deployment ready** — load credentials from environment variables

### Basic Usage

```python
from rotator_library import RotatingClient

client = RotatingClient(
    api_keys={"gemini": ["key1", "key2"], "openai": ["key3"]},
    global_timeout=30,
    max_retries=2
)

async with client:
    response = await client.acompletion(
        model="gemini/gemini-2.5-flash",
        messages=[{"role": "user", "content": "Hello!"}]
    )
```

### Library Documentation

See the [Library README](src/rotator_library/README.md) for complete documentation including:
- All initialization parameters
- Streaming support
- Error handling and cooldown strategies
- Provider plugin system
- Credential prioritization

---

## Interactive TUI

The proxy includes a powerful text-based UI for configuration and management.

<!-- TODO: Add TUI main menu screenshot here -->

### TUI Features

- **🚀 Run Proxy** — Start the server with saved settings
- **⚙️ Configure Settings** — Host, port, API key, request logging
- **🔑 Manage Credentials** — Add/edit API keys and OAuth credentials
- **📊 View Status** — See configured providers and credential counts
- **🔧 Advanced Settings** — Custom providers, model definitions, concurrency

### Configuration Files

| File | Contents |
|------|----------|
| `.env` | All credentials and advanced settings |
| `launcher_config.json` | TUI-specific settings (host, port, logging) |

---

## Features

### Core Capabilities

- **Universal OpenAI-compatible endpoint** for all providers
- **Multi-provider support** via [LiteLLM](https://docs.litellm.ai/docs/providers) fallback
- **Automatic key rotation** and load balancing
- **Interactive TUI** for easy configuration
- **Detailed request logging** for debugging

<details>
<summary><b>🛡️ Resilience & High Availability</b></summary>

- **Global timeout** with deadline-driven retries
- **Escalating cooldowns** per model (10s → 30s → 60s → 120s)
- **Key-level lockouts** for consistently failing keys
- **Stream error detection** and graceful recovery
- **Batch embedding aggregation** for improved throughput
- **Automatic daily resets** for cooldowns and usage stats

</details>

<details>
<summary><b>🔑 Credential Management</b></summary>

- **Auto-discovery** of API keys from environment variables
- **OAuth discovery** from standard paths (`~/.gemini/`, `~/.qwen/`, `~/.iflow/`)
- **Duplicate detection** warns when same account added multiple times
- **Credential prioritization** — paid tier used before free tier
- **Stateless deployment** — export OAuth to environment variables
- **Local-first storage** — credentials isolated in `oauth_creds/` directory

</details>

<details>
<summary><b>⚙️ Advanced Configuration</b></summary>

- **Model whitelists/blacklists** with wildcard support
- **Per-provider concurrency limits** (`MAX_CONCURRENT_REQUESTS_PER_KEY_<PROVIDER>`)
- **Rotation modes** — balanced (distribute load) or sequential (use until exhausted)
- **Priority multipliers** — higher concurrency for paid credentials
- **Model quota groups** — shared cooldowns for related models
- **Temperature override** — prevent tool hallucination issues
- **Weighted random rotation** — unpredictable selection patterns

</details>

<details>
<summary><b>🔌 Provider-Specific Features</b></summary>

**Gemini CLI:**
- Zero-config Google Cloud project discovery
- Internal API access with higher rate limits
- Automatic fallback to preview models on rate limit
- Paid vs free tier detection

**Antigravity:**
- Gemini 3 Pro with `thinkingLevel` support
- Claude Opus 4.5 (thinking mode)
- Claude Sonnet 4.5 (thinking and non-thinking)
- Thought signature caching for multi-turn conversations
- Tool hallucination prevention

**Qwen Code:**
- Dual auth (API key + OAuth Device Flow)
- `<think>` tag parsing as `reasoning_content`
- Tool schema cleaning

**iFlow:**
- Dual auth (API key + OAuth Authorization Code)
- Hybrid auth with separate API key fetch
- Tool schema cleaning

**NVIDIA NIM:**
- Dynamic model discovery
- DeepSeek thinking support

</details>

<details>
<summary><b>📝 Logging & Debugging</b></summary>

- **Per-request file logging** with `--enable-request-logging`
- **Unique request directories** with full transaction details
- **Streaming chunk capture** for debugging
- **Performance metadata** (duration, tokens, model used)
- **Provider-specific logs** for Qwen, iFlow, Antigravity

</details>

---

## Advanced Configuration

<details>
<summary><b>Environment Variables Reference</b></summary>

### Proxy Settings

| Variable | Description | Default |
|----------|-------------|---------|
| `PROXY_API_KEY` | Authentication key for your proxy | Required |
| `OAUTH_REFRESH_INTERVAL` | Token refresh check interval (seconds) | `600` |
| `SKIP_OAUTH_INIT_CHECK` | Skip interactive OAuth setup on startup | `false` |

### Per-Provider Settings

| Pattern | Description | Example |
|---------|-------------|---------|
| `<PROVIDER>_API_KEY_<N>` | API key for provider | `GEMINI_API_KEY_1` |
| `MAX_CONCURRENT_REQUESTS_PER_KEY_<PROVIDER>` | Concurrent request limit | `MAX_CONCURRENT_REQUESTS_PER_KEY_OPENAI=3` |
| `ROTATION_MODE_<PROVIDER>` | `balanced` or `sequential` | `ROTATION_MODE_GEMINI=sequential` |
| `IGNORE_MODELS_<PROVIDER>` | Blacklist (comma-separated, supports `*`) | `IGNORE_MODELS_OPENAI=*-preview*` |
| `WHITELIST_MODELS_<PROVIDER>` | Whitelist (overrides blacklist) | `WHITELIST_MODELS_GEMINI=gemini-2.5-pro` |

### Advanced Features

| Variable | Description |
|----------|-------------|
| `ROTATION_TOLERANCE` | `0.0`=deterministic, `3.0`=weighted random (default) |
| `CONCURRENCY_MULTIPLIER_<PROVIDER>_PRIORITY_<N>` | Concurrency multiplier per priority tier |
| `QUOTA_GROUPS_<PROVIDER>_<GROUP>` | Models sharing quota limits |
| `OVERRIDE_TEMPERATURE_ZERO` | `remove` or `set` to prevent tool hallucination |

</details>

<details>
<summary><b>Model Filtering (Whitelists & Blacklists)</b></summary>

Control which models are exposed through your proxy.

### Blacklist Only
```env
# Hide all preview models
IGNORE_MODELS_OPENAI="*-preview*"
```

### Pure Whitelist Mode
```env
# Block all, then allow specific models
IGNORE_MODELS_GEMINI="*"
WHITELIST_MODELS_GEMINI="gemini-2.5-pro,gemini-2.5-flash"
```

### Exemption Mode
```env
# Block preview models, but allow one specific preview
IGNORE_MODELS_OPENAI="*-preview*"
WHITELIST_MODELS_OPENAI="gpt-4o-2024-08-06-preview"
```

**Logic order:** Whitelist check → Blacklist check → Default allow

</details>

<details>
<summary><b>Concurrency & Rotation Settings</b></summary>

### Concurrency Limits

```env
# Allow 3 concurrent requests per OpenAI key
MAX_CONCURRENT_REQUESTS_PER_KEY_OPENAI=3

# Default is 1 (no concurrency)
MAX_CONCURRENT_REQUESTS_PER_KEY_GEMINI=1
```

### Rotation Modes

```env
# balanced (default): Distribute load evenly - best for per-minute rate limits
ROTATION_MODE_OPENAI=balanced

# sequential: Use until exhausted - best for daily/weekly quotas
ROTATION_MODE_GEMINI=sequential
```

### Priority Multipliers

Paid credentials can handle more concurrent requests:

```env
# Priority 1 (paid ultra): 10x concurrency
CONCURRENCY_MULTIPLIER_ANTIGRAVITY_PRIORITY_1=10

# Priority 2 (standard paid): 3x
CONCURRENCY_MULTIPLIER_ANTIGRAVITY_PRIORITY_2=3
```

### Model Quota Groups

Models sharing quota limits:

```env
# Claude models share quota - when one hits limit, both cool down
QUOTA_GROUPS_ANTIGRAVITY_CLAUDE="claude-sonnet-4-5,claude-opus-4-5"
```

</details>

<details>
<summary><b>Timeout Configuration</b></summary>

Fine-grained control over HTTP timeouts:

```env
TIMEOUT_CONNECT=30              # Connection establishment
TIMEOUT_WRITE=30                # Request body send
TIMEOUT_POOL=60                 # Connection pool acquisition
TIMEOUT_READ_STREAMING=180      # Between streaming chunks (3 min)
TIMEOUT_READ_NON_STREAMING=600  # Full response wait (10 min)
```

**Recommendations:**
- Long thinking tasks: Increase `TIMEOUT_READ_STREAMING` to 300-360s
- Unstable network: Increase `TIMEOUT_CONNECT` to 60s
- Large outputs: Increase `TIMEOUT_READ_NON_STREAMING` to 900s+

</details>

---

## OAuth Providers

<details>
<summary><b>Gemini CLI</b></summary>

Uses Google OAuth to access internal Gemini endpoints with higher rate limits.

**Setup:**
1. Run `python -m rotator_library.credential_tool`
2. Select "Add OAuth Credential" → "Gemini CLI"
3. Complete browser authentication
4. Credentials saved to `oauth_creds/gemini_cli_oauth_1.json`

**Features:**
- Zero-config project discovery
- Automatic free-tier project onboarding
- Paid vs free tier detection
- Smart fallback on rate limits

**Environment Variables (for stateless deployment):**
```env
=======
### Credential Types

| Type | Providers | How to Add |
|------|-----------|------------|
| **API Keys** | Gemini, OpenAI, Anthropic, OpenRouter, Groq, Mistral, NVIDIA, Cohere, Chutes | Enter key in TUI or add to `.env` |
| **OAuth** | Gemini CLI, Antigravity, Qwen Code, iFlow | Interactive browser login via credential tool |

### The `.env` File

Credentials are stored in a `.env` file. You can edit it directly or use the TUI:

```env
# Required: Authentication key for YOUR proxy
PROXY_API_KEY="your-secret-proxy-key"

# Provider API Keys (add multiple with _1, _2, etc.)
GEMINI_API_KEY_1="your-gemini-key"
GEMINI_API_KEY_2="another-gemini-key"
OPENAI_API_KEY_1="your-openai-key"
ANTHROPIC_API_KEY_1="your-anthropic-key"
```

> Copy `.env.example` to `.env` as a starting point.

---

## The Resilience Library

The proxy is powered by a standalone Python library that you can use directly in your own applications.

### Key Features

- **Async-native** with `asyncio` and `httpx`
- **Intelligent key selection** with tiered, model-aware locking
- **Deadline-driven requests** with configurable global timeout
- **Automatic failover** between keys on errors
- **OAuth support** for Gemini CLI, Antigravity, Qwen, iFlow
- **Stateless deployment ready** — load credentials from environment variables

### Basic Usage

```python
from rotator_library import RotatingClient

client = RotatingClient(
    api_keys={"gemini": ["key1", "key2"], "openai": ["key3"]},
    global_timeout=30,
    max_retries=2
)

async with client:
    response = await client.acompletion(
        model="gemini/gemini-2.5-flash",
        messages=[{"role": "user", "content": "Hello!"}]
    )
```

### Library Documentation

See the [Library README](src/rotator_library/README.md) for complete documentation including:
- All initialization parameters
- Streaming support
- Error handling and cooldown strategies
- Provider plugin system
- Credential prioritization

---

## Interactive TUI

The proxy includes a powerful text-based UI for configuration and management.

<!-- TODO: Add TUI main menu screenshot here -->

### TUI Features

- **🚀 Run Proxy** — Start the server with saved settings
- **⚙️ Configure Settings** — Host, port, API key, request logging
- **🔑 Manage Credentials** — Add/edit API keys and OAuth credentials
- **📊 View Status** — See configured providers and credential counts
- **🔧 Advanced Settings** — Custom providers, model definitions, concurrency

### Configuration Files

| File | Contents |
|------|----------|
| `.env` | All credentials and advanced settings |
| `launcher_config.json` | TUI-specific settings (host, port, logging) |

---

## Features

### Core Capabilities

- **Universal OpenAI-compatible endpoint** for all providers
- **Multi-provider support** via [LiteLLM](https://docs.litellm.ai/docs/providers) fallback
- **Automatic key rotation** and load balancing
- **Interactive TUI** for easy configuration
- **Detailed request logging** for debugging

<details>
<summary><b>🛡️ Resilience & High Availability</b></summary>

- **Global timeout** with deadline-driven retries
- **Escalating cooldowns** per model (10s → 30s → 60s → 120s)
- **Key-level lockouts** for consistently failing keys
- **Stream error detection** and graceful recovery
- **Batch embedding aggregation** for improved throughput
- **Automatic daily resets** for cooldowns and usage stats

</details>

<details>
<summary><b>🔑 Credential Management</b></summary>

- **Auto-discovery** of API keys from environment variables
- **OAuth discovery** from standard paths (`~/.gemini/`, `~/.qwen/`, `~/.iflow/`)
- **Duplicate detection** warns when same account added multiple times
- **Credential prioritization** — paid tier used before free tier
- **Stateless deployment** — export OAuth to environment variables
- **Local-first storage** — credentials isolated in `oauth_creds/` directory

</details>

<details>
<summary><b>⚙️ Advanced Configuration</b></summary>

- **Model whitelists/blacklists** with wildcard support
- **Per-provider concurrency limits** (`MAX_CONCURRENT_REQUESTS_PER_KEY_<PROVIDER>`)
- **Rotation modes** — balanced (distribute load) or sequential (use until exhausted)
- **Priority multipliers** — higher concurrency for paid credentials
- **Model quota groups** — shared cooldowns for related models
- **Temperature override** — prevent tool hallucination issues
- **Weighted random rotation** — unpredictable selection patterns

</details>

<details>
<summary><b>🔌 Provider-Specific Features</b></summary>

**Gemini CLI:**
- Zero-config Google Cloud project discovery
- Internal API access with higher rate limits
- Automatic fallback to preview models on rate limit
- Paid vs free tier detection

**Antigravity:**
- Gemini 3 Pro with `thinkingLevel` support
- Claude Opus 4.5 (thinking mode)
- Claude Sonnet 4.5 (thinking and non-thinking)
- Thought signature caching for multi-turn conversations
- Tool hallucination prevention

**Qwen Code:**
- Dual auth (API key + OAuth Device Flow)
- `<think>` tag parsing as `reasoning_content`
- Tool schema cleaning

**iFlow:**
- Dual auth (API key + OAuth Authorization Code)
- Hybrid auth with separate API key fetch
- Tool schema cleaning

**NVIDIA NIM:**
- Dynamic model discovery
- DeepSeek thinking support

</details>

<details>
<summary><b>📝 Logging & Debugging</b></summary>

- **Per-request file logging** with `--enable-request-logging`
- **Unique request directories** with full transaction details
- **Streaming chunk capture** for debugging
- **Performance metadata** (duration, tokens, model used)
- **Provider-specific logs** for Qwen, iFlow, Antigravity

</details>

---

## Advanced Configuration

<details>
<summary><b>Environment Variables Reference</b></summary>

### Proxy Settings

| Variable | Description | Default |
|----------|-------------|---------|
| `PROXY_API_KEY` | Authentication key for your proxy | Required |
| `OAUTH_REFRESH_INTERVAL` | Token refresh check interval (seconds) | `600` |
| `SKIP_OAUTH_INIT_CHECK` | Skip interactive OAuth setup on startup | `false` |

### Per-Provider Settings

| Pattern | Description | Example |
|---------|-------------|---------|
| `<PROVIDER>_API_KEY_<N>` | API key for provider | `GEMINI_API_KEY_1` |
| `MAX_CONCURRENT_REQUESTS_PER_KEY_<PROVIDER>` | Concurrent request limit | `MAX_CONCURRENT_REQUESTS_PER_KEY_OPENAI=3` |
| `ROTATION_MODE_<PROVIDER>` | `balanced` or `sequential` | `ROTATION_MODE_GEMINI=sequential` |
| `IGNORE_MODELS_<PROVIDER>` | Blacklist (comma-separated, supports `*`) | `IGNORE_MODELS_OPENAI=*-preview*` |
| `WHITELIST_MODELS_<PROVIDER>` | Whitelist (overrides blacklist) | `WHITELIST_MODELS_GEMINI=gemini-2.5-pro` |

### Advanced Features

| Variable | Description |
|----------|-------------|
| `ROTATION_TOLERANCE` | `0.0`=deterministic, `3.0`=weighted random (default) |
| `CONCURRENCY_MULTIPLIER_<PROVIDER>_PRIORITY_<N>` | Concurrency multiplier per priority tier |
| `QUOTA_GROUPS_<PROVIDER>_<GROUP>` | Models sharing quota limits |
| `OVERRIDE_TEMPERATURE_ZERO` | `remove` or `set` to prevent tool hallucination |

</details>

<details>
<summary><b>Model Filtering (Whitelists & Blacklists)</b></summary>

Control which models are exposed through your proxy.

### Blacklist Only
```env
# Hide all preview models
IGNORE_MODELS_OPENAI="*-preview*"
```

### Pure Whitelist Mode
```env
# Block all, then allow specific models
IGNORE_MODELS_GEMINI="*"
WHITELIST_MODELS_GEMINI="gemini-2.5-pro,gemini-2.5-flash"
```

### Exemption Mode
```env
# Block preview models, but allow one specific preview
IGNORE_MODELS_OPENAI="*-preview*"
WHITELIST_MODELS_OPENAI="gpt-4o-2024-08-06-preview"
```

**Logic order:** Whitelist check → Blacklist check → Default allow

</details>

<details>
<summary><b>Concurrency & Rotation Settings</b></summary>

### Concurrency Limits

```env
# Allow 3 concurrent requests per OpenAI key
MAX_CONCURRENT_REQUESTS_PER_KEY_OPENAI=3

# Default is 1 (no concurrency)
MAX_CONCURRENT_REQUESTS_PER_KEY_GEMINI=1
```

### Rotation Modes

```env
# balanced (default): Distribute load evenly - best for per-minute rate limits
ROTATION_MODE_OPENAI=balanced

# sequential: Use until exhausted - best for daily/weekly quotas
ROTATION_MODE_GEMINI=sequential
```

### Priority Multipliers

Paid credentials can handle more concurrent requests:

```env
# Priority 1 (paid ultra): 10x concurrency
CONCURRENCY_MULTIPLIER_ANTIGRAVITY_PRIORITY_1=10

# Priority 2 (standard paid): 3x
CONCURRENCY_MULTIPLIER_ANTIGRAVITY_PRIORITY_2=3
```

### Model Quota Groups

Models sharing quota limits:

```env
# Claude models share quota - when one hits limit, both cool down
QUOTA_GROUPS_ANTIGRAVITY_CLAUDE="claude-sonnet-4-5,claude-opus-4-5"
```

</details>

<details>
<summary><b>Timeout Configuration</b></summary>

Fine-grained control over HTTP timeouts:

```env
TIMEOUT_CONNECT=30              # Connection establishment
TIMEOUT_WRITE=30                # Request body send
TIMEOUT_POOL=60                 # Connection pool acquisition
TIMEOUT_READ_STREAMING=180      # Between streaming chunks (3 min)
TIMEOUT_READ_NON_STREAMING=600  # Full response wait (10 min)
```

**Recommendations:**
- Long thinking tasks: Increase `TIMEOUT_READ_STREAMING` to 300-360s
- Unstable network: Increase `TIMEOUT_CONNECT` to 60s
- Large outputs: Increase `TIMEOUT_READ_NON_STREAMING` to 900s+

</details>

---

## OAuth Providers

<details>
<summary><b>Gemini CLI</b></summary>

Uses Google OAuth to access internal Gemini endpoints with higher rate limits.

**Setup:**
1. Run `python -m rotator_library.credential_tool`
2. Select "Add OAuth Credential" → "Gemini CLI"
3. Complete browser authentication
4. Credentials saved to `oauth_creds/gemini_cli_oauth_1.json`

**Features:**
- Zero-config project discovery
- Automatic free-tier project onboarding
- Paid vs free tier detection
- Smart fallback on rate limits

**Environment Variables (for stateless deployment):**
```env
>>>>>>> origin/main
GEMINI_CLI_ACCESS_TOKEN="ya29.your-access-token"
GEMINI_CLI_REFRESH_TOKEN="1//your-refresh-token"
GEMINI_CLI_EXPIRY_DATE="1234567890000"
GEMINI_CLI_EMAIL="your-email@gmail.com"
<<<<<<< HEAD
# Optional: GEMINI_CLI_PROJECT_ID, GEMINI_CLI_CLIENT_ID, etc.
# See IMPLEMENTATION_SUMMARY.md for full list of supported variables

# --- Dual Authentication Support ---
# Some providers (qwen_code, iflow) support BOTH OAuth and direct API keys.
# You can use either method, or mix both for credential rotation:
QWEN_CODE_API_KEY_1="your-qwen-api-key"  # Direct API key
# AND/OR use OAuth: oauth_creds/qwen_code_oauth_1.json
IFLOW_API_KEY_1="sk-your-iflow-key"      # Direct API key
# AND/OR use OAuth: oauth_creds/iflow_oauth_1.json
```

### 4. Run the Proxy

You can run the proxy in two ways:

**A) Using the Compiled Executable (Recommended)**

A pre-compiled, standalone executable for Windows is available on the [latest GitHub Release](https://github.com/Mirrowel/LLM-API-Key-Proxy/releases/latest). This is the easiest way to get started as it requires no setup.

For the simplest experience, follow the **Quick Start** guide at the top of this document.

**B) Running from Source**

Start the server by running the `main.py` script

```bash
python src/proxy_app/main.py
```
This launches the interactive TUI launcher by default. To run the proxy directly, use:

```bash
python src/proxy_app/main.py --host 0.0.0.0 --port 8000
```

The proxy is now running and available at `http://127.0.0.1:8000`.

### 5. Make a Request

You can now send requests to the proxy. The endpoint is `http://127.0.0.1:8000/v1/chat/completions`.

Remember to:
1.  Set the `Authorization` header to `Bearer your-super-secret-proxy-key`.
2.  Specify the `model` in the format `provider/model_name`.

Here is an example using `curl`:
```bash
curl -X POST http://127.0.0.1:8000/v1/chat/completions \
-H "Content-Type: application/json" \
-H "Authorization: Bearer your-super-secret-proxy-key" \
-d '{
    "model": "gemini/gemini-2.5-flash",
    "messages": [{"role": "user", "content": "What is the capital of France?"}]
}'
```

---

## Advanced Usage

### Using with the OpenAI Python Library (Recommended)

The proxy is OpenAI-compatible, so you can use it directly with the `openai` Python client.

```python
import openai

# Point the client to your local proxy
client = openai.OpenAI(
    base_url="http://127.0.0.1:8000/v1",
    api_key="a-very-secret-and-unique-key" # Use your PROXY_API_KEY here
)

# Make a request
response = client.chat.completions.create(
    model="gemini/gemini-2.5-flash", # Specify provider and model
    messages=[
        {"role": "user", "content": "Write a short poem about space."}
    ]
)

print(response.choices[0].message.content)
```

### Using with `curl`

```bash
You can also send requests directly using tools like `curl`.

```bash
curl -X POST http://127.0.0.1:8000/v1/chat/completions \
-H "Content-Type: application/json" \
-H "Authorization: Bearer a-very-secret-and-unique-key" \
-d '{
    "model": "gemini/gemini-2.5-flash",
    "messages": [{"role": "user", "content": "What is the capital of France?"}]
}'
```

### Available API Endpoints

-   `POST /v1/chat/completions`: The main endpoint for making chat requests.
-   `POST /v1/embeddings`: The endpoint for creating embeddings.
-   `GET /v1/models`: Returns a list of all available models from your configured providers.
-   `GET /v1/providers`: Returns a list of all configured providers.
-   `POST /v1/token-count`: Calculates the token count for a given message payload.

---

## 4. Advanced Topics

### Batch Request Processing

The proxy includes a `Batch Manager` that optimizes high-volume embedding requests.
- **Automatic Aggregation**: Multiple individual embedding requests are automatically collected into a single batch API call.
- **Configurable**: Works out of the box, but can be tuned for specific needs.
- **Benefits**: Significantly reduces the number of HTTP requests to providers, helping you stay within rate limits while improving throughput.

### How It Works

The proxy is built on a robust architecture:

1.  **Intelligent Routing**: The `UsageManager` selects the best available key from your pool. It prioritizes idle keys first, then keys that can handle concurrency, ensuring optimal load balancing.
2.  **Resilience & Deadlines**: Every request has a strict deadline (`global_timeout`). If a provider is slow or fails, the proxy retries with a different key immediately, ensuring your application never hangs.
3.  **Batching**: High-volume embedding requests are automatically aggregated into optimized batches, reducing API calls and staying within rate limits.
4.  **Deep Observability**: (Optional) Detailed logs capture every byte of the transaction, including raw streaming chunks, for precise debugging of complex agentic interactions.

### Command-Line Arguments and Scripts

The proxy server can be configured at runtime using the following command-line arguments:

-   `--host`: The IP address to bind the server to. Defaults to `0.0.0.0` (accessible from your local network).
-   `--port`: The port to run the server on. Defaults to `8000`.
-   `--enable-request-logging`: A flag to enable detailed, per-request logging. When active, the proxy creates a unique directory for each transaction in the `logs/detailed_logs/` folder, containing the full request, response, streaming chunks, and performance metadata. This is highly recommended for debugging.

### New Provider Highlights

#### **Gemini CLI (Advanced)**
A powerful provider that mimics the Google Cloud Code extension.
-   **Zero-Config Project Discovery**: Automatically finds your Google Cloud Project ID or onboards you to a free-tier project if none exists.
-   **Internal API Access**: Uses high-limit internal endpoints (`cloudcode-pa.googleapis.com`) rather than the public Vertex AI API.
-   **Smart Rate Limiting**: Automatically falls back to preview models (e.g., `gemini-2.5-pro-preview`) if the main model hits a rate limit.

#### **Qwen Code**
-   **Dual Authentication**: Use either standard API keys or OAuth 2.0 Device Flow credentials.
-   **Schema Cleaning**: Automatically removes `strict` and `additionalProperties` from tool schemas to prevent API errors.
-   **Stream Stability**: Injects a dummy `do_not_call_me` tool to prevent stream corruption issues when no tools are provided.
-   **Reasoning Support**: Parses `<think>` tags in responses and exposes them as `reasoning_content` (similar to OpenAI's o1 format).
-   **Dedicated Logging**: Optional per-request file logging to `logs/qwen_code_logs/` for debugging.
-   **Custom Models**: Define additional models via `QWEN_CODE_MODELS` environment variable (JSON array format).

#### **iFlow**
-   **Dual Authentication**: Use either standard API keys or OAuth 2.0 Authorization Code Flow.
-   **Hybrid Auth**: OAuth flow provides an access token, but actual API calls use a separate `apiKey` retrieved from user profile.
-   **Local Callback Server**: OAuth flow runs a temporary server on port 11451 to capture the redirect.
-   **Schema Cleaning**: Same as Qwen Code - removes unsupported properties from tool schemas.
-   **Stream Stability**: Injects placeholder tools to stabilize streaming for empty tool lists.
-   **Dedicated Logging**: Optional per-request file logging to `logs/iflow_logs/` for debugging proprietary API behaviors.
-   **Custom Models**: Define additional models via `IFLOW_MODELS` environment variable (JSON array format).


### Advanced Configuration

The following advanced settings can be added to your `.env` file (or configured interactively via the TUI Settings Tool):

#### OAuth and Refresh Settings

-   **`OAUTH_REFRESH_INTERVAL`**: Controls how often (in seconds) the background refresher checks for expired OAuth tokens. Default is `600` (10 minutes).
    ```env
    OAUTH_REFRESH_INTERVAL=600  # Check every 10 minutes
    ```

-   **`SKIP_OAUTH_INIT_CHECK`**: Set to `true` to skip the interactive OAuth setup/validation check on startup. Essential for non-interactive environments like Docker containers or CI/CD pipelines.
    ```env
    SKIP_OAUTH_INIT_CHECK=true


#### **Antigravity (Advanced - Gemini 3 \ Claude Opus 4.5 / Sonnet 4.5 Access)**
The newest and most sophisticated provider, offering access to cutting-edge models via Google's internal Antigravity API.

**Supported Models:**
-   Gemini 2.5 (Pro/Flash) with `thinkingBudget` parameter
-   **Gemini 3 Pro (High/Low)** - Latest preview models
-   **🆕 Claude Opus 4.5 + Thinking** - Anthropic's most powerful model via Antigravity proxy
-   **Claude Sonnet 4.5 + Thinking** via Antigravity proxy

**Advanced Features:**
-   **Thought Signature Caching**: Preserves encrypted signatures for multi-turn Gemini 3 conversations
-   **Tool Hallucination Prevention**: Automatic system instruction and parameter signature injection for Gemini 3 to prevent tools from being called with incorrect parameters
-   **Thinking Preservation**: Caches Claude thinking content for consistency across conversation turns
-   **Automatic Fallback**: Tries sandbox endpoints before falling back to production
-   **Schema Cleaning**: Handles Claude-specific tool schema requirements

**Configuration:**
-   **OAuth Setup**: Uses Google OAuth similar to Gemini CLI (separate scopes)
-   **Stateless Deployment**: Full environment variable support
-   **Paid Tier Recommended**: Gemini 3 models require a paid Google Cloud project

**Environment Variables:**
```env
# Stateless deployment
ANTIGRAVITY_ACCESS_TOKEN="..."
ANTIGRAVITY_REFRESH_TOKEN="..."
ANTIGRAVITY_EXPIRY_DATE="..."
ANTIGRAVITY_EMAIL="user@gmail.com"

# Feature toggles
ANTIGRAVITY_ENABLE_SIGNATURE_CACHE=true  # Multi-turn conversation support
ANTIGRAVITY_GEMINI3_TOOL_FIX=true  # Prevent tool hallucination
```


    ```

#### Credential Rotation Modes

-   **`ROTATION_MODE_<PROVIDER>`**: Controls how credentials are rotated when multiple are available. Default: `balanced` (except Antigravity which defaults to `sequential`).
    - `balanced`: Rotate credentials evenly across requests to distribute load. Best for per-minute rate limits.
    - `sequential`: Use one credential until exhausted (429 error), then switch to next. Best for daily/weekly quotas.
    ```env
    ROTATION_MODE_GEMINI=sequential    # Use Gemini keys until quota exhausted
    ROTATION_MODE_OPENAI=balanced      # Distribute load across OpenAI keys (default)
    ROTATION_MODE_ANTIGRAVITY=balanced # Override Antigravity's sequential default
    ```

#### Priority-Based Concurrency Multipliers

-   **`CONCURRENCY_MULTIPLIER_<PROVIDER>_PRIORITY_<N>`**: Assign concurrency multipliers to priority tiers. Higher-tier credentials handle more concurrent requests.
    ```env
    # Universal multipliers (apply to all rotation modes)
    CONCURRENCY_MULTIPLIER_ANTIGRAVITY_PRIORITY_1=10   # 10x for paid ultra tier
    CONCURRENCY_MULTIPLIER_ANTIGRAVITY_PRIORITY_3=1    # 1x for lower tiers
    
    # Mode-specific overrides
    CONCURRENCY_MULTIPLIER_ANTIGRAVITY_PRIORITY_2_BALANCED=1  # P2 = 1x in balanced mode only
    ```
    
    **Provider Defaults** (built into provider classes):
    - **Antigravity**: Priority 1: 5x, Priority 2: 3x, Priority 3+: 2x (sequential) or 1x (balanced)
    - **Gemini CLI**: Priority 1: 5x, Priority 2: 3x, Others: 1x

#### Model Quota Groups

-   **`QUOTA_GROUPS_<PROVIDER>_<GROUP>`**: Define models that share quota/cooldown timing. When one model hits quota, all in the group receive the same cooldown timestamp.
    ```env
    QUOTA_GROUPS_ANTIGRAVITY_CLAUDE="claude-sonnet-4-5,claude-opus-4-5"
    QUOTA_GROUPS_ANTIGRAVITY_GEMINI="gemini-3-pro-preview,gemini-3-pro-image-preview"
    
    # To disable a default group:
    QUOTA_GROUPS_ANTIGRAVITY_CLAUDE=""
    ```
    
    **Default Groups**:
    - **Antigravity**: Claude group (Sonnet 4.5 + Opus 4.5) with Opus counting 2x vs Sonnet

#### Concurrency Control

-   **`MAX_CONCURRENT_REQUESTS_PER_KEY_<PROVIDER>`**: Set the maximum number of simultaneous requests allowed per API key for a specific provider. Default is `1` (no concurrency). Useful for high-throughput providers.
    ```env
    MAX_CONCURRENT_REQUESTS_PER_KEY_OPENAI=3
    MAX_CONCURRENT_REQUESTS_PER_KEY_ANTHROPIC=2
    MAX_CONCURRENT_REQUESTS_PER_KEY_GEMINI=1
    ```

#### Custom Model Lists

For providers that support custom model definitions (Qwen Code, iFlow), you can override the default model list:

-   **`QWEN_CODE_MODELS`**: JSON array of custom Qwen Code models. These models take priority over hardcoded defaults.
    ```env
    QWEN_CODE_MODELS='["qwen3-coder-plus", "qwen3-coder-flash", "custom-model-id"]'
    ```

-   **`IFLOW_MODELS`**: JSON array of custom iFlow models. These models take priority over hardcoded defaults.
    ```env
    IFLOW_MODELS='["glm-4.6", "qwen3-coder-plus", "deepseek-v3.2"]'
    ```

#### Provider-Specific Settings

-   **`GEMINI_CLI_PROJECT_ID`**: Manually specify a Google Cloud Project ID for Gemini CLI OAuth. Only needed if automatic discovery fails.


#### Antigravity Provider

-   **`ANTIGRAVITY_OAUTH_1`**: Path to Antigravity OAuth credential file (auto-discovered from `~/.antigravity/` or use the credential tool).
    ```env
    ANTIGRAVITY_OAUTH_1="/path/to/your/antigravity_creds.json"
    ```

-   **Stateless Deployment** (Environment Variables):
    ```env
    ANTIGRAVITY_ACCESS_TOKEN="ya29.your-access-token"


#### Credential Rotation Strategy

-   **`ROTATION_TOLERANCE`**: Controls how credentials are selected for requests. Set via environment variable or programmatically.
    - `0.0`: **Deterministic** - Always selects the least-used credential for perfect load balance
    - `3.0` (default, recommended): **Weighted Random** - Randomly selects with bias toward less-used credentials. Provides unpredictability (harder to fingerprint/detect) while maintaining good balance
    - `5.0+`: **High Randomness** - Maximum unpredictability, even heavily-used credentials can be selected
    
    ```env
    # For maximum security/unpredictability (recommended for production)
    ROTATION_TOLERANCE=3.0
    
    # For perfect load balancing (default)
    ROTATION_TOLERANCE=0.0
    ```
    
    **Why use weighted random?**
    - Makes traffic patterns less predictable
    - Still maintains good load distribution across keys
    - Recommended for production environments with multiple credentials


    ANTIGRAVITY_REFRESH_TOKEN="1//your-refresh-token"
    ANTIGRAVITY_EXPIRY_DATE="1234567890000"
    ANTIGRAVITY_EMAIL="your-email@gmail.com"
    ```

-   **`ANTIGRAVITY_ENABLE_SIGNATURE_CACHE`**: Enable/disable thought signature caching for Gemini 3 multi-turn conversations. Default: `true`.
    ```env
    ANTIGRAVITY_ENABLE_SIGNATURE_CACHE=true
    ```

-   **`ANTIGRAVITY_GEMINI3_TOOL_FIX`**: Enable/disable tool hallucination prevention for Gemini 3 models. Default: `true`.
    ```env
    ANTIGRAVITY_GEMINI3_TOOL_FIX=true
    ```

#### Temperature Override (Global)

-   **`OVERRIDE_TEMPERATURE_ZERO`**: Prevents tool hallucination caused by temperature=0 settings. Modes:
    - `"remove"`: Deletes temperature=0 from requests (lets provider use default)
    - `"set"`: Changes temperature=0 to temperature=1.0
    - `"false"` or unset: Disabled (default)

#### Credential Prioritization

-   **`GEMINI_CLI_PROJECT_ID`**: Manually specify a Google Cloud Project ID for Gemini CLI OAuth. Auto-discovered unless unexpected failure occurs.
    ```env
    GEMINI_CLI_PROJECT_ID="your-gcp-project-id"
    ```


    ```env
    GEMINI_CLI_PROJECT_ID="your-gcp-project-id"
    ```

**Example:**
```bash
python src/proxy_app/main.py --host 127.0.0.1 --port 9999 --enable-request-logging
```


#### Windows Batch Scripts

For convenience on Windows, you can use the provided `.bat` scripts in the root directory:

-   **`launcher.bat`** *(deprecated)*: Legacy launcher with manual menu system. Still functional but superseded by the new TUI.

### Troubleshooting

-   **`401 Unauthorized`**: Ensure your `PROXY_API_KEY` is set correctly in the `.env` file and included in the `Authorization: Bearer <key>` header of your request.
-   **`500 Internal Server Error`**: Check the console logs of the `uvicorn` server for detailed error messages. This could indicate an issue with one of your provider API keys (e.g., it's invalid or has been revoked) or a problem with the provider's service. If you have logging enabled (`--enable-request-logging`), inspect the `final_response.json` and `metadata.json` files in the corresponding log directory under `logs/detailed_logs/` for the specific error returned by the upstream provider.
-   **All keys on cooldown**: If you see a message that all keys are on cooldown, it means all your keys for a specific provider have recently failed. If you have logging enabled (`--enable-request-logging`), check the `logs/detailed_logs/` directory to find the logs for the failed requests and inspect the `final_response.json` to see the underlying error from the provider.

---

## Library and Technical Docs

-   **Using the Library**: For documentation on how to use the `api-key-manager` library directly in your own Python projects, please refer to its [README.md](src/rotator_library/README.md).
-   **Technical Details**: For a more in-depth technical explanation of the library's architecture, components, and internal workings, please refer to the [Technical Documentation](DOCUMENTATION.md).

### Advanced Model Filtering (Whitelists & Blacklists)

The proxy provides a powerful way to control which models are available to your applications using environment variables in your `.env` file.

#### How It Works

The filtering logic is applied in this order:

1.  **Whitelist Check**: If a provider has a whitelist defined (`WHITELIST_MODELS_<PROVIDER>`), any model on that list will **always be available**, even if it's on the blacklist.
2.  **Blacklist Check**: For any model *not* on the whitelist, the proxy checks the blacklist (`IGNORE_MODELS_<PROVIDER>`). If the model is on the blacklist, it will be hidden.
3.  **Default**: If a model is on neither list, it will be available.

This allows for two powerful patterns:

#### Use Case 1: Pure Whitelist Mode

You can expose *only* the specific models you want. To do this, set the blacklist to `*` to block all models by default, and then add the desired models to the whitelist.

**Example `.env`:**
```env
# Block all Gemini models by default
IGNORE_MODELS_GEMINI="*"

# Only allow gemini-1.5-pro and gemini-1.5-flash
WHITELIST_MODELS_GEMINI="gemini-1.5-pro-latest,gemini-1.5-flash-latest"
```

#### Use Case 2: Exemption Mode

You can block a broad category of models and then use the whitelist to make specific exceptions.

**Example `.env`:**
```env
# Block all preview models from OpenAI
IGNORE_MODELS_OPENAI="*-preview*"

# But make an exception for a specific preview model you want to test
WHITELIST_MODELS_OPENAI="gpt-4o-2024-08-06-preview"
```
=======
GEMINI_CLI_PROJECT_ID="your-gcp-project-id"  # Optional
```

</details>

<details>
<summary><b>Antigravity (Gemini 3 + Claude Opus 4.5)</b></summary>

Access Google's internal Antigravity API for cutting-edge models.

**Supported Models:**
- **Gemini 3 Pro** — with `thinkingLevel` support (low/high)
- **Claude Opus 4.5** — Anthropic's most powerful model (thinking mode only)
- **Claude Sonnet 4.5** — supports both thinking and non-thinking modes
- Gemini 2.5 Pro/Flash

**Setup:**
1. Run `python -m rotator_library.credential_tool`
2. Select "Add OAuth Credential" → "Antigravity"
3. Complete browser authentication

**Advanced Features:**
- Thought signature caching for multi-turn conversations
- Tool hallucination prevention via parameter signature injection
- Automatic thinking block sanitization for Claude
- Credential prioritization (paid resets every 5 hours, free weekly)

**Environment Variables:**
```env
ANTIGRAVITY_ACCESS_TOKEN="ya29.your-access-token"
ANTIGRAVITY_REFRESH_TOKEN="1//your-refresh-token"
ANTIGRAVITY_EXPIRY_DATE="1234567890000"
ANTIGRAVITY_EMAIL="your-email@gmail.com"

# Feature toggles
ANTIGRAVITY_ENABLE_SIGNATURE_CACHE=true
ANTIGRAVITY_GEMINI3_TOOL_FIX=true
```

> **Note:** Gemini 3 models require a paid-tier Google Cloud project.

</details>

<details>
<summary><b>Qwen Code</b></summary>

Uses OAuth Device Flow for Qwen/Dashscope APIs.

**Setup:**
1. Run the credential tool
2. Select "Add OAuth Credential" → "Qwen Code"
3. Enter the code displayed in your browser
4. Or add API key directly: `QWEN_CODE_API_KEY_1="your-key"`

**Features:**
- Dual auth (API key or OAuth)
- `<think>` tag parsing as `reasoning_content`
- Automatic tool schema cleaning
- Custom models via `QWEN_CODE_MODELS` env var

</details>

<details>
<summary><b>iFlow</b></summary>

Uses OAuth Authorization Code flow with local callback server.

**Setup:**
1. Run the credential tool
2. Select "Add OAuth Credential" → "iFlow"
3. Complete browser authentication (callback on port 11451)
4. Or add API key directly: `IFLOW_API_KEY_1="sk-your-key"`

**Features:**
- Dual auth (API key or OAuth)
- Hybrid auth (OAuth token fetches separate API key)
- Automatic tool schema cleaning
- Custom models via `IFLOW_MODELS` env var

</details>

<details>
<summary><b>Stateless Deployment (Export to Environment Variables)</b></summary>

For platforms without file persistence (Railway, Render, Vercel):

1. **Set up credentials locally:**
   ```bash
   python -m rotator_library.credential_tool
   # Complete OAuth flows
   ```

2. **Export to environment variables:**
   ```bash
   python -m rotator_library.credential_tool
   # Select "Export [Provider] to .env"
   ```

3. **Copy generated variables to your platform:**
   The tool creates files like `gemini_cli_credential_1.env` containing all necessary variables.

4. **Set `SKIP_OAUTH_INIT_CHECK=true`** to skip interactive validation on startup.

</details>

<details>
<summary><b>OAuth Callback Port Configuration</b></summary>

Customize OAuth callback ports if defaults conflict:

| Provider | Default Port | Environment Variable |
|----------|-------------|---------------------|
| Gemini CLI | 8085 | `GEMINI_CLI_OAUTH_PORT` |
| Antigravity | 51121 | `ANTIGRAVITY_OAUTH_PORT` |
| iFlow | 11451 | `IFLOW_OAUTH_PORT` |

</details>

---

## Deployment

<details>
<summary><b>Command-Line Arguments</b></summary>

```bash
python src/proxy_app/main.py [OPTIONS]

Options:
  --host TEXT                Host to bind (default: 0.0.0.0)
  --port INTEGER             Port to run on (default: 8000)
  --enable-request-logging   Enable detailed per-request logging
  --add-credential           Launch interactive credential setup tool
```

**Examples:**
```bash
# Run on custom port
python src/proxy_app/main.py --host 127.0.0.1 --port 9000

# Run with logging
python src/proxy_app/main.py --enable-request-logging

# Add credentials without starting proxy
python src/proxy_app/main.py --add-credential
```

</details>

<details>
<summary><b>Render / Railway / Vercel</b></summary>

See the [Deployment Guide](Deployment%20guide.md) for complete instructions.

**Quick Setup:**
1. Fork the repository
2. Create a `.env` file with your credentials
3. Create a new Web Service pointing to your repo
4. Set build command: `pip install -r requirements.txt`
5. Set start command: `uvicorn src.proxy_app.main:app --host 0.0.0.0 --port $PORT`
6. Upload `.env` as a secret file

**OAuth Credentials:**
Export OAuth credentials to environment variables using the credential tool, then add them to your platform's environment settings.

</details>

<details>
<summary><b>Custom VPS / Docker</b></summary>

**Option 1: Authenticate locally, deploy credentials**
1. Complete OAuth flows on your local machine
2. Export to environment variables
3. Deploy `.env` to your server

**Option 2: SSH Port Forwarding**
```bash
# Forward callback ports through SSH
ssh -L 51121:localhost:51121 -L 8085:localhost:8085 user@your-vps

# Then run credential tool on the VPS
```

**Systemd Service:**
```ini
[Unit]
Description=LLM API Key Proxy
After=network.target

[Service]
Type=simple
WorkingDirectory=/path/to/LLM-API-Key-Proxy
ExecStart=/path/to/python -m uvicorn src.proxy_app.main:app --host 0.0.0.0 --port 8000
Restart=always

[Install]
WantedBy=multi-user.target
```

See [VPS Deployment](Deployment%20guide.md#appendix-deploying-to-a-custom-vps) for complete guide.

</details>

---

## Troubleshooting

| Issue | Solution |
|-------|----------|
| `401 Unauthorized` | Verify `PROXY_API_KEY` matches your `Authorization: Bearer` header exactly |
| `500 Internal Server Error` | Check provider key validity; enable `--enable-request-logging` for details |
| All keys on cooldown | All keys failed recently; check `logs/detailed_logs/` for upstream errors |
| Model not found | Verify format is `provider/model_name` (e.g., `gemini/gemini-2.5-flash`) |
| OAuth callback failed | Ensure callback port (8085, 51121, 11451) isn't blocked by firewall |
| Streaming hangs | Increase `TIMEOUT_READ_STREAMING`; check provider status |

**Detailed Logs:**

When `--enable-request-logging` is enabled, check `logs/detailed_logs/` for:
- `request.json` — Exact request payload
- `final_response.json` — Complete response or error
- `streaming_chunks.jsonl` — All SSE chunks received
- `metadata.json` — Performance metrics

---

## Documentation

| Document | Description |
|----------|-------------|
| [Technical Documentation](DOCUMENTATION.md) | Architecture, internals, provider implementations |
| [Library README](src/rotator_library/README.md) | Using the resilience library directly |
| [Deployment Guide](Deployment%20guide.md) | Hosting on Render, Railway, VPS |
| [.env.example](.env.example) | Complete environment variable reference |

---

## License

This project is dual-licensed:
- **Proxy Application** (`src/proxy_app/`) — [MIT License](src/proxy_app/LICENSE)
- **Resilience Library** (`src/rotator_library/`) — [LGPL-3.0](src/rotator_library/COPYING.LESSER)
>>>>>>> origin/main
