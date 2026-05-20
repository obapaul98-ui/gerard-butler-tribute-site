import glob
import re

files = glob.glob("*.html")
for f in files:
    with open(f, 'r') as file:
        content = file.read()
        
    # Check if charity.html is missing in the nav-links block
    if '<a href="news.html"' in content and '<a href="charity.html"' not in content:
        print(f"Fixing {f}")
        # Insert charity link after news link
        # Need to match the style of the news link
        news_pattern = r'(<a href="news\.html"[^>]*>News</a>)'
        
        def replace_func(match):
            news_tag = match.group(1)
            # Create charity tag with the same style
            if 'style=' in news_tag:
                charity_tag = '\n      <a href="charity.html" style="color: white;">Charity</a>'
            else:
                charity_tag = '\n        <a href="charity.html">Charity</a>'
            return news_tag + charity_tag
            
        new_content = re.sub(news_pattern, replace_func, content)
        
        with open(f, 'w') as file:
            file.write(new_content)
