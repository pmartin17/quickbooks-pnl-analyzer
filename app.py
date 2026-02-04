"""
QuickBooks P&L Analyzer - Main Application
"""

from flask import Flask, request, redirect, session, jsonify
import requests
import os
from config import (
    QUICKBOOKS_CLIENT_ID,
    QUICKBOOKS_CLIENT_SECRET,
    QUICKBOOKS_REDIRECT_URI,
    QUICKBOOKS_SCOPE,
    ENVIRONMENT
)

app = Flask(__name__)
app.secret_key = os.urandom(24)

# QuickBooks API endpoints
if ENVIRONMENT == "sandbox":
    QB_BASE_URL = "https://sandbox-quickbooks.api.intuit.com"
    QB_AUTH_URL = "https://appcenter.intuit.com/connect/oauth2"
else:
    QB_BASE_URL = "https://quickbooks.api.intuit.com"
    QB_AUTH_URL = "https://appcenter.intuit.com/connect/oauth2"

@app.route('/')
def index():
    """Home page"""
    if 'access_token' in session:
        return '<h1>QuickBooks P&L Analyzer</h1><p>You are authenticated. <a href="/pnl">Get P&L Statement</a></p>'
    else:
        return '<h1>QuickBooks P&L Analyzer</h1><p><a href="/auth">Authenticate with QuickBooks</a></p>'

@app.route('/auth')
def auth():
    """Initiate OAuth flow"""
    auth_url = f"{QB_AUTH_URL}?client_id={QUICKBOOKS_CLIENT_ID}&response_type=code&scope={QUICKBOOKS_SCOPE}&redirect_uri={QUICKBOOKS_REDIRECT_URI}&access_type=offline"
    return redirect(auth_url)

@app.route('/auth/callback')
def callback():
    """Handle OAuth callback"""
    code = request.args.get('code')
    realm_id = request.args.get('realmId')
    
    # Exchange code for access token
    token_url = f"{QB_AUTH_URL}/token"
    token_data = {
        'grant_type': 'authorization_code',
        'code': code,
        'redirect_uri': QUICKBOOKS_REDIRECT_URI
    }
    
    response = requests.post(
        token_url,
        data=token_data,
        auth=(QUICKBOOKS_CLIENT_ID, QUICKBOOKS_CLIENT_SECRET),
        headers={'Accept': 'application/json'}
    )
    
    if response.status_code == 200:
        tokens = response.json()
        session['access_token'] = tokens.get('access_token')
        session['refresh_token'] = tokens.get('refresh_token')
        session['realm_id'] = realm_id
        return redirect('/')
    else:
        return f"Error: {response.text}", 400

@app.route('/pnl')
def get_pnl():
    """Retrieve Profit & Loss statement"""
    if 'access_token' not in session:
        return redirect('/auth')
    
    # Query for P&L report
    url = f"{QB_BASE_URL}/v3/company/{session['realm_id']}/reports/ProfitAndLoss"
    headers = {
        'Authorization': f"Bearer {session['access_token']}",
        'Accept': 'application/json'
    }
    
    response = requests.get(url, headers=headers)
    
    if response.status_code == 200:
        pnl_data = response.json()
        return jsonify(pnl_data)
    else:
        return f"Error retrieving P&L: {response.text}", response.status_code

@app.route('/disconnect')
def disconnect():
    """Disconnect from QuickBooks"""
    session.clear()
    return '<h1>Disconnected</h1><p>You have been disconnected from QuickBooks. <a href="/">Return to home</a></p>'

if __name__ == '__main__':
    app.run(debug=True, port=5000)
