#!/usr/bin/env python3

import os
import re
import sys
import signal
from pathlib import Path
from typing import List, Dict, Tuple
from rich import box
from rich.prompt import Prompt, Confirm
from rich.table import Table
from rich.panel import Panel
from rich.console import Console
from rich.text import Text
from rich import print as rprint

# Constants
SSH_CONFIG_PATH = str(Path.home() / ".ssh/config")
DEFAULT_SSH_KEY = str(Path.home() / ".ssh/id_rsa")
console = Console()

def handle_exit(signum, frame):
    """Handle clean exit on Ctrl+C"""
    console.print("\n[yellow]👋 Thank you for using ossh! Goodbye![/yellow]")
    sys.exit(0)

def validate_name(name: str) -> Tuple[bool, str]:
    """Validate server name or hostname"""
    if ' ' in name:
        return False, "Name cannot contain spaces"
    if not name:
        return False, "Name cannot be empty"
    return True, ""

def get_valid_input(prompt: str, current_value: str = "") -> str:
    """Get valid input from user"""
    while True:
        if current_value:
            value = Prompt.ask(prompt, default=current_value).strip()
        else:
            value = Prompt.ask(prompt).strip()
            
        is_valid, error = validate_name(value)
        if is_valid:
            return value
        console.print(f"[red]Error: {error}. Please try again.[/red]")

def ensure_ssh_config():
    """Ensure SSH config directory and file exist"""
    ssh_dir = Path.home() / ".ssh"
    ssh_dir.mkdir(mode=0o700, exist_ok=True)
    
    config_path = Path(SSH_CONFIG_PATH)
    if not config_path.exists():
        config_path.touch(mode=0o600)

def parse_ssh_config() -> List[Dict]:
    """Parse SSH config file and return sorted server list"""
    servers = []
    try:
        if not os.path.exists(SSH_CONFIG_PATH):
            return servers

        with open(SSH_CONFIG_PATH, "r") as f:
            content = f.read()

        blocks = re.split(r'\n(?=Host\s+)', content)
        
        for block in blocks:
            if not block.strip() or block.startswith('Include'):
                continue
                
            host_match = re.match(r'Host\s+(.+?)(?:\n|$)', block)
            if not host_match:
                continue
                
            host = host_match.group(1).strip()
            
            hostname_match = re.search(r'(?:^|\n)\s*HostName\s+(.+?)(?:\n|$)', block)
            user_match = re.search(r'(?:^|\n)\s*User\s+(.+?)(?:\n|$)', block)
            identity_match = re.search(r'(?:^|\n)\s*IdentityFile\s+(.+?)(?:\n|$)', block)
            port_match = re.search(r'(?:^|\n)\s*Port\s+(.+?)(?:\n|$)', block)
            
            if hostname_match:
                servers.append({
                    "host": host,
                    "hostname": hostname_match.group(1).strip(),
                    "user": user_match.group(1).strip() if user_match else "-",
                    "identity": identity_match.group(1).strip() if identity_match else None,
                    "port": port_match.group(1).strip() if port_match else "22",
                    "raw_config": block  # Store original config block
                })

    except Exception as e:
        console.print(f"[red]Error parsing SSH config: {str(e)}[/red]")
        
    return sorted(servers, key=lambda x: x["host"].lower())

def display_header():
    """Display application header"""
    header = Text()
    header.append("🚀 ", style="bold green")
    header.append("ossh", style="bold blue")
    header.append(" - SSH Connection Manager", style="bold white")
    console.print(Panel(header, box=box.ROUNDED))

def list_servers() -> List[Dict]:
    """Display formatted server list and return servers data"""
    servers = parse_ssh_config()
    
    if not servers:
        console.print("[yellow]No servers configured yet. Use --create to add a new server.[/yellow]")
        return []

    table = Table(box=box.ROUNDED, title="[bold]Available SSH Servers[/bold]", 
                 title_style="white", header_style="bold blue")
    table.add_column("#", justify="right", style="cyan")
    table.add_column("Server Name", style="green")
    table.add_column("Hostname/IP", style="yellow")
    table.add_column("Username", style="magenta")
    table.add_column("Port", style="blue")
    table.add_column("Auth Method", style="blue")

    for idx, server in enumerate(servers, start=1):
        auth_method = "SSH Key" if server.get("identity") else "Password"
        table.add_row(
            str(idx),
            server["host"],
            server["hostname"],
            server["user"],
            server["port"],
            auth_method
        )
    
    console.print(table)
    return servers

