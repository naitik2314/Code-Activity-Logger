# Code Activity Logger

## Overview
Code Activity Logger is a **Python-based automation tool** designed to track, summarize, and log code changes across projects. It leverages **Google Gemini AI** to generate intelligent summaries of modifications and maintains a structured changelog. The tool enables seamless backup of project files and **automatically commits updates to a Git repository** for version control. It runs automatically at midnight to detect and log changes without manual intervention.

## Features
- **Automated Code Change Detection**: Compares current and previous project versions to identify modifications.
- **AI-Powered Summaries**: Uses Google Gemini API to generate concise summaries of code changes.
- **Version Control Integration**: Updates and pushes the changelog to a Git repository.
- **Backup System**: Creates daily backups of specified project directories.
- **Automatic Execution**: The script runs automatically at midnight every day to check for code changes and update the changelog.

---

## Installation

### 1. Clone the Repository
```sh
git clone https://github.com/naitik2314/Code-Activity-Logger.git
cd Code-Activity-Logger
```

### 2. Set Up a Virtual Environment
**Option 1: Using Python venv**
```sh
python3 -m venv env
source env/bin/activate  # On Windows, use `env\Scripts\activate`
```

**Option 2: Using Conda**
```sh
conda create --name code_logger_env python=3.9
conda activate code_logger_env
```

### 3. Install Dependencies
```sh
pip install -r requirements.txt
```

### Configuration

#### Set Up Environment Variables
Create a `.env` file in the root directory and add your Google Gemini API key:
```
GEMINI_API_KEY=your_api_key_here
```

#### Project Directories & Backup Locations
Update `main.py` to specify the directories being tracked and where backups should be stored:
```python
PROJECT_DIRECTORIES = ['/path/to/your/project']
BACKUP_LOCATION = '/path/to/your/backup/directory'
```

### Initialize Git (If Not Already Set Up)
```sh
git init
git remote add origin https://github.com/yourusername/yourrepository.git
```

### Set Up Changelog Repository
1. Create a new repository on GitHub named `changelog or whatever suits you`. 
2. Clone the repository to your local system:
    ```sh
    git clone https://github.com/yourusername/changelog.git
    cd changelog
    ```
3. Create an empty `changelog.md` file:
    ```sh
    touch changelog.md
    git add changelog.md
    git commit -m "Initial commit with changelog.md"
    git push origin main
    ```

### Set Up GitHub Personal Access Token (PAT)
1. Go to GitHub Settings > Developer settings > Personal access tokens.
2. Click on "Generate new token".
3. Select the scopes you need (e.g., `repo` for full control of private repositories).
4. Generate the token and copy it.
5. Add the token to your `.env` file:
    ```
    GITHUB_PAT=your_personal_access_token_here
    ```

## Usage

To run the tool, simply execute:
```sh
python main.py
```

To run the unit tests:
```sh
python -m unittest test_script.py
```

## Project Structure

```
/Code-Activity-Logger
│── main.py              # Main script for logging and summarizing changes
│── test_script.py       # Unit tests for validation
│── requirements.txt     # Dependencies
│── .env                 # Environment variables (not included in repo)
│── README.md            # Project documentation
│── changelog.md         # Maintains a log of detected changes
```

## Dependencies

- Python 3.9 or higher (Required for Google Gemini)
- google-generativeai (Google Gemini API)
- python-dotenv (Environment variable management)

To install manually:
```sh
pip install google-generativeai python-dotenv
```

## Changelog

All changes are logged in `changelog.md`, which is automatically updated and pushed to GitHub when changes are detected.

## License

This project is open-source and available under the MIT License.

## Contributing

Contributions are welcome! Please submit a pull request with detailed explanations of your changes.

## Author

- Your Name
- LinkedIn: [Naitik Shah](https://www.linkedin.com/in/naitik-shah-49baba1a1/)
- GitHub: [naitik2314](https://github.com/naitik2314)
