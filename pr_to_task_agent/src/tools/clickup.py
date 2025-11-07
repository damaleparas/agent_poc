import requests
from langchain.tools import tool
from src.config import settings

@tool
def create_clickup_task(task_name: str, description: str) -> str:
    """Creates a new task in ClickUp and returns the task's URL."""
    print(f"\n--- TOOL: Creating ClickUp Task ---")
    print(f"Task Name: {task_name}")

    url = f"https://api.clickup.com/api/v2/list/{settings.CLICKUP_LIST_ID}/task"
    
    headers = {
        "Authorization": settings.CLICKUP_TOKEN,
        "Content-Type": "application/json"
    }
    
    data = {
        "name": task_name,
        "description": description,
        "assignees": [
            settings.CLICKUP_ASSIGNEE_ID
        ]
        # "status": "Open" # Or any status you prefer
    }

    try:
        response = requests.post(url, headers=headers, json=data)
        response.raise_for_status() # Raises an HTTPError for bad responses
        
        task_url = response.json()['url']
        print(f"Task created: {task_url}")
        return task_url
    except requests.exceptions.HTTPError as e:
        print(f"Error creating ClickUp task: {e.response.text}")
        return f"Error: {e.response.text}"
    except Exception as e:
        print(f"An error occurred: {e}")
        return f"Error: {e}"