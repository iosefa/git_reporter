import os

# Configuration for GitLab API
GITLAB_API_TOKEN = os.getenv('GITLAB_API_TOKEN')
GITLAB_REPO_IDS = ['20889975', '25568234']
GITLAB_USER = os.getenv('GITLAB_USER')
GITLAB_BRANCH = 'master'
DAYS_BACK = 3

# Configuration for OpenAI API
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
OPENAI_MODEL = "gpt-3.5-turbo-1106"

# Configuration for discord
DISCORD_BOT_TOKEN = os.getenv('DISCORD_BOT_TOKEN')
DISCORD_CHANNEL_ID = os.getenv('DISCORD_CHANNEL_ID')

# app config
USE_DIFF = False
USE_MESSAGES = True
WRITE_SUMMARIES = False
REPOS = {
    '20889975': 'Server',
    '25568234': 'Frontend'
}
