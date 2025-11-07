# 🤖 PR-to-Task Agent

This agent automates project management by:
1.  Triggering on a GitHub PR (via Webhook).
2.  Finding the relevant design spec in Google Drive.
3.  Creating a "Review" task in ClickUp.
4.  Posting a confirmation comment back to the PR.

## 🛠️ Tech Stack
* **Server:** FastAPI
* **Workflow:** LangGraph
* **LLM:** Pluggable - **Google Gemini** or **Anthropic Claude**
* **APIs:** PyGithub, Google API Client, ClickUp (via `requests`)

## 🚀 Setup & Installation

### 1. Clone & Install
```bash
# Clone the repository
git clone <your-repo-url>
cd pr_to_task_agent

# Create and activate a virtual environment
python -m venv venv
source venv/bin/activate  # (or .\venv\Scripts\activate on Windows)

# Install dependencies
pip install -r requirements.txt
```

### 2. API Credentials & Configuration

**a. Create `.env` file:**
Copy the example file.
```bash
cp .env.example .env
```
Now, you must find and fill in the values in your new `.env` file.

**b. Choose Your LLM (`LLM_PROVIDER`):**
* In `.env`, set `LLM_PROVIDER="gemini"` or `LLM_PROVIDER="claude"`.

**c. LLM API Keys:**
* **Gemini (`GOOGLE_API_KEY`):**
    * Go to [Google AI Studio](https://aistudio.google.com/app/apikey).
    * Click "Create API key" and paste it into `.env`.
    * **Note:** This is *different* from your Google Drive key.
* **Claude (`ANTHROPIC_API_KEY`):**
    * Go to the [Anthropic Console](https://console.anthropic.com/account/keys).
    * Create a new key and paste it into `.env`.

**d. GitHub (`GITHUB_TOKEN`):**
* Go to **GitHub > Settings > Developer settings > Personal access tokens > Fine-grained tokens**.
* Generate a new token with **Read & Write** access for **Pull requests**.

**e. ClickUp (`CLICKUP_TOKEN`, `CLICKUP_LIST_ID`, `CLICKUP_ASSIGNEE_ID`):**
* **Token:** Go to **ClickUp > Settings > My Apps > API Token**.
* **List ID:** Open your target list. The URL is `https://app.clickup.com/t/12345678/LIST_ID`.
* **Assignee ID:** Go to **Settings > People** and click a user. The URL has their ID.



### 3. Run the Server
```bash
# This starts your server on http://localhost:8000
uvicorn src.main:app --reload
```

### 4. Test (Locally)
In a **new terminal**, run the test script.
```bash
chmod +x ./test_webhook.sh
./test_webhook.sh
```
Watch your server logs. It will now show it's using Gemini or Claude!