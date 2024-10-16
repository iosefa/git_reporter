# Git Reporter

This tool reads and summarizes your git commits and JIRA activity for a project and generates summary using OpenAI's API.

## Installation

- Clone the repository: `git clone iosefa/gitreporter`
- Install necessary libraries/packages as mentioned in `requirements.txt` using pip : `pip install -r requirements.txt`
- Set the correct environmental variables by copying the example file with `cp .env-example .env` and filling in the missing values

## Usage

Once all the above are defined, run the main.py script with the following command:

```bash
python main.py <author> <since> [until] [filename] <git_directory>
```

### Command-Line Arguments:

	•	<author>: The Git author whose commits you want to report on (required).
	•	<since>: The start date for the report period (in YYYY-MM-DD format, required).
	•	[until]: The end date for the report period (in YYYY-MM-DD format, optional, defaults to the present day).
	•	[filename]: The name of the output markdown file where the report will be saved (optional, defaults to report.md).
    •	<git_directory>: The path to the Git repository directory where the script will run the log command (optional, defaults to the current directory).

### Example:

To generate a report for the author “iosefa” from September 1, 2024, to September 30, 2024, and save it as september_report.md, run:

```bash
python main.py iosefa 2024-09-01 2024-09-30 september_report.md /path/to/git/repository
```

This will generate a summary of work done for the git user iosefa between 2024-09-01 and 2024-09-30 in the Git repository located at /path/to/git/repository, and save the report to a file named september_report.md. If you don’t specify an end date (until), the script will use the current date by default.

## Contributing 

We welcome contributions to the GitLab Reporter project! If you have suggestions for improvements or new features, feel free to submit a pull request or open an issue. For major changes, please open an issue first to discuss what you would like to change.

## License 

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details.

## Contact 

If you have any questions or feedback, please contact me at [ipercival@gmail.com](mailto:ipercival@gmail.com).
