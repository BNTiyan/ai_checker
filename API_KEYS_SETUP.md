# API Keys Configuration Guide

This guide explains how to set up API keys for the AI & Plagiarism Detector in different environments.

---

## 📋 Required API Keys

| API Key | Required? | Purpose | Get It From |
|---------|-----------|---------|-------------|
| `OPENAI_API_KEY` | Recommended | AI detection (primary) | https://platform.openai.com/api-keys |
| `GEMINI_API_KEY` | Recommended | AI detection (fallback) | https://makersuite.google.com/app/apikey |
| `GOOGLE_SEARCH_API_KEY` | Required | Plagiarism checking | https://console.cloud.google.com/ |
| `GOOGLE_SEARCH_ENGINE_ID` | Required | Plagiarism checking | https://programmablesearchengine.google.com/ |
| `GPTZERO_API_KEY` | Optional | Professional AI detection | https://gptzero.me/ |

---

## 🖥️ Local Development (Your Computer)

### Method 1: Using `.env` File (Recommended)

1. **Create `.env` file** in the project root:
```bash
cd /Users/bhavananare/github/webapp/ai-plagiarism-detector
touch .env
```

2. **Edit `.env` file** and add your keys:
```bash
# Open with your favorite editor
nano .env
# or
code .env
# or
vim .env
```

3. **Add the following content**:
```env
# AI Detection APIs (at least one required)
OPENAI_API_KEY=sk-proj-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
GEMINI_API_KEY=AIzaSyxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx

# Plagiarism Detection (both required)
GOOGLE_SEARCH_API_KEY=AIzaSyxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
GOOGLE_SEARCH_ENGINE_ID=xxxxxxxxxxxxxxxxx

# Optional
GPTZERO_API_KEY=xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
```

4. **Save the file** (Ctrl+O, Enter, Ctrl+X for nano)

5. **Verify** the file is NOT tracked by git:
```bash
git status
# .env should NOT appear in the list
```

### Method 2: Export in Terminal (Temporary)

Set environment variables in your current terminal session:

```bash
# Set one by one
export OPENAI_API_KEY="sk-proj-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
export GEMINI_API_KEY="AIzaSyxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
export GOOGLE_SEARCH_API_KEY="AIzaSyxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
export GOOGLE_SEARCH_ENGINE_ID="xxxxxxxxxxxxxxxxx"

# Then run the app
python app.py
```

**Note**: These will be lost when you close the terminal.

### Method 3: Add to Shell Profile (Permanent)

Add to `~/.bashrc`, `~/.zshrc`, or `~/.bash_profile`:

```bash
# Edit your shell profile
nano ~/.zshrc  # for zsh (macOS default)
# or
nano ~/.bashrc  # for bash

# Add at the end:
export OPENAI_API_KEY="sk-proj-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
export GEMINI_API_KEY="AIzaSyxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
export GOOGLE_SEARCH_API_KEY="AIzaSyxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
export GOOGLE_SEARCH_ENGINE_ID="xxxxxxxxxxxxxxxxx"

# Save and reload
source ~/.zshrc
```

---

## ☁️ Cloud Deployment

### Heroku

#### Via Heroku Dashboard:
1. Go to https://dashboard.heroku.com/
2. Select your app
3. Go to **Settings** tab
4. Click **Reveal Config Vars**
5. Add each key-value pair:
   - Key: `OPENAI_API_KEY`
   - Value: `sk-proj-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx`
   - Click **Add**
6. Repeat for all API keys

#### Via Heroku CLI:
```bash
heroku config:set OPENAI_API_KEY="sk-proj-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
heroku config:set GEMINI_API_KEY="AIzaSyxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
heroku config:set GOOGLE_SEARCH_API_KEY="AIzaSyxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
heroku config:set GOOGLE_SEARCH_ENGINE_ID="xxxxxxxxxxxxxxxxx"
heroku config:set GPTZERO_API_KEY="xxxxxxxxxxxxxxxxx"

# Verify
heroku config
```

