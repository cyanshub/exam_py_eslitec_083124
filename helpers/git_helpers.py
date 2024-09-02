import subprocess
import argparse


# git 初始化
def git_init():
    result = subprocess.run(["git", "init"], capture_output=True, text=True)
    if result.returncode == 0:
        print("Git repository initialized successfully.")
        print(result.stdout)
    else:
        print("Failed to initialize Git repository.")
        print(result.stderr)


# 執行 `git add .` 命令
def git_add(file="."):
    result = subprocess.run(["git", "add", file], capture_output=True, text=True)
    if result.returncode == 0:
        print(f"File(s) {file} added successfully.")
        print(result.stdout)
    else:
        print(f"Failed to add file(s) {file}.")
        print(result.stderr)


# 執行 `git commit` 命令
def git_commit(message):
    result = subprocess.run(
        ["git", "commit", "-m", message], capture_output=True, text=True
    )
    if result.returncode == 0:
        print("Commit successful.")
        print(result.stdout)
    else:
        print("Failed to commit.")
        print(result.stderr)


# 操作分支（創建、刪除、重命名）
def git_branch(branch_name=None, delete=False, rename=False):
    if rename:
        result = subprocess.run(
            ["git", "branch", "-M", branch_name], capture_output=True, text=True
        )
        action = "renamed"
    elif delete:
        result = subprocess.run(
            ["git", "branch", "-D", branch_name], capture_output=True, text=True
        )
        action = "deleted"
    else:
        result = subprocess.run(
            ["git", "branch", branch_name], capture_output=True, text=True
        )
        action = "created"

    if result.returncode == 0:
        print(f"Branch {branch_name} {action} successfully.")
        print(result.stdout)
    else:
        print(f"Failed to {action} branch {branch_name}.")
        print(result.stderr)


# 切換分支
def git_checkout(branch_name):
    result = subprocess.run(
        ["git", "checkout", branch_name], capture_output=True, text=True
    )
    if result.returncode == 0:
        print(f"Switched to branch {branch_name} successfully.")
        print(result.stdout)
    else:
        print(f"Failed to switch to branch {branch_name}.")
        print(result.stderr)


# 推送分支到遠端，支援強制推送
def git_push(remote, branch_name, force=False):
    command = ["git", "push", remote, branch_name]
    if force:
        command.append("--force")

    result = subprocess.run(command, capture_output=True, text=True)
    if result.returncode == 0:
        print(f"Branch {branch_name} pushed to {remote} successfully.")
        print(result.stdout)
    else:
        print(f"Failed to push branch {branch_name} to {remote}.")
        print(result.stderr)


# 添加遠端倉庫
def git_remote_add(remote_name, remote_url):
    result = subprocess.run(
        ["git", "remote", "add", remote_name, remote_url],
        capture_output=True,
        text=True,
    )
    if result.returncode == 0:
        print(f"Remote {remote_name} added successfully with URL {remote_url}.")
        print(result.stdout)
    else:
        print(f"Failed to add remote {remote_name}.")
        print(result.stderr)


# 查看當前分支
def git_current_branch():
    result = subprocess.run(
        ["git", "branch", "--show-current"], capture_output=True, text=True
    )
    if result.returncode == 0:
        print(f"Current branch: {result.stdout.strip()}")
    else:
        print("Failed to retrieve current branch.")
        print(result.stderr)


# 查看遠端倉庫
def git_remote_view():
    result = subprocess.run(["git", "remote", "-v"], capture_output=True, text=True)
    if result.returncode == 0:
        print("Remote repositories:")
        print(result.stdout)
    else:
        print("Failed to retrieve remote repositories.")
        print(result.stderr)


def main():
    parser = argparse.ArgumentParser(
        description="Git helper script for basic Git operations."
    )
    parser.add_argument(
        "command",
        choices=[
            "init",
            "add",
            "commit",
            "branch",
            "checkout",
            "push",
            "remote-add",
            "remote-view",
            "current-branch",
        ],
        help="The git operation to perform.",
    )
    parser.add_argument(
        "-f", "--file", default=".", help="The file to add (default: all files)."
    )
    parser.add_argument(
        "-m", "--message", help="The commit message (required for commit command)."
    )
    parser.add_argument(
        "-b",
        "--branch",
        help="The branch name (required for branch, checkout, and push commands).",
    )
    parser.add_argument(
        "--delete",
        action="store_true",
        help="Delete the branch (used with branch command).",
    )
    parser.add_argument(
        "--rename",
        action="store_true",
        help="Rename the branch to the given name (used with branch command).",
    )
    parser.add_argument(
        "-r",
        "--remote",
        help="The remote name (used with push and remote-add commands).",
    )
    parser.add_argument(
        "--url", help="The remote URL (required for remote-add command)."
    )
    parser.add_argument(
        "--force",
        action="store_true",
        help="Force push the branch (used with push command).",
    )

    args = parser.parse_args()

    if args.command == "init":
        git_init()
    elif args.command == "add":
        git_add(args.file)
    elif args.command == "commit":
        if args.message:
            git_commit(args.message)
        else:
            print("Error: Commit message is required for commit command.")
    elif args.command == "branch":
        if args.branch:
            git_branch(args.branch, delete=args.delete, rename=args.rename)
        else:
            print("Error: Branch name is required for branch command.")
    elif args.command == "checkout":
        if args.branch:
            git_checkout(args.branch)
        else:
            print("Error: Branch name is required for checkout command.")
    elif args.command == "push":
        if args.remote and args.branch:
            git_push(args.remote, args.branch, force=args.force)
        else:
            print("Error: Remote name and branch name are required for push command.")
    elif args.command == "remote-add":
        if args.remote and args.url:
            git_remote_add(args.remote, args.url)
        else:
            print("Error: Remote name and URL are required for remote-add command.")
    elif args.command == "remote-view":
        git_remote_view()
    elif args.command == "current-branch":
        git_current_branch()
    else:
        print("Unknown command")


if __name__ == "__main__":
    main()


# 筆記:
# 初始化 Git 儲存庫：python .\helpers\git_helpers.py init
# 添加所有文件：python .\helpers\git_helpers.py add
# 提交變更：python .\helpers\git_helpers.py commit -m "Your commit message"

# 重命名分支為 main：python .\helpers\git_helpers.py branch -b main --rename
# 創建新分支：python .\helpers\git_helpers.py branch -b new_branch_name
# 刪除分支：python .\helpers\git_helpers.py branch -b branch_to_delete --delete
# 切換到分支：python .\helpers\git_helpers.py checkout -b branch_name
# 查看當前分支：python .\helpers\git_helpers.py current-branch

# 查看遠端倉庫：python .\helpers\git_helpers.py remote-view
# 添加遠端倉庫：python .\helpers\git_helpers.py remote-add -r origin --url <remote_url>
# 推送分支到遠端：python .\helpers\git_helpers.py push -r origin -b main
# 強制推送分支到遠端：python .\helpers\git_helpers.py push -r origin -b main --force