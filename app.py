import os
import io
import json
import hashlib
from datetime import datetime
from flask import Flask, request, jsonify
from flask_cors import CORS
import pdfplumber
import openai
import requests
import numpy as np
import nltk
from textstat import textstat
from dotenv import load_dotenv
import google.generativeai as genai

# Download required NLTK data
try:
    nltk.data.find('tokenizers/punkt')
except LookupError:
    nltk.download('punkt')

load_dotenv()

app = Flask(__name__)
CORS(app)

# Configuration
openai.api_key = os.getenv('OPENAI_API_KEY')
GOOGLE_SEARCH_API_KEY = os.getenv('GOOGLE_SEARCH_API_KEY')
GOOGLE_SEARCH_ENGINE_ID = os.getenv('GOOGLE_SEARCH_ENGINE_ID')
GPTZERO_API_KEY = os.getenv('GPTZERO_API_KEY')
GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')

# Configure Gemini
if GEMINI_API_KEY:
    genai.configure(api_key=GEMINI_API_KEY)

# In-memory cache for reports (in production, use Redis or database)
reports_cache = {}


def extract_text_from_pdf(pdf_file):
    """Extract text from uploaded PDF file"""
    try:
        text = ""
        with pdfplumber.open(pdf_file) as pdf:
            for page in pdf.pages:
                page_text = page.extract_text()
                if page_text:
                    text += page_text + "\n"
        return text.strip()
    except Exception as e:
        raise Exception(f"Error extracting text from PDF: {str(e)}")


def calculate_perplexity_score(text):
    """
    Calculate perplexity-like score using AI analysis with OpenAI -> Gemini fallback
    AI-generated text typically has lower perplexity (more predictable)
    """
    try:
        # Split text into sentences
        sentences = nltk.sent_tokenize(text)
        if len(sentences) < 3:
            return {"score": 50, "confidence": "low", "reason": "Text too short"}
        
        # Analyze readability metrics
        flesch_reading_ease = textstat.flesch_reading_ease(text)
        flesch_kincaid_grade = textstat.flesch_kincaid_grade(text)
        
        # AI text tends to have very consistent readability
        # Human text varies more
        avg_sentence_length = np.mean([len(s.split()) for s in sentences])
        sentence_length_variance = np.var([len(s.split()) for s in sentences])
        
        # Calculate AI probability based on patterns
        ai_score = 0
        
        # Factor 1: Consistent sentence length (AI tends to be more consistent)
        if sentence_length_variance < 10:
            ai_score += 25
        elif sentence_length_variance < 20:
            ai_score += 15
        
        # Factor 2: Optimal readability (AI aims for 60-70 Flesch score)
        if 55 <= flesch_reading_ease <= 75:
            ai_score += 25
        elif 45 <= flesch_reading_ease <= 85:
            ai_score += 15
        
        # Factor 3: Grade level consistency
        if 8 <= flesch_kincaid_grade <= 12:
            ai_score += 20
        elif 6 <= flesch_kincaid_grade <= 14:
            ai_score += 10
        
        # Factor 4: Check for repetitive patterns
        words = text.lower().split()
        unique_ratio = len(set(words)) / len(words) if words else 0
        if unique_ratio < 0.4:  # Too repetitive
            ai_score += 30
        elif unique_ratio < 0.6:
            ai_score += 15
        
        # Factor 5: Try AI-powered analysis with fallback
        ai_enhanced_score = get_ai_enhanced_detection(text[:2000])  # Limit to first 2000 chars
        if ai_enhanced_score is not None:
            # Blend heuristic score with AI analysis (60% heuristic, 40% AI)
            ai_score = (ai_score * 0.6) + (ai_enhanced_score * 0.4)
        
        confidence = "high" if ai_score > 60 else "medium" if ai_score > 40 else "low"
        
        return {
            "score": min(ai_score, 100),
            "confidence": confidence,
            "metrics": {
                "flesch_reading_ease": round(flesch_reading_ease, 2),
                "flesch_kincaid_grade": round(flesch_kincaid_grade, 2),
                "avg_sentence_length": round(avg_sentence_length, 2),
                "sentence_length_variance": round(sentence_length_variance, 2),
                "unique_word_ratio": round(unique_ratio, 2)
            }
        }
    except Exception as e:
        return {"score": 0, "confidence": "error", "reason": str(e)}


