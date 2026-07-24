from fastapi import FastAPI, BackgroundTasks
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
import logging
import json
from typing import Dict, List
import asyncio
from main import AIRadar
from datetime import datetime

logger = logging.getLogger(__name__)
app = FastAPI(
    title="AI RADAR API",
    description="Real-time AI Technology Tracking & Trend Analysis",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

radar = AIRadar()
last_scan_data = None
last_scan_time = None

@app.get("/")
async def root():
    return {
        "status": "AI RADAR is running 🎯",
        "version": "1.0.0",
        "endpoints": ["/trends", "/papers", "/repos", "/news", "/radar/scan", "/radar/status", "/health"]
    }

@app.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "last_scan": last_scan_time
    }

@app.get("/trends")
async def get_trends():
    if last_scan_data:
        analysis = last_scan_data.get('analysis', {})
        return {
            "trends": analysis.get('top_trends', []),
            "source_distribution": analysis.get('source_distribution', {}),
            "timestamp": last_scan_time
        }
    return {"error": "No scan data available. Run /radar/scan first"}

@app.get("/papers")
async def get_papers():
    if last_scan_data:
        papers = last_scan_data.get('sources', {}).get('arxiv', [])
        return {"papers": papers, "count": len(papers), "timestamp": last_scan_time}
    return {"error": "No scan data available. Run /radar/scan first"}

@app.get("/repos")
async def get_repositories():
    if last_scan_data:
        repos = last_scan_data.get('sources', {}).get('github', [])
        repos_sorted = sorted(repos, key=lambda x: x.get('stars', 0), reverse=True)
        return {"repositories": repos_sorted, "count": len(repos), "timestamp": last_scan_time}
    return {"error": "No scan data available. Run /radar/scan first"}

@app.get("/news")
async def get_news():
    if last_scan_data:
        news = last_scan_data.get('sources', {}).get('hackernews', [])
        return {"news": news, "count": len(news), "timestamp": last_scan_time}
    return {"error": "No scan data available. Run /radar/scan first"}

@app.post("/radar/scan")
async def radar_scan(background_tasks: BackgroundTasks):
    global last_scan_data, last_scan_time
    
    logger.info("🎯 Starting radar scan via API...")
    
    try:
        last_scan_data = await radar.run()
        last_scan_time = datetime.now().isoformat()
        
        return {
            "status": "✅ Scan completed",
            "timestamp": last_scan_time,
            "data_summary": {
                "papers": len(last_scan_data.get('sources', {}).get('arxiv', [])),
                "repositories": len(last_scan_data.get('sources', {}).get('github', [])),
                "news": len(last_scan_data.get('sources', {}).get('hackernews', []))
            }
        }
    except Exception as e:
        logger.error(f"❌ Scan error: {e}")
        return {"error": str(e)}

@app.get("/radar/status")
async def radar_status():
    return {
        "status": "running",
        "last_scan": last_scan_time,
        "data_available": last_scan_data is not None
    }

@app.get("/api/v1/summary")
async def api_summary():
    if not last_scan_data:
        return {"error": "No scan data available"}
    
    sources = last_scan_data.get('sources', {})
    analysis = last_scan_data.get('analysis', {})
    
    return {
        "timestamp": last_scan_time,
        "summary": {
            "total_items": analysis.get('total_items', 0),
            "sources": {
                "papers": len(sources.get('arxiv', [])),
                "repositories": len(sources.get('github', [])),
                "news": len(sources.get('hackernews', []))
            },
            "top_5_trends": analysis.get('top_trends', [])[:5],
            "source_distribution": analysis.get('source_distribution', {})
        },
        "data": last_scan_data
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)