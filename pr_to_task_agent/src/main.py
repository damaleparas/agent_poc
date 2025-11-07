import uvicorn
from fastapi import FastAPI, Request, BackgroundTasks, HTTPException
from pydantic import BaseModel, Field
from typing import Optional # <-- Make sure this is imported

# Import the compiled graph from our graph.py file
from src.graph import app_runnable, PRWorkflowState
from src.config import settings

# --- FastAPI App ---
app = FastAPI(
    title=settings.PROJECT_NAME,
    description="Receives GitHub webhooks to trigger a LangGraph workflow."
)

# --- Pydantic Models for Webhook Payload ---
class PRHead(BaseModel):
    ref: str  # The branch name

class PullRequest(BaseModel):
    title: str
    html_url: str = Field(..., alias='html_url')
    head: PRHead
    body: Optional[str] = None  # <--- ADD THIS LINE

class GitHubWebhookPayload(BaseModel):
    action: str
    pull_request: PullRequest = Field(..., alias='pull_request')

# --- Background Task ---
def run_pr_workflow(payload: GitHubWebhookPayload):
    """The function that will be run in the background."""
    print(f"\n--- BACKGROUND TASK: Starting workflow for PR '{payload.pull_request.title}' ---")
    
    initial_state = {
        "pr_title": payload.pull_request.title,
        "pr_url": payload.pull_request.html_url,
        "pr_branch": payload.pull_request.head.ref,
        "pr_body": payload.pull_request.body  # <--- ADD THIS LINE
    }
    
    try:
        final_state = app_runnable.invoke(initial_state)
        print(f"\n--- BACKGROUND TASK: Workflow complete ---")
        print(f"Final State: {final_state}")
    except Exception as e:
        print(f"\n--- BACKGROUND TASK: Workflow FAILED ---")
        print(f"Error: {e}")
        # Optionally, you could try to post a "failed" comment back to the PR here

# --- Webhook Endpoint ---
@app.post("/webhook/github")
async def handle_github_webhook(
    payload: GitHubWebhookPayload, 
    background_tasks: BackgroundTasks
):
    """
    Receives the GitHub 'pull_request' webhook.
    """
    print(f"\n--- WEBHOOK RECEIVED: Action '{payload.action}' ---")
    
    if payload.action != "opened":
        return {"status": "ignored", "reason": f"action was '{payload.action}', not 'opened'"}
    
    # Run the graph in the background to send an immediate 200 OK
    background_tasks.add_task(run_pr_workflow, payload)
    
    return {"status": "queued", "detail": "PR workflow added to background tasks."}

@app.get("/")
def read_root():
    return {"hello": f"{settings.PROJECT_NAME} is running."}

# --- Run the server ---
if __name__ == "__main__":
    print(f"Starting {settings.PROJECT_NAME} server...")
    uvicorn.run(app, host="0.0.0.0", port=8000)