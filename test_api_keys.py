#!/usr/bin/env python3
"""
Test script to verify API keys configuration
"""

import os
import sys
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def check_api_keys():
    """Check if API keys are configured"""
    print("🔍 Checking API Keys Configuration...\n")
    print("=" * 60)
    
    keys = {
        "OPENAI_API_KEY": {
            "value": os.getenv('OPENAI_API_KEY'),
            "required": False,
            "description": "AI detection (primary)"
        },
        "GEMINI_API_KEY": {
            "value": os.getenv('GEMINI_API_KEY'),
            "required": False,
            "description": "AI detection (fallback)"
        },
        "GOOGLE_SEARCH_API_KEY": {
            "value": os.getenv('GOOGLE_SEARCH_API_KEY'),
            "required": True,
            "description": "Plagiarism checking"
        },
        "GOOGLE_SEARCH_ENGINE_ID": {
            "value": os.getenv('GOOGLE_SEARCH_ENGINE_ID'),
            "required": True,
            "description": "Plagiarism checking"
        },
        "GPTZERO_API_KEY": {
            "value": os.getenv('GPTZERO_API_KEY'),
            "required": False,
            "description": "Professional AI detection"
        },
    }
    
    missing_required = []
    missing_optional = []
    
    for name, config in keys.items():
        value = config["value"]
        required = config["required"]
        description = config["description"]
        
        if value:
            # Mask the key for security
            if len(value) > 12:
                masked = value[:8] + "..." + value[-4:]
            else:
                masked = "***"
            
            print(f"✅ {name}")
            print(f"   Value: {masked}")
            print(f"   Purpose: {description}")
            print()
        else:
            if required:
                print(f"❌ {name} - REQUIRED BUT MISSING!")
                print(f"   Purpose: {description}")
                print()
                missing_required.append(name)
            else:
                print(f"⚠️  {name} - Optional (not set)")
                print(f"   Purpose: {description}")
                print()
                missing_optional.append(name)
    
    print("=" * 60)
    print("\n📊 Summary:\n")
    
    # Check AI detection
    has_ai_detection = keys["OPENAI_API_KEY"]["value"] or keys["GEMINI_API_KEY"]["value"]
    
    if missing_required:
        print("❌ CONFIGURATION INCOMPLETE!")
        print(f"   Missing required keys: {', '.join(missing_required)}")
        print("\n   The application will NOT work without these keys.")
        print("   Please see API_KEYS_SETUP.md for instructions.\n")
        return False
    
    if not has_ai_detection:
        print("⚠️  WARNING: No AI detection API configured!")
        print("   Neither OPENAI_API_KEY nor GEMINI_API_KEY is set.")
        print("   The tool will use heuristic-only analysis (reduced accuracy).")
        print("   Consider adding at least one AI detection API.\n")
    
    if missing_optional:
        print(f"ℹ️  Optional keys not set: {', '.join(missing_optional)}")
        print("   The tool will work, but with limited features.\n")
    
    if not missing_required and has_ai_detection:
        print("✅ CONFIGURATION COMPLETE!")
        print("   All required keys are set and at least one AI API is configured.")
        print("   You're ready to run the application!\n")
        return True
    
    return not missing_required


