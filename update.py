import requests
import re, os, time
from glob import glob
from concurrent.futures import ThreadPoolExecutor
import json, pyperclip as cp

def main():
    titles=["a-returners-magic-should-be-special",
           "survival-story-of-a-sword-king-in-a-fantasy-world",
           "omniscient-readers-viewpoint",
           "the-beginning-after-the-end",
           "seoul-station-druid",
           "reincarnated-into-a-warlock-66666-years-later",
           "tower-of-god",
           "the-gamer",
           "the-tutorial-towers-advanced-player",
           "infinite-level-up-in-murim",
           "99-wooden-stick",
           "doom-breaker",
           "i-grow-stronger-by-eating",
           "helmut-the-forsaken-child",
           "eleceed",
           "earth-savior-selection",
           "the-exorcism-record",
           "legend-of-the-northern-blade",
           "the-return-of-the-crazy-demon",
           "the-lazy-prince-becomes-a-genius",
           "the-max-level-hero-has-returned",
           "the-scholars-reincarnation",
            "the-legendary-moonlight-sculptor",
            "reverse-villain",
            "return-of-the-blossoming-blade",
            "warrior-high-school-dungeon-raid-course",
            "endless-devourer",
            "ill-be-taking-a-break-for-personal-reasons",
            "drug-devourer"
           ]

    for title in titles:
        if os.path.exists(f"{title}.json"):
            GIST = json.load(open(f"{title}.json","r"))
            page = int(max(GIST['chapters'].keys(),key=int))+1
        else:
            GIST={}
            GIST['title']=title
            GIST['description']=''
            GIST['artist']=""
            GIST['author']=''
            GIST['cover']=''
            GIST['chapters']={}        
            page=0

        failure_counter = 0

        new_image_urls = {}
        print(f"Scraping {title}...")
        while True:
            res = requests.get(f"https://mangaonlineteam.com/manga/{title}/chapter-{page}/")    
            s = str(res.content)
            searchers = re.findall("image-[0-9]+",s)
            if len(searchers)==0:
                failure_counter += 1

            if failure_counter == 3:
                break
            elif len(searchers)==0:
                page+=1
                continue
            else:
                failure_counter = 0

            print(f"Downloading chapter {page}...")
            for i in searchers:
                url = 'http'+s[s.find(i):].split('http')[1].split('\"')[0]
                L = new_image_urls.get(page,[])
                L.append(url)
                new_image_urls[page]=L
            page+=1

        ti = int(time.time())
        for i in new_image_urls:
            GIST['chapters'][str(i)] = {
                "title": str(i),
                "volume": "1",
                "last_updated": str(ti),
                "groups": {
                    "1": new_image_urls[i]
                }
            }
            ti-=1    
        json.dump(GIST,open(f'{title}.json','w'))
if __name__=="__main__":
    main()
    os.system("bash update_git.sh")
