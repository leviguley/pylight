import aiohttp
import asyncio
import json
import random
import argparse
from bs4 import BeautifulSoup
from urllib.parse import unquote
from seleniumbase import sb_cdp

USER_AGENTS = [
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36",
        "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.5735.198 Safari/537.36",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 13_0) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.0 Safari/605.1.15",
        "Mozilla/5.0 (Windows NT 10.0; WOW64; Trident/7.0; rv:11.0) like Gecko",
        "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:102.0) Gecko/20100101 Firefox/102.0",
        "Mozilla/5.0 (Linux; Android 10; SM-G973F) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.5481.65 Mobile Safari/537.36",
        "Mozilla/5.0 (iPhone; CPU iPhone OS 15_5 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.5 Mobile/15E148 Safari/604.1",
        "Mozilla/5.0 (Linux; U; Android 4.4.2; en-US; GT-I9505 Build/KOT49H) AppleWebKit/534.30 (KHTML, like Gecko) Version/4.0 Mobile Safari/534.30",
        "Mozilla/5.0 (Windows NT 10.0; rv:109.0) Gecko/20100101 Firefox/114.0",
        "Mozilla/5.0 (iPad; CPU OS 15_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.2 Mobile/15E148 Safari/604.1",
        "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/111.0",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 12_6_3) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.4 Safari/605.1.15",
        "Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.1; Trident/6.0)",
        "Mozilla/5.0 (Linux; Android 11; Pixel 5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.5615.137 Mobile Safari/537.36",
        "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:40.0) Gecko/20100101 Firefox/40.1",
        "Mozilla/5.0 (Linux; Android 9; Redmi Note 7 Pro) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.5249.126 Mobile Safari/537.36",
        "Mozilla/5.0 (Windows NT 6.3; Trident/7.0; rv:11.0) like Gecko",
        "Mozilla/5.0 (X11; Fedora; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/109.0",
        "Mozilla/5.0 (Linux; U; Android 4.2.2; en-us; GT-P5113 Build/JDQ39) AppleWebKit/534.30 (KHTML, like Gecko) Version/4.0 Safari/534.30",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.102 Safari/537.36 Edge/18.19577",
        "Mozilla/5.0 (X11) AppleWebKit/62.41 (KHTML, like Gecko) Edge/17.10859 Safari/452.6",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML like Gecko) Chrome/51.0.2704.79 Safari/537.36 Edge/14.14931",
        "Chrome (AppleWebKit/537.1; Chrome50.0; Windows NT 6.3) AppleWebKit/537.36 (KHTML like Gecko) Chrome/51.0.2704.79 Safari/537.36 Edge/14.14393",
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML like Gecko) Chrome/46.0.2486.0 Safari/537.36 Edge/13.9200",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML like Gecko) Chrome/46.0.2486.0 Safari/537.36 Edge/13.10586",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.135 Safari/537.36 Edge/12.246Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.1.16) Gecko/20120421 Firefox/11.0",
        "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:11.0) Gecko Firefox/11.0",
        "Mozilla/5.0 (Windows NT 6.1; U;WOW64; de;rv:11.0) Gecko Firefox/11.0",
        "Mozilla/5.0 (Windows NT 5.1; rv:11.0) Gecko Firefox/11.0",
        "Mozilla/6.0 (Macintosh; I; Intel Mac OS X 11_7_9; de-LI; rv:1.9b4) Gecko/2012010317 Firefox/10.0a4",
        "Mozilla/5.0 (Macintosh; I; Intel Mac OS X 11_7_9; de-LI; rv:1.9b4) Gecko/2012010317 Firefox/10.0a4",
        "Mozilla/5.0 (X11; Mageia; Linux x86_64; rv:10.0.9) Gecko/20100101 Firefox/10.0.9",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.6; rv:9.0a2) Gecko/20111101 Firefox/9.0a2",
        "Mozilla/5.0 (Windows NT 6.2; rv:9.0.1) Gecko/20100101 Firefox/9.0.1",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.6; rv:9.0) Gecko/20100101 Firefox/9.0",
        "Mozilla/5.0 (Windows NT 5.1; rv:8.0; en_us) Gecko/20100101 Firefox/8.0",
        "Mozilla/5.0 (Windows NT 6.1; rv:6.0) Gecko/20100101 Firefox/7.0",
        "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:6.0a2) Gecko/20110613 Firefox/6.0a2",
        "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:6.0a2) Gecko/20110612 Firefox/6.0a2",
        "Mozilla/5.0 (X11; Linux i686; rv:6.0) Gecko/20100101 Firefox/6.0",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/27.0.1453.93 Safari/537.36",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/27.0.1453.93 Safari/537.36",
        "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/27.0.1453.90 Safari/537.36",
        "Mozilla/5.0 (X11; NetBSD) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/27.0.1453.116 Safari/537.36",
        "Mozilla/5.0 (X11; CrOS i686 3912.101.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/27.0.1453.116 Safari/537.36",
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.17 (KHTML, like Gecko) Chrome/24.0.1312.60 Safari/537.17",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_2) AppleWebKit/537.17 (KHTML, like Gecko) Chrome/24.0.1309.0 Safari/537.17",
        "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.15 (KHTML, like Gecko) Chrome/24.0.1295.0 Safari/537.15",
        "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.14 (KHTML, like Gecko) Chrome/24.0.1292.0 Safari/537.14",
        "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.13 (KHTML, like Gecko) Chrome/24.0.1290.1 Safari/537.13",
        "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/537.13 (KHTML, like Gecko) Chrome/24.0.1290.1 Safari/537.13"
    ]

