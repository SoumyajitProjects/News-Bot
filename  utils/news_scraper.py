import requests
from newspaper import Article
from bs4 import BeautifulSoup
from typing import Optional, List, Dict
import logging
from datetime import datetime
from config import config
from models import NewsArticle

logger = logging.getLogger(__name__)

class NewsScraperError(Exception):
    """Custom exception for news scraping errors"""
    pass

class NewsScraper:
    def __init__(self):
        self.news_api_key = config.NEWS_API_KEY
        self.base_url = config.NEWS_API_BASE_URL
        
    def scrape_article(self, url: str) -> NewsArticle:
        """Scrape a news article from a given URL"""
        try:
            article = Article(url)
            article.download()
            article.parse()
            
            # Extract publish date
            publish_date = None
            if article.publish_date:
                publish_date = article.publish_date
            
            return NewsArticle(
                title=article.title or "No title found",
                url=url,
                content=article.text or "No content found",
                author=", ".join(article.authors) if article.authors else None,
                publish_date=publish_date,
                source=article.source_url or url
            )
            
        except Exception as e:
            logger.error(f"Error scraping article from {url}: {str(e)}")
            raise NewsScraperError(f"Failed to scrape article: {str(e)}")
    
    def search_news_by_topic(self, topic: str, limit: int = 5) -> List[Dict]:
        """Search for news articles by topic using News API"""
        try:
            url = f"{self.base_url}/everything"
            params = {
                'q': topic,
                'apiKey': self.news_api_key,
                'sortBy': 'publishedAt',
                'pageSize': limit,
                'language': 'en'
            }
            
            response = requests.get(url, params=params)
            response.raise_for_status()
            
            data = response.json()
            
            if data.get('status') != 'ok':
                raise NewsScraperError(f"News API error: {data.get('message', 'Unknown error')}")
            
            articles = []
            for article_data in data.get('articles', []):
                if article_data.get('url'):
                    articles.append({
                        'title': article_data.get('title', ''),
                        'url': article_data.get('url', ''),
                        'description': article_data.get('description', ''),
                        'source': article_data.get('source', {}).get('name', ''),
                        'published_at': article_data.get('publishedAt', ''),
                        'author': article_data.get('author', '')
                    })
            
            return articles
            
        except requests.exceptions.RequestException as e:
            logger.error(f"Request error while searching news: {str(e)}")
            raise NewsScraperError(f"Failed to search news: {str(e)}")
        except Exception as e:
            logger.error(f"Unexpected error while searching news: {str(e)}")
            raise NewsScraperError(f"Unexpected error: {str(e)}")
    
    def get_top_headlines(self, category: str = 'general', limit: int = 10) -> List[Dict]:
        """Get top headlines from News API"""
        try:
            url = f"{self.base_url}/top-headlines"
            params = {
                'category': category,
                'apiKey': self.news_api_key,
                'pageSize': limit,
                'country': 'us'
            }
            
            response = requests.get(url, params=params)
            response.raise_for_status()
            
            data = response.json()
            
            if data.get('status') != 'ok':
                raise NewsScraperError(f"News API error: {data.get('message', 'Unknown error')}")
            
            articles = []
            for article_data in data.get('articles', []):
                if article_data.get('url'):
                    articles.append({
                        'title': article_data.get('title', ''),
                        'url': article_data.get('url', ''),
                        'description': article_data.get('description', ''),
                        'source': article_data.get('source', {}).get('name', ''),
                        'published_at': article_data.get('publishedAt', ''),
                        'author': article_data.get('author', '')
                    })
            
            return articles
            
        except requests.exceptions.RequestException as e:
            logger.error(f"Request error while getting headlines: {str(e)}")
            raise NewsScraperError(f"Failed to get headlines: {str(e)}")
        except Exception as e:
            logger.error(f"Unexpected error while getting headlines: {str(e)}")
            raise NewsScraperError(f"Unexpected error: {str(e)}")