def get_ai_enhanced_detection(text_sample):
    """
    Use OpenAI or Gemini to enhance AI detection
    Returns a score from 0-100 or None if both fail
    """
    prompt = f"""Analyze the following text and determine if it was likely written by AI or a human. 
Consider factors like:
- Writing style consistency
- Vocabulary sophistication
- Natural flow and transitions
- Presence of AI-typical patterns (overly formal, generic phrases)
- Human elements (personal anecdotes, unique perspectives, inconsistencies)

Text to analyze:
{text_sample}

Respond with ONLY a number from 0-100, where:
- 0-30 = Definitely human-written
- 31-50 = Likely human-written
- 51-70 = Uncertain/Mixed
- 71-90 = Likely AI-generated
- 91-100 = Definitely AI-generated

Your response (number only):"""

    # Try OpenAI first
    if openai.api_key:
        try:
            response = openai.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content": "You are an expert at detecting AI-generated text. Respond with only a number."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.3,
                max_tokens=10
            )
            
            score_text = response.choices[0].message.content.strip()
            score = float(''.join(filter(lambda x: x.isdigit() or x == '.', score_text)))
            print(f"[OpenAI] AI detection score: {score}")
            return score
            
        except Exception as e:
            print(f"[OpenAI] Failed: {str(e)}, falling back to Gemini...")
    
    # Fallback to Gemini
    if GEMINI_API_KEY:
        try:
            model = genai.GenerativeModel('gemini-1.5-flash')
            response = model.generate_content(prompt)
            
            score_text = response.text.strip()
            score = float(''.join(filter(lambda x: x.isdigit() or x == '.', score_text)))
            print(f"[Gemini] AI detection score: {score}")
            return score
            
        except Exception as e:
            print(f"[Gemini] Failed: {str(e)}")
    
    # Both failed
    print("[AI Detection] Both OpenAI and Gemini failed, using heuristic-only scoring")
    return None


def check_gptzero(text):
    """Use GPT-Zero API for AI detection (if API key provided)"""
    if not GPTZERO_API_KEY:
        return None
    
    try:
        response = requests.post(
            'https://api.gptzero.me/v2/predict/text',
            headers={'Authorization': f'Bearer {GPTZERO_API_KEY}'},
            json={'document': text},
            timeout=30
        )
        
        if response.status_code == 200:
            data = response.json()
            return {
                "completely_generated_prob": data.get("documents", [{}])[0].get("completely_generated_prob", 0) * 100,
                "average_generated_prob": data.get("documents", [{}])[0].get("average_generated_prob", 0) * 100
            }
    except Exception as e:
        print(f"GPT-Zero API error: {str(e)}")
    
    return None


def check_plagiarism(text):
    """Check for plagiarism using Google Custom Search API"""
    if not GOOGLE_SEARCH_API_KEY or not GOOGLE_SEARCH_ENGINE_ID:
        return {"score": 0, "sources": [], "note": "API keys not configured"}
    
    try:
        # Split text into chunks (Google search has character limits)
        sentences = nltk.sent_tokenize(text)
        chunks = []
        current_chunk = ""
        
        for sentence in sentences:
            if len(current_chunk) + len(sentence) < 200:  # Keep chunks under 200 chars
                current_chunk += " " + sentence
            else:
                if current_chunk:
                    chunks.append(current_chunk.strip())
                current_chunk = sentence
        
        if current_chunk:
            chunks.append(current_chunk.strip())
        
        # Search for first 5 chunks (to avoid rate limits)
        matches = []
        total_checked = min(5, len(chunks))
        
        for i, chunk in enumerate(chunks[:total_checked]):
            try:
                # Add quotes for exact match search
                query = f'"{chunk}"'
                response = requests.get(
                    'https://www.googleapis.com/customsearch/v1',
                    params={
                        'key': GOOGLE_SEARCH_API_KEY,
                        'cx': GOOGLE_SEARCH_ENGINE_ID,
                        'q': query,
                        'num': 3
                    },
                    timeout=10
                )
                
                if response.status_code == 200:
                    results = response.json()
                    if 'items' in results and len(results['items']) > 0:
                        for item in results['items'][:2]:  # Top 2 results
                            matches.append({
                                "title": item.get('title', 'Unknown'),
                                "url": item.get('link', ''),
                                "snippet": item.get('snippet', ''),
                                "matched_text": chunk[:100] + "..."
                            })
            except Exception as e:
                print(f"Search error for chunk {i}: {str(e)}")
                continue
        
        # Calculate plagiarism score
        plagiarism_score = min((len(matches) / total_checked) * 100, 100)
        
        return {
            "score": round(plagiarism_score, 2),
            "sources": matches,
            "chunks_checked": total_checked
        }
    except Exception as e:
        return {"score": 0, "sources": [], "error": str(e)}


