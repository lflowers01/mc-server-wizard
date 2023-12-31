
# MC Server Wizard 🪄

*CS50 Final Project*

### Table of Contents

- [Introduction](#introduction)
- [Installation](#installation)
  - [Troubleshooting](#troubleshooting)
- [Usage](#usage)
- [Building from Source](#building-from-source)
- [Contributing](#contributing)
- [License](#license)
- [Acknowledgements](#acknowledgements)

### Introduction

Welcome to MC Server Wizard, a magical tool designed to simplify the installation and management of Minecraft servers on Windows. This project, developed as part of the CS50 Final Project, aims to provide a seamless experience for users who want to set up their Minecraft server without dealing with the intricacies of manual installation.

[Watch the Video Demo](https://youtu.be/qC2HDNDb-4Y)

### Features

- Easy installation process.
- Simplified server management commands.
- Plugin installation and management.
- Backup creation for server files.

### Compatibility

Currently, MC Server Wizard is only available for Windows. However, we are actively exploring the possibility of extending support to Linux in future releases.

### Installation

1. Download the `.exe` from the [Releases](https://github.com/lflowers01/mc-server-wizard/releases) tab.
2. Run the executable in an empty directory.
3. Follow the on-screen instructions to complete the installation.

### Troubleshooting

If you encounter any issues during installation, consider the following troubleshooting steps:

- Ensure the directory is empty, including hidden files.
- Run the program as an administrator.
- Avoid placing the installation directory at the root of your drive.
- For older machines, try running in compatibility mode for your operating system version.

### Usage

Once the server is installed, you can use the `help` command to show all available commands:

```plaintext
help - Shows this help message
start - Starts the server
update plugins - Updates all plugins
install plugin - Installs a plugin
list plugins - Lists all plugins
create backup - Creates a backup of your server files
clear - Clears the console
delete plugin - Deletes selected plugins
exit - Exits the program
disable plugin - Disables/enables a plugin
```

Explore these commands to manage your Minecraft server efficiently.

### Building from Source
If you prefer to build MC Server Wizard from the source code, follow these steps:

Download the source code from the repository.
Run the `./build.ps1 file`.
Use the `-clean` argument to delete all files in the `/dist` directory before building.
Use the `-test` argument to run the `.exe` after building.
The script will then build the `.exe` in the `/dist` directory.
