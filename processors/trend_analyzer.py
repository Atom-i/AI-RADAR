import logging
from typing import List, Dict
from collections import Counter
from datetime import datetime

logger = logging.getLogger(__name__)

class TrendAnalyzer:
    def __init__(self):
        logger.info("📈 Initializing Trend Analyzer...")
        self.trends = {}

    def analyze(self, items: List[Dict]) -> Dict:
        try:
            keywords = []
            categories = []
            sources = []
            
            for item in items:
                if 'title' in item:
                    words = item['title'].lower().split()
                    keywords.extend(words)
                
                if 'keyword' in item:
                    keywords.append(item['keyword'])
                
                if 'query' in item:
                    keywords.append(item['query'])
                
                if 'keywords' in item:
                    keywords.extend(item['keywords'])
                
                sources.append(item.get('source', 'unknown'))
            
            keyword_counter = Counter(keywords)
            source_counter = Counter(sources)
            
            common_words = {'ai', 'the', 'and', 'or', 'a', 'an', 'to', 'of', 'in', 'is', 'for'}
            filtered_keywords = [
                (kw, count) for kw, count in keyword_counter.most_common(20)
                if kw not in common_words and len(kw) > 2
            ]
            
            return {
                'top_trends': filtered_keywords[:10],
                'source_distribution': dict(source_counter),
                'total_items': len(items),
                'analysis_time': datetime.now().isoformat()
            }
        
        except Exception as e:
            logger.error(f"Error analyzing trends: {e}")
            return {
                'top_trends': [],
                'source_distribution': {},
                'total_items': len(items),
                'analysis_time': datetime.now().isoformat()
            }

    def get_top_trends(self, limit: int = 10) -> List[tuple]:
        return self.trends.get('top_trends', [])[:limit]