import os
import glob
import re

html_files = glob.glob("*.html")

for filepath in html_files:
    with open(filepath, "r") as f:
        content = f.read()
    
    # Replace href="page.html" with href="page"
    # But keep index.html as "/" or "index.html"? Let's change href="index.html" to href="/"
    # And href="index.html#about" to href="/#about"
    content = content.replace('href="index.html"', 'href="/"')
    content = content.replace('href="index.html#about"', 'href="/#about"')
    
    # For all other .html files
    pages = ["films", "reels", "gallery", "news", "charity", "fanclub", "about", "vip-treatment", "meet-greet", "private-shows", "auctions"]
    for page in pages:
        content = content.replace(f'href="{page}.html"', f'href="{page}"')
    
    with open(filepath, "w") as f:
        f.write(content)