def add_server():
    """Add a new server configuration"""
    console.print("\n[bold blue]📝 Add New Server Configuration[/bold blue]")
    
    server_name = get_valid_input("Enter server name")
    hostname = get_valid_input("Enter hostname or IP address")
    username = get_valid_input("Enter username")
    port = Prompt.ask("Enter port", default="22").strip()
    
    use_password = Confirm.ask(
        "Would you like to use password authentication?",
        default=False
    )
    
    with open(SSH_CONFIG_PATH, "a") as f:
        f.write(f"\nHost {server_name}\n")
        f.write(f"    HostName {hostname}\n")
        f.write(f"    User {username}\n")
        if port != "22":
            f.write(f"    Port {port}\n")
        
        if not use_password:
            key_path = Prompt.ask(
                "Enter SSH key path",
                default=DEFAULT_SSH_KEY,
                show_default=True
            ).strip()
            f.write(f"    IdentityFile {key_path}\n")
    
    console.print(f"\n[bold green]✅ Server [white]{server_name}[/white] added successfully![/bold green]")

def edit_server():
    """Edit existing server configuration"""
    servers = list_servers()
    if not servers:
        return

    try:
        choice = Prompt.ask("\nSelect server number to edit")
        selected = servers[int(choice) - 1]
        
        console.print(f"\n[bold blue]✏️  Editing server: [white]{selected['host']}[/white][/bold blue]")
        
        new_name = get_valid_input("New server name", selected["host"])
        new_hostname = get_valid_input("New hostname/IP", selected["hostname"])
        new_username = get_valid_input("New username", selected["user"])
        new_port = Prompt.ask("New port", default=selected.get("port", "22")).strip()
        
        use_password = Confirm.ask(
            "Use password authentication?",
            default=not bool(selected.get("identity"))
        )

        # Read the entire config file
        with open(SSH_CONFIG_PATH, "r") as f:
            config_lines = f.readlines()

        # Find the start and end of the selected server's config block
        start_index = -1
        end_index = -1
        for i, line in enumerate(config_lines):
            if line.strip().startswith(f"Host {selected['host']}"):
                start_index = i
                # Find the end of this block
                for j in range(i + 1, len(config_lines)):
                    if j == len(config_lines) - 1 or config_lines[j].startswith("Host "):
                        end_index = j
                        break
                break

        if start_index != -1 and end_index != -1:
            # Create new config lines
            new_config = [
                f"Host {new_name}\n",
                f"    HostName {new_hostname}\n",
                f"    User {new_username}\n"
            ]
            if new_port != "22":
                new_config.append(f"    Port {new_port}\n")
            if not use_password:
                key_path = Prompt.ask(
                    "Enter SSH key path",
                    default=selected.get("identity", DEFAULT_SSH_KEY)
                ).strip()
                new_config.append(f"    IdentityFile {key_path}\n")

            # Replace the old config block with the new one
            config_lines[start_index:end_index] = new_config

            # Write back to file
            with open(SSH_CONFIG_PATH, "w") as f:
                f.writelines(config_lines)

            console.print(f"\n[bold green]✅ Server [white]{selected['host']}[/white] updated successfully![/bold green]")

    except (KeyboardInterrupt, EOFError):
        console.print("\n[yellow]Edit cancelled.[/yellow]")
    except Exception as e:
        console.print(f"\n[bold red]Error updating server: {str(e)}[/bold red]")

def connect_server():
    """Connect to selected server"""
    servers = list_servers()
    if not servers:
        return

    try:
        choice = Prompt.ask("\nSelect server number to connect")
        selected = servers[int(choice) - 1]
        
        console.print(f"\n[bold green]🔌 Connecting to [white]{selected['host']}[/white]...[/bold green]")
        
        ssh_cmd = f"ssh"
        if selected.get("port") != "22":
            ssh_cmd += f" -p {selected['port']}"
        ssh_cmd += f" {selected['host']}"
        
        os.system(ssh_cmd)
        
    except (KeyboardInterrupt, EOFError):
        console.print("\n[yellow]Connection cancelled.[/yellow]")

def main():
    """Main application entry point"""
    # Register signal handlers
    signal.signal(signal.SIGINT, handle_exit)
    signal.signal(signal.SIGTERM, handle_exit)
    
    # Ensure SSH config exists
    ensure_ssh_config()
    
    # Parse command line arguments
    import argparse
    parser = argparse.ArgumentParser(
        description="🚀 ossh - Professional SSH Connection Manager",
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument("--create", action="store_true", help="Create a new SSH connection")
    parser.add_argument("--edit", action="store_true", help="Edit an existing SSH connection")
    parser.add_argument("--list", action="store_true", help="List all configured servers")
    args = parser.parse_args()

    try:
        display_header()
        
        if args.create:
            add_server()
        elif args.edit:
            edit_server()
        elif args.list:
            list_servers()
        else:
            connect_server()
            
    except Exception as e:
        console.print(f"\n[bold red]Error: {str(e)}[/bold red]")
        sys.exit(1)

if __name__ == "__main__":
    main()