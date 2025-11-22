#!/bin/bash

# AI & Plagiarism Detector - Local Development Setup

echo "🚀 Setting up AI & Plagiarism Detector..."

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed. Please install Python 3.8 or higher."
    exit 1
fi

# Create virtual environment
echo "📦 Creating virtual environment..."
python3 -m venv venv

# Activate virtual environment
echo "🔧 Activating virtual environment..."
source venv/bin/activate

# Install dependencies
echo "📥 Installing dependencies..."
pip install --upgrade pip
pip install -r requirements.txt

# Download NLTK data
echo "📚 Downloading NLTK data..."
python3 -c "import nltk; nltk.download('punkt')"

# Check for .env file
if [ ! -f .env ]; then
    echo "⚠️  No .env file found. Creating from .env.example..."
    cp .env.example .env
    echo "📝 Please edit .env and add your API keys"
    echo ""
    echo "For detailed instructions, see API_KEYS_SETUP.md"
    echo ""
fi

echo "✅ Setup complete!"
echo ""
echo "Next steps:"
echo "  1. Configure API keys: nano .env"
echo "     (See API_KEYS_SETUP.md for help getting keys)"
echo ""
echo "  2. Test configuration: python test_api_keys.py"
echo ""
echo "  3. Start the server: python app.py"
echo ""
echo "  4. Open http://localhost:5000 in your browser"
echo ""
echo "⚠️  The app requires API keys to work!"
echo "   At minimum: GOOGLE_SEARCH_API_KEY and GOOGLE_SEARCH_ENGINE_ID"
echo "   Recommended: Also add OPENAI_API_KEY or GEMINI_API_KEY"

