import os
import re
import subprocess
import tempfile
import shutil
from core.indexer import CodeIndex
from core.logger import get_logger



logger = get_logger("git_clone")

def clone_and_index(index: CodeIndex, github_url: str, state: dict) -> str:
    """
    Clone a GitHub repo to a temp directory and index it.
    Accepts full GitHub URLs or shorthand like 'owner/repo'.
    """
    raw = github_url.strip()
    valid_full = re.match(r'^https://github\.com/[\w.\-]+/[\w.\-]+(\.git)?/?$', raw)
    valid_short = re.match(r'^[\w.\-]+/[\w.\-]+$', raw)
    if not valid_full and not valid_short:
        return (
            f"Invalid GitHub URL: '{raw}'\n"
            f"Expected formats:\n"
            f"  https://github.com/owner/repo\n"
            f"  owner/repo\n"
            f"Example: gothinkster/spring-boot-realworld-example-app"
        )

    # url is defined BEFORE being used in the log
    url = raw if raw.startswith("http") else f"https://github.com/{raw}"
    logger.info(f"Cloning: {url}")

    repo_name = url.rstrip("/").split("/")[-1]
    if repo_name.endswith(".git"):
        repo_name = repo_name[:-4]

    base_temp = os.path.join(tempfile.gettempdir(), "springboot-intel")
    os.makedirs(base_temp, exist_ok=True)
    target_dir = os.path.join(base_temp, repo_name)
    partial_flag = target_dir + ".partial"
    if os.path.isfile(partial_flag):
        logger.warning(f"Found partial clone, cleaning up: {target_dir}")
        shutil.rmtree(target_dir, ignore_errors=True)
        os.remove(partial_flag)

    if os.path.isdir(target_dir):
        logger.info(f"Re-using cached clone: {target_dir}")
        action = "Re-using existing clone"
    else:
        logger.info(f"Cloning remote repo: {url} → {target_dir}")
        if shutil.which("git") is None:
            logger.error("git not found on PATH")
            return (
                "git is not installed or not on PATH. "
                "Install git from https://git-scm.com and try again."
            )
        open(partial_flag, 'w').close()
        try:
            result = subprocess.Popen(
                ["git", "clone", "--depth=1", "--progress", url, target_dir],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )
            _, stderr = result.communicate(timeout=120)
            if result.returncode != 0:
                logger.error(f"git clone failed for {url}: {stderr.strip()}")
                return (
                    f"git clone failed:\n{result.stderr.strip()}\n\n"
                    f"Check the URL is correct and the repo is public."
                )
            if os.path.isfile(partial_flag):
                os.remove(partial_flag)

            logger.info(f"Clone successful: {url}")
            action = "Cloned"
                
        except subprocess.TimeoutExpired:
            result.kill()
            shutil.rmtree(target_dir, ignore_errors=True) 
            if os.path.isfile(partial_flag):
                os.remove(partial_flag)

            logger.error(f"Clone timed out: {url}")
            return (
                "Clone timed out after 2 minutes. "
                "The repo may be too large — clone manually and use set_project instead."
            )
        except Exception as e:
            shutil.rmtree(target_dir, ignore_errors=True)
            if os.path.isfile(partial_flag):
                os.remove(partial_flag)
            logger.error(f"Clone error: {str(e)}", exc_info=True)
            return f"Clone error: {str(e)}"

    logger.info(f"Indexing: {target_dir}")
    index.build(target_dir)
    state["project_root"] = target_dir
    logger.info(f"Index complete — {len(index.classes)} classes, {len(index.endpoints)} endpoints")

    return (
        f"{action}: {url}\n"
        f"Location : {target_dir}\n"
        f"Classes  : {len(index.classes)}\n"
        f"Endpoints: {len(index.endpoints)}\n\n"
        f"Ready — ask me anything about this codebase."
    )


def list_cloned_repos() -> str:
    """
    List all the repos that have been cloned.
    """
    base_temp = os.path.join(tempfile.gettempdir(), "springboot-intel")
    if not os.path.isdir(base_temp):
        return "No cloned repos found"

    repos = [
        d for d in os.listdir(base_temp)
        if os.path.isdir(os.path.join(base_temp, d))
    ]    
    if not repos:
        return "No cloned repos found"
    
    lines = [f"Cloned Repos in {base_temp}:\n"]
    total_size = 0
    for repo in sorted(repos):
        repo_path = os.path.join(base_temp, repo)
        size_mb =_dir_size_mb(repo_path)
        total_size += size_mb
        lines.append(f"  {repo}  ({size_mb:.1f} MB)")

    lines.append(f"\nTotal: {total_size:.1f} MB")
    lines.append("\nTo delete a repo: ask Claude to delete cloned repo <name>")
    return "\n".join(lines)



def delete_cloned_repo(repo_name: str) -> str:
    """
    Delete a specific cloned repo from the temp folder
    """
    base_temp = os.path.join(tempfile.gettempdir(), "springboot-intel")
    target = os.path.join(base_temp, repo_name)

    if not target.startswith(base_temp):
        return f"Refusing to delete path outside temp folder: {target}"

    if not os.path.isdir(target):
        available = os.listdir(base_temp) if os.path.isdir(base_temp) else []
        return (
            f"Repo '{repo_name}' not found in temp folder.\n"
            f"Available: {', '.join(available) or 'none'}"
        )

    try:
        shutil.rmtree(target)
        return f"Deleted: {target}"
    except Exception as e:
        return f"Error deleting {target}: {str(e)}"

def delete_all_cloned_repos() -> str:
    """
    Delete all cloned repos from the temp folder
    """
    base_temp = os.path.join(tempfile.gettempdir(), "springboot-intel")
    if not os.path.isdir(base_temp):
        return "No cloned repos found — nothing to delete."

    try:
        shutil.rmtree(base_temp)
        return f"Deleted all cloned repos from {base_temp}"
    except Exception as e:
        return f"Error deleting temp folder: {str(e)}"


def _dir_size_mb(path: str) -> float:
    """
    Calculate directory size in MB.
    """
    total = 0
    for dirpath, _, filenames in os.walk(path):
        for f in filenames:
            fp = os.path.join(dirpath, f)
            try:
                total += os.path.getsize(fp)
            except OSError:
                pass
    return total / (1024 * 1024)
