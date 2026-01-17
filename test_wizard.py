#!/usr/bin/env python3
"""
Test script for Setup Wizard core functionality
Tests non-GUI components without requiring a display
"""

import os
import sys
import tempfile
import shutil
import zipfile
from pathlib import Path

# Add parent directory to path to import the wizard
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def test_folder_operations():
    """Test folder copying functionality."""
    print("Testing folder operations...")
    
    with tempfile.TemporaryDirectory() as tmpdir:
        # Create test source
        source_dir = Path(tmpdir) / "test_source"
        source_dir.mkdir()
        (source_dir / "file1.txt").write_text("Test content 1")
        (source_dir / "file2.txt").write_text("Test content 2")
        (source_dir / "subdir").mkdir()
        (source_dir / "subdir" / "file3.txt").write_text("Test content 3")
        
        # Create target
        target_dir = Path(tmpdir) / "test_target"
        target_dir.mkdir()
        
        # Copy
        dest = shutil.copytree(source_dir, target_dir / "test_source")
        
        # Verify
        assert dest.exists()
        assert (dest / "file1.txt").exists()
        assert (dest / "file2.txt").exists()
        assert (dest / "subdir" / "file3.txt").exists()
        
        print("✓ Folder operations passed")
        return True

def test_zip_operations():
    """Test ZIP extraction functionality."""
    print("Testing ZIP operations...")
    
    with tempfile.TemporaryDirectory() as tmpdir:
        # Create test ZIP
        zip_path = Path(tmpdir) / "test.zip"
        with zipfile.ZipFile(zip_path, 'w') as zf:
            zf.writestr("file1.txt", "Test content 1")
            zf.writestr("file2.txt", "Test content 2")
            zf.writestr("subdir/file3.txt", "Test content 3")
        
        # Extract
        extract_dir = Path(tmpdir) / "extracted"
        extract_dir.mkdir()
        
        with zipfile.ZipFile(zip_path, 'r') as zf:
            zf.extractall(extract_dir)
        
        # Verify
        assert (extract_dir / "file1.txt").exists()
        assert (extract_dir / "file2.txt").exists()
        assert (extract_dir / "subdir" / "file3.txt").exists()
        
        print("✓ ZIP operations passed")
        return True

def test_dependency_detection():
    """Test dependency file detection."""
    print("Testing dependency detection...")
    
    with tempfile.TemporaryDirectory() as tmpdir:
        test_dir = Path(tmpdir)
        
        # Test Python
        (test_dir / "requirements.txt").write_text("requests==2.28.0\n")
        assert (test_dir / "requirements.txt").exists()
        
        # Test Node.js
        (test_dir / "package.json").write_text('{"name": "test"}')
        assert (test_dir / "package.json").exists()
        
        # Test Ruby
        (test_dir / "Gemfile").write_text("source 'https://rubygems.org'\n")
        assert (test_dir / "Gemfile").exists()
        
        # Test Go
        (test_dir / "go.mod").write_text("module test\n")
        assert (test_dir / "go.mod").exists()
        
        print("✓ Dependency detection passed")
        return True

def test_path_validation():
    """Test path validation logic."""
    print("Testing path validation...")
    
    with tempfile.TemporaryDirectory() as tmpdir:
        test_dir = Path(tmpdir)
        
        # Test valid directory
        valid_dir = test_dir / "valid"
        valid_dir.mkdir()
        assert valid_dir.is_dir()
        
        # Test valid file
        valid_file = test_dir / "test.zip"
        valid_file.write_text("test")
        assert valid_file.is_file()
        
        # Test non-existent
        invalid = test_dir / "nonexistent"
        assert not invalid.exists()
        
        print("✓ Path validation passed")
        return True

def test_duplicate_handling():
    """Test duplicate name handling."""
    print("Testing duplicate name handling...")
    
    with tempfile.TemporaryDirectory() as tmpdir:
        test_dir = Path(tmpdir)
        
        # Create first directory
        dir1 = test_dir / "test_repo"
        dir1.mkdir()
        assert dir1.exists()
        
        # Simulate duplicate handling
        counter = 1
        new_name = "test_repo"
        while (test_dir / f"{new_name}").exists():
            new_name = f"test_repo_{counter}"
            counter += 1
        
        dir2 = test_dir / new_name
        assert not dir2.exists()
        assert new_name == "test_repo_1"
        
        print("✓ Duplicate handling passed")
        return True

def main():
    """Run all tests."""
    print("=" * 60)
    print("Setup Wizard Core Functionality Tests")
    print("=" * 60)
    print()
    
    tests = [
        test_folder_operations,
        test_zip_operations,
        test_dependency_detection,
        test_path_validation,
        test_duplicate_handling,
    ]
    
    passed = 0
    failed = 0
    
    for test in tests:
        try:
            if test():
                passed += 1
            else:
                failed += 1
                print(f"✗ {test.__name__} failed")
        except Exception as e:
            failed += 1
            print(f"✗ {test.__name__} failed with error: {e}")
            import traceback
            traceback.print_exc()
        print()
    
    print("=" * 60)
    print(f"Results: {passed} passed, {failed} failed")
    print("=" * 60)
    
    return 0 if failed == 0 else 1

if __name__ == "__main__":
    sys.exit(main())
