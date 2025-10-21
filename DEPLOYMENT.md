# V9N Consulting Deployment Guide

This repository uses a simple webhook-based deployment system that automatically updates the production site when changes are pushed to the `main` branch.

**Status**: Active and deployed at https://vanstaveren.us/~trick/v9n-webhook/webhook.cgi

## Architecture

The deployment system has three components:

- **GitHub Actions** - Triggers on push to `main` branch
- **Webhook CGI Script** - Receives deployment requests and executes pull script
- **Pull Script** - Updates production files from git repository

## Files

### `webhook.cgi`
CGI script that handles incoming webhook requests from GitHub Actions.

**Deployed to**: `https://vanstaveren.us/~trick/v9n-webhook/webhook.cgi`

**Key Features**:
- Logs all deployment attempts to `/tmp/v9n-webhook.log`
- Executes the `pull` script in the repository
- Returns deployment status to GitHub Actions

### `.github/workflows/deploy.yml`
GitHub Actions workflow that triggers deployment.

**Triggers**:
- Automatic: On push to `main` branch
- Manual: Via GitHub Actions UI (workflow_dispatch)

### `pull`
Git pull script that updates the production deployment (assumed to exist).

## Installation Steps

### 1. Deploy Webhook Script

Copy the webhook script to your web server:

```bash
# On your web server
mkdir -p ~/public_html/v9n-webhook
cp webhook.cgi ~/public_html/v9n-webhook/
chmod +x ~/public_html/v9n-webhook/webhook.cgi
```

### 2. Configure Apache for CGI

Ensure your `.htaccess` or Apache config allows CGI execution:

```apache
# In ~/public_html/v9n-webhook/.htaccess
Options +ExecCGI
AddHandler cgi-script .cgi
```

### 3. Test Webhook Locally

```bash
# Test the webhook endpoint
curl -X POST https://vanstaveren.us/~trick/v9n-webhook/webhook.cgi
```

You should see either "SUCCESS" or "ERROR" output, and check `/tmp/v9n-webhook.log` for details.

### 4. Verify GitHub Actions

The workflow is already committed to the repository. It will trigger automatically on the next push to `main`.

You can also manually trigger it:
1. Go to GitHub repository > Actions tab
2. Select "Deploy to Production" workflow
3. Click "Run workflow"

## File Permissions

Ensure proper permissions are set:

```bash
# Webhook script must be executable
chmod +x ~/public_html/v9n-webhook/webhook.cgi

# Pull script must be executable
chmod +x /home/trick/src/github.com/trickv/v9n-consulting/pull

# Log file should be writable by web server user
touch /tmp/v9n-webhook.log
chmod 666 /tmp/v9n-webhook.log  # Or set appropriate ownership
```

## Troubleshooting

### Check Webhook Logs

```bash
tail -f /tmp/v9n-webhook.log
```

### Test Pull Script Manually

```bash
/home/trick/src/github.com/trickv/v9n-consulting/pull
```

### Verify CGI Execution

```bash
# Check Apache error logs
tail -f /var/log/apache2/error.log

# Or user-specific logs
tail -f ~/logs/error.log
```

### Common Issues

1. **Permission Denied**: Ensure webhook.cgi and pull script are executable
2. **Script Not Found**: Verify paths in webhook.cgi match your setup
3. **Git Pull Fails**: Check git repository permissions and SSH keys
4. **Logs Not Written**: Verify web server user can write to `/tmp/v9n-webhook.log`

## Security Considerations

This is a simple webhook implementation without authentication. Consider adding:

- **IP Whitelisting**: Only allow requests from GitHub's IP ranges
- **Secret Token**: Add HMAC signature verification
- **Rate Limiting**: Prevent abuse of the webhook endpoint

For enhanced security, you can modify `webhook.cgi` to verify the request origin.

## Manual Deployment

If needed, you can always deploy manually:

```bash
# SSH to server
cd /var/www/html
./pull  # Or whatever your pull script does
```

## Monitoring

Monitor deployment status via:

- GitHub Actions tab in repository
- `/tmp/v9n-webhook.log` on server
- Apache access/error logs
