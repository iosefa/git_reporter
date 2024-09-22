import os

# Configuration for GitLab API
GITLAB_API_TOKEN = os.getenv('GITLAB_API_TOKEN')
GITLAB_REPO_IDS = [item.strip() for item in os.getenv('GITLAB_REPO_IDS').split(',')]
GITLAB_USER = os.getenv('GITLAB_USER')
GITLAB_BRANCH = os.getenv('GITLAB_BRANCH', 'main')
DAYS_BACK = 3

# Configuration for OpenAI API
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
OPENAI_MODEL = os.getenv('OPENAI_MODEL', "gpt-3.5-turbo-1106")

# Configuration for discord
DISCORD_BOT_TOKEN = os.getenv('DISCORD_BOT_TOKEN')
DISCORD_CHANNEL_ID = os.getenv('DISCORD_CHANNEL_ID')

# app config
USE_DIFF = False
USE_MESSAGES = True
WRITE_SUMMARIES = False
REPOS = {
    'your_repo_id': 'your_repo_name',
    ...
}
