import urllib.request
import json
import ssl
import urllib.parse
import os

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

movies = {
    "Den of Thieves 2: Pantera": "poster_den_of_thieves_2.jpg",
    "How to Train Your Dragon (2025 film)": "poster_httyd_live_action.jpg",
    "Plane (film)": "poster_plane.jpg",
    "Last Seen Alive": "poster_last_seen_alive.jpg",
    "Greenland (film)": "poster_greenland.jpg",
    "Angel Has Fallen": "poster_angel_has_fallen.jpg",
    "Den of Thieves (film)": "poster_den_of_thieves.jpg",
    "Hunter Killer (film)": "poster_hunter_killer.jpg",
    "London Has Fallen": "poster_london_has_fallen.jpg",
    "Olympus Has Fallen": "poster_olympus_has_fallen.jpg",
    "How to Train Your Dragon (film)": "poster_httyd_animated.jpg",
    "Law Abiding Citizen": "poster_law_abiding_citizen.jpg",
    "300 (film)": "poster_300.jpg",
    "P.S. I Love You (film)": "poster_ps_i_love_you.jpg",
    "The Phantom of the Opera (2004 film)": "poster_phantom.jpg"
}

os.makedirs('img', exist_ok=True)

def download_poster(title, filename):
    try:
        url = "https://en.wikipedia.org/w/api.php?action=query&titles=" + urllib.parse.quote(title) + "&prop=images&format=json&imlimit=50"
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
        with urllib.request.urlopen(req, context=ctx) as response:
            data = json.loads(response.read().decode())
            pages = data["query"]["pages"]
            for page_id in pages:
                images = pages[page_id].get("images", [])
                target_img = None
                for img in images:
                    t = img["title"].lower()
                    if "svg" in t or "icon" in t or "logo" in t: continue
                    if "poster" in t or "theatrical" in t or "cover" in t or "release" in t:
                        target_img = img["title"]
                        break
                if not target_img and images:
                    for img in images:
                        t = img["title"].lower()
                        if "svg" not in t and "icon" not in t and "logo" not in t and "disambig" not in t and "wikiquote" not in t:
                            target_img = img["title"]
                            break
                
                if target_img:
                    img_url = "https://en.wikipedia.org/w/api.php?action=query&titles=" + urllib.parse.quote(target_img) + "&prop=imageinfo&iiprop=url&format=json"
                    req2 = urllib.request.Request(img_url, headers={"User-Agent": "Mozilla/5.0"})
                    with urllib.request.urlopen(req2, context=ctx) as res2:
                        data2 = json.loads(res2.read().decode())
                        pages2 = data2["query"]["pages"]
                        for pid2 in pages2:
                            final_url = pages2[pid2]["imageinfo"][0]["url"]
                            
                            # Download
                            req_dl = urllib.request.Request(final_url, headers={"User-Agent": "Mozilla/5.0"})
                            with urllib.request.urlopen(req_dl, context=ctx) as dl_res:
                                with open(os.path.join("img", filename), "wb") as f:
                                    f.write(dl_res.read())
                            print(f"Downloaded: {filename}")
                            return
    except Exception as e:
        print(f"Failed {title}: {e}")
    print(f"Failed {title}: No image found")

for t, f in movies.items():
    download_poster(t, f)
