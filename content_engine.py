# content_engine.py
import feedparser
import random
from config import CONTENT_SOURCES
import re

class ContentFetcher:
    def __init__(self):
        self.sources = CONTENT_SOURCES

    def _clean_html(self, raw_html):
        cleanr = re.compile('<.*?>')
        cleantext = re.sub(cleanr, '', raw_html)
        return cleantext

    def fetch_random_article(self, category):
        rss_url = self.sources.get(category)
        if not rss_url:
            print(f"No RSS URL for category: {category}")
            return None

        print(f"-> Fetching articles from {category}...")
        try:
            feed = feedparser.parse(rss_url)
            if not feed.entries:
                print(f"No entries found in feed for {category}")
                return None

            entry = random.choice(feed.entries)
            summary = self._clean_html(entry.summary) if hasattr(entry, 'summary') else entry.title

            return {
                "title": entry.title,
                "summary": summary,
                "link": entry.link,
                "source": feed.feed.title
            }
        except Exception as e:
            print(f"Error parsing feed for {category}: {e}")
            return None
