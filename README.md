# QuickBooks P&L Analyzer

Internal tool for pulling QuickBooks Profit & Loss statements for financial analysis.

## Quick Start

### 1. Get a Public URL (Required for QuickBooks OAuth)

QuickBooks requires a real domain (not localhost). Use **ngrok** for testing:

```bash
# Install ngrok from https://ngrok.com/download
# Then run:
ngrok http 5000
```

You'll get a URL like: `https://xxxx.ngrok-free.app`

### 2. Configure

1. Copy `config.py` and add your QuickBooks OAuth credentials
2. Update `QUICKBOOKS_REDIRECT_URI` with your ngrok URL:
   ```python
   QUICKBOOKS_REDIRECT_URI = "https://xxxx.ngrok-free.app/auth/callback"
   ```

### 3. Install & Run

```bash
pip install -r requirements.txt
python app.py
```

### 4. Register with QuickBooks

Use these URLs in QuickBooks app registration:
- **Host domain:** `xxxx.ngrok-free.app` (no https://)
- **Launch URL:** `https://xxxx.ngrok-free.app/auth/callback`
- **Disconnect URL:** `https://xxxx.ngrok-free.app/disconnect`

## Features

- OAuth authentication with QuickBooks
- Retrieve P&L statements via QuickBooks API
- Store data securely for analysis
- Generate reports from financial data

## Privacy

See [PRIVACY.md](PRIVACY.md) for information about data collection and usage.

## License

See [EULA.md](EULA.md) for end-user license agreement.
