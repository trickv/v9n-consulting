# Just Do AI - Website

Professional website for AI consulting services targeting small businesses.

## Auto-Deployment Setup

This repo uses GitHub Actions to automatically deploy to your server when you push to the main branch.

### Server Setup (One-time)

1. **Generate SSH key pair** (if you don't have one):
   ```bash
   ssh-keygen -t ed25519 -C "github-actions-just-do-ai"
   ```

2. **Add public key to server**:
   ```bash
   # On your server
   cat ~/.ssh/id_ed25519.pub >> ~/.ssh/authorized_keys
   ```

3. **Configure Apache** (copy the provided apache-config.conf):
   ```bash
   sudo cp apache-config.conf /etc/apache2/sites-available/just-do-ai.conf
   sudo a2ensite just-do-ai.conf
   sudo systemctl reload apache2
   ```

4. **Create web directory**:
   ```bash
   sudo mkdir -p /var/www/html/just-do-ai
   sudo chown -R www-data:www-data /var/www/html/just-do-ai
   ```

### GitHub Secrets Setup

Add these secrets to your GitHub repository (Settings → Secrets and variables → Actions):

- `HOST`: Your server's IP address or domain
- `USERNAME`: SSH username (usually your user account)
- `SSH_PRIVATE_KEY`: Contents of your private key file (id_ed25519)
- `PORT`: SSH port (usually 22)

### Deploy

Once setup is complete:

```bash
git add .
git commit -m "Deploy Just Do AI website"
git push origin main
```

Your site will automatically deploy to: https://v9n.us/just-do-ai

### Manual Deployment

You can also trigger deployment manually from the GitHub Actions tab.

## Local Development

Just open `index.html` in your browser to preview changes locally.

## Contact

Questions? Email: trick@vanstaveren.us
