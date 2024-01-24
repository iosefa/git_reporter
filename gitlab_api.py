import requests


def fetch_commits(repo_id, branch, since_date, token, all_commits=True, per_page=100):
    """
    Fetch all commits from a GitLab repository within a date range, across all pages.

    Parameters:
    repo_id (str): The ID of the GitLab repository.
    branch (str): The branch to fetch commits from.
    since_date (str): The start date for fetching commits (ISO 8601 format).
    until_date (str): The end date for fetching commits (ISO 8601 format).
    token (str): GitLab personal access token.
    all_commits (bool): Fetch all commits if True. Defaults to True.
    per_page (int): Number of commits per page. Defaults to 100.

    Returns:
    list: A list of all commits within the date range.
    """
    all_commits_list = []
    page = 1
    while True:
        url = f"https://gitlab.com/api/v4/projects/{repo_id}/repository/commits"
        headers = {'Authorization': f'Bearer {token}'}
        params = {
            'ref_name': branch,
            'since': since_date,
            'all': all_commits,
            'per_page': per_page,
            'page': page
        }

        response = requests.get(url, headers=headers, params=params)

        if response.status_code != 200:
            raise Exception(f"GitLab API Error: {response.status_code} - {response.json().get('message', '')}")

        commits = response.json()
        if not commits:
            break
        all_commits_list.extend(commits)
        page += 1

    return all_commits_list


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
