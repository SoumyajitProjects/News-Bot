from crewai import Agent, Task, Crew, Process
from crewai.tools import SerperDevTool
from typing import List, Dict, Any
import logging
from models import NewsArticle, Summary, FactCheck
from config import config

logger = logging.getLogger(__name__)

class NewsAnalysisCrew:
    def __init__(self):
        self.search_tool = SerperDevTool()
        
    def _create_summarizer_agent(self) -> Agent:
        """Create an agent specialized in summarizing news articles"""
        return Agent(
            role="News Summarizer",
            goal="Create concise, accurate summaries of news articles while preserving key information",
            backstory=(
                "You are an expert news summarizer with years of experience in journalism. "
                "You excel at distilling complex news stories into clear, comprehensive summaries "
                "that capture the essence of the original article while highlighting key points."
            ),
            verbose=True,
            allow_delegation=False,
            tools=[]
        )
    
    def _create_fact_checker_agent(self) -> Agent:
        """Create an agent specialized in fact-checking news content"""
        return Agent(
            role="Fact Checker",
            goal="Verify claims made in news articles and assess their credibility",
            backstory=(
                "You are a meticulous fact-checker with expertise in verifying information "
                "across multiple sources. You have a keen eye for identifying potential "
                "misinformation and are skilled at cross-referencing claims with reliable sources."
            ),
            verbose=True,
            allow_delegation=False,
            tools=[self.search_tool]
        )
    
    def _create_credibility_analyst_agent(self) -> Agent:
        """Create an agent specialized in assessing news source credibility"""
        return Agent(
            role="Credibility Analyst",
            goal="Evaluate the overall credibility and reliability of news sources and articles",
            backstory=(
                "You are a media literacy expert with deep knowledge of journalistic standards "
                "and source reliability. You assess the credibility of news sources based on "
                "their reputation, editorial standards, and track record of accuracy."
            ),
            verbose=True,
            allow_delegation=False,
            tools=[self.search_tool]
        )
    
    def _create_summarization_task(self, article: NewsArticle) -> Task:
        """Create a task for summarizing the news article"""
        return Task(
            description=(
                f"Summarize the following news article:\n"
                f"Title: {article.title}\n"
                f"Content: {article.content}\n\n"
                f"Provide:\n"
                f"1. A concise summary (2-3 sentences)\n"
                f"2. Key points (3-5 bullet points)\n"
                f"3. Sentiment analysis (positive/negative/neutral)\n"
                f"Format your response as JSON with keys: summary, key_points, sentiment"
            ),
            expected_output="A JSON object containing summary, key_points array, and sentiment",
            agent=self._create_summarizer_agent()
        )
    
    def _create_fact_checking_task(self, article: NewsArticle) -> Task:
        """Create a task for fact-checking the news article"""
        return Task(
            description=(
                f"Fact-check the following news article:\n"
                f"Title: {article.title}\n"
                f"Content: {article.content}\n\n"
                f"Identify key claims and verify them using reliable sources. "
                f"For each claim, provide:\n"
                f"1. The specific claim\n"
                f"2. Verification status (verified/false/partially_true/unverified)\n"
                f"3. Supporting evidence\n"
                f"4. Confidence score (0-1)\n"
                f"5. Sources used for verification\n"
                f"Format as JSON array of fact-check objects"
            ),
            expected_output="A JSON array of fact-check objects with claim, status, evidence, confidence, and sources",
            agent=self._create_fact_checker_agent()
        )
    
    def _create_credibility_assessment_task(self, article: NewsArticle) -> Task:
        """Create a task for assessing article credibility"""
        return Task(
            description=(
                f"Assess the credibility of this news article and its source:\n"
                f"Title: {article.title}\n"
                f"Source: {article.source}\n"
                f"Author: {article.author}\n"
                f"Content: {article.content[:500]}...\n\n"
                f"Evaluate based on:\n"
                f"1. Source reputation and reliability\n"
                f"2. Editorial standards and fact-checking practices\n"
                f"3. Author credentials and expertise\n"
                f"4. Content quality and journalistic standards\n"
                f"5. Potential bias or agenda\n"
                f"Provide a credibility score (0-100) and detailed assessment.\n"
                f"Format as JSON with keys: credibility_score, assessment"
            ),
            expected_output="A JSON object with credibility_score and detailed assessment",
            agent=self._create_credibility_analyst_agent()
        )
    
    def analyze_article(self, article: NewsArticle) -> Dict[str, Any]:
        """Analyze a news article using the crew of AI agents"""
        try:
            # Create tasks
            summarization_task = self._create_summarization_task(article)
            fact_checking_task = self._create_fact_checking_task(article)
            credibility_task = self._create_credibility_assessment_task(article)
            
            # Create and run crew
            crew = Crew(
                agents=[
                    self._create_summarizer_agent(),
                    self._create_fact_checker_agent(),
                    self._create_credibility_analyst_agent()
                ],
                tasks=[summarization_task, fact_checking_task, credibility_task],
                process=Process.sequential,
                verbose=True
            )
            
            # Execute the crew
            results = crew.kickoff()
            
            # Parse results
            return self._parse_crew_results(results)
            
        except Exception as e:
            logger.error(f"Error in crew analysis: {str(e)}")
            raise
    
    def _parse_crew_results(self, results: List[str]) -> Dict[str, Any]:
        """Parse the results from the crew execution"""
        try:
            import json
            
            # Initialize default values
            summary_data = {
                "summary": "Unable to generate summary",
                "key_points": [],
                "sentiment": "neutral"
            }
            
            fact_checks = []
            credibility_data = {
                "credibility_score": 50.0,
                "assessment": "Unable to assess credibility"
            }
            
            # Parse each result
            for i, result in enumerate(results):
                try:
                    if i == 0:  # Summarization result
                        summary_data = json.loads(result)
                    elif i == 1:  # Fact-checking result
                        fact_checks = json.loads(result)
                    elif i == 2:  # Credibility assessment result
                        credibility_data = json.loads(result)
                except json.JSONDecodeError:
                    logger.warning(f"Failed to parse result {i}: {result}")
                    continue
            
            return {
                "summary": summary_data,
                "fact_checks": fact_checks,
                "credibility": credibility_data
            }
            
        except Exception as e:
            logger.error(f"Error parsing crew results: {str(e)}")
            return {
                "summary": {"summary": "Error generating summary", "key_points": [], "sentiment": "neutral"},
                "fact_checks": [],
                "credibility": {"credibility_score": 0.0, "assessment": "Error assessing credibility"}
            }
