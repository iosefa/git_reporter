import os

# Configuration for GitLab API
GITLAB_API_TOKEN = os.getenv('GITLAB_API_TOKEN')
GITLAB_REPO_IDS = ['20889975', '25568234']
GITLAB_USER = os.getenv('GITLAB_USER')
DAYS_BACK = 7

# Configuration for OpenAI API
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