class GoogleDork:
   def __init__(self, username):
      self.username = username

   def __enter__(self):
     self.sb = sb_cdp.Chrome(incognito=False, headless=True)
     self.sb.goto(f"https://www.google.com/search?q={self.username}+site%3Ainstagram.com+&sca_esv=35c26612a7d06f4b&rlz=1C1HKFL_enAU1220AU1220&sxsrf=APpeQnuUYf0uh02DHHqUi3_6v-F0sGARkg%3A1786201674465&ei=SkZ3aumIHJithvcPr8_ZgAw&biw=1920&bih=911&ved=0ahUKEwjp1bbip5GWAxWYluEIHa9nFsAQ4dUDCBA&uact=5&oq=sethnorthcott+site%3Ainstagram.com+&gs_lp=Egxnd3Mtd2l6LXNlcnAiIXNldGhub3J0aGNvdHQgc2l0ZTppbnN0YWdyYW0uY29tIEjFClAAWJMJcAB4AJABAJgBoAGgAe4EqgEDMC40uAEDyAEA-AEB-AECmAIAoAIAmAMAkgcAoAcwsgcAuAcAwgcAyAcAgAgB&sclient=gws-wiz-serp")
     self.sb.sleep(1.5)
     self.html = self.sb.get_page_source()
     return self

   def __exit__(self, exc_type, exc, tb):
      self.sb.quit()
   
def main(username):
 with GoogleDork(username) as gd:
    print("\033[0m Dorked ->", f"(\033[38;5;159m{gd.username}\033[0m)")  
    soup = BeautifulSoup(gd.html, "html.parser") 
    noDupe = set()
    for links in soup.find_all("a"):
       href = links.get("href")
       if href and href.startswith("https://www.instagram.com"):
          noDupe.add(href)

    for oDuped in noDupe:
       if oDuped and oDuped.startswith("https://www.instagram.com/p/"):
        print(f"\033[38;5;238m{oDuped}\033[38;5;194m[PHOTOS]\033[0m")
       if oDuped and oDuped.startswith("https://www.instagram.com/reel/"):
          print(f"\033[38;5;238m{oDuped}\033[38;5;214m[REELS]\033[0m")
       
