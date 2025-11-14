from datetime import datetime
from pathlib import Path
import shutil
from typing import Optional

import git
import yaml


# DotLocker directory structure paths
repo_path = Path.home() / ".dotlocker"        # Main repository directory
config_path = repo_path / "config.yaml"       # Configuration file  
tracks_path = repo_path / "tracks"            # Tracked files backup directory


def init_dotlocker() -> None:
    """
    Initialize DotLocker repository and configuration.
    
    Creates the core directory structure:
    - ~/.dotlocker/ - main repository directory
    - Initializes Git repository for version control
    - Creates default config.yaml with empty tracks list
    
    This is the first command that should be run to set up DotLocker.
    """

    _ensure_dir(repo_path)
    _init_git_repo(repo_path)
    _create_default_config(config_path)

def remote_sync():
    pass

def _ensure_dir(path: Path) -> None:
    """
    Ensure directory exists, create if it doesn't.
    
    Safely creates directory and all necessary parent directories.
    Handles errors gracefully and provides informative error messages.
    
    Args:
        path: Directory path to ensure existence of
        
    Raises:
        OSError: If directory creation fails due to system errors
    """

    try:
        path.mkdir(parents=True, exist_ok=True)
    except Exception as e:
        print(f"Error create directory {str(path)}", e, sep="\n")

def _init_git_repo(repo_path: Path) -> None:
    """
    Initialize a Git repository at the specified path.
    
    Creates a new Git repository if one doesn't already exist.
    Safe to call multiple times - won't reinitialize existing repository.
    
    Args:
        repo_path: Path where Git repository should be initialized
        
    Note:
        This is an idempotent operation - calling multiple times has same effect
        as calling once.
    """

    try:
        git.Repo.init(repo_path)
    except Exception as e:
        print("Error initialized Git-repository", e, sep="\n")

def _create_default_config(config_path: Path) -> None:
    """
    Create default configuration file with basic structure.
    
    Generates config.yaml with:
    - Empty tracks list (no files tracked initially)
    - Remote section with null URL (no remote repository configured)
    
    Only creates the file if it doesn't already exist.
    
    Args:
        config_path: Path where configuration file should be created
    """

    if not config_path.exists():
        default_yaml_config = {
            "tracks": [],
            "remote": {
                "url": None,
            }
        }

        try:
            with open(config_path, "w") as file:
                yaml.dump(default_yaml_config, file)
        except Exception as e:
            print("Error created default yaml-config", e, sep="\n")

