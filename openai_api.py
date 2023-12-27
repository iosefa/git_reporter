import openai


def _get_completion(prompt, model="gpt-4"):
    messages = [{"role": "user", "content": prompt}]
    response = openai.ChatCompletion.create(
        model=model,
        messages=messages,
        temperature=0
    )
    return response.choices[0].message["content"]


def _summarize_diffs(text):
    return f"""
    Your task is to generate a summary and explanation of the work done in the git diffs provided. You need to 
    understand what sort of changes were made and infer what work was done. These summaries will be used to 
    report the activity of developers. As a bonus, try to infer how much time all this work took. 

    Summarize and explain the diffs below, delimited by triple backticks

    Section: ```{text}```
    """


def summarize_changes(text, api_key):
    openai.api_key = api_key
    try:
        prompt = _summarize_diffs(text)
        summary = _get_completion(prompt, model='gpt-4')
        return summary
    except Exception as e:
        raise Exception(f"OpenAI API Error: {e}")



