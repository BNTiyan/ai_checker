# AI & Plagiarism Detection Tool

A web-based tool that analyzes PDF documents to detect AI-generated content and check for plagiarism.

## Features

- **PDF Upload**: Upload PDF documents for analysis
- **AI Content Detection**: Detects percentage of AI-generated text using multiple methods:
  - Perplexity analysis
  - Writing pattern analysis
  - Content consistency checks
  - AI-powered detection (OpenAI GPT-4 with Gemini fallback)
  - GPT-Zero API integration (optional)
- **Plagiarism Detection**: Checks content against online sources
- **Detailed Reports**: Visual breakdown of results with highlighted sections
- **Export Results**: Download analysis reports as PDF or JSON

## Tech Stack

- **Frontend**: HTML5, CSS3, JavaScript (Vanilla)
- **Backend**: Python Flask API (Netlify Functions)
- **PDF Processing**: PyPDF2, pdfplumber
- **AI Detection**: 
  - Custom perplexity scoring
  - OpenAI API for embeddings analysis
  - GPT-Zero API (optional paid service)
- **Plagiarism**: Copyscape API / Google Custom Search API
- **Deployment**: Netlify

## Setup

### Prerequisites

```bash
pip install -r requirements.txt
```

### Environment Variables

Create a `.env` file:

```env
OPENAI_API_KEY=your_openai_key
GEMINI_API_KEY=your_gemini_key
GPTZERO_API_KEY=your_gptzero_key (optional)
GOOGLE_SEARCH_API_KEY=your_google_key
GOOGLE_SEARCH_ENGINE_ID=your_search_engine_id
```

**Need help getting API keys?** See [API_KEYS_SETUP.md](API_KEYS_SETUP.md) for detailed instructions.

### Local Development

```bash
# Install dependencies
pip install -r requirements.txt

# Configure API keys (see API_KEYS_SETUP.md)
cp .env.example .env
nano .env  # Add your API keys

# Test configuration (optional but recommended)
python test_api_keys.py

# Run Flask server
python app.py

# Or use Netlify CLI
netlify dev
```

## API Endpoints

- `POST /api/analyze` - Upload PDF and get analysis
- `GET /api/report/{id}` - Retrieve analysis report
- `POST /api/analyze-text` - Analyze plain text input

## How It Works

1. **Text Extraction**: Extracts text from PDF using pdfplumber
2. **AI Detection**:
   - Calculates perplexity scores (AI text typically has lower perplexity)
   - Analyzes sentence structure consistency
   - Checks for repetitive patterns common in AI text
   - Uses AI-powered analysis (OpenAI GPT-4 with automatic Gemini fallback)
   - Optional: Uses GPT-Zero API for professional detection
3. **Plagiarism Check**:
   - Breaks text into chunks
   - Searches each chunk against Google/Bing
   - Identifies matching sources
   - Calculates similarity scores
4. **Report Generation**:
   - Combines all analysis results
   - Highlights suspicious sections
   - Provides confidence scores

## Deployment

### Netlify Deployment

1. Push to GitHub
2. Connect to Netlify
3. Set environment variables in Netlify dashboard
4. Deploy!

```bash
netlify deploy --prod
```

## Usage

1. Open the web app
2. Upload a PDF document
3. Wait for analysis (typically 10-30 seconds)
4. View detailed report with:
   - AI generation probability (0-100%)
   - Plagiarism score (0-100%)
   - Highlighted suspicious sections
   - Source matches for plagiarized content
5. Export or save the report

## Limitations

- Maximum file size: 10MB
- Text-only PDFs (scanned images not supported without OCR)
- API rate limits apply
- Accuracy depends on text length (minimum 100 words recommended)

## Privacy

- Files are processed in memory only
- No documents are stored permanently
- Analysis results are cached for 24 hours only

## License

MIT License - feel free to use and modify

