import subprocess
import os

# ======= Configuration =======
project_path = r'F:\python'  # Your local project path
github_repo = 'https://github.com/Priyanka2903184/cybersecurity'  # Your GitHub repo link
commit_message = "Automated sync: Added/Removed folders and files with confirmation"
# =============================

os.chdir(project_path)

# Step 1: Git Init and Remote Setup
try:
    subprocess.run(['git', 'rev-parse', '--is-inside-work-tree'], check=True, stdout=subprocess.PIPE)
except subprocess.CalledProcessError:
    subprocess.run(['git', 'init'])
    print("Git initialized.")

remotes = subprocess.check_output(['git', 'remote'], text=True).splitlines()
if 'origin' not in remotes:
    subprocess.run(['git', 'remote', 'add', 'origin', github_repo])
    print("Remote origin added.")

branches = subprocess.check_output(['git', 'branch'], text=True)
if 'main' not in branches:
    subprocess.run(['git', 'branch', '-M', 'main'])

# Step 2: Get Tracked Files and Folders from Git
tracked_items = subprocess.check_output(['git', 'ls-files'], text=True).splitlines()
tracked_set = set(tracked_items)
tracked_folders = set(os.path.dirname(f).replace("\\", "/") for f in tracked_items if "/" in f)

# Step 3: Collect Local Folders, Excluding .git and Hidden
local_folders = set()
for root, dirs, _ in os.walk(project_path):
    dirs[:] = [d for d in dirs if not d.startswith('.') and d != '.git']
    for d in dirs:
        folder_path = os.path.relpath(os.path.join(root, d), project_path)
        local_folders.add(folder_path.replace("\\", "/"))

# Step 4: Handle Deleted Folders First
deleted_folders = tracked_folders - local_folders
for folder in sorted(deleted_folders, reverse=True):
    print(f"\n⚠ Folder '{folder}' is deleted locally.")
    confirm = input(f"Do you want to remove '{folder}' from GitHub? (yes/no): ").strip().lower()
    if confirm == 'yes':
        subprocess.run(['git', 'rm', '-r', folder])
        print(f"Deleted folder from GitHub: {folder}")
    else:
        print(f"Skipped deleting folder: {folder}")

# Step 5: Re-collect Local Files and Folders After Deletions
local_files = set()
local_folders.clear()

for root, dirs, files in os.walk(project_path):
    dirs[:] = [d for d in dirs if not d.startswith('.') and d != '.git']
    for d in dirs:
        folder_path = os.path.relpath(os.path.join(root, d), project_path)
        local_folders.add(folder_path.replace("\\", "/"))
    for f in files:
        if not f.startswith('.'):
            file_path = os.path.relpath(os.path.join(root, f), project_path)
            local_files.add(file_path.replace("\\", "/"))

# Step 6: Add New Folders
new_folders = local_folders - tracked_folders
for folder in sorted(new_folders):
    subprocess.run(['git', 'add', folder])
    print(f"Added new folder: {folder}")

# Step 7: Handle New and Deleted Files
new_files = local_files - tracked_set
deleted_files = tracked_set - local_files

for file in sorted(new_files):
    subprocess.run(['git', 'add', file])
    print(f"Added new file: {file}")

# Use deleted_folders again to avoid duplicate prompts
deleted_folders = tracked_folders - local_folders

for file in sorted(deleted_files):
    parent_folder = os.path.dirname(file).replace("\\", "/")

    # Skip files inside already deleted folders
    if parent_folder in deleted_folders:
        continue

    print(f"\n⚠ File '{file}' is deleted locally.")
    confirm = input(f"Do you want to remove '{file}' from GitHub? (yes/no): ").strip().lower()
    if confirm == 'yes':
        subprocess.run(['git', 'rm', file])
        print(f"Deleted file from GitHub: {file}")
    else:
        print(f"Skipped deleting file: {file}")

# Step 8: Commit and Push Changes
status = subprocess.check_output(['git', 'status', '--porcelain'], text=True)
if status.strip():
    subprocess.run(['git', 'commit', '-m', commit_message])
    subprocess.run(['git', 'push', '-u', 'origin', 'main'])
    print("\n✔ All changes synced to GitHub.")
else:
    print("\nNo changes to commit.")
