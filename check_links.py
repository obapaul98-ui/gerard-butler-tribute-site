import os
import re

html_files = [f for f in os.listdir('.') if f.endswith('.html')]

# We'll build a set of valid targets: the html files themselves, and their extensionless names.
valid_targets = set(html_files)
for f in html_files:
    valid_targets.add(f.replace('.html', ''))

# Some special valid targets:
valid_targets.add('/')
valid_targets.add('#')
valid_targets.add('') # Empty links

broken_links = []

for file in html_files:
    with open(file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Simple regex to find href="..."
    # This might catch some false positives but we can filter them.
    matches = re.finditer(r'href=["\'](.*?)["\']', content)
    for match in matches:
        link = match.group(1)
        
        # Ignore external links, mailto, etc.
        if link.startswith('http') or link.startswith('mailto:') or link.startswith('tel:'):
            continue
            
        # Strip query params or hash for file checking
        base_link = link.split('?')[0].split('#')[0]
        
        if base_link and base_link not in valid_targets:
            # Maybe it's a directory like 'img/' or 'css/'? We can check if it exists.
            if not os.path.exists(base_link):
                broken_links.append((file, link))

if broken_links:
    print("Found broken links:")
    for file, link in broken_links:
        print(f"  {file}: {link}")
else:
    print("All internal links appear to be working!")
