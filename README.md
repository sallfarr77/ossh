# OSSH - Simple SSH Connection Manager

OSSH is a lightweight, user-friendly SSH connection manager designed for Unix like systems. It simplifies the management of multiple SSH connections by providing an intuitive interface to add, edit, and connect to your servers.

## Features

- 🚀 Simple and intuitive command-line interface
- 📝 Easy server configuration management
- 🔑 Support for both password and SSH key authentication
- 📋 Alphabetically sorted server list
- 🛠️ Interactive server editing
- 💼 Professional terminal UI with color-coding

## Prerequisites

- Python 3.6 or higher
- Unix-based system (Linux, macOS)
- SSH client installed

## Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/ossh.git
cd ossh
```

2. Install required dependencies:
```bash
pip install rich
```

3. Make the script executable:
```bash
chmod +x ossh.py
```

## Usage

### Basic Commands

```bash
# List and connect to servers
./ossh.py

# List all servers
./ossh.py --list

# Add a new server
./ossh.py --create

# Edit existing server
./ossh.py --edit
```

### Adding a New Server

1. Run the create command:
```bash
./ossh.py --create
```

2. Follow the interactive prompts:
   - Enter server name (no spaces allowed)
   - Enter hostname or IP address
   - Enter username
   - Enter port (default: 22)
   - Choose authentication method (password/SSH key)
   - Enter SSH key path if using key authentication

### Editing a Server

1. Run the edit command:
```bash
./ossh.py --edit
```

2. Select the server to edit by number
3. Update the server details through interactive prompts

### Connecting to a Server

1. Run OSSH:
```bash
./ossh.py
```

2. Select the server number from the list
3. OSSH will establish the SSH connection using your configured settings

## Configuration

OSSH manages your SSH configurations in the standard SSH config file:
```
~/.ssh/config
```

All server configurations follow the OpenSSH format and can be manually edited if needed.

## Features in Detail

- **Server Management**
  - Add new server configurations
  - Edit existing servers
  - List all configured servers
  - Connect to servers with a single command

- **Authentication Support**
  - Password authentication
  - SSH key-based authentication
  - Custom port configuration

- **User Interface**
  - Color-coded server list
  - Interactive prompts
  - Clear error messages
  - Clean exit handling

## Contributing

Contributions are welcome! Feel free to submit issues and pull requests.

## License

This project is licensed under the GPL-3.0 license - see the LICENSE file for details.

## Acknowledgments

- Built with [Rich](https://github.com/Textualize/rich) for beautiful terminal formatting
- Inspired by the need for a simple, efficient SSH connection manager
