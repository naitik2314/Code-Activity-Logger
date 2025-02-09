import os
import shutil
import subprocess
import difflib
import logging
from datetime import datetime, timedelta
import time
import platform
import filecmp
from google import genai
from google.genai import types
from dotenv import load_dotenv

load_dotenv()

# Configuration variables
PROJECT_DIRECTORIES = ['/home/naitik/Codes/Code-Activity-Logger']
BACKUP_LOCATION = '/home/naitik/project_backups'
CHANGELOG_FILE = '/home/naitik/Codes/Code-Activity-Logger/changelog.md'
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY") 

if not GEMINI_API_KEY:
    print("Gemini API key not loaded! Add it to the .env file!")

# Logging setup
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Function to compare directories and return a unified diff
def get_project_diff(previous_project_path, current_project_path):
    """
    Compares two versions of a project directory and returns a combined diff
    for all modified files. Uses `diff -ur` on Linux/macOS and Python-based comparison on Windows.
    """
    if not os.path.exists(previous_project_path):
        logging.warning(f"No previous backup found for {current_project_path}. Skipping diff.")
        return None

    diff_summary = []

    # Detect OS
    system_type = platform.system()

    if system_type in ["Linux", "Darwin"]:  # Darwin is macOS
        try:
            command = f"diff -ur {previous_project_path} {current_project_path}"
            result = subprocess.run(command, shell=True, capture_output=True, text=True)
            if result.stdout:
                return result.stdout.strip()
        except Exception as e:
            logging.error(f"Error running `diff -ur`: {e}")

    # If Windows or `diff -ur` fails, use Python's `filecmp` and `difflib`
    dcmp = filecmp.dircmp(previous_project_path, current_project_path)

    added_files = dcmp.right_only
    removed_files = dcmp.left_only
    modified_files = dcmp.diff_files

    if added_files:
        diff_summary.append(f"Added files: {', '.join(added_files)}")
    if removed_files:
        diff_summary.append(f"Removed files: {', '.join(removed_files)}")

    # Generate diffs for modified files
    for file in modified_files:
        old_file = os.path.join(previous_project_path, file)
        new_file = os.path.join(current_project_path, file)

        try:
            with open(old_file, "r") as f1, open(new_file, "r") as f2:
                diff = difflib.unified_diff(
                    f1.readlines(), f2.readlines(), fromfile=old_file, tofile=new_file
                )
                file_diff = ''.join(diff)
                if file_diff.strip():
                    diff_summary.append(f"Changes in {file}:\n{file_diff}")
        except Exception as e:
            logging.error(f"Error comparing {file}: {e}")

    return "\n".join(diff_summary) if diff_summary else None


# Function to summarize changes using Gemini API
# Initialize Gemini API client
client = genai.Client(api_key=GEMINI_API_KEY)

def summarize_changes(diff_text):
    """
    Summarizes code changes using the Gemini API.
    """
    if not diff_text:
        return None

    try:
        response = client.models.generate_content(
            model="gemini-2.0-flash",
            contents=[f"Summarize these code changes:\n{diff_text}"],
            config=types.GenerateContentConfig(
                max_output_tokens=200,  # Adjust based on expected summary length
                temperature=0.3  # Low temperature for concise and factual summaries
            )
        )
        return response.text.strip()
    
    except Exception as e:
        logging.error(f"Error summarizing changes: {e}")
        return "Error generating summary."


# Function to create daily backups
def backup_projects():
    """
    Backs up all project directories to the backup location, organized by date.
    """
    today = datetime.now().strftime("%Y-%m-%d")
    backup_dir = os.path.join(BACKUP_LOCATION, today)

    if os.path.exists(backup_dir):
        logging.info(f"Backup directory for {today} already exists. Skipping backup.")
        return

    os.makedirs(backup_dir, exist_ok=True)

    for project_dir in PROJECT_DIRECTORIES:
        project_name = os.path.basename(project_dir)
        dest_dir = os.path.join(backup_dir, project_name)
        try:
            shutil.copytree(project_dir, dest_dir, dirs_exist_ok=True)
            logging.info(f"Successfully backed up {project_name} to {dest_dir}")
        except Exception as e:
            logging.error(f"Error backing up {project_name}: {e}")

# Function to detect changes and summarize them
def detect_and_summarize_changes():
    """
    Detects changes in project directories, summarizes them using Gemini API,
    and updates the changelog file.
    """
    today = datetime.now().strftime("%Y-%m-%d")
    yesterday = (datetime.now() - timedelta(days=1)).strftime("%Y-%m-%d")
    yesterday_backup_dir = os.path.join(BACKUP_LOCATION, yesterday)

    if not os.path.exists(yesterday_backup_dir):
        logging.warning(f"No backup found for {yesterday}. Skipping change detection.")
        return

    changelog_entries = []

    for project_dir in PROJECT_DIRECTORIES:
        project_name = os.path.basename(project_dir)
        previous_project_path = os.path.join(yesterday_backup_dir, project_name)

        if not os.path.exists(previous_project_path):
            logging.warning(f"Project {project_name} not found in {yesterday}'s backup. Skipping.")
            continue

        diff_output = get_project_diff(previous_project_path, project_dir)

        if diff_output:
            summary = summarize_changes(diff_output)
            changelog_entries.append((today, project_name, summary))
            logging.info(f"Changes detected and summarized for {project_name}")
        else:
            logging.info(f"No changes detected for {project_name}")

    if changelog_entries:
        update_changelog(changelog_entries)
    else:
        logging.info("No changes detected in any project. Changelog not updated.")

# Function to update changelog
def update_changelog(changelog_entries):
    """
    Updates the changelog.md file with summarized change entries.
    """
    try:
        existing_content = ""
        if os.path.exists(CHANGELOG_FILE):
            with open(CHANGELOG_FILE, 'r') as f:
                existing_content = f.read()

        new_entries = "\n".join([f"| {date} | {project} | {summary} |" for date, project, summary in changelog_entries])
        header = "| Date | Project | Summary |\n|---|---|---|\n"
        updated_content = header + new_entries + "\n" + existing_content

        with open(CHANGELOG_FILE, 'w') as f:
            f.write(updated_content)

        logging.info(f"Changelog updated at {CHANGELOG_FILE}")
        commit_and_push_changes()

    except Exception as e:
        logging.error(f"Error updating changelog: {e}")

# Function to commit and push changes
def commit_and_push_changes():
    """
    Commits and pushes the updated changelog to GitHub.
    """
    try:
        date = datetime.now().strftime("%Y-%m-%d")
        subprocess.run(["git", "-C", os.path.dirname(CHANGELOG_FILE), "add", CHANGELOG_FILE])
        subprocess.run(["git", "-C", os.path.dirname(CHANGELOG_FILE), "commit", "-m", f"Updated changelog for {date}"])
        subprocess.run(["git", "-C", os.path.dirname(CHANGELOG_FILE), "push"])
        logging.info("Changelog committed and pushed successfully.")
    except Exception as e:
        logging.error(f"Error committing/pushing changes: {e}")

# Main execution loop
def main():
    while True:
        now = datetime.now()
        midnight = now.replace(hour=0, minute=0, second=0, microsecond=0) + timedelta(days=1)
        time.sleep((midnight - now).seconds)
        backup_projects()
        detect_and_summarize_changes()

if __name__ == "__main__":
    main()
