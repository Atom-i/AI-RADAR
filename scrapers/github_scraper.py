import aiohttp
import logging
from typing import List, Dict
from config import GITHUB_QUERIES, GITHUB_TOKEN
import asyncio

logger = logging.getLogger(__name__)

class GitHubScraper:
    def __init__(self):
        self.api_url = "https://api.github.com/search/repositories"
        self.queries = GITHUB_QUERIES
        self.token = GITHUB_TOKEN
        self.timeout = aiohttp.ClientTimeout(total=30)
        self.headers = {'Accept': 'application/vnd.github.v3+json'}
        if self.token:
            self.headers['Authorization'] = f'token {self.token}'

    async def scrape(self) -> List[Dict]:
        logger.info("🐙 Starting GitHub scraper...")
        repos = []
        
        async with aiohttp.ClientSession(timeout=self.timeout, headers=self.headers) as session:
            for query in self.queries:
                try:
                    logger.debug(f"  Searching for: {query}")
                    params = {'q': query, 'sort': 'stars', 'per_page': 10}
                    
                    async with session.get(self.api_url, params=params) as response:
                        if response.status == 200:
                            data = await response.json()
                            
                            for repo in data.get('items', [])[:3]:
                                repository = {
                                    'name': repo['name'],
                                    'owner': repo['owner']['login'],
                                    'url': repo['html_url'],
                                    'description': repo['description'],
                                    'stars': repo['stargazers_count'],
                                    'language': repo['language'],
                                    'updated_at': repo['updated_at'],
                                    'source': 'github',
                                    'query': query
                                }
                                repos.append(repository)
                        
                        await asyncio.sleep(0.5)
                
                except Exception as e:
                    logger.warning(f"❌ Error scraping '{query}': {e}")
        
        logger.info(f"✅ GitHub scraper found {len(repos)} repositories")
        return repos