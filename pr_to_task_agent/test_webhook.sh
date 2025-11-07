#!/bin/bash

echo "Sending test GitHub webhook payload to localhost:8000..."

curl -X POST http://localhost:8000/webhook/github \
     -H "Content-Type: application/json" \
     -d '{
          "action": "opened",
          "pull_request": {
            "title": "feat: Add new user login page",
            "html_url": "https://github.com/YourOrg/YourRepo/pull/123",
            "head": {
              "ref": "feat-user-login"
            }
          }
        }'

echo "\nDone. Check your server logs."