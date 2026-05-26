import urllib.request
import re
import json

url = "https://www.youtube.com/@thefactor-firmansyahadvanc7208/videos"
req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
try:
    html = urllib.request.urlopen(req).read().decode('utf-8')
    match = re.search(r'var ytInitialData = ({.*?});</script>', html)
    if match:
        data = json.loads(match.group(1))
        results = []
        def extract(obj):
            if isinstance(obj, dict):
                if 'videoId' in obj and 'title' in obj:
                    try:
                        title = obj['title']['runs'][0]['text']
                        results.append((obj['videoId'], title))
                    except:
                        pass
                for v in obj.values():
                    extract(v)
            elif isinstance(obj, list):
                for i in obj:
                    extract(i)
        extract(data)
        seen = set()
        for v, t in results:
            if v not in seen:
                seen.add(v)
                print(f"{v} | {t}")
except Exception as e:
    print(e)
