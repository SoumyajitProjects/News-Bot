# 🧠 News Summarization & Fact-Checking Bot

An AI-powered news analysis tool that summarizes articles and verifies their credibility using **CrewAI**, **OpenAI**, and **FastAPI**.

---

## ✨ Features

- 🔍 **News Article Scraping** – Extracts content from news URLs  
- 📄 **AI-Powered Summarization** – Generates concise summaries with key points  
- ✅ **Fact-Checking** – Verifies claims and assesses credibility  
- 🎯 **Topic Search** – Find articles by topic or keyword  
- 📊 **Credibility Scoring** – Rates news sources and content reliability  
- 🚀 **FastAPI Backend** – Modern async API with automatic docs  
- 🐳 **Docker Support** – Easy containerized deployment

---

## 🛠 Tech Stack

| Technology     | Role                                      |
|----------------|-------------------------------------------|
| **CrewAI**     | Multi-agent system for news analysis      |
| **OpenAI**     | LLM for NLP, summarization, fact-checking |
| **FastAPI**    | Backend web framework                     |
| **News API**   | Real-time news article sourcing           |
| **Serper API** | Search functionality for fact-checking    |
| **Docker**     | Containerization and deployment           |

---

## 🚀 Quick Start

### ✅ Prerequisites

- Python 3.11+
- API Keys:
  - `OPENAI_API_KEY`
  - `NEWS_API_KEY` (from [newsapi.org](https://newsapi.org))
  - `SERPER_API_KEY` (from [serper.dev](https://serper.dev))

---

### 🔧 Installation

```bash
# Clone the repository
git clone https://github.com/SoumyajitProjects/New-Bot.git
cd New-Bot

# Create virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Configure environment variables
cp .env.example .env
# Edit `.env` file and add your API keys
```

---

### ▶️ Run the App

```bash
python main.py
```

App will be available at: [http://localhost:8000](http://localhost:8000)

---

## 📚 API Documentation

- Swagger UI: [http://localhost:8000/docs](http://localhost:8000/docs)  
- ReDoc: [http://localhost:8000/redoc](http://localhost:8000/redoc)

---

## 🔍 API Endpoints

### 📄 Analyze a Single Article

```http
POST /analyze/article
Content-Type: application/json

{
  "url": "https://example.com/news-article"
}
```

### 📑 Batch Analyze Articles

```http
POST /analyze/batch
Content-Type: application/json

[
  "https://example.com/article1",
  "https://example.com/article2"
]
```

### 🎯 Search News by Topic

```http
POST /search/topic
Content-Type: application/json

{
  "topic": "artificial intelligence",
  "limit": 5
}
```

### 📰 Get Headlines by Category

```http
GET /headlines/{category}?limit=10
```

- Categories: `general`, `business`, `entertainment`, `health`, `science`, `sports`, `technology`

---

## ⚙️ Response Format

```json
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
    "summary": "Concise summary...",
    "key_points": ["Point 1", "Point 2"],
    "sentiment": "neutral"
  },
  "fact_checks": [
    {
      "claim": "Claim text",
      "verification_status": "verified",
      "confidence_score": 0.85,
      "evidence": ["Evidence 1", "Evidence 2"],
      "sources": ["source1.com", "source2.com"]
    }
  ],
  "credibility_score": 75.5,
  "overall_assessment": "Detailed credibility assessment...",
  "processing_time": 12.34
}
```

---

## 🐳 Docker Deployment

### 🔁 With Docker Compose (Recommended)

```bash
docker-compose up --build
# or run in background
docker-compose up -d
```

### 🐋 With Docker CLI

```bash
docker build -t news-bot .
docker run -p 8000:8000 --env-file .env news-bot
```

---

## 🧱 Architecture Overview

- `main.py`: FastAPI entrypoint
- `services/news_service.py`: Core business logic
- `utils/news_scraper.py`: Article scraping utilities
- `crew/news_crew.py`: CrewAI agents
- `models.py`: Pydantic data models

### 🤖 AI Agent Roles

| Agent              | Role                                       |
|--------------------|--------------------------------------------|
| **News Summarizer**| Generates concise summaries with key points|
| **Fact Checker**   | Verifies article claims                    |
| **Credibility Analyst** | Scores source reliability              |

---

## 🛡 Error Handling

- `400`: Bad request / scraping failure
- `404`: Resource not found
- `500`: Internal server error
- Validation: Input errors handled by Pydantic

---

## 📈 Logging & Performance

- Log level: `INFO` (can be set to `DEBUG`)
- Async FastAPI + asyncio for high throughput
- Structured logs (timestamped, color-coded)
- Batch article analysis is concurrent
- Suggestions:
  - Add rate limiting
  - Cache frequently accessed results

---

## 🔐 Security

- Input validation via Pydantic
- CORS enabled
- No sensitive data in error responses
- Docker runs as non-root user

---

## 🧪 Contributing

1. Fork this repo  
2. Create a feature branch  
3. Implement your changes  
4. Add tests if needed  
5. Submit a PR!

---

## 📄 License

This project is licensed under the **MIT License**.

---

## 🧠 API Key Setup

| Service     | Link                                |
|-------------|-------------------------------------|
| OpenAI      | [openai.com](https://openai.com)     |
| News API    | [newsapi.org](https://newsapi.org)   |
| Serper API  | [serper.dev](https://serper.dev)     |

---

## 🧰 Troubleshooting

| Problem              | Solution                                     |
|----------------------|----------------------------------------------|
| API Key Error        | Double-check `.env` file                     |
| Port Conflict        | Change port in `config.py`                   |
| Missing Dependencies | Run `pip install -r requirements.txt`        |
| Docker Issues        | Check Docker is running, port is open        |

### Debug Mode

```python
# main.py
import logging
logging.basicConfig(level=logging.DEBUG)
```

---
