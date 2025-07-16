import logging
import time
from contextlib import asynccontextmanager
from typing import List, Dict, Any

from fastapi import FastAPI, HTTPException, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from config import config
from models import (
    NewsArticleRequest, 
    NewsTopicRequest, 
    NewsAnalysis, 
    ErrorResponse
)
from services.news_service import NewsService
from utils.news_scraper import NewsScraperError

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Global service instance
news_service = None

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Lifecycle management for FastAPI app"""
    global news_service
    
    # Startup
    logger.info("Starting News Bot API...")
    
    # Validate configuration
    try:
        config.validate()
        logger.info("Configuration validated successfully")
    except ValueError as e:
        logger.error(f"Configuration validation failed: {str(e)}")
        raise
    
    # Initialize services
    news_service = NewsService()
    logger.info("News service initialized")
    
    yield
    
    # Shutdown
    logger.info("Shutting down News Bot API...")

# Create FastAPI app
app = FastAPI(
    title="News Summarization & Fact-Checking Bot",
    description="AI-powered news analysis tool that summarizes articles and verifies their credibility",
    version="1.0.0",
    lifespan=lifespan
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    """Root endpoint with API information"""
    return {
        "message": "News Summarization & Fact-Checking Bot API",
        "version": "1.0.0",
        "docs": "/docs",
        "status": "running"
    }

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "timestamp": time.time(),
        "service": "news-bot"
    }

@app.post("/analyze/article", response_model=NewsAnalysis)
async def analyze_article(request: NewsArticleRequest):
    """Analyze a single news article from URL"""
    try:
        logger.info(f"Analyzing article: {request.url}")
        
        analysis = await news_service.analyze_article_by_url(str(request.url))
        
        logger.info(f"Analysis completed for: {request.url}")
        return analysis
        
    except NewsScraperError as e:
        logger.error(f"Scraping error: {str(e)}")
        raise HTTPException(
            status_code=400,
            detail=f"Failed to scrape article: {str(e)}"
        )
    except Exception as e:
        logger.error(f"Analysis error: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Analysis failed: {str(e)}"
        )

@app.post("/analyze/batch")
async def batch_analyze_articles(urls: List[str]):
    """Analyze multiple articles concurrently"""
    try:
        logger.info(f"Starting batch analysis of {len(urls)} articles")
        
        if len(urls) > 10:
            raise HTTPException(
                status_code=400,
                detail="Maximum 10 articles allowed per batch"
            )
        
        analyses = await news_service.batch_analyze_articles(urls)
        
        logger.info(f"Batch analysis completed. {len(analyses)} successful analyses")
        return {
            "total_requested": len(urls),
            "successful_analyses": len(analyses),
            "analyses": analyses
        }
        
    except Exception as e:
        logger.error(f"Batch analysis error: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Batch analysis failed: {str(e)}"
        )

@app.post("/search/topic")
async def search_news_by_topic(request: NewsTopicRequest):
    """Search for news articles by topic"""
    try:
        logger.info(f"Searching for articles on topic: {request.topic}")
        
        articles = await news_service.search_and_analyze_topic(
            request.topic, 
            request.limit
        )
        
        logger.info(f"Found {len(articles)} articles for topic: {request.topic}")
        return {
            "topic": request.topic,
            "total_results": len(articles),
            "articles": articles
        }
        
    except NewsScraperError as e:
        logger.error(f"Search error: {str(e)}")
        raise HTTPException(
            status_code=400,
            detail=f"Failed to search news: {str(e)}"
        )
    except Exception as e:
        logger.error(f"Search error: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Search failed: {str(e)}"
        )

@app.get("/headlines/{category}")
async def get_headlines(category: str = "general", limit: int = 10):
    """Get top headlines by category"""
    try:
        logger.info(f"Getting headlines for category: {category}")
        
        valid_categories = [
            "general", "business", "entertainment", "health", 
            "science", "sports", "technology"
        ]
        
        if category not in valid_categories:
            raise HTTPException(
                status_code=400,
                detail=f"Invalid category. Valid categories: {', '.join(valid_categories)}"
            )
        
        if limit > 50:
            raise HTTPException(
                status_code=400,
                detail="Maximum 50 headlines allowed"
            )
        
        headlines = await news_service.get_top_headlines(category, limit)
        
        logger.info(f"Retrieved {len(headlines)} headlines for category: {category}")
        return {
            "category": category,
            "total_results": len(headlines),
            "headlines": headlines
        }
        
    except NewsScraperError as e:
        logger.error(f"Headlines error: {str(e)}")
        raise HTTPException(
            status_code=400,
            detail=f"Failed to get headlines: {str(e)}"
        )
    except Exception as e:
        logger.error(f"Headlines error: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Failed to get headlines: {str(e)}"
        )

@app.exception_handler(Exception)
async def global_exception_handler(request, exc):
    """Global exception handler"""
    logger.error(f"Unhandled exception: {str(exc)}")
    return JSONResponse(
        status_code=500,
        content={
            "error": "Internal Server Error",
            "message": "An unexpected error occurred",
            "status_code": 500
        }
    )

if __name__ == "__main__":
    import uvicorn
    
    uvicorn.run(
        "main:app",
        host=config.API_HOST,
        port=config.API_PORT,
        reload=True,
        log_level="info"
    )