class Katfinder:
    def __init__(self, version):
        self.version = version
        self.ascii = r"""
   __        __  ____         __       
  / /_____ _/ /_/ _(_)__  ___/ /__ ____
 /  '_/ _ `/ __/ _/ / _ \/ _  / -_) __/
/_/\_\\_,_/\__/_//_/_//_/\_,_/\__/_/   
"""

    def vers(self):
        print(self.ascii)
        print(self.version)

    async def websites(self):
        async with aiohttp.ClientSession() as session:
         async with session.get("https://github.com/leviguley/katfinder/raw/refs/heads/main/katfinder.json") as response:
            html = await response.text(errors="ignore")
            websites = json.loads(html)
            urls = websites["sites"]
            self.urls = urls
            
    async def setup(self, random_Agent, username, timeout_seconds, limit):
        headers = {"User-Agent":random_Agent}
        print(f"[\033[48;5;218m\033[30m{random_Agent}\033[0m]")
        connecting_specs = aiohttp.TCPConnector(limit=limit, ssl=False)
        timeout = aiohttp.ClientTimeout(total=timeout_seconds)
        async with aiohttp.ClientSession(connector=connecting_specs, timeout=timeout, headers=headers) as new_session:  
          
         found_urls = []
         async def search(sites):
          urls = sites["uri_check"].replace("{account}", username) 
          try:
                  async with new_session.get(urls) as response:
                   text = await response.text(errors="ignore")
                   e_string = sites["e_string"]
                   category = sites["cat"]
                   name = sites["name"]
                   filter = name.replace("(", "")
                   pretty_name = filter.replace(")", "")
                   filter_twitter = urls.replace("https://api.x.com/i/users/username_available.json?username=", "https://x.com/")
                   filter_tiktok = filter_twitter.replace("https://www.tiktok.com/oembed?url=https://www.tiktok.com/", "https://tiktok.com/")
                   filter_chess = filter_tiktok.replace("https://api.chess.com/pub/player/", "https://www.chess.com/members/")
                   filter_roblox = filter_chess.replace(f"https://auth.roblox.com/v1/usernames/validate?username={username}&birthday=2019-12-31T23:00:00.000Z", f"https://www.roblox.com/search/users?keyword={username} \033[0m[\033[38;5;178mUsername name exists, but may have been deleted\033[0m]")
                   if e_string and e_string in text:
                    display_url = filter_roblox.replace(username, f"\033[38;5;33m{username}\033[38;5;30m")
                    print(f"(\033[38;5;210m{pretty_name}\033[0m) [\033[38;2;0;199;124m{category}\033[0m] \033[38;5;183m{display_url}\033[0m")
                    found_urls.append(urls)
          except Exception:
               pass
           
         tasks = [search(sites) for sites in self.urls]
         await asyncio.gather(*tasks)
         if not found_urls:
           print("\n[\033[48;5;30mUser Not Found On AnyWebsite\033[0m]")
             
    def check(self, username, timeout, limit):
       if len(self.urls) > 0:
        asyncio.run(self.setup(random.choice(USER_AGENTS), username, timeout, limit))


if __name__ == "__main__":    
 parser = argparse.ArgumentParser(description="Katfinder is the Fastest 100% Accurate Username Checker. writtin in python. i Didn't add in file save because it doesn't show color but if you wanna save do > anyname.txt & it will show color")    
 parser.add_argument("-u", "--username", required=True, help="Username")   
 parser.add_argument("-t", "--timeout", type=int, help="Timeout", default=10) 
 parser.add_argument("-l", "--limit", type=int, help="Request Limit", default=200)
 args = parser.parse_args()

 main(args.username)

 l = Katfinder("\033[0m[\033[38;5;33mINF\033[0m] Instagram @leviguley " 
 "\n[\033[1;32mVERSION\033[0m] 0.1\n\033[48;2;211;69;69m\033[97m[TIP]\033[0m\033[0]\033[0m Ctrl \033[38;2;211;69;69m+ Left Click\033[0m On Links To Open\n\033[48;2;253;195;5m\033[30m[WRN]\033[0m Instagram links are just for checking what they commented on and stuff if they don't have a insta then its going to be random people\n")
 l.vers()
 try:
  asyncio.run(l.websites())
  l.check(args.username, args.timeout, args.limit)
 except:
   print("Goodbye!")
