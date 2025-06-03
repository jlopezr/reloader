# GitHub Repository Checker

This Python script checks for new commits, tags, or releases in a specified GitHub repository at regular intervals. If a new commit, tag, or release is detected, it can execute a specified command.

## Configuration

The script uses a configuration file (`config.json`) to specify the repository details, delay between checks, and the command to execute when a new commit, tag, or release is detected.

### Example `config.json`

```json
{
    "repo": "jlopezr/ysh",
    "delay": 60,
    "command": "echo 'New commit detected!'"
}
```

### Configuration Options

- `repo`: The GitHub repository to check. Format: `owner/repo`.
- `delay`: The delay between checks in seconds.
- `command`: The command to execute when a new commit, tag, or release is detected.

## Usage

1. Install the required Python packages:

```bash
pip install requests
```

2. Create a `config.json` file with the required configuration options.

3. Run the script:

```bash
python github_checker.py
```

The script will check for new commits, tags, or releases in the specified GitHub repository at regular intervals. If a new commit, tag, or release is detected, it will execute the specified command.