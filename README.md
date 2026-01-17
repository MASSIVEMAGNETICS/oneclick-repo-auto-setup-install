# Universal Repository Setup Wizard

A production-ready, user-friendly GUI application for setting up repositories from multiple sources with comprehensive error handling and automatic dependency installation.

## ✨ Features

- **🎯 Multiple Input Sources**
  - Local folder
  - ZIP archive
  - Git URL (HTTP/HTTPS/SSH)

- **🛡️ Production-Ready**
  - Comprehensive error handling
  - Crash-proof with exception catching
  - Input validation
  - Detailed logging system
  - Progress indicators
  - Thread-safe operations

- **🚀 Smart Setup**
  - Automatic dependency detection
  - Support for Python (pip, pipenv, Poetry), Node.js (npm), Ruby (bundle), Go, Rust (Cargo), and Java (Maven/Gradle)
  - Intelligent file extraction
  - Duplicate name handling
  - Optional Python virtualenv creation
  - Monorepo project discovery
  - Optional Docker build/run
  - Post-setup scripts and recipes (trusted repos only)
  - Optional CI workflow template generation

- **💎 Polished UI**
  - Modern, intuitive interface
  - Real-time progress updates
  - Scrollable log display
  - Cross-platform compatibility

## 🔧 Requirements

- Python 3.7 or higher
- tkinter (included with most Python installations)
- Git (optional, only needed for URL cloning)

### Platform-Specific tkinter Installation

**Linux:**
```bash
# Ubuntu/Debian
sudo apt-get install python3-tk

# Fedora
sudo dnf install python3-tkinter

# Arch
sudo pacman -S tk
```

**macOS:**
tkinter is included with Python from python.org

**Windows:**
tkinter is included with Python installer

## 📦 Installation

1. Clone or download this repository:
```bash
git clone https://github.com/MASSIVEMAGNETICS/oneclick-repo-auto-setup-install.git
cd oneclick-repo-auto-setup-install
```

2. Ensure Python 3.7+ is installed:
```bash
python3 --version
```

3. Make the script executable (Linux/macOS):
```bash
chmod +x setup_wizard.py
```

## 🚀 Usage

### Quick Start

Run the application:

```bash
python3 setup_wizard.py
```

Or on Linux/macOS with executable permissions:
```bash
./setup_wizard.py
```

### Step-by-Step Guide

1. **Select Repository Source**
   - Choose from: Local Folder, ZIP File, or Git URL
   - Browse to select folder/file, or paste Git URL

2. **Select Target Directory**
   - Choose where the repository should be set up
   - Default: `~/repo_setups`

3. **Configure Options**
   - Enable/disable automatic dependency installation
   - Optional Python virtualenv creation and Docker build/run
   - Optional post-setup scripts/recipes and CI template generation
   - (Automatically detects requirements.txt, package.json, Gemfile, go.mod, etc.)

4. **Start Setup**
   - Click "Start Setup" to begin
   - Monitor progress in real-time
   - Review log messages

### Examples

**Setup from Local Folder:**
1. Select "Local Folder"
2. Click "Browse..." and select your repository folder
3. Choose target directory
4. Click "Start Setup"

**Setup from ZIP File:**
1. Select "ZIP File"
2. Click "Browse..." and select your .zip file
3. Choose target directory
4. Click "Start Setup"

**Setup from Git URL:**
1. Select "Git URL"
2. Enter URL (e.g., `https://github.com/user/repo.git`)
3. Choose target directory
4. Click "Start Setup"
5. (Optional) Provide SSH key, OAuth token, or credential helper for private repos

## 🔒 Error Handling & Safety

The wizard includes comprehensive error handling:

- **Input Validation**: Checks all inputs before processing
- **File System Checks**: Verifies paths and permissions
- **Network Resilience**: Timeout protection for Git operations
- **Duplicate Handling**: Automatically renames if target exists
- **Graceful Failures**: Clear error messages with logging
- **Thread Safety**: Non-blocking UI during operations

## 📝 Logging

All operations are logged to:
```
~/.repo_setup_wizard/logs/setup_YYYYMMDD_HHMMSS.log
```

Logs include:
- Timestamps
- Operation details
- Error traces
- Command outputs

## 🔍 Automatic Dependency Detection

The wizard automatically detects and installs dependencies for:

| Language/Framework | File Detected | Command Run |
|-------------------|---------------|-------------|
| Python (pip) | requirements.txt | `pip install -r requirements.txt` |
| Python (pipenv) | Pipfile | `pipenv install` |
| Python (Poetry) | pyproject.toml | `poetry install` |
| Node.js | package.json | `npm install` |
| Ruby | Gemfile | `bundle install` |
| Go | go.mod | `go mod download` |
| Rust | Cargo.toml | `cargo fetch` |
| Maven | pom.xml | `mvn -q -DskipTests dependency:resolve` |
| Gradle | build.gradle / build.gradle.kts | `gradle dependencies` |

**Note**: Respective package managers (pip, npm, bundle, go) must be installed on your system.

## 🎨 UI Features

- **Progress Bar**: Visual feedback during operations
- **Real-time Log**: See exactly what's happening
- **Responsive Design**: Resizable window with minimum size constraints
- **Clear Actions**: Intuitive button layout
- **Status Messages**: Clear success/error dialogs

## 🛠️ Technical Details

### Architecture

- **Single File Application**: Easy distribution and maintenance
- **Threading**: Background operations keep UI responsive
- **Modular Design**: Clean separation of concerns
- **Cross-Platform**: Works on Windows, macOS, and Linux

### Error Recovery

- Invalid inputs are caught before processing
- Network timeouts prevent hanging
- File operation errors are logged and reported
- Partial operations are handled gracefully

### Performance

- Efficient file operations
- Streaming for large files
- Non-blocking UI
- Optimized Git cloning

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📄 License

This project is open source and available under the MIT License.

## 🐛 Troubleshooting

**Issue**: "tkinter not found"
- **Solution**: Install tkinter for your platform (see Requirements section)

**Issue**: "git not found" when cloning from URL
- **Solution**: Install Git from https://git-scm.com/

**Issue**: Dependency installation fails
- **Solution**: Install the relevant package manager (pip, npm, bundle, go)

**Issue**: Permission denied
- **Solution**: Check write permissions on target directory

## 💡 Tips

- The wizard creates a unique folder name if the target already exists
- Logs are kept for debugging and audit purposes
- You can run multiple setups by launching multiple instances
- Use the "Clear Log" button to reset the display between setups

## 🔮 Future Enhancements

Potential future features:
- Repository templates
- Batch processing
- Configuration profiles
- Dark mode theme

## 📧 Support

For issues, questions, or suggestions, please open an issue on GitHub.

---

**Made with ❤️ for developers who value convenience and reliability**
