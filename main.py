import argparse
import os
import subprocess
import requests
from requests.auth import HTTPBasicAuth
from openai import OpenAI
from dotenv import load_dotenv


load_dotenv()


OPENAI_KEY = os.getenv('OPENAI_KEY')
OPENAI_MODEL = os.getenv('OPENAI_MODEL', 'gpt-3.5-turbo-1106')

JIRA_API_TOKEN = os.getenv('JIRA_API_TOKEN')
JIRA_EMAIL = os.getenv('JIRA_EMAIL')
JIRA_DOMAIN = os.getenv('JIRA_DOMAIN')
PROJECT_KEY = os.getenv('PROJECT_KEY')

client = OpenAI(api_key=OPENAI_KEY)


def _get_completion(prompt, model=OPENAI_MODEL):
    """
    Retrieves the completion message from the OpenAI chat model.
    """
    messages = [{"role": "user", "content": prompt}]
    response = client.chat.completions.create(
        model=model,
        messages=messages,
        temperature=0
    )
    response_message = response.choices[0].message.content
    return response_message


def fetch_git_log(author, since, until=None, git_dir='.'):
    """
    Fetch git log for a specific author between a given time period from a local Git repository.
    """
    git_command = [
        'git', 'log',
        f'--author={author}',
        f'--since={since}',
        '--all'
    ]

    if until:
        git_command.append(f'--until={until}')

    print(f"Running git command: {' '.join(git_command)}")

    try:
        result = subprocess.run(git_command, cwd=git_dir, capture_output=True, text=True, check=True)
        return result.stdout

    except subprocess.CalledProcessError as e:
        print(f"Error while running git command: {e.stderr}")
        return None


def fetch_jira_issues(jql_query):
    """
    Fetch issues from JIRA using JQL.
    """
    url = f"https://{JIRA_DOMAIN}/rest/api/3/search"
    headers = {
        "Content-Type": "application/json"
    }
    response = requests.get(url, headers=headers, auth=HTTPBasicAuth(JIRA_EMAIL, JIRA_API_TOKEN), params={"jql": jql_query})
    if response.status_code == 200:
        return response.json()['issues']
    else:
        print(f"Error fetching JIRA issues: {response.status_code} - {response.text}")
        return None


def get_jira_issues_by_status(start_date, end_date, assignee_email):
    """
    Get JIRA issues created, closed, in DEVELOP, and in STAGING for a specific assignee and time period.
    """
    created_query = f'project = {PROJECT_KEY} AND assignee = "{assignee_email}" AND created >= "{start_date}" AND created <= "{end_date}"'
    closed_query = f'project = {PROJECT_KEY} AND assignee = "{assignee_email}" AND status = Closed AND resolved >= "{start_date}" AND resolved <= "{end_date}"'
    develop_query = f'project = {PROJECT_KEY} AND assignee = "{assignee_email}" AND status = "DEVELOP" AND updated >= "{start_date}" AND updated <= "{end_date}"'
    staging_query = f'project = {PROJECT_KEY} AND assignee = "{assignee_email}" AND status = "STAGING" AND updated >= "{start_date}" AND updated <= "{end_date}"'

    issues_created = fetch_jira_issues(created_query)
    issues_closed = fetch_jira_issues(closed_query)
    issues_in_develop = fetch_jira_issues(develop_query)
    issues_in_staging = fetch_jira_issues(staging_query)

    return {
        "created": issues_created,
        "closed": issues_closed,
        "develop": issues_in_develop,
        "staging": issues_in_staging
    }


def generate_summary_from_commit_messages(commit_log):
    """
    Generate a detailed summary of the work done based on the commit messages using OpenAI's API.
    """
    prompt = f"""
    You are a professional summarizer. I will provide you with a list of commit messages from a Git log. 
    Please generate a structured report that summarizes the work done. Use the following structure:

    1. **Overview**: A high-level summary of the work done during the specified period.
    2. **Key Features Implemented**: A list of the most significant features or changes introduced.
    3. **Bug Fixes**: A summary of bugs that were fixed.
    4. **Refactorings**: Changes made to improve code structure or performance without adding new functionality.
    5. **Technical Debt Addressed**: Areas of the codebase that were cleaned up or improved to reduce technical debt.
    6. **Testing and Documentation**: Updates related to tests and documentation.

    Here is the commit log:
    {commit_log}

    Please provide a detailed summary following this structure.
    """

    try:
        return _get_completion(prompt)
    except Exception as e:
        print(f"Error while generating summary: {e}")
        return None


def create_detailed_report(author, since, until=None, git_dir='.'):
    """
    Fetch git log, JIRA issues, and generate a comprehensive report.
    """
    git_log = fetch_git_log(author, since, until, git_dir)
    if not git_log:
        return "No git log found."

    jira_issues = get_jira_issues_by_status(since, until, JIRA_EMAIL)

    git_summary = generate_summary_from_commit_messages(git_log)

    report = f"""
    ### Comprehensive Report for {author} from {since} to {until or 'Present'}:

    #### **Git Log Summary:**
    {git_summary}

    #### **JIRA Issues:**

    - **Issues Created:**
    {format_jira_issues(jira_issues['created'])}

    - **Issues Closed (Merged into Production):**
    {format_jira_issues(jira_issues['closed'])}

    - **Issues in DEVELOP Branch:**
    {format_jira_issues(jira_issues['develop'])}

    - **Issues in STAGING:**
    {format_jira_issues(jira_issues['staging'])}
    """

    return report


def format_jira_issues(issues):
    """
    Format JIRA issues for the report.
    """
    if not issues:
        return "No issues found."

    issue_list = []
    for issue in issues:
        issue_list.append(
            f"- {issue['key']}: {issue['fields']['summary']} (Status: {issue['fields']['status']['name']})"
        )

    return "\n".join(issue_list)


def write_report_to_md(report, filename="report.md"):
    """
    Write the generated report to a markdown (.md) file in the reports directory.
    """
    reports_dir = "reports"
    if not os.path.exists(reports_dir):
        os.makedirs(reports_dir)

    filepath = os.path.join(reports_dir, filename)

    with open(filepath, "w") as file:
        file.write(report)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Generate a detailed report from Git and JIRA data.")

    parser.add_argument("author", type=str, help="Author of the Git commits")
    parser.add_argument("since", type=str, help="Start date for the report period (YYYY-MM-DD)")
    parser.add_argument("until", type=str, nargs="?", default=None,
                        help="End date for the report period (YYYY-MM-DD, optional)")
    parser.add_argument("filename", type=str, nargs="?", default="report.md", help="Filename to save the report as")
    parser.add_argument("git_dir", type=str, nargs="?", default=".", help="Git directory to summarize commits for")

    args = parser.parse_args()

    report = create_detailed_report(args.author, args.since, args.until, args.git_dir)
    write_report_to_md(report, args.filename)

    print(f"Report saved to {args.filename}")
