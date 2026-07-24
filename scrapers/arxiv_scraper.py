import aiohttp
import logging
from typing import List, Dict
from config import ARXIV_KEYWORDS
from bs4 import BeautifulSoup
import asyncio

logger = logging.getLogger(__name__)

class ArxivScraper:
    def __init__(self):
        self.base_url = "https://arxiv.org/search/"
        self.keywords = ARXIV_KEYWORDS
        self.timeout = aiohttp.ClientTimeout(total=30)

    async def scrape(self) -> List[Dict]:
        logger.info("📚 Starting ArXiv scraper...")
        papers = []
        
        async with aiohttp.ClientSession(timeout=self.timeout) as session:
            for keyword in self.keywords:
                try:
                    logger.debug(f"  Searching for: {keyword}")
                    params = {'query': keyword, 'searchtype': 'all', 'size': 10}
                    
                    async with session.get(self.base_url, params=params) as response:
                        if response.status == 200:
                            html = await response.text()
                            soup = BeautifulSoup(html, 'html.parser')
                            results = soup.find_all('div', class_='arxiv-result')
                            
                            for result in results[:3]:
                                try:
                                    title_elem = result.find('p', class_='title')
                                    authors_elem = result.find('p', class_='authors')
                                    
                                    if title_elem:
                                        paper = {
                                            'title': title_elem.get_text(strip=True),
                                            'authors': authors_elem.get_text(strip=True) if authors_elem else '',
                                            'source': 'arxiv',
                                            'keyword': keyword
                                        }
                                        papers.append(paper)
                                except Exception as e:
                                    logger.debug(f"Error parsing paper: {e}")
                        
                        await asyncio.sleep(0.5)
                
                except Exception as e:
                    logger.warning(f"❌ Error scraping '{keyword}': {e}")
        
        logger.info(f"✅ ArXiv scraper found {len(papers)} papers")
        return papers