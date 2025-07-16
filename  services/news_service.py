import asyncio
import time
from typing import List, Dict, Any
import logging
from models import NewsArticle, NewsAnalysis, Summary, FactCheck
from ..utils.news_scraper import NewsScraper, NewsScraperError
from ..crew.news_crew import NewsAnalysisCrew

logger = logging.getLogger(__name__)

class NewsService:
    def __init__(self):
        self.scraper = NewsScraper()
        self.analysis_crew = NewsAnalysisCrew()
    
    async def analyze_article_by_url(self, url: str) -> NewsAnalysis:
        """Analyze a news article from a given URL"""
        start_time = time.time()
        
        try:
            # Scrape the article
            logger.info(f"Scraping article from URL: {url}")
            article = self.scraper.scrape_article(url)
            
            # Analyze the article with AI crew
            logger.info("Starting AI crew analysis...")
            analysis_results = await self._run_crew_analysis(article)
            
            # Parse results into structured format
            summary = Summary(
                original_title=article.title,
                summary=analysis_results["summary"]["summary"],
                key_points=analysis_results["summary"]["key_points"],
                sentiment=analysis_results["summary"]["sentiment"]
            )
            
            fact_checks = []
            for fc_data in analysis_results["fact_checks"]:
                fact_check = FactCheck(
                    claim=fc_data.get("claim", ""),
                    verification_status=fc_data.get("verification_status", "unverified"),
                    evidence=fc_data.get("evidence", []),
                    confidence_score=fc_data.get("confidence_score", 0.0),
                    sources=fc_data.get("sources", [])
                )
                fact_checks.append(fact_check)
            
            # Calculate processing time
            processing_time = time.time() - start_time
            
            # Create final analysis
            news_analysis = NewsAnalysis(
                article=article,
                summary=summary,
                fact_checks=fact_checks,
                credibility_score=analysis_results["credibility"]["credibility_score"],
                overall_assessment=analysis_results["credibility"]["assessment"],
                processing_time=processing_time
            )
            
            logger.info(f"Analysis completed in {processing_time:.2f} seconds")
            return news_analysis
            
        except NewsScraperError as e:
            logger.error(f"Error scraping article: {str(e)}")
            raise
        except Exception as e:
            logger.error(f"Error analyzing article: {str(e)}")
            raise
    
    async def search_and_analyze_topic(self, topic: str, limit: int = 5) -> List[Dict[str, Any]]:
        """Search for news articles on a topic and return basic information"""
        try:
            logger.info(f"Searching for articles on topic: {topic}")
            articles = self.scraper.search_news_by_topic(topic, limit)
            
            # Return basic article information without full analysis
            results = []
            for article_data in articles:
                results.append({
                    "title": article_data["title"],
                    "url": article_data["url"],
                    "description": article_data["description"],
                    "source": article_data["source"],
                    "published_at": article_data["published_at"],
                    "author": article_data["author"]
                })
            
            logger.info(f"Found {len(results)} articles for topic: {topic}")
            return results
            
        except NewsScraperError as e:
            logger.error(f"Error searching for topic: {str(e)}")
            raise
        except Exception as e:
            logger.error(f"Unexpected error searching for topic: {str(e)}")
            raise
    
    async def get_top_headlines(self, category: str = "general", limit: int = 10) -> List[Dict[str, Any]]:
        """Get top headlines from news sources"""
        try:
            logger.info(f"Getting top headlines for category: {category}")
            headlines = self.scraper.get_top_headlines(category, limit)
            
            results = []
            for headline_data in headlines:
                results.append({
                    "title": headline_data["title"],
                    "url": headline_data["url"],
                    "description": headline_data["description"],
                    "source": headline_data["source"],
                    "published_at": headline_data["published_at"],
                    "author": headline_data["author"]
                })
            
            logger.info(f"Retrieved {len(results)} headlines for category: {category}")
            return results
            
        except NewsScraperError as e:
            logger.error(f"Error getting headlines: {str(e)}")
            raise
        except Exception as e:
            logger.error(f"Unexpected error getting headlines: {str(e)}")
            raise
    
    async def _run_crew_analysis(self, article: NewsArticle) -> Dict[str, Any]:
        """Run the AI crew analysis in a separate thread to avoid blocking"""
        loop = asyncio.get_event_loop()
        
        # Run crew analysis in thread pool to avoid blocking
        return await loop.run_in_executor(
            None, 
            self.analysis_crew.analyze_article, 
            article
        )
    
    async def batch_analyze_articles(self, urls: List[str]) -> List[NewsAnalysis]:
        """Analyze multiple articles concurrently"""
        try:
            logger.info(f"Starting batch analysis of {len(urls)} articles")
            
            # Create tasks for concurrent processing
            tasks = []
            for url in urls:
                task = asyncio.create_task(self.analyze_article_by_url(url))
                tasks.append(task)
            
            # Wait for all tasks to complete
            results = await asyncio.gather(*tasks, return_exceptions=True)
            
            # Filter out exceptions and return successful analyses
            successful_analyses = []
            for i, result in enumerate(results):
                if isinstance(result, Exception):
                    logger.error(f"Failed to analyze article {urls[i]}: {str(result)}")
                else:
                    successful_analyses.append(result)
            
            logger.info(f"Batch analysis completed. {len(successful_analyses)} successful, {len(results) - len(successful_analyses)} failed")
            return successful_analyses
            
        except Exception as e:
            logger.error(f"Error in batch analysis: {str(e)}")
            raise