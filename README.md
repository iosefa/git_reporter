# GitLab Reporter

This tool fetches commits from a GitLab repository for a specified branch and duration, generates summary of the fetched commits using OpenAI's API, and posts the summary into a Discord channel or writes it into a file.

## Installation

- Clone the repository: `git clone iosefa/gitreporter`
- Install necessary libraries/packages as mentioned in `requirements.txt` using pip : `pip install -r requirements.txt`

## Required Configuration

Create a `config.py` file in the project's main directory and define the following:

- `GITLAB_API_TOKEN`: GitLab API token.
- `GITLAB_USER`: GitLab username.
- `GITLAB_BRANCH`: GitLab repository branch to fetch commits from.
- `GITLAB_REPO_IDS`: An array of GitLab repository IDs to monitor.
- `REPOS`: A dictionary mapping repository IDs to repository names.
- `DAYS_BACK`: Number of days back from the current date to fetch commits.
- `USE_DIFF`: Set this to True to generate summary on the basis of commit diffs.
- `USE_MESSAGES`: Set this to True to generate summary on the basis of commit messages.
- `WRITE_SUMMARIES`: Set this to True to save the summary to a .txt file.

> Note: `USE_DIFF` and `USE_MESSAGES` both can't be True at same time.

## Usage

Once all the above are defined, run your `main.py` script with the command: `python main.py`

The program will fetch commits from the specified GitLab repositories and generate a summary depending on your configurations. The summary will then be posted to the configured Discord channel or saved to a .txt file as a summary.

## Contributing 

We welcome contributions to the GitLab Reporter project! If you have suggestions for improvements or new features, feel free to submit a pull request or open an issue. For major changes, please open an issue first to discuss what you would like to change.

## License 

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details.

## Contact 

If you have any questions or feedback, please contact me at [ipercival@gmail.com](mailto:ipercival@gmail.com).
