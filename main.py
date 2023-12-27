from datetime import datetime, timedelta
from dotenv import load_dotenv

load_dotenv()

import gitlab_api
import openai_api
import config


def main():
    try:
        start_date = (datetime.now() - timedelta(days=config.DAYS_BACK)).strftime("%Y-%m-%d")
        today_date = datetime.now().strftime("%Y-%m-%d")

        for repo_id in config.GITLAB_REPO_IDS:
            print(f"Fetching commits from GitLab repository: {repo_id}")
            commits = gitlab_api.fetch_commits(
                repo_id=repo_id,
                author=config.GITLAB_USER,
                n_days=config.DAYS_BACK,
                token=config.GITLAB_API_TOKEN
            )

            # Fetch and concatenate commit diffs
            diffs = []
            for commit in commits:
                commit_diff = gitlab_api.get_commit_changes(repo_id, commit['id'], config.GITLAB_API_TOKEN)
                formatted_diff = f"Commit ID: {commit['id']}\nDiff: {commit_diff}\n"
                diffs.append(formatted_diff)
            formatted_diffs = "\n".join(diffs)

            # Generate summary using OpenAI
            print("Generating summary with OpenAI...")
            summary = openai_api.summarize_changes(
                text=formatted_diffs,
                api_key=config.OPENAI_API_KEY
            )

            # Write summary to file
            file_name = f"{config.GITLAB_USER}_{start_date}_{today_date}_{repo_id}_summary.txt"
            with open(file_name, 'w') as file:
                file.write(summary)
            print(f"Summary written to {file_name}")

    except Exception as e:
        print(f"An error occurred: {e}")


if __name__ == "__main__":
    main()
