from pathlib import Path

import yaml
import git
import pytest

import dotlocker.core as core


@pytest.fixture
def test_repo(tmp_path):
    """
    Fixture to create temporary test repository directory.
    
    Creates:
    - Isolated test_repo directory in temporary path
    
    Provides clean repository directory for git initialization tests.
    """

    test_repo_path = tmp_path / "test_repo"
    test_repo_path.mkdir()

    return test_repo_path

@pytest.fixture
def fake_home(tmp_path, monkeypatch):
    """
    Fixture to create and set up fake home directory for testing.
    
    Creates:
    - Temporary fake home directory structure
    - Monkeypatches Path.home() to return fake home path
    
    Provides isolated home directory to prevent interference with real user
    files.
    """

    fake_home = tmp_path / "fake_home"
    fake_home.mkdir()
    monkeypatch.setattr(Path, "home", lambda: fake_home)
    return fake_home

@pytest.fixture
def fake_args(fake_home, monkeypatch):
    """
    Fixture to set up fake dotlocker paths for testing.
    
    Sets up monkeypatched paths for:
    - repo_path: base dotlocker directory
    - config_path: configuration file path  
    - tracks_path: tracks directory path
    
    Uses fake_home to create isolated testing environment.
    """

    base_path = fake_home / ".dotlocker"
    monkeypatch.setattr(core, "repo_path", base_path)
    monkeypatch.setattr(core, "config_path", base_path / "config.yaml")
    monkeypatch.setattr(core, "tracks_path", base_path / "tracks")

    return base_path


def test_ensure_dir_creation(tmp_path):
    """
    Test that _ensure_dir creates directory when it doesn't exist.
    
    Scenario:
    - Call _ensure_dir with non-existent directory path
    - Verify directory is created successfully
    - Check that directory exists and is accessible
    
    Tests the directory creation utility function.
    """

    test_dir = tmp_path / "test_directory"
    core._ensure_dir(test_dir)
    assert test_dir.exists()

def test_init_git_repo(test_repo):
    """
    Test that _init_git_repo initializes a valid git repository.
    
    Scenario:
    - Call _init_git_repo on test directory
    - Verify git repository is created with proper structure
    - Check that .git directory exists and repository is functional
    
    Tests the basic git repository initialization functionality.
    """

    core._init_git_repo(test_repo)
    _assert_repo_valid(test_repo)

def test_init_git_repo_idempotent(test_repo):
    """
    Test that _init_git_repo is idempotent when called multiple times.
    
    Scenario:
    - Call _init_git_repo twice on the same directory
    - Verify git repository remains valid after both calls
    - Ensure no errors occur and repository structure is maintained
    
    Tests that repeated initialization calls don't break the repository.
    """

    core._init_git_repo(test_repo)
    core._init_git_repo(test_repo)
    _assert_repo_valid(test_repo)

def test_create_default_config(tmp_path):
    """
    Test that _create_default_config creates config file with correct structure.
    
    Scenario:
    - Call _create_default_config with test file path
    - Verify config file is created with expected default content:
      - Empty tracks list
      - Remote section with null URL
    - Validate YAML structure and content matches expectations
    
    Tests the default configuration file creation.
    """

    test_config_path = tmp_path / "test_config.yaml"
    core._create_default_config(test_config_path)
    assert test_config_path.exists()

    with open(test_config_path) as file:
        content = yaml.safe_load(file)
        assert content == {
            "tracks": [],
            "remote": {
                "url": None,
            }
        }

def _assert_repo_valid(repo_path):
    """
    Test helper to validate git repository structure and functionality.
    
    Validates:
    - .git directory exists in repository path
    - Git repository is properly initialized and accessible
    - Repository object can be created and used
    
    This is a utility function used by multiple test cases.
    """

    repo = git.Repo(repo_path)
    assert (repo_path / ".git").exists()
    assert repo.git_dir is not None

def test_init_dotlocker(fake_home, fake_args):
    """
    Test that init_dotlocker initializes the dotlocker repository structure.
    
    Scenario:
    - Create test files in home directory
    - Call init_dotlocker to initialize the repository
    - Verify all required directories and files are created:
      - .dotlocker directory exists
      - Git repository is initialized
      - config.yaml file is created with default structure
    
    Tests the complete initialization workflow.
    """

    (fake_home / ".testrc").write_text("test content")
    (fake_home / ".config").mkdir()
    (fake_home / ".config" / "app.conf").write_text("test content config")

    core.init_dotlocker()
    dotlocker_dir = fake_home / ".dotlocker"
    assert dotlocker_dir.exists()
    assert (dotlocker_dir / ".git").exists()
    assert (dotlocker_dir / "config.yaml").exists()