def test_api_connections():
    """Test actual API connections"""
    print("\n" + "=" * 60)
    print("🔌 Testing API Connections...\n")
    print("=" * 60)
    
    all_passed = True
    
    # Test OpenAI
    if os.getenv('OPENAI_API_KEY'):
        try:
            import openai
            openai.api_key = os.getenv('OPENAI_API_KEY')
            response = openai.chat.completions.create(
                model="gpt-4o-mini",
                messages=[{"role": "user", "content": "Say hello"}],
                max_tokens=10
            )
            print("✅ OpenAI API: Connected successfully")
            print(f"   Response: {response.choices[0].message.content}\n")
        except ImportError:
            print("⚠️  OpenAI library not installed. Run: pip install openai\n")
        except Exception as e:
            print(f"❌ OpenAI API: Connection failed")
            print(f"   Error: {str(e)}\n")
            all_passed = False
    else:
        print("⏭️  OpenAI API: Skipped (no key provided)\n")
    
    # Test Gemini
    if os.getenv('GEMINI_API_KEY'):
        try:
            import google.generativeai as genai
            genai.configure(api_key=os.getenv('GEMINI_API_KEY'))
            model = genai.GenerativeModel('gemini-1.5-flash')
            response = model.generate_content("Say hello")
            print("✅ Gemini API: Connected successfully")
            print(f"   Response: {response.text[:50]}...\n")
        except ImportError:
            print("⚠️  Gemini library not installed. Run: pip install google-generativeai\n")
        except Exception as e:
            print(f"❌ Gemini API: Connection failed")
            print(f"   Error: {str(e)}\n")
            all_passed = False
    else:
        print("⏭️  Gemini API: Skipped (no key provided)\n")
    
    # Test Google Search
    if os.getenv('GOOGLE_SEARCH_API_KEY') and os.getenv('GOOGLE_SEARCH_ENGINE_ID'):
        try:
            import requests
            response = requests.get(
                'https://www.googleapis.com/customsearch/v1',
                params={
                    'key': os.getenv('GOOGLE_SEARCH_API_KEY'),
                    'cx': os.getenv('GOOGLE_SEARCH_ENGINE_ID'),
                    'q': 'test',
                    'num': 1
                },
                timeout=10
            )
            if response.status_code == 200:
                data = response.json()
                results = data.get('searchInformation', {}).get('totalResults', 0)
                print("✅ Google Custom Search API: Connected successfully")
                print(f"   Test query returned {results} results\n")
            else:
                print(f"❌ Google Custom Search API: Connection failed")
                print(f"   Status: {response.status_code}")
                print(f"   Error: {response.json().get('error', {}).get('message', 'Unknown error')}\n")
                all_passed = False
        except ImportError:
            print("⚠️  Requests library not installed. Run: pip install requests\n")
        except Exception as e:
            print(f"❌ Google Custom Search API: Connection failed")
            print(f"   Error: {str(e)}\n")
            all_passed = False
    else:
        print("❌ Google Custom Search API: Cannot test (missing keys)\n")
        all_passed = False
    
    # Test GPT-Zero
    if os.getenv('GPTZERO_API_KEY'):
        try:
            import requests
            response = requests.post(
                'https://api.gptzero.me/v2/predict/text',
                headers={'Authorization': f'Bearer {os.getenv("GPTZERO_API_KEY")}'},
                json={'document': 'This is a test.'},
                timeout=10
            )
            if response.status_code == 200:
                print("✅ GPT-Zero API: Connected successfully\n")
            else:
                print(f"❌ GPT-Zero API: Connection failed")
                print(f"   Status: {response.status_code}\n")
        except Exception as e:
            print(f"❌ GPT-Zero API: Connection failed")
            print(f"   Error: {str(e)}\n")
    else:
        print("⏭️  GPT-Zero API: Skipped (optional, no key provided)\n")
    
    print("=" * 60)
    
    if all_passed:
        print("✅ All API connection tests passed!")
    else:
        print("⚠️  Some API connection tests failed. Check the errors above.")
    
    return all_passed


def main():
    """Main test function"""
    print("\n" + "🚀 AI & Plagiarism Detector - API Configuration Test")
    print("=" * 60 + "\n")
    
    # Check if .env file exists
    if not os.path.exists('.env'):
        print("⚠️  Warning: No .env file found in current directory")
        print("   Create one from .env.example: cp .env.example .env\n")
    
    # Check API keys configuration
    keys_ok = check_api_keys()
    
    if not keys_ok:
        print("\n❌ Please configure your API keys before running the application.")
        print("   See API_KEYS_SETUP.md for detailed instructions.\n")
        sys.exit(1)
    
    # Ask user if they want to test connections
    try:
        print("\nDo you want to test API connections? (y/n): ", end='')
        answer = input().strip().lower()
        
        if answer in ['y', 'yes']:
            test_api_connections()
    except KeyboardInterrupt:
        print("\n\nTest cancelled by user.")
        sys.exit(0)
    
    print("\n✅ Configuration test complete!")
    print("   You can now run: python app.py\n")


if __name__ == '__main__':
    main()

