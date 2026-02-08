import feedparser
import time
from datetime import datetime, timedelta, timezone
from typing import List, Dict, Any
import re


# Loads feed URLs; fails if config path is modified.
from config.feeds import INITIAL_FEEDS

def clean_and_truncate(text: str, sentence_limit: int = 5) -> str:
    """
    Cleans RSS content by removing HTML and whitespace.
    Truncates to N sentences to provide concise context for the SLM agent while minimizing token costs.
    """
    if not text:
        return ""
    # 1. Remove HTML tags
    clean_text = re.sub(r'<[^>]+>', '', text)
    # 2. Normalize whitespace
    clean_text = re.sub(r'\s+', ' ', clean_text).strip()
    # 3. Simple sentence splitting (greedy)
    sentences = re.split(r'(?<=[.!?])\s+', clean_text)
    return " ".join(sentences[:sentence_limit])


def fetch_recent_news(minutes_back: int = 30) -> List[Dict[str, Any]]:
    """Fetches articles published within the last N minutes."""
    cutoff_time = datetime.now(timezone.utc) - timedelta(minutes=minutes_back)
    all_news = []

    print(f"[*] Fetching news posted after: {cutoff_time.strftime('%Y-%m-%d %H:%M:%S UTC')}")

    for source_name, url in INITIAL_FEEDS:
        try:
            print(f"    - Checking {source_name}...", end="", flush=True)
            feed = feedparser.parse(url)
            
            count = 0
            for entry in feed.entries:
                # Normalizing the published time
                # Some feeds use published_parsed, others might not have it
                published_struct = getattr(entry, 'published_parsed', None)
                if not published_struct:
                    continue
                
                published_dt = datetime.fromtimestamp(time.mktime(published_struct), tz=timezone.utc)
                
                if published_dt > cutoff_time:
                    # SMART PARSING: Try content, fallback to summary, then title
                    raw_text = ""
                    if hasattr(entry, 'content'):
                        raw_text = entry.content[0].value
                    elif hasattr(entry, 'summary'):
                        raw_text = entry.summary
                    
                    processed_summary = clean_and_truncate(raw_text, sentence_limit=5)
                    
                    # If the result is too short, the title might be more descriptive
                    if len(processed_summary) < 30:
                        processed_summary = entry.title

                    all_news.append({
                        "source": source_name,
                        "title": entry.title,
                        "url": entry.link,
                        "published_at": published_dt,
                        "summary": processed_summary
                    })
                    count += 1
            
            print(f" Found {count} new articles.")
            
        except Exception as e:
            print(f" ERROR: {e}")

    # Sort by time, newest first
    return sorted(all_news, key=lambda x: x['published_at'], reverse=True)

if __name__ == "__main__":
    # Run for 30 minutes as per project spec
    recent_articles = fetch_recent_news(30)
    
    if not recent_articles:
        print("\n[OK] No news in the last 30 minutes.")
    else:
        print("\n" + "="*50)
        print(f"Found {len(recent_articles)} articles in last 30 mins:")
        print("="*50)
    
    for art in recent_articles:
        print(f"[{art['source']}] {art['title']}")
        print(f"   Link: {art['url']}")
        print(f"   Time: {art['published_at'].strftime('%H:%M:%S UTC')}\n")
