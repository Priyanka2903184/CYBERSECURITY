import subprocess
import os

# ======= Configuration =======
project_path = r'D:\COLLEGE PROJECTS\Cyber Project'   # Your project path
github_repo = 'https://github.com/Priyanka2903184/CYBERSECURITY'  # Your GitHub repo link
commit_message = "Automated sync: Added new files and removed deleted files"
# =============================

os.chdir(project_path)

# Step 1: Initialize Git (only if not already done)
try:
    subprocess.run(['git', 'rev-parse', '--is-inside-work-tree'], check=True, stdout=subprocess.PIPE)
    print("Git already initialized.")
except subprocess.CalledProcessError:
    subprocess.run(['git', 'init'])
    print("Git initialized.")

# Step 2: Connect to GitHub if remote not set
remotes = subprocess.check_output(['git', 'remote'], text=True).splitlines()
if 'origin' not in remotes:
    subprocess.run(['git', 'remote', 'add', 'origin', github_repo])
    print("Remote origin added.")
else:
    print("Remote origin already set.")

# Step 3: Check branch & create 'main' if needed
branches = subprocess.check_output(['git', 'branch'], text=True)
if 'main' not in branches:
    subprocess.run(['git', 'branch', '-M', 'main'])
    print("Main branch set.")

# Step 4: Sync Files (All Files, Any Extension)
tracked_files = subprocess.check_output(['git', 'ls-files'], text=True).splitlines()

# Recursively collect all files
all_files = []
for root, dirs, files in os.walk(project_path):
    dirs[:] = [d for d in dirs if d != '.git']  # Skip .git folder
    for f in files:
        if not f.startswith('.'):  # Ignore hidden files if needed
            file_path = os.path.relpath(os.path.join(root, f), project_path)
            all_files.append(file_path.replace("\\", "/"))  # Normalize paths for Git

new_files = [f for f in all_files if f not in tracked_files]
deleted_files = [f for f in tracked_files if f not in all_files]

# Add new files
for file in sorted(new_files):
    subprocess.run(['git', 'add', file])
    print(f"Added new file: {file}")

# Remove deleted files with confirmation
for file in sorted(deleted_files):
    print(f"\n⚠ File '{file}' is deleted locally.")
    confirm = input(f"Do you want to remove '{file}' from GitHub? (yes/no): ").strip().lower()
    if confirm == 'yes':
        subprocess.run(['git', 'rm', file])
        print(f"Deleted file from GitHub: {file}")
    else:
        print(f"Skipped deleting file: {file}")

# Commit and Push if there are changes
status = subprocess.check_output(['git', 'status', '--porcelain'], text=True)

if status.strip():
    subprocess.run(['git', 'commit', '-m', commit_message])
    subprocess.run(['git', 'push', '-u', 'origin', 'main'])
    print("\n✔ All changes pushed to GitHub.")
else:
    print("\nNo changes to commit.")
