import git
import os

def get_git_info():
    try:
        repo = git.Repo(os.getcwd(), search_parent_directories=True)
        branch = repo.active_branch.name
        remote = repo.remote().url if repo.remotes else "No remote"
        return f"Git: {branch} ({remote})"
    except Exception:
        return None
