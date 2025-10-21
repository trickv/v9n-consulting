#!/bin/bash
#
# V9N Consulting Webhook Handler
# Deploy as: https://vanstaveren.us/~trick/v9n-webhook/webhook.cgi
#
# This script handles GitHub webhook calls and triggers a git pull
# in the deployment directory.

# Configuration
DEPLOY_DIR="/var/www/v9n.us"
LOG_FILE="/tmp/v9n-webhook.log"
PULL_SCRIPT="/var/www/v9n.us/pull"

# Function to log messages
log_message() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] $1" >> "$LOG_FILE"
}

# Send HTTP headers
echo "Content-Type: text/plain"
echo ""

# Log the webhook call
log_message "Webhook triggered from ${REMOTE_ADDR:-unknown}"

# Check if pull script exists
if [ ! -f "$PULL_SCRIPT" ]; then
    echo "ERROR: Pull script not found at $PULL_SCRIPT"
    log_message "ERROR: Pull script not found at $PULL_SCRIPT"
    exit 1
fi

# Make sure pull script is executable
chmod +x "$PULL_SCRIPT" 2>> "$LOG_FILE"

# Change to deployment directory before running pull script
cd "$(dirname "$PULL_SCRIPT")" || {
    echo "ERROR: Failed to change to deployment directory"
    log_message "ERROR: Failed to cd to $(dirname "$PULL_SCRIPT")"
    exit 1
}

# Execute the pull script
log_message "Executing pull script: $PULL_SCRIPT from directory $(pwd)"
OUTPUT=$("$PULL_SCRIPT" 2>&1)
EXIT_CODE=$?

# Log the output
log_message "Pull script output: $OUTPUT"
log_message "Pull script exit code: $EXIT_CODE"

# Return response
if [ $EXIT_CODE -eq 0 ]; then
    echo "SUCCESS: Deployment completed"
    echo "$OUTPUT"
    log_message "Deployment successful"
else
    echo "ERROR: Deployment failed with exit code $EXIT_CODE"
    echo "$OUTPUT"
    log_message "ERROR: Deployment failed with exit code $EXIT_CODE"
fi

exit $EXIT_CODE
