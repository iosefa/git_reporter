import time
from datetime import datetime, timedelta
from threading import Thread

import discord_api
import gitlab_api
import openai_api
import config


def main():
    """
    Fetches commits from GitLab repository, generates summary using OpenAI API,
    and writes the summary to a file if specified in the config.

    :return: None
    """
    if config.USE_DIFF == config.USE_MESSAGES and config.USE_DIFF is True:
        raise ValueError("Only one of USE_DIFF and USE_MESSAGES should be True.")
    elif config.USE_DIFF == config.USE_MESSAGES:
        raise ValueError("You must set either USE_DIFF or USE_MESSAGES in config.py")
    try:
        start_date = (datetime.now() - timedelta(days=config.DAYS_BACK)).strftime("%Y-%m-%d")
        today_date = datetime.now().strftime("%Y-%m-%d")
        since_date = (datetime.now() - timedelta(days=config.DAYS_BACK)).isoformat() + 'Z'

        for repo_id in config.GITLAB_REPO_IDS:
            print(f"Fetching commits from GitLab repository: {repo_id}")
            commits = gitlab_api.fetch_commits(
                repo_id=repo_id,
                branch=config.GITLAB_BRANCH,
                since_date=since_date,
                token=config.GITLAB_API_TOKEN
            )
            summary = ''
            if len(commits) == 0:
                summary = f'No commits were made for {config.REPOS[repo_id]}'
            else:
                if config.USE_DIFF:
                    diffs = []

                    for commit in commits:
                        commit_diff = gitlab_api.get_commit_changes(repo_id, commit['id'], config.GITLAB_API_TOKEN)
                        formatted_diff = f"Commit ID: {commit['id']}\nDiff: {commit_diff}\n"
                        diffs.append(formatted_diff)
                    formatted_diffs = "\n".join(diffs)

                    print("Generating summary with OpenAI...")
                    summary = openai_api.summarize_diffs(
                        text=formatted_diffs
                    )

                if config.USE_MESSAGES:
                    messages = []
                    for commit in commits:
                        title = commit['title']
                        message = commit['message']
                        if title != message:
                            formatted_message = f"{title}: {message}"
                        else:
                            formatted_message = f"{message}"
                        messages.append(formatted_message)
                    formatted_messages = "\n\n".join(messages)

                    print("Generating summary with OpenAI...")
                    summary = openai_api.summarize_messages(
                        text=formatted_messages
                    )

            if config.WRITE_SUMMARIES:
                file_name = f"{config.GITLAB_USER}_{start_date}_{today_date}_{repo_id}_summary.txt"
                with open(file_name, 'w') as file:
                    file.write(summary)
                print(f"Summary written to {file_name}")

            discord_api.queue_message(summary, config.GITLAB_USER, config.REPOS[repo_id])

    except Exception as e:
        print(f"An error occurred: {e}")


if __name__ == "__main__":
    discord_thread = Thread(target=discord_api.run_bot)
    discord_thread.start()

    main()

    time.sleep(10)

    discord_api.stop_bot()

    discord_thread.join()
