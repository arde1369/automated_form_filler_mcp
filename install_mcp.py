"""Installer for the Word Form MCP server.

This script:
1. Verifies that Claude Desktop config exists in the default OS location.
2. Installs required Python packages for this MCP server.
3. Prompts for Outlook credentials and writes them to a local .env file.
4. Adds or updates the MCP server entry in claude_desktop_config.json.

Run:
    python install_mcp.py
"""

from __future__ import annotations

import getpass
import json
import os
import platform
import subprocess
import sys
from pathlib import Path

MCP_SERVER_NAME = "automated-form-filler-mcp"
REQUIRED_ENV_KEYS = ("O365_EMAIL", "O365_PASSWORD")


def install_dependencies(project_dir: Path) -> None:
    """Install required packages from requirements.txt using this Python interpreter."""
    requirements_path = project_dir / "requirements.txt"
    if not requirements_path.exists():
        raise FileNotFoundError(f"requirements.txt not found: {requirements_path}")

    print(f"Installing dependencies from: {requirements_path}")
    command = [
        sys.executable,
        "-m",
        "pip",
        "install",
        "-r",
        str(requirements_path),
    ]

    result = subprocess.run(command, capture_output=True, text=True)
    if result.returncode != 0:
        stderr = (result.stderr or "").strip()
        stdout = (result.stdout or "").strip()
        details = stderr or stdout or "No additional output from pip."
        raise RuntimeError(f"Dependency installation failed. pip output: {details}")

    print("Dependencies installed successfully.")


def get_default_claude_config_path() -> Path:
    """Return the default Claude Desktop config path based on the current OS."""
    system = platform.system().lower()

    if "windows" in system:
        appdata = os.environ.get("APPDATA")
        if not appdata:
            raise RuntimeError("APPDATA is not set. Cannot locate Claude Desktop config path.")
        return Path(appdata) / "Claude" / "claude_desktop_config.json"

    if "darwin" in system:
        return Path.home() / "Library" / "Application Support" / "Claude" / "claude_desktop_config.json"

    # Common Linux location
    return Path.home() / ".config" / "Claude" / "claude_desktop_config.json"


def prompt_for_credentials() -> dict[str, str]:
    """Prompt user for Outlook credentials."""
    print("Enter Outlook / Office 365 credentials:")
    username = input("O365 email: ").strip()
    password = getpass.getpass("O365 password (or app password): ").strip()

    if not username:
        raise ValueError("O365 email is required.")
    if "@" not in username:
        raise ValueError("O365 email must be a valid email address.")
    if not password:
        raise ValueError("O365 password is required.")

    return {
        "O365_EMAIL": username,
        "O365_PASSWORD": password,
    }


def write_env_file(project_dir: Path, values: dict[str, str]) -> Path:
    """Write .env file in the project directory."""
    env_path = project_dir / ".env"
    content = "\n".join(f"{k}={v}" for k, v in values.items()) + "\n"
    env_path.write_text(content, encoding="utf-8")

    # Best-effort file permission tightening on POSIX systems.
    try:
        os.chmod(env_path, 0o600)
    except OSError:
        pass

    return env_path


def load_claude_config(config_path: Path) -> dict:
    """Load claude_desktop_config.json as a dict."""
    try:
        data = json.loads(config_path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        raise ValueError(
            f"Invalid JSON in Claude config file: {config_path}. Error: {exc}"
        ) from exc

    if not isinstance(data, dict):
        raise ValueError("Claude config root must be a JSON object.")

    return data


def update_claude_config(
    config: dict,
    project_dir: Path,
    credentials: dict[str, str],
) -> dict:
    """Insert or update this MCP server in the Claude config."""
    mcp_servers = config.get("mcpServers")
    if mcp_servers is None:
        mcp_servers = {}
        config["mcpServers"] = mcp_servers

    if not isinstance(mcp_servers, dict):
        raise ValueError("The 'mcpServers' key in Claude config must be an object.")

    server_script = (project_dir / "server.py").resolve()
    if not server_script.exists():
        raise FileNotFoundError(f"Server script not found: {server_script}")

    # Use the current Python interpreter so command is explicit and predictable.
    mcp_servers[MCP_SERVER_NAME] = {
        "command": sys.executable,
        "args": [str(server_script)],
        "env": {k: credentials[k] for k in REQUIRED_ENV_KEYS},
    }

    return config


def backup_file(file_path: Path) -> Path:
    """Create a backup copy before writing changes."""
    backup_path = file_path.with_suffix(file_path.suffix + ".bak")
    backup_path.write_text(file_path.read_text(encoding="utf-8"), encoding="utf-8")
    return backup_path


def install() -> None:
    """Execute installation workflow with clear validation and error reporting."""
    project_dir = Path(__file__).resolve().parent
    config_path = get_default_claude_config_path()

    if not config_path.exists():
        raise FileNotFoundError(
            "Claude Desktop config was not found in the default location. "
            f"Expected: {config_path}. "
            "Open Claude Desktop once to generate it, then rerun this installer."
        )

    install_dependencies(project_dir)

    credentials = prompt_for_credentials()
    env_path = write_env_file(project_dir, credentials)

    config = load_claude_config(config_path)
    backup_path = backup_file(config_path)
    updated = update_claude_config(config, project_dir, credentials)

    config_path.write_text(json.dumps(updated, indent=2), encoding="utf-8")

    print("MCP server installed successfully.")
    print(f"Updated Claude config: {config_path}")
    print(f"Backup created: {backup_path}")
    print(f"Environment file created: {env_path}")
    print("Restart Claude Desktop to load the new MCP server.")


def main() -> int:
    try:
        install()
        return 0
    except Exception as exc:
        print("MCP server installation failed.")
        print(f"Reason: {exc}")
        print("What to fix:")
        print("1. Ensure Claude Desktop is installed and has generated claude_desktop_config.json.")
        print("2. Verify this project contains server.py and requirements.txt.")
        print("3. Ensure pip can access packages (internet/proxy) and rerun installer.")
        print("4. Rerun and provide valid Outlook credentials.")
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
