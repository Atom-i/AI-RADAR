import asyncio
import logging
from datetime import datetime
from typing import List, Dict
import json
from scrapers.arxiv_scraper import ArxivScraper
from scrapers.github_scraper import GitHubScraper
from scrapers.hackernews_scraper import HackNewsScraper
from processors.nlp_processor import NLPProcessor
from processors.trend_analyzer import TrendAnalyzer

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class AIRadar:
    def __init__(self):
        logger.info("🎯 Initializing AI RADAR...")
        self.arxiv_scraper = ArxivScraper()
        self.github_scraper = GitHubScraper()
        self.hackernews_scraper = HackNewsScraper()
        self.nlp_processor = NLPProcessor()
        self.trend_analyzer = TrendAnalyzer()
        self.data = {'timestamp': datetime.now().isoformat(), 'sources': {}}

    async def run(self):
        logger.info("\n" + "="*60)
        logger.info("🎯 STARTING AI RADAR SCAN")
        logger.info("="*60)
        
        start_time = datetime.now()
        
        try:
            logger.info("📋 Running concurrent scrapers...")
            results = await asyncio.gather(
                self.arxiv_scraper.scrape(),
                self.github_scraper.scrape(),
                self.hackernews_scraper.scrape(),
                return_exceptions=True
            )
            
            for i, result in enumerate(results):
                if isinstance(result, Exception):
                    logger.error(f"❌ Scraper error: {result}")
                else:
                    logger.info(f"✅ Scraper {i+1} completed")
            
            self.data['sources']['arxiv'] = results[0] if not isinstance(results[0], Exception) else []
            self.data['sources']['github'] = results[1] if not isinstance(results[1], Exception) else []
            self.data['sources']['hackernews'] = results[2] if not isinstance(results[2], Exception) else []
            
            await self.analyze_trends()
            
            duration = (datetime.now() - start_time).total_seconds()
            logger.info(f"\n✅ AI RADAR SCAN COMPLETE in {duration:.2f}s")
            logger.info("="*60 + "\n")
            
        except Exception as e:
            logger.error(f"❌ Fatal error during scan: {e}")
        
        return self.data

    async def analyze_trends(self):
        logger.info("📈 Analyzing trends...")
        all_items = []
        for source_data in self.data['sources'].values():
            if isinstance(source_data, list):
                all_items.extend(source_data)
        
        if all_items:
            analysis = self.trend_analyzer.analyze(all_items)
            self.data['analysis'] = analysis
            logger.info(f"🔥 Found {len(analysis.get('top_trends', []))} trending topics")

    def save_results(self, filename: str = 'ai_radar_results.json'):
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(self.data, f, indent=2, ensure_ascii=False)
            logger.info(f"💾 Results saved to {filename}")
        except Exception as e:
            logger.error(f"❌ Error saving results: {e}")

    def print_summary(self):
        print("\n" + "="*60)
        print("📋 AI RADAR SUMMARY")
        print("="*60)
        print(f"ArXiv Papers: {len(self.data['sources'].get('arxiv', []))}")
        print(f"GitHub Repos: {len(self.data['sources'].get('github', []))}")
        print(f"HackerNews Items: {len(self.data['sources'].get('hackernews', []))}")
        
        if 'analysis' in self.data:
            trends = self.data['analysis'].get('top_trends', [])
            if trends:
                print("\n🔥 Top Trends:")
                for i, (trend, count) in enumerate(trends[:5], 1):
                    print(f"  {i}. {trend} ({count} mentions)")
        
        print("="*60 + "\n")

async def main():
    radar = AIRadar()
    results = await radar.run()
    radar.save_results()
    radar.print_summary()

if __name__ == "__main__":
    asyncio.run(main())