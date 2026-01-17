#!/usr/bin/env python3
"""
Universal Repository Setup Wizard
A production-ready GUI application for setting up repositories from various sources.
"""

import tkinter as tk
from tkinter import ttk, filedialog, messagebox, scrolledtext
import os
import sys
import subprocess
import shutil
import zipfile
import tempfile
import threading
import logging
from pathlib import Path
from urllib.parse import urlparse
import json
from datetime import datetime


class SetupWizard:
    """Main application class for the Repository Setup Wizard."""
    
    def __init__(self, root):
        self.root = root
        self.root.title("Universal Repository Setup Wizard")
        self.root.geometry("800x600")
        self.root.minsize(700, 500)
        
        # Initialize variables
        self.source_type = tk.StringVar(value="folder")
        self.source_path = tk.StringVar()
        self.target_path = tk.StringVar(value=str(Path.home() / "repo_setups"))
        self.auto_install = tk.BooleanVar(value=True)
        self.is_processing = False
        
        # Setup logging
        self.setup_logging()
        
        # Create UI
        self.create_ui()
        
        # Center window
        self.center_window()
        
    def setup_logging(self):
        """Setup comprehensive logging system."""
        log_dir = Path.home() / ".repo_setup_wizard" / "logs"
        log_dir.mkdir(parents=True, exist_ok=True)
        
        log_file = log_dir / f"setup_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log"
        
        logging.basicConfig(
            level=logging.DEBUG,
            format='%(asctime)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler(log_file),
                logging.StreamHandler()
            ]
        )
        self.logger = logging.getLogger(__name__)
        self.logger.info("Setup Wizard initialized")
        
    def center_window(self):
        """Center the window on the screen."""
        self.root.update_idletasks()
        width = self.root.winfo_width()
        height = self.root.winfo_height()
        x = (self.root.winfo_screenwidth() // 2) - (width // 2)
        y = (self.root.winfo_screenheight() // 2) - (height // 2)
        self.root.geometry(f'{width}x{height}+{x}+{y}')
        
    def create_ui(self):
        """Create the main user interface."""
        # Main container with padding
        main_frame = ttk.Frame(self.root, padding="20")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(0, weight=1)
        
        # Title
        title_label = ttk.Label(
            main_frame, 
            text="Repository Setup Wizard",
            font=('Helvetica', 16, 'bold')
        )
        title_label.grid(row=0, column=0, pady=(0, 20))
        
        # Source selection section
        source_frame = ttk.LabelFrame(main_frame, text="1. Select Repository Source", padding="10")
        source_frame.grid(row=1, column=0, sticky=(tk.W, tk.E), pady=(0, 10))
        source_frame.columnconfigure(1, weight=1)
        
        # Radio buttons for source type
        ttk.Radiobutton(
            source_frame, 
            text="Local Folder", 
            variable=self.source_type,
            value="folder",
            command=self.on_source_type_change
        ).grid(row=0, column=0, sticky=tk.W, pady=5)
        
        ttk.Radiobutton(
            source_frame, 
            text="ZIP File", 
            variable=self.source_type,
            value="zip",
            command=self.on_source_type_change
        ).grid(row=0, column=1, sticky=tk.W, pady=5)
        
        ttk.Radiobutton(
            source_frame, 
            text="Git URL", 
            variable=self.source_type,
            value="url",
            command=self.on_source_type_change
        ).grid(row=0, column=2, sticky=tk.W, pady=5)
        
        # Source path/URL entry
        ttk.Label(source_frame, text="Source:").grid(row=1, column=0, sticky=tk.W, pady=5)
        self.source_entry = ttk.Entry(source_frame, textvariable=self.source_path)
        self.source_entry.grid(row=1, column=1, columnspan=2, sticky=(tk.W, tk.E), pady=5, padx=(5, 5))
        
        self.browse_button = ttk.Button(source_frame, text="Browse...", command=self.browse_source)
        self.browse_button.grid(row=1, column=3, pady=5)
        
        # Target directory section
        target_frame = ttk.LabelFrame(main_frame, text="2. Select Target Directory", padding="10")
        target_frame.grid(row=2, column=0, sticky=(tk.W, tk.E), pady=(0, 10))
        target_frame.columnconfigure(1, weight=1)
        
        ttk.Label(target_frame, text="Target:").grid(row=0, column=0, sticky=tk.W, pady=5)
        ttk.Entry(target_frame, textvariable=self.target_path).grid(
            row=0, column=1, sticky=(tk.W, tk.E), pady=5, padx=(5, 5)
        )
        ttk.Button(target_frame, text="Browse...", command=self.browse_target).grid(
            row=0, column=2, pady=5
        )
        
        # Options section
        options_frame = ttk.LabelFrame(main_frame, text="3. Setup Options", padding="10")
        options_frame.grid(row=3, column=0, sticky=(tk.W, tk.E), pady=(0, 10))
        
        ttk.Checkbutton(
            options_frame,
            text="Automatically install dependencies",
            variable=self.auto_install
        ).grid(row=0, column=0, sticky=tk.W, pady=5)
        
        # Progress section
        progress_frame = ttk.LabelFrame(main_frame, text="Progress", padding="10")
        progress_frame.grid(row=4, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), pady=(0, 10))
        progress_frame.columnconfigure(0, weight=1)
        progress_frame.rowconfigure(1, weight=1)
        main_frame.rowconfigure(4, weight=1)
        
        self.progress_bar = ttk.Progressbar(progress_frame, mode='indeterminate')
        self.progress_bar.grid(row=0, column=0, sticky=(tk.W, tk.E), pady=(0, 5))
        
        self.log_text = scrolledtext.ScrolledText(
            progress_frame,
            height=10,
            wrap=tk.WORD,
            font=('Courier', 9)
        )
        self.log_text.grid(row=1, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        self.log_text.config(state=tk.DISABLED)
        
        # Action buttons
        button_frame = ttk.Frame(main_frame)
        button_frame.grid(row=5, column=0, pady=(10, 0))
        
        self.start_button = ttk.Button(
            button_frame,
            text="Start Setup",
            command=self.start_setup,
            style='Accent.TButton'
        )
        self.start_button.grid(row=0, column=0, padx=5)
        
        ttk.Button(
            button_frame,
            text="Clear Log",
            command=self.clear_log
        ).grid(row=0, column=1, padx=5)
        
        ttk.Button(
            button_frame,
            text="Exit",
            command=self.exit_application
        ).grid(row=0, column=2, padx=5)
        
    def on_source_type_change(self):
        """Handle source type radio button changes."""
        source_type = self.source_type.get()
        if source_type == "url":
            self.browse_button.config(state=tk.DISABLED)
            self.source_entry.delete(0, tk.END)
            self.source_entry.insert(0, "https://")
        else:
            self.browse_button.config(state=tk.NORMAL)
            self.source_path.set("")
            
    def browse_source(self):
        """Open file/folder browser for source selection."""
        source_type = self.source_type.get()
        
        if source_type == "folder":
            path = filedialog.askdirectory(title="Select Repository Folder")
            if path:
                self.source_path.set(path)
        elif source_type == "zip":
            path = filedialog.askopenfilename(
                title="Select ZIP File",
                filetypes=[("ZIP files", "*.zip"), ("All files", "*.*")]
            )
            if path:
                self.source_path.set(path)
                
    def browse_target(self):
        """Open folder browser for target directory."""
        path = filedialog.askdirectory(title="Select Target Directory")
        if path:
            self.target_path.set(path)
            
    def log_message(self, message, level="INFO"):
        """Add message to the log display."""
        self.log_text.config(state=tk.NORMAL)
        timestamp = datetime.now().strftime("%H:%M:%S")
        self.log_text.insert(tk.END, f"[{timestamp}] {level}: {message}\n")
        self.log_text.see(tk.END)
        self.log_text.config(state=tk.DISABLED)
        
        # Also log to file
        if level == "ERROR":
            self.logger.error(message)
        elif level == "WARNING":
            self.logger.warning(message)
        else:
            self.logger.info(message)
            
    def clear_log(self):
        """Clear the log display."""
        self.log_text.config(state=tk.NORMAL)
        self.log_text.delete(1.0, tk.END)
        self.log_text.config(state=tk.DISABLED)
        
    def validate_inputs(self):
        """Validate user inputs before processing."""
        source_type = self.source_type.get()
        source = self.source_path.get().strip()
        target = self.target_path.get().strip()
        
        if not source:
            raise ValueError("Please specify a source location")
            
        if not target:
            raise ValueError("Please specify a target directory")
            
        if source_type == "folder":
            if not os.path.isdir(source):
                raise ValueError(f"Source folder does not exist: {source}")
        elif source_type == "zip":
            if not os.path.isfile(source):
                raise ValueError(f"ZIP file does not exist: {source}")
            if not zipfile.is_zipfile(source):
                raise ValueError(f"Invalid ZIP file: {source}")
        elif source_type == "url":
            if not source.startswith(("http://", "https://", "git@")):
                raise ValueError("Invalid Git URL format")
                
        return True
        
    def start_setup(self):
        """Start the setup process in a separate thread."""
        if self.is_processing:
            messagebox.showwarning("Processing", "Setup is already in progress")
            return
            
        try:
            self.validate_inputs()
        except ValueError as e:
            messagebox.showerror("Validation Error", str(e))
            return
            
        self.is_processing = True
        self.start_button.config(state=tk.DISABLED)
        self.progress_bar.start(10)
        self.clear_log()
        
        # Run setup in separate thread to keep UI responsive
        thread = threading.Thread(target=self.run_setup, daemon=True)
        thread.start()
        
    def run_setup(self):
        """Execute the setup process."""
        try:
            self.log_message("Starting repository setup...")
            
            source_type = self.source_type.get()
            source = self.source_path.get().strip()
            target = self.target_path.get().strip()
            
            # Create target directory
            target_dir = Path(target)
            target_dir.mkdir(parents=True, exist_ok=True)
            self.log_message(f"Target directory: {target_dir}")
            
            # Process based on source type
            if source_type == "folder":
                repo_path = self.setup_from_folder(source, target_dir)
            elif source_type == "zip":
                repo_path = self.setup_from_zip(source, target_dir)
            elif source_type == "url":
                repo_path = self.setup_from_url(source, target_dir)
            else:
                raise ValueError(f"Unknown source type: {source_type}")
                
            self.log_message(f"Repository extracted to: {repo_path}")
            
            # Auto-install dependencies if enabled
            if self.auto_install.get():
                self.install_dependencies(repo_path)
                
            self.log_message("Setup completed successfully!", "SUCCESS")
            self.root.after(0, lambda: messagebox.showinfo(
                "Success",
                f"Repository setup completed!\n\nLocation: {repo_path}"
            ))
            
        except Exception as e:
            error_msg = f"Setup failed: {str(e)}"
            self.log_message(error_msg, "ERROR")
            self.logger.exception("Setup failed")
            self.root.after(0, lambda: messagebox.showerror("Error", error_msg))
            
        finally:
            self.is_processing = False
            self.root.after(0, self.finish_setup)
            
    def setup_from_folder(self, source, target_dir):
        """Setup repository from a local folder."""
        self.log_message(f"Copying from folder: {source}")
        
        source_path = Path(source)
        repo_name = source_path.name
        dest_path = target_dir / repo_name
        
        # Check if destination exists
        if dest_path.exists():
            counter = 1
            while (target_dir / f"{repo_name}_{counter}").exists():
                counter += 1
            dest_path = target_dir / f"{repo_name}_{counter}"
            
        # Copy directory
        shutil.copytree(source_path, dest_path, symlinks=True)
        self.log_message(f"Copied {self.count_files(dest_path)} files")
        
        return dest_path
        
    def setup_from_zip(self, source, target_dir):
        """Setup repository from a ZIP file."""
        self.log_message(f"Extracting ZIP file: {source}")
        
        zip_path = Path(source)
        repo_name = zip_path.stem
        dest_path = target_dir / repo_name
        
        # Check if destination exists
        if dest_path.exists():
            counter = 1
            while (target_dir / f"{repo_name}_{counter}").exists():
                counter += 1
            dest_path = target_dir / f"{repo_name}_{counter}"
            
        # Extract ZIP
        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            zip_ref.extractall(dest_path)
            
        self.log_message(f"Extracted {self.count_files(dest_path)} files")
        
        # Handle single root folder in ZIP
        items = list(dest_path.iterdir())
        if len(items) == 1 and items[0].is_dir():
            temp_dir = dest_path.parent / f"temp_{repo_name}"
            items[0].rename(temp_dir)
            dest_path.rmdir()
            temp_dir.rename(dest_path)
            
        return dest_path
        
    def setup_from_url(self, url, target_dir):
        """Setup repository from a Git URL."""
        self.log_message(f"Cloning from URL: {url}")
        
        # Check if git is available
        if not self.check_command("git"):
            raise RuntimeError("Git is not installed or not in PATH")
            
        # Extract repository name from URL
        parsed = urlparse(url)
        repo_name = Path(parsed.path).stem.replace('.git', '')
        
        if not repo_name:
            repo_name = "repository"
            
        dest_path = target_dir / repo_name
        
        # Check if destination exists
        if dest_path.exists():
            counter = 1
            while (target_dir / f"{repo_name}_{counter}").exists():
                counter += 1
            dest_path = target_dir / f"{repo_name}_{counter}"
            
        # Clone repository
        try:
            result = subprocess.run(
                ["git", "clone", url, str(dest_path)],
                capture_output=True,
                text=True,
                timeout=300,
                check=True
            )
            self.log_message("Clone completed successfully")
            if result.stdout:
                self.log_message(result.stdout.strip())
                
        except subprocess.TimeoutExpired:
            raise RuntimeError("Git clone timed out (5 minutes)")
        except subprocess.CalledProcessError as e:
            raise RuntimeError(f"Git clone failed: {e.stderr}")
            
        return dest_path
        
    def install_dependencies(self, repo_path):
        """Automatically detect and install dependencies."""
        self.log_message("Checking for dependencies...")
        
        repo_path = Path(repo_path)
        installed_any = False
        
        # Python dependencies (requirements.txt, setup.py, pyproject.toml)
        if (repo_path / "requirements.txt").exists():
            self.log_message("Found requirements.txt")
            if self.check_command("pip"):
                try:
                    self.run_command(
                        ["pip", "install", "-r", "requirements.txt"],
                        cwd=repo_path
                    )
                    installed_any = True
                except Exception as e:
                    self.log_message(f"Failed to install Python dependencies: {e}", "WARNING")
                    
        # Node.js dependencies (package.json)
        if (repo_path / "package.json").exists():
            self.log_message("Found package.json")
            if self.check_command("npm"):
                try:
                    self.run_command(["npm", "install"], cwd=repo_path)
                    installed_any = True
                except Exception as e:
                    self.log_message(f"Failed to install Node.js dependencies: {e}", "WARNING")
                    
        # Ruby dependencies (Gemfile)
        if (repo_path / "Gemfile").exists():
            self.log_message("Found Gemfile")
            if self.check_command("bundle"):
                try:
                    self.run_command(["bundle", "install"], cwd=repo_path)
                    installed_any = True
                except Exception as e:
                    self.log_message(f"Failed to install Ruby dependencies: {e}", "WARNING")
                    
        # Go dependencies (go.mod)
        if (repo_path / "go.mod").exists():
            self.log_message("Found go.mod")
            if self.check_command("go"):
                try:
                    self.run_command(["go", "mod", "download"], cwd=repo_path)
                    installed_any = True
                except Exception as e:
                    self.log_message(f"Failed to install Go dependencies: {e}", "WARNING")
                    
        if not installed_any:
            self.log_message("No dependency files found or no package managers available")
            
    def check_command(self, command):
        """Check if a command is available in PATH."""
        return shutil.which(command) is not None
        
    def run_command(self, cmd, cwd=None):
        """Run a command and log output."""
        self.log_message(f"Running: {' '.join(cmd)}")
        
        result = subprocess.run(
            cmd,
            cwd=cwd,
            capture_output=True,
            text=True,
            timeout=600
        )
        
        if result.stdout:
            for line in result.stdout.strip().split('\n'):
                if line.strip():
                    self.log_message(line.strip())
                    
        if result.returncode != 0:
            error_msg = result.stderr.strip() if result.stderr else f"Command failed with exit code {result.returncode}"
            raise RuntimeError(error_msg)
            
    def count_files(self, path):
        """Count files in a directory recursively."""
        return sum(1 for _ in Path(path).rglob('*') if _.is_file())
        
    def finish_setup(self):
        """Cleanup after setup completes."""
        self.progress_bar.stop()
        self.start_button.config(state=tk.NORMAL)
        
    def exit_application(self):
        """Exit the application safely."""
        if self.is_processing:
            if not messagebox.askyesno(
                "Confirm Exit",
                "Setup is in progress. Are you sure you want to exit?"
            ):
                return
                
        self.logger.info("Application closed")
        self.root.quit()


def main():
    """Main entry point for the application."""
    try:
        root = tk.Tk()
        
        # Apply modern theme
        style = ttk.Style()
        available_themes = style.theme_names()
        
        # Use best available theme
        if 'clam' in available_themes:
            style.theme_use('clam')
        elif 'alt' in available_themes:
            style.theme_use('alt')
            
        # Configure accent button style
        style.configure(
            'Accent.TButton',
            font=('Helvetica', 10, 'bold')
        )
        
        app = SetupWizard(root)
        root.protocol("WM_DELETE_WINDOW", app.exit_application)
        root.mainloop()
        
    except KeyboardInterrupt:
        print("\nApplication interrupted by user")
        sys.exit(0)
    except Exception as e:
        print(f"Fatal error: {e}", file=sys.stderr)
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
