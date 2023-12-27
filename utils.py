from datetime import datetime, timedelta


def format_date_for_gitlab(date):
    """
    Format a datetime object into a string suitable for GitLab API queries.

    Parameters:
    date (datetime): The datetime object to format.

    Returns:
    str: A string representing the formatted date.
    """
    return date.isoformat()


def n_days_ago(n):
    """
    Calculate the date 'n' days ago from the current date.

    Parameters:
    n (int): Number of days to subtract from the current date.

    Returns:
    datetime: A datetime object representing the date 'n' days ago.
    """
    return datetime.now() - timedelta(days=n)


def clean_and_format_text(text):
    """
    Perform basic cleaning and formatting on a text string.

    Parameters:
    text (str): The text to clean and format.

    Returns:
    str: The cleaned and formatted text.
    """
    # Example: Strip leading/trailing whitespace and replace newlines with spaces
    return text.strip().replace('\n', ' ')
