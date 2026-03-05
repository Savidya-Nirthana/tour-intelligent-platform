"""
web crawler service
"""

from playwright.async_api import async_playwright
from collections import deque
import asyncio
from bs4 import BeautifulSoup
from typing import Dict, Any, List, Set
import re
from urllib.parse import urljoin, urlparse
from markdownify import markdownify as md
import json

class CEYSAIDWebCrawler:
    def __init__(self, base_url: str, max_depth: int, exclude_patterns: List[str]):
        self.base_url = base_url
        self.max_depth = max_depth
        self.exclude_patterns = exclude_patterns
        self.visited: Set[str] = set()
        self.documents: List[Dice[str, Any]] = []

    def should_crawl(self, url: str) -> bool:
        """
        Determine if a URL should be crawled
        """
        
        if url in self.visited:
            return False

        if not url.startswith(self.base_url):
            return False

        for pattern in self.exclude_patterns:
            if pattern in url:
                return False
            
        if re.search(r'\.(jpg|jpeg|png|gif|pdf|zip|exe)$', url, re.I):
            return False

        return True

    def extract_content(self, soup: BeautifulSoup, url: str, start_urls: List[str]) -> Dict[str, Any]:
        """
        Extract content from a BeautifulSoup object
        """
        
        for element in soup(["script", "style", "noscript", "iframe"]):
            element.decompose()


        title = soup.title.string if soup.title else url.split("/")[-1]
        title = title.strip() if title else "untitled"

        categories_tag = soup.select_one(".entry-meta .categories a")
        category = categories_tag.get_text() if categories_tag else "other"

        info_category = ""

        if category.lower() == "visa" or title.lower() == "visa":
            info_category = "visa"


        elif '/tour/' in url:
            info_category = "tour"

        content_md = ""
        
        if info_category == "visa":
            ad_container = soup.new_tag("div")

            entry_title_elm = soup.find("h1", class_="entry-title")
            if entry_title_elm:
                ad_container.append(entry_title_elm)

            article = soup.find("article")
            if article:
                content = article.find('div', class_="entry-content")
                if content:
                    ad_container.append(content)

            if ad_container:
                content_md = md(str(ad_container), heading_style="ATX")
                content_md = re.sub(r'\n{3,}', '\n\n', content_md)
                content_md = content_md.strip()


        elif info_category == "tour":
            ad_container = soup.new_tag("div")

            tour_title_elm = soup.select_one("aside .tour-details h1")
            
            if tour_title_elm:
                ad_container.append(tour_title_elm)

            # extract the aside infomation
            aside_details = soup.select_one("aside .tour-details .description")
            if aside_details:
                ad_container.append(aside_details)

            aside_tags = soup.select_one("aside .tour-details .tags")
            if aside_tags:
                ad_container.append(aside_tags)


            # description section
            description_section = soup.find("section", id="description")
            if description_section:
                article = description_section.find('article')
                if article:
                    for btn in article.find_all('a', class_='bookingbtn'):
                        btn.decompose()

                    # for rate in article.find_all('h2', class_='tourrate'):
                    #     rate.decompose()

                    ad_container.append(article)
            

            # extract the location infomation
            locations_section = soup.find("section", id="locations")
            if locations_section:
                location_header = soup.new_tag('h2')
                location_header.string = "Locations"
                ad_container.append(location_header)

                for location in locations_section.find_all("article", class_="location_item"):
                    loc_name = location.find("h3")
                    loc_link = location.find("a", class_="overlay-link")
                    if loc_name:
                        loc_tag = soup.new_tag('p')
                        if loc_link:
                            a_tag = soup.new_tag('a', href=loc_link.get('href', ''))
                            a_tag.string = loc_name.get_text(strip=True)
                            loc_tag.append(a_tag)
                        else:
                            loc_tag.string = loc_name.get_text(strip=True)
                        ad_container.append(loc_tag)

            # ── Reviews section ──
            reviews_section = soup.find("section", id="reviews")
            if reviews_section:
                review_header = soup.new_tag('h2')
                review_header.string = "Reviews"
                ad_container.append(review_header)

                reviews = reviews_section.find_all("article")
                if reviews:
                    for review in reviews:
                        ad_container.append(review)
                else:
                    no_review = soup.new_tag('p')
                    no_review.string = "No reviews yet."
                    ad_container.append(no_review)

            if ad_container.contents:
                content_md = md(str(ad_container), heading_style='ATX')
                content_md = re.sub(r'\n{3,}', '\n\n', content_md)
                content_md = content_md.strip()


        links = []
        for a in soup.find_all('a', href=True):
            href = a.get('href', '')
            if not href:
                continue
            if href.startswith('/'):
                href = self.base_url + href
            elif not href.startswith('http'):
                href = urljoin(url, href)
            
            if href.startswith(self.base_url):
                href = href.split('#')[0].split('?')[0]
                if href and href != url:
                    links.append(href)

        return {
            "title": title,
            "info_category" : info_category,
            "content" : content_md,
            "links": links
        }

    async def _crawl_async(self, start_urls: List[str], request_delay: float = 2.0,) -> List[Dict[str, Any]]:
        queue = deque([(url, 0) for url in start_urls])

        async with async_playwright() as p:
            browser = await p.chromium.launch(headless=True)
            page = await browser.new_page()
            page.set_default_timeout(30000)

            while queue:
                url, depth = queue.popleft()
                if depth > self.max_depth or not self.should_crawl(url):
                    continue

                try:
                    print(f"🔍 [{depth}] {url}")
                    self.visited.add(url)

                    await page.goto(url, wait_until="domcontentloaded", timeout=60000)

                    try:
                        await page.wait_for_selector("body", timeout=10000)
                        await page.wait_for_timeout(3000)

                        await page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
                        await page.wait_for_timeout(1000)

                    except:
                        await page.wait_for_timeout(5000)

                    html = await page.content()
                    soup = BeautifulSoup(html, "html.parser")
                    
                    doc_data = self.extract_content(soup, url, start_urls)
                    doc_data['url'] = url
                    doc_data['depth_level'] = depth
                    if url not in start_urls:
                        if len(doc_data['content']) >= 100:
                            self.documents.append(doc_data)
                            print(f"   ✅ Saved ({len(doc_data['content'])} chars, {len(doc_data['links'])} links found)")
                        else:
                            print(f"   ⚠️ Skipped ({len(doc_data['content'])} chars) - too short")

                    
                        if depth < self.max_depth:
                            links_added = 0
                            for link in doc_data['links']:
                                if link not in self.visited and link not in [item[0] for item in queue]:
                                    queue.append((link, depth-1))
                                    links_added += 1
                            if links_added > 0:
                                print(f" 📎 Added {links_added} new URLs to queue (depth {depth + 1})")

                        print(f" 📊 Progress: {len(self.documents)} docs saved, {len(self.visited)} visited, {len(queue)} in queue")
                    else:
                        if depth < self.max_depth:
                            links_added = 0
                            for link in doc_data['links']:
                                if link not in self.visited and link not in [item[0] for item in queue]:
                                    queue.append((link, depth-1))
                                    links_added += 1
                            if links_added > 0:
                                print(f" 📎 Added {links_added} new URLs to queue (depth {depth + 1})")
                        print(f"   ⚠️ Skipped ({url}) - not a property page")
                    await asyncio.sleep(request_delay)
                
                except Exception as e:
                    error_msg = str(e)
                    if "404" in error_msg or "net::ERR_" in error_msg:
                        print(f"   ⚠️ Skipped ({url}) - 404 or network error")
                    else:
                        print(f"   ❌ Error: {error_msg[:100]}")
                    continue

            await browser.close()
        
        return self.documents



                

        


    def crawl(self, start_urls: List[str], request_delay: float = 2.0) -> List[Dict[str, Any]]:
        """
        Crawl the website and extract documents
        """
        import sys
        import concurrent.futures

        def _run_in_thread():
            """ Run the async crawl in a fresh proactorEventLoop on a new thread. """
            if sys.platform == "win32":
                loop = asyncio.ProactorEventLoop()
            else:
                loop = asyncio.new_event_loop()
            
            asyncio.set_event_loop(loop)
            try:
                return loop.run_until_complete(self._crawl_async(start_urls, request_delay))
            finally:
                loop.close()

        with concurrent.futures.ThreadPoolExecutor(max_workers=1) as executor:
            future = executor.submit(_run_in_thread)
            return future.result()


__all__ = [
    "CEYSAIDWebCrawler"
]