### Netlify

#### Via Netlify Dashboard:
1. Go to https://app.netlify.com/
2. Select your site
3. Go to **Site settings** → **Environment variables**
4. Click **Add a variable**
5. Add each key-value pair:
   - Key: `OPENAI_API_KEY`
   - Value: `sk-proj-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx`
6. Select scopes: **All**, **Production**, **Deploy Previews**
7. Click **Create variable**
8. Repeat for all keys

#### Via Netlify CLI:
```bash
netlify env:set OPENAI_API_KEY "sk-proj-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
netlify env:set GEMINI_API_KEY "AIzaSyxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
netlify env:set GOOGLE_SEARCH_API_KEY "AIzaSyxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
netlify env:set GOOGLE_SEARCH_ENGINE_ID "xxxxxxxxxxxxxxxxx"

# Verify
netlify env:list
```

### Railway

1. Go to your project on https://railway.app/
2. Select your service
3. Go to **Variables** tab
4. Click **+ New Variable**
5. Add each key-value pair
6. Railway will automatically redeploy

### Render

1. Go to your service on https://render.com/
2. Go to **Environment** tab
3. Click **Add Environment Variable**
4. Add each key-value pair:
   - Key: `OPENAI_API_KEY`
   - Value: `sk-proj-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx`
5. Click **Save Changes**
6. Render will automatically redeploy

### Vercel

#### Via Vercel Dashboard:
1. Go to your project on https://vercel.com/
2. Go to **Settings** → **Environment Variables**
3. Add each variable:
   - Name: `OPENAI_API_KEY`
   - Value: `sk-proj-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx`
   - Environment: Production, Preview, Development
4. Click **Save**

#### Via Vercel CLI:
```bash
vercel env add OPENAI_API_KEY
# Paste your key when prompted
# Select environments: Production, Preview, Development
```

### AWS (Lambda / Elastic Beanstalk)

#### Lambda via AWS Console:
1. Go to Lambda Console
2. Select your function
3. Go to **Configuration** → **Environment variables**
4. Click **Edit**
5. Add each key-value pair
6. Click **Save**

#### Elastic Beanstalk:
```bash
eb setenv OPENAI_API_KEY="sk-proj-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx" \
         GEMINI_API_KEY="AIzaSyxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx" \
         GOOGLE_SEARCH_API_KEY="AIzaSyxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx" \
         GOOGLE_SEARCH_ENGINE_ID="xxxxxxxxxxxxxxxxx"
```

### Google Cloud Run

```bash
gcloud run deploy ai-plagiarism-detector \
  --set-env-vars OPENAI_API_KEY="sk-proj-xxx",GEMINI_API_KEY="AIzaSy-xxx",GOOGLE_SEARCH_API_KEY="AIzaSy-xxx",GOOGLE_SEARCH_ENGINE_ID="xxx"
```

Or via `app.yaml`:
```yaml
env_variables:
  OPENAI_API_KEY: "sk-proj-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
  GEMINI_API_KEY: "AIzaSyxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
  GOOGLE_SEARCH_API_KEY: "AIzaSyxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
  GOOGLE_SEARCH_ENGINE_ID: "xxxxxxxxxxxxxxxxx"
```

---

## 🔑 How to Get Each API Key

### 1. OpenAI API Key

**Cost**: Pay-as-you-go (~$0.002 per request)

1. Go to https://platform.openai.com/
2. Sign up or log in
3. Click on your profile (top right) → **View API keys**
4. Click **Create new secret key**
5. Name it (e.g., "AI Plagiarism Detector")
6. Copy the key (starts with `sk-proj-...`)
7. **⚠️ Save it immediately** - you won't see it again!

**Add credits**:
- Go to **Settings** → **Billing**
- Add payment method
- Add at least $5 for testing

### 2. Gemini API Key (Google AI Studio)

**Cost**: Free tier available (60 requests/minute)

