import requests
import utils


def fetch_commits(repo_id, author, n_days, token):
    """
    Fetch commits from a GitLab repository filtered by author and date.

    Parameters:
    repo_id (str): The ID of the GitLab repository.
    author (str): The username of the author of the commits.
    n_days (int): The number of days in the past to retrieve commits from.
    token (str): GitLab personal access token.

    Returns:
    list: A list of commits.
    """
    # Use the n_days_ago function from utils to calculate the since date
    since_date = utils.n_days_ago(n_days)

    # Format the date for GitLab API using the format_date_for_gitlab function
    formatted_since_date = utils.format_date_for_gitlab(since_date)

    # GitLab API endpoint for listing repository commits
    url = f"https://gitlab.com/api/v4/projects/{repo_id}/repository/commits"

    # Headers including the private token for authentication
    headers = {
        'Authorization': f'Bearer {token}'
    }

    # Parameters for the API request
    params = {
        'since': formatted_since_date,
        'author': author
    }

    # Sending a GET request to the GitLab API
    response = requests.get(url, headers=headers, params=params)

    # Handling potential errors
    if response.status_code != 200:
        raise Exception(f"GitLab API Error: {response.status_code} - {response.json().get('message', '')}")

    # Return the list of commits
    return response.json()


def get_commit_changes(repo_id, commit_id, token):
    """
    Fetch the changes of a specific commit in a GitLab repository.

    Parameters:
    repo_id (str): The ID of the GitLab repository.
    commit_id (str): The ID of the commit.
    token (str): GitLab personal access token.

    Returns:
    dict: A dictionary containing the changes made in the commit.
    """
    # GitLab API endpoint for getting commit diffs
    url = f"https://gitlab.com/api/v4/projects/{repo_id}/repository/commits/{commit_id}/diff"

    # Headers including the private token for authentication
    headers = {
        'Authorization': f'Bearer {token}'
    }

    # Sending a GET request to the GitLab API
    response = requests.get(url, headers=headers)

    # Handling potential errors
    if response.status_code != 200:
        raise Exception(f"GitLab API Error: {response.status_code} - {response.json().get('message', '')}")

    # Return the commit changes
    return response.json()