@app.route('/api/analyze', methods=['POST'])
def analyze_document():
    """Main endpoint to analyze uploaded PDF"""
    try:
        if 'file' not in request.files:
            return jsonify({"error": "No file uploaded"}), 400
        
        file = request.files['file']
        
        if not file.filename.endswith('.pdf'):
            return jsonify({"error": "Only PDF files are supported"}), 400
        
        # Extract text from PDF
        pdf_bytes = io.BytesIO(file.read())
        text = extract_text_from_pdf(pdf_bytes)
        
        if not text or len(text.split()) < 50:
            return jsonify({"error": "PDF contains insufficient text (minimum 50 words required)"}), 400
        
        # Generate report ID
        report_id = hashlib.md5(text.encode()).hexdigest()
        
        # Check if already analyzed (cache)
        if report_id in reports_cache:
            return jsonify(reports_cache[report_id])
        
        # Perform AI detection
        ai_analysis = calculate_perplexity_score(text)
        
        # Optional: Use GPT-Zero API
        gptzero_result = check_gptzero(text)
        
        # Perform plagiarism check
        plagiarism_result = check_plagiarism(text)
        
        # Combine scores
        final_ai_score = ai_analysis["score"]
        if gptzero_result:
            # Average with GPT-Zero if available
            final_ai_score = (ai_analysis["score"] + gptzero_result["average_generated_prob"]) / 2
        
        # Generate report
        report = {
            "report_id": report_id,
            "filename": file.filename,
            "analyzed_at": datetime.now().isoformat(),
            "text_stats": {
                "total_words": len(text.split()),
                "total_characters": len(text),
                "total_sentences": len(nltk.sent_tokenize(text))
            },
            "ai_detection": {
                "probability": round(final_ai_score, 2),
                "confidence": ai_analysis["confidence"],
                "metrics": ai_analysis.get("metrics", {}),
                "verdict": "Likely AI-generated" if final_ai_score > 60 else "Likely human-written" if final_ai_score < 40 else "Uncertain",
                "gptzero": gptzero_result
            },
            "plagiarism": plagiarism_result,
            "overall_verdict": {
                "ai_generated": final_ai_score > 60,
                "plagiarized": plagiarism_result["score"] > 30,
                "risk_level": "high" if (final_ai_score > 70 or plagiarism_result["score"] > 50) else "medium" if (final_ai_score > 50 or plagiarism_result["score"] > 30) else "low"
            }
        }
        
        # Cache report
        reports_cache[report_id] = report
        
        return jsonify(report)
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/api/analyze-text', methods=['POST'])
def analyze_text():
    """Analyze plain text input"""
    try:
        data = request.get_json()
        text = data.get('text', '')
        
        if not text or len(text.split()) < 50:
            return jsonify({"error": "Text too short (minimum 50 words required)"}), 400
        
        # Generate report ID
        report_id = hashlib.md5(text.encode()).hexdigest()
        
        # Perform analysis
        ai_analysis = calculate_perplexity_score(text)
        gptzero_result = check_gptzero(text)
        plagiarism_result = check_plagiarism(text)
        
        final_ai_score = ai_analysis["score"]
        if gptzero_result:
            final_ai_score = (ai_analysis["score"] + gptzero_result["average_generated_prob"]) / 2
        
        report = {
            "report_id": report_id,
            "analyzed_at": datetime.now().isoformat(),
            "text_stats": {
                "total_words": len(text.split()),
                "total_characters": len(text),
                "total_sentences": len(nltk.sent_tokenize(text))
            },
            "ai_detection": {
                "probability": round(final_ai_score, 2),
                "confidence": ai_analysis["confidence"],
                "metrics": ai_analysis.get("metrics", {}),
                "verdict": "Likely AI-generated" if final_ai_score > 60 else "Likely human-written" if final_ai_score < 40 else "Uncertain",
                "gptzero": gptzero_result
            },
            "plagiarism": plagiarism_result,
            "overall_verdict": {
                "ai_generated": final_ai_score > 60,
                "plagiarized": plagiarism_result["score"] > 30,
                "risk_level": "high" if (final_ai_score > 70 or plagiarism_result["score"] > 50) else "medium" if (final_ai_score > 50 or plagiarism_result["score"] > 30) else "low"
            }
        }
        
        reports_cache[report_id] = report
        return jsonify(report)
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/api/report/<report_id>', methods=['GET'])
def get_report(report_id):
    """Retrieve a cached report"""
    if report_id in reports_cache:
        return jsonify(reports_cache[report_id])
    return jsonify({"error": "Report not found"}), 404


@app.route('/health', methods=['GET'])
def health():
    return jsonify({"status": "healthy"})


if __name__ == '__main__':
    app.run(debug=True, port=5000)

