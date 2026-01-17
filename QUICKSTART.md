# Quick Start Guide for Universal Repository Setup Wizard

## 🚀 5-Minute Quick Start

### 1. Prerequisites Check
```bash
# Check Python version (needs 3.7+)
python3 --version

# Check if tkinter is available
python3 -c "import tkinter; print('tkinter OK')"

# Check if Git is available (optional, for URL cloning)
git --version
```

### 2. Launch the Wizard

**Linux/macOS:**
```bash
./launch.sh
```
or
```bash
python3 setup_wizard.py
```

**Windows:**
```cmd
launch.bat
```
or
```cmd
python setup_wizard.py
```

### 3. First Setup - Local Folder

1. In the wizard window:
   - Select "Local Folder"
   - Click "Browse..." next to Source
   - Navigate to any repository folder on your computer
   - Click "Start Setup"

2. Watch the progress in the log window
3. Done! Your repository is set up in `~/repo_setups`

### 4. Try ZIP File Setup

1. Create a test ZIP:
   ```bash
   zip -r test_repo.zip /path/to/your/repo
   ```

2. In the wizard:
   - Select "ZIP File"
   - Click "Browse..." and select your ZIP file
   - Click "Start Setup"

### 5. Try Git URL Setup

1. In the wizard:
   - Select "Git URL"
   - Enter a repository URL, for example:
     - `https://github.com/octocat/Hello-World.git`
     - `git@github.com:user/repo.git`
   - Click "Start Setup"

## 📋 Common Use Cases

### Use Case 1: Setup Multiple Projects
- Launch multiple wizard instances
- Each can run independently
- Different target directories per project

### Use Case 2: Quick Repository Testing
1. Clone a repo using Git URL
2. Enable "Automatically install dependencies"
3. Wizard installs all dependencies automatically
4. Start testing immediately

### Use Case 3: Share Repository via ZIP
1. ZIP your repository
2. Share ZIP file with team
3. Team members use wizard to extract and setup
4. All dependencies installed automatically

## 🔧 Troubleshooting Quick Fixes

**Error: "tkinter not found"**
```bash
# Ubuntu/Debian
sudo apt-get install python3-tk

# macOS (reinstall Python from python.org)
# Windows (reinstall Python with tkinter enabled)
```

**Error: "git not found"**
```bash
# Ubuntu/Debian
sudo apt-get install git

# macOS
brew install git

# Windows: Download from https://git-scm.com/
```

**Wizard won't start**
```bash
# Check Python version
python3 --version

# Run directly with verbose output
python3 -v setup_wizard.py
```

## 🎯 Tips for Best Experience

1. **Use absolute paths** when possible
2. **Check logs** in `~/.repo_setup_wizard/logs/` for debugging
3. **Enable auto-install** to save time with dependencies
4. **Choose descriptive target directories** for organization
5. **Monitor the progress log** for real-time status

## 📊 Feature Matrix

| Feature | Status | Notes |
|---------|--------|-------|
| Local Folder | ✅ | Instant copy |
| ZIP File | ✅ | Handles nested archives |
| Git URL | ✅ | Requires Git installed |
| Auto Dependencies | ✅ | Python, Node, Ruby, Go |
| Progress Tracking | ✅ | Real-time updates |
| Error Recovery | ✅ | Graceful failure handling |
| Logging | ✅ | Detailed operation logs |
| Cross-Platform | ✅ | Windows, macOS, Linux |

## 🎓 Learning Path

1. **Beginner**: Start with local folder setup
2. **Intermediate**: Try ZIP file extraction
3. **Advanced**: Use Git URL with auto-install
4. **Expert**: Customize for your workflow

## 📞 Getting Help

1. Check the main README.md for detailed documentation
2. Review logs in `~/.repo_setup_wizard/logs/`
3. Open an issue on GitHub with:
   - Your OS and Python version
   - Steps to reproduce
   - Relevant log excerpts

## ⚡ Pro Tips

- **Keyboard Shortcuts**: Use Tab to navigate between fields
- **Quick Setup**: Press Enter after entering URL
- **Batch Processing**: Run multiple wizard instances
- **Log Analysis**: Filter logs by ERROR or WARNING
- **Custom Targets**: Create organized target directory structure

## 🎉 You're Ready!

The wizard is designed to be intuitive. Just:
1. Pick your source
2. Choose your target
3. Click Start Setup
4. ☕ Relax while it works

---
**Need more help?** See README.md for complete documentation
