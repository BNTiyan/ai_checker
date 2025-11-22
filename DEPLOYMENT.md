# Deployment Guide

## Local Deployment

### Prerequisites
- Python 3.8 or higher
- pip package manager

### Setup Steps

1. Clone the repository:
```bash
cd ai-plagiarism-detector
```

2. Run setup script:
```bash
chmod +x setup.sh
./setup.sh
```

3. Configure environment variables:
Edit `.env` file with your API keys:
```env
OPENAI_API_KEY=sk-...
GEMINI_API_KEY=AIza...
GOOGLE_SEARCH_API_KEY=AIza...
GOOGLE_SEARCH_ENGINE_ID=...
GPTZERO_API_KEY=...  # Optional
```

4. Start the Flask server:
```bash
source venv/bin/activate
python app.py
```

5. Open http://localhost:5000 in your browser

## Cloud Deployment Options

### Option 1: Heroku (Recommended for Full-Stack)

1. Install Heroku CLI
2. Create Heroku app:
```bash
heroku create ai-plagiarism-detector
```

3. Add buildpack:
```bash
heroku buildpacks:set heroku/python
```

4. Set environment variables:
```bash
heroku config:set OPENAI_API_KEY=your_key
heroku config:set GEMINI_API_KEY=your_key
heroku config:set GOOGLE_SEARCH_API_KEY=your_key
heroku config:set GOOGLE_SEARCH_ENGINE_ID=your_id
```

5. Create `Procfile`:
```
web: gunicorn app:app
```

6. Deploy:
```bash
git add .
git commit -m "Deploy to Heroku"
git push heroku main
```

### Option 2: AWS Lambda + API Gateway

1. Package the application:
```bash
pip install -r requirements.txt -t package/
cd package
zip -r ../deployment.zip .
cd ..
zip -g deployment.zip app.py
```

2. Create Lambda function in AWS Console
3. Upload deployment.zip
4. Set environment variables in Lambda configuration
5. Create API Gateway to expose endpoints

### Option 3: Google Cloud Run

1. Create `Dockerfile`:
```dockerfile
FROM python:3.9-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
RUN python -c "import nltk; nltk.download('punkt')"
COPY . .
CMD ["gunicorn", "--bind", "0.0.0.0:8080", "app:app"]
```

2. Build and deploy:
```bash
gcloud builds submit --tag gcr.io/PROJECT_ID/ai-detector
gcloud run deploy --image gcr.io/PROJECT_ID/ai-detector --platform managed
```

### Option 4: Netlify (Static + Functions)

**Note**: Netlify Functions have limitations with file uploads. For PDF analysis, consider:

1. Deploy frontend to Netlify
2. Deploy backend API to Heroku/Railway/Render
3. Update `API_BASE_URL` in `app.js`

#### Frontend Only on Netlify:
```bash
netlify deploy --prod
```

Set environment variables in Netlify dashboard:
- `OPENAI_API_KEY`
- `GEMINI_API_KEY`
- `GOOGLE_SEARCH_API_KEY`
- `GOOGLE_SEARCH_ENGINE_ID`

### Option 5: Railway (Recommended Alternative)

1. Connect GitHub repository to Railway
2. Set environment variables in Railway dashboard
3. Deploy automatically on push

### Option 6: Render

1. Create new Web Service on Render
2. Connect GitHub repository
3. Set build command: `pip install -r requirements.txt`
4. Set start command: `gunicorn app:app`
5. Add environment variables

## API Keys Setup

### OpenAI API Key
1. Go to https://platform.openai.com/
2. Create account and navigate to API keys
3. Create new API key
4. Add to `.env` as `OPENAI_API_KEY`

### Gemini API Key (Fallback)
1. Go to https://makersuite.google.com/app/apikey
2. Create Google AI Studio account
3. Generate API key
4. Add to `.env` as `GEMINI_API_KEY`
5. **Note**: If OpenAI fails, the system will automatically use Gemini

### Google Custom Search API
1. Go to https://console.cloud.google.com/
2. Enable Custom Search API
3. Create credentials (API Key)
4. Add to `.env` as `GOOGLE_SEARCH_API_KEY`

### Google Search Engine ID
1. Go to https://programmablesearchengine.google.com/
2. Create new search engine
3. Set to search entire web
4. Copy Search Engine ID
5. Add to `.env` as `GOOGLE_SEARCH_ENGINE_ID`

### GPT-Zero API (Optional)
1. Go to https://gptzero.me/
2. Sign up for API access
3. Get API key
4. Add to `.env` as `GPTZERO_API_KEY`

## Production Considerations

### Security
- Never commit `.env` file to Git
- Use environment variables for all sensitive data
- Implement rate limiting (e.g., Flask-Limiter)
- Add authentication if needed

### Performance
- Implement Redis caching for reports
- Use CDN for static assets
- Optimize PDF processing for large files
- Consider background jobs for long analyses

### Monitoring
- Set up error tracking (Sentry)
- Implement logging (CloudWatch, Papertrail)
- Monitor API usage and costs
- Set up uptime monitoring

### Scalability
- Use managed databases (PostgreSQL) for report storage
- Implement queue system (Celery + Redis) for async processing
- Auto-scaling for cloud deployments
- Consider serverless architecture for sporadic usage

## Troubleshooting

### NLTK Data Not Found
```bash
python -c "import nltk; nltk.download('punkt')"
```

### Module Import Errors
```bash
pip install --upgrade -r requirements.txt
```

### CORS Issues
Add your domain to CORS configuration in `app.py`

### Memory Errors on Large PDFs
- Increase server memory allocation
- Implement streaming for large files
- Add file size validation

## Cost Estimates

### API Costs (Monthly)
- OpenAI API: $0.002 per 1K tokens (~$5-20 for moderate usage)
- Google Custom Search: $5 per 1000 queries (100 free queries/day)
- GPT-Zero: Varies by plan (optional)

### Hosting Costs
- Heroku: $7/month (Hobby tier)
- Railway: $5/month (Starter)
- Render: Free tier available
- AWS Lambda: Pay per request (likely < $5/month)
- Google Cloud Run: Pay per request (free tier available)

## Support

For issues or questions:
1. Check README.md
2. Review error logs
3. Test API endpoints individually
4. Verify environment variables are set correctly

