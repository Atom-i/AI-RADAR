import feedparser
import logging
from typing import List, Dict
from config import HACKERNEWS_KEYWORDS
import asyncio

logger = logging.getLogger(__name__)

class HackNewsScraper:
    def __init__(self):
        self.feed_url = "https://news.ycombinator.com/rss"
        self.keywords = HACKERNEWS_KEYWORDS

    async def scrape(self) -> List[Dict]:
        logger.info("📰 Starting HackerNews scraper...")
        news = []
        
        try:
            logger.debug("  Fetching HackerNews RSS feed...")
            feed = feedparser.parse(self.feed_url)
            
            for entry in feed.entries[:30]:
                title = entry.get('title', '').lower()
                matching_keywords = [kw for kw in self.keywords if kw.lower() in title]
                
                if matching_keywords:
                    article = {
                        'title': entry.get('title', ''),
                        'link': entry.get('link', ''),
                        'published': entry.get('published', ''),
                        'source': 'hackernews',
                        'keywords': matching_keywords
                    }
                    news.append(article)
            
            logger.info(f"✅ HackerNews scraper found {len(news)} relevant articles")
        
        except Exception as e:
            logger.error(f"❌ Error scraping HackerNews: {e}")
        
        return news