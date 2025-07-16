News Summarization & Fact-Checking Bot
An AI-powered news analysis tool that summarizes articles and verifies their credibility using CrewAI, OpenAI, and FastAPI.
Features
🔍 News Article Scraping: Extract content from news URLs
📄 AI-Powered Summarization: Generate concise summaries with key points
✅ Fact-Checking: Verify claims and assess credibility
🎯 Topic Search: Find articles by topic
📊 Credibility Scoring: Rate news sources and content reliability
🚀 FastAPI Backend: Modern, async API with automatic documentation
🐳 Docker Support: Easy containerized deployment
Tech Stack
CrewAI: Multi-agent AI system for news analysis
OpenAI: LLM for natural language processing
FastAPI: Modern web framework for APIs
News API: Real-time news data
Serper API: Search functionality for fact-checking
Docker: Containerization for easy deployment
Quick Start
Prerequisites
Python 3.11+
API Keys:
OpenAI API Key
News API Key (from newsapi.org)
Serper API Key (from serper.dev)
Installation
Clone the repository:
git clone https://github.com/SoumyajitProjects/New-Bot.git
cd New-Bot
Create a virtual environment:
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
Install dependencies:
pip install -r requirements.txt
Set up environment variables:
cp .env.example .env
# Edit .env with your API keys
Run the application:
python main.py
The API will be available at http://localhost:8000
API Endpoints
📚 Documentation
Interactive Docs: http://localhost:8000/docs
ReDoc: http://localhost:8000/redoc
🔍 Main Endpoints
#### Analyze Single Article
POST /analyze/article
Content-Type: application/json
{
  "url": "https://example.com/news-article"
}
#### Batch Analyze Articles
POST /analyze/batch
Content-Type: application/json
["https://example.com/article1", "https://example.com/article2"]
#### Search News by Topic
POST /search/topic
Content-Type: application/json
{
  "topic": "artificial intelligence",
  "limit": 5
}
#### Get Headlines by Category
GET /headlines/{category}?limit=10
Categories: general, business, entertainment, health, science, sports, technology
🏥 Health Check
GET /health
Response Format
News Analysis Response
{
  "article": {
    "title": "Article Title",
    "url": "https://example.com/article",
    "content": "Full article content...",
    "author": "Author Name",
    "publish_date": "2024-01-15T10:30:00Z",
    "source": "news-source.com"
  },
  "summary": {
    "original_title": "Article Title",
    "summary": "Concise summary of the article...",
    "key_points": ["Key point 1", "Key point 2", "Key point 3"],
    "sentiment": "neutral"
  },
  "fact_checks": [
    {
      "claim": "Specific claim from article",
      "verification_status": "verified",
      "evidence": ["Supporting evidence 1", "Supporting evidence 2"],
      "confidence_score": 0.85,
      "sources": ["source1.com", "source2.com"]
    }
  ],
  "credibility_score": 75.5,
  "overall_assessment": "Detailed credibility assessment...",
  "processing_time": 12.34
}
Docker Deployment
Using Docker Compose (Recommended)
# Build and run
docker-compose up --build
# Run in background
docker-compose up -d
Using Docker directly
# Build image
docker build -t news-bot .
# Run container
docker run -p 8000:8000 --env-file .env news-bot
Configuration
Environment Variables
OPENAI_API_KEY=your_openai_api_key_here
SERPER_API_KEY=your_serper_api_key_here
NEWS_API_KEY=your_news_api_key_here
API Configuration
Host: 0.0.0.0 (configurable in config.py)
Port: 8000 (configurable in config.py)
OpenAI Model: gpt-3.5-turbo (configurable in config.py)
Usage Examples
Python Client Example
import requests
# Analyze a single article
response = requests.post(
    "http://localhost:8000/analyze/article",
    json={"url": "https://example.com/news-article"}
)
analysis = response.json()
print(f"Summary: {analysis['summary']['summary']}")
print(f"Credibility Score: {analysis['credibility_score']}")
# Search for articles
response = requests.post(
    "http://localhost:8000/search/topic",
    json={"topic": "climate change", "limit": 3}
)
articles = response.json()
print(f"Found {len(articles['articles'])} articles")
cURL Examples
# Analyze article
curl -X POST "http://localhost:8000/analyze/article" \
  -H "Content-Type: application/json" \
  -d '{"url": "https://example.com/news-article"}'
# Get headlines
curl "http://localhost:8000/headlines/technology?limit=5"
# Search by topic
curl -X POST "http://localhost:8000/search/topic" \
  -H "Content-Type: application/json" \
  -d '{"topic": "artificial intelligence", "limit": 3}'
Architecture
Components
FastAPI Application (main.py): REST API endpoints
News Service (services/news_service.py): Core business logic
News Scraper (utils/news_scraper.py): Web scraping utilities
CrewAI Agents (crew/news_crew.py): AI agents for analysis
Models (models.py): Pydantic data models
AI Agents
News Summarizer: Creates concise summaries with key points
Fact Checker: Verifies claims and finds supporting evidence
Credibility Analyst: Assesses source reliability and content quality
Error Handling
The API includes comprehensive error handling:
400 Bad Request: Invalid input or scraping errors
404 Not Found: Resource not found
500 Internal Server Error: Server-side errors
Validation Errors: Pydantic model validation
Logging
Structured logging is implemented throughout the application:
Level: INFO (configurable)
Format: Timestamp, logger name, level, message
Output: Console (Docker logs in containerized deployment)
Performance Considerations
Async/Await: Non-blocking operations for better performance
Concurrent Processing: Batch analysis uses asyncio for parallel processing
Rate Limiting: Consider implementing rate limiting for production use
Caching: Consider caching frequently accessed news articles
Security
CORS: Configured for cross-origin requests
Input Validation: Pydantic models validate all inputs
Error Handling: Prevents information leakage in error responses
Non-root User: Docker container runs as non-root user
Contributing
Fork the repository
Create a feature branch
Make your changes
Add tests if applicable
Submit a pull request
License
This project is licensed under the MIT License.
API Key Setup
OpenAI API
Visit OpenAI
Create an account and get your API key
Add to .env file
News API
Visit News API
Sign up for a free account
Get your API key
Add to .env file
Serper API
Visit Serper
Sign up for an account
Get your API key
Add to .env file
Troubleshooting
Common Issues
API Key Errors: Ensure all API keys are properly set in .env
Port Conflicts: Change port in config.py if 8000 is in use
Dependencies: Run pip install -r requirements.txt to install all dependencies
Docker Issues: Ensure Docker is running and ports are available
Debug Mode
Set logging level to DEBUG in main.py for detailed logs:
logging.basicConfig(level=logging.DEBUG)
Support
For issues and questions:
Check the documentation
Review the logs for error messages
Ensure all API keys are valid and have sufficient credits
Check network connectivity for external API calls
