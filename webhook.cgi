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

# Function to send error response and exit
send_error() {
    local message="$1"
    local exit_code="${2:-1}"
    echo "Status: 500 Internal Server Error"
    echo "Content-Type: text/plain"
    echo ""
    echo "ERROR: $message"
    log_message "ERROR: $message (exit code: $exit_code)"
    exit 1
}

# Function to send success response
send_success() {
    local message="$1"
    echo "Status: 200 OK"
    echo "Content-Type: text/plain"
    echo ""
    echo "SUCCESS: $message"
}

# Log the webhook call
log_message "Webhook triggered from ${REMOTE_ADDR:-unknown}"

# Check if pull script exists
if [ ! -f "$PULL_SCRIPT" ]; then
    send_error "Pull script not found at $PULL_SCRIPT"
fi

# Make sure pull script is executable
chmod +x "$PULL_SCRIPT" 2>> "$LOG_FILE"

# Change to deployment directory before running pull script
cd "$(dirname "$PULL_SCRIPT")" || {
    send_error "Failed to change to deployment directory $(dirname "$PULL_SCRIPT")"
}

# Execute the pull script
log_message "Executing pull script: $PULL_SCRIPT from directory $(pwd)"
OUTPUT=$("$PULL_SCRIPT" 2>&1)
EXIT_CODE=$?

# Log the output
log_message "Pull script output: $OUTPUT"
log_message "Pull script exit code: $EXIT_CODE"

# Return response based on exit code
if [ $EXIT_CODE -eq 0 ]; then
    send_success "Deployment completed"
    echo "$OUTPUT"
    log_message "Deployment successful"
    exit 0
else
    send_error "Deployment failed with exit code $EXIT_CODE: $OUTPUT" "$EXIT_CODE"
fi
