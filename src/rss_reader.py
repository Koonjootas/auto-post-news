
import feedparser

def read_rss_sources(path="rss_sources.txt"):
    with open(path, "r") as f:
        return [line.strip() for line in f if line.strip()]

def fetch_news(url, limit=5):
    feed = feedparser.parse(url)
    return [
        {
            "title": entry.title,
            "link": entry.link,
            "summary": entry.get("summary", "")
        }
        for entry in feed.entries[:limit]
    ]
