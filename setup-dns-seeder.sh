#!/bin/bash

set -e

echo "🔧 Setting up AdventureCoin Lightweight DNS Seeder..."

# 1. Install dependencies
echo "📦 Installing Python packages..."
pip install --upgrade pip
pip install dnslib requests

# 2. Seeder directory and script
SEEDER_DIR="/opt/advc-dnsseeder"
SEEDER_SCRIPT="$SEEDER_DIR/api_dns_seeder.py"
GITHUB_SCRIPT_URL="https://raw.githubusercontent.com/CryptoDevelopmentServices/Lightweight_DNS_Seeder/main/api_dns_seeder.py"

echo "📁 Creating seeder directory..."
sudo mkdir -p "$SEEDER_DIR"

echo "🌐 Downloading latest seeder script from GitHub..."
sudo curl -fsSL "$GITHUB_SCRIPT_URL" -o "$SEEDER_SCRIPT"
sudo chmod +x "$SEEDER_SCRIPT"

# 3. Create systemd service
echo "🛠️ Creating systemd service..."
sudo tee /etc/systemd/system/advc-dnsseeder.service > /dev/null <<EOF
[Unit]
Description=AdventureCoin DNS Seeder
After=network.target

[Service]
ExecStart=/usr/bin/python3 $SEEDER_SCRIPT
WorkingDirectory=$SEEDER_DIR
Restart=always
User=root

[Install]
WantedBy=multi-user.target
EOF

# 4. Enable and start service
sudo systemctl daemon-reexec
sudo systemctl daemon-reload
sudo systemctl enable advc-dnsseeder.service
sudo systemctl restart advc-dnsseeder.service

# 5. Open the configured DNS port
echo "🌐 Opening DNS port 8053..."
sudo ufw allow 8053/tcp
sudo ufw allow 8053/udp
sudo ufw reload

echo "✅ DNS Seeder is installed and running!"
echo "🔍 Use: 'sudo systemctl status advc-dnsseeder' to check status"