1. Go to https://makersuite.google.com/app/apikey
2. Sign in with Google account
3. Click **Create API key**
4. Select existing Google Cloud project or create new one
5. Copy the key (starts with `AIzaSy...`)

**Alternative** (Google Cloud Console):
1. Go to https://console.cloud.google.com/
2. Enable **Generative Language API**
3. Create credentials → **API Key**

### 3. Google Custom Search API Key

**Cost**: 100 free queries/day, then $5 per 1000 queries

1. Go to https://console.cloud.google.com/
2. Create a new project or select existing
3. Enable **Custom Search API**:
   - Search for "Custom Search API"
   - Click **Enable**
4. Go to **Credentials**
5. Click **Create Credentials** → **API Key**
6. Copy the key (starts with `AIzaSy...`)
7. (Optional) Restrict the key:
   - Click on the key
   - Under **API restrictions**, select "Custom Search API"
   - Save

### 4. Google Search Engine ID

**Free** (part of Custom Search)

1. Go to https://programmablesearchengine.google.com/
2. Click **Add** or **Get started**
3. Configure search engine:
   - Name: "Plagiarism Checker"
   - What to search: **Search the entire web**
   - Click **Create**
4. Go to **Control Panel**
5. Under **Basics**, find **Search engine ID**
6. Copy the ID (alphanumeric string)
7. Enable **Search the entire web**:
   - Turn ON "Search the entire web"
   - Save

### 5. GPT-Zero API Key (Optional)

**Cost**: Starts at $10/month

1. Go to https://gptzero.me/
2. Sign up for an account
3. Subscribe to API access plan
4. Go to **API** section
5. Copy your API key

---

## ✅ Verify Your Configuration

### Test Locally

Create a test script `test_api_keys.py`:

```python
import os
from dotenv import load_dotenv

load_dotenv()

print("🔍 Checking API Keys Configuration...\n")

keys = {
    "OPENAI_API_KEY": os.getenv('OPENAI_API_KEY'),
    "GEMINI_API_KEY": os.getenv('GEMINI_API_KEY'),
    "GOOGLE_SEARCH_API_KEY": os.getenv('GOOGLE_SEARCH_API_KEY'),
    "GOOGLE_SEARCH_ENGINE_ID": os.getenv('GOOGLE_SEARCH_ENGINE_ID'),
    "GPTZERO_API_KEY": os.getenv('GPTZERO_API_KEY'),
}

for name, value in keys.items():
    if value:
        masked = value[:8] + "..." + value[-4:] if len(value) > 12 else "***"
        print(f"✅ {name}: {masked}")
    else:
        required = name in ["GOOGLE_SEARCH_API_KEY", "GOOGLE_SEARCH_ENGINE_ID"]
        symbol = "❌" if required else "⚠️ "
        status = "REQUIRED - MISSING" if required else "Optional - Not set"
        print(f"{symbol} {name}: {status}")

print("\n" + "="*50)
if not keys["GOOGLE_SEARCH_API_KEY"] or not keys["GOOGLE_SEARCH_ENGINE_ID"]:
    print("❌ Missing required keys for plagiarism detection")
elif not keys["OPENAI_API_KEY"] and not keys["GEMINI_API_KEY"]:
    print("⚠️  No AI detection API configured (heuristic-only mode)")
else:
    print("✅ Configuration looks good!")
```

Run it:
```bash
python test_api_keys.py
```

### Test API Connections

