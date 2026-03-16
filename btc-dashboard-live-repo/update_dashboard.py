#!/usr/bin/env python3
"""Update GitHub Pages dashboard with latest trading data"""
import json
import subprocess
import os
from datetime import datetime

def update_dashboard():
    # Load current trading data
    with open('/Users/dannyvett/.openclaw/workspace/bitcoin-trading-log.json', 'r') as f:
        data = json.load(f)
    
    # Update trading data JSON
    with open('/Users/dannyvett/.openclaw/workspace/btc-dashboard-live-repo/trading-data.json', 'w') as f:
        json.dump(data, f, indent=2)
    
    # Update embedded data in HTML
    with open('/Users/dannyvett/.openclaw/workspace/btc-dashboard-live-repo/index.html', 'r') as f:
        html = f.read()
    
    # Replace the script tag with new data
    import re
    pattern = r'<script id="tradingData" type="application/json">.*?</script>'
    replacement = f'<script id="tradingData" type="application/json">\n{json.dumps(data, indent=2)}\n    </script>'
    html = re.sub(pattern, replacement, html, flags=re.DOTALL)
    
    with open('/Users/dannyvett/.openclaw/workspace/btc-dashboard-live-repo/index.html', 'w') as f:
        f.write(html)
    
    # Commit and push changes
    try:
        os.chdir('/Users/dannyvett/.openclaw/workspace/btc-dashboard-live-repo')
        subprocess.run(['git', 'add', '.'], check=True)
        subprocess.run(['git', 'commit', '-m', f'Update trading data - {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}'], check=True)
        subprocess.run(['git', 'push'], check=True)
        print(f"✅ Dashboard updated and deployed at {datetime.now().strftime('%H:%M:%S')}")
        return True
    except Exception as e:
        print(f"❌ Update failed: {e}")
        return False

if __name__ == '__main__':
    update_dashboard()