```python
# test_apis.py
import os
from dotenv import load_dotenv
import openai
import google.generativeai as genai
import requests

load_dotenv()

# Test OpenAI
if os.getenv('OPENAI_API_KEY'):
    try:
        openai.api_key = os.getenv('OPENAI_API_KEY')
        response = openai.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": "Say hello"}],
            max_tokens=10
        )
        print("✅ OpenAI API: Connected")
    except Exception as e:
        print(f"❌ OpenAI API: {str(e)}")

# Test Gemini
if os.getenv('GEMINI_API_KEY'):
    try:
        genai.configure(api_key=os.getenv('GEMINI_API_KEY'))
        model = genai.GenerativeModel('gemini-1.5-flash')
        response = model.generate_content("Say hello")
        print("✅ Gemini API: Connected")
    except Exception as e:
        print(f"❌ Gemini API: {str(e)}")

# Test Google Search
if os.getenv('GOOGLE_SEARCH_API_KEY') and os.getenv('GOOGLE_SEARCH_ENGINE_ID'):
    try:
        response = requests.get(
            'https://www.googleapis.com/customsearch/v1',
            params={
                'key': os.getenv('GOOGLE_SEARCH_API_KEY'),
                'cx': os.getenv('GOOGLE_SEARCH_ENGINE_ID'),
                'q': 'test'
            }
        )
        if response.status_code == 200:
            print("✅ Google Search API: Connected")
        else:
            print(f"❌ Google Search API: {response.json()}")
    except Exception as e:
        print(f"❌ Google Search API: {str(e)}")
```

Run it:
```bash
python test_apis.py
```

---

## 🔒 Security Best Practices

### ✅ DO:
- ✅ Use `.env` files for local development
- ✅ Add `.env` to `.gitignore`
- ✅ Use environment variables in production
- ✅ Rotate API keys regularly
- ✅ Use different keys for dev/staging/prod
- ✅ Restrict API keys by:
  - IP address (if static)
  - HTTP referrer (for frontend)
  - Specific APIs only

### ❌ DON'T:
- ❌ Commit API keys to Git
- ❌ Share API keys in Slack/email
- ❌ Hardcode keys in source code
- ❌ Use production keys in development
- ❌ Share keys between projects

### If You Accidentally Commit a Key:

1. **Immediately revoke** the exposed key
2. **Create a new key**
3. **Remove from Git history**:
```bash
# Install BFG Repo Cleaner
brew install bfg  # macOS

# Remove the key from all commits
bfg --replace-text passwords.txt  # create passwords.txt with the key

# Force push (CAUTION!)
git push --force
```

4. **Update** all deployments with the new key

---

## 🐛 Troubleshooting

### "ModuleNotFoundError: No module named 'dotenv'"
```bash
pip install python-dotenv
```

### "OpenAI API key not found"
```bash
# Check if .env exists
ls -la .env

# Check if python-dotenv is loading it
python -c "from dotenv import load_dotenv; load_dotenv(); import os; print(os.getenv('OPENAI_API_KEY'))"
```

### "Invalid API key" errors
- Verify the key is correct (no extra spaces)
- Check if the key is active (not revoked)
- Verify billing is set up (for OpenAI)
- Check if the API is enabled (for Google Cloud)

### Environment variables not loading in production
- Verify variables are set in the platform dashboard
- Restart the service after adding variables
- Check variable names match exactly (case-sensitive)
- Some platforms need `process.env.VAR_NAME` (Node.js) vs `os.getenv('VAR_NAME')` (Python)

---

## 📊 Cost Estimation

Assuming 100 document analyses per day:

| Service | Usage | Cost/Month |
|---------|-------|------------|
| OpenAI GPT-4-mini | 100 requests/day × 1K tokens | ~$6 |
| Gemini API | Fallback only | Free |
| Google Custom Search | 100 queries/day | Free (within limit) |
| Total | | **~$6/month** |

For heavy usage (1000 analyses/day):
- OpenAI: ~$60/month
- Google Search: ~$15/month (after free tier)
- **Total: ~$75/month**

---

## 🆘 Need Help?

If you're still having issues:

1. Check the main README.md
2. Review error logs
3. Test each API key individually
4. Verify billing is set up
5. Check API usage limits

For quick testing without full setup:
- Set `GEMINI_API_KEY` only (free tier)
- Skip `GPTZERO_API_KEY` (optional)
- The tool will work with reduced accuracy using heuristic analysis

