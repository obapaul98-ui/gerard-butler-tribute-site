import re
import glob

with open('index.html', 'r') as f:
    index_content = f.read()

# Extract About sections
about_match = re.search(r'(<!-- ABOUT / BIO SECTION -->.*?)(?=<!-- CTA -->)', index_content, flags=re.DOTALL)
if about_match:
    about_sections = about_match.group(1)
    # Remove from index.html
    new_index_content = index_content.replace(about_sections, '')
    with open('index.html', 'w') as f:
        f.write(new_index_content)
    
    # Create about.html
    head_match = re.search(r'(<!DOCTYPE html>.*?</nav>)', index_content, flags=re.DOTALL)
    footer_match = re.search(r'(<!-- FOOTER -->.*?</html>)', index_content, flags=re.DOTALL)
    
    if head_match and footer_match:
        head = head_match.group(1)
        # Update title in head
        head = head.replace('<title>Gerard Butler | Action Hero</title>', '<title>About | Gerard Butler</title>')
        # Remove active class from anything in nav
        head = re.sub(r'class="active"', '', head)
        
        footer = footer_match.group(1)
        
        about_html = head + '\n\n' + about_sections + '\n\n' + footer
        with open('about.html', 'w') as f:
            f.write(about_html)

# Update navigation in all files
html_files = glob.glob('*.html')
for filepath in html_files:
    with open(filepath, 'r') as f:
        content = f.read()
    
    # In nav-links, ensure Home and About are correct
    # The current links look like:
    # <div class="nav-links">
    #   <a href="/#about" style="color: white;">About</a>
    # or
    # <div class="nav-links">
    #   <a href="#about">About</a>
    
    # First, let's normalize the 'About' link
    content = re.sub(r'<a href="/?#about"[^>]*>About</a>', '<a href="about">About</a>', content)
    
    # Check if 'Home' is missing, and inject it before 'About'
    if '<a href="/">Home</a>' not in content and 'href="/" style="color: white;">Home' not in content:
        # Inject <a href="/">Home</a> right after <div class="nav-links">
        # Or right before <a href="about">
        content = re.sub(r'(<a href="about">About</a>)', r'<a href="/">Home</a>\n        \1', content)
        content = re.sub(r'(<a href="about" style="color: white;">About</a>)', r'<a href="/" style="color: white;">Home</a>\n      \1', content)
    
    # Now fix active states
    # Remove all 'class="active"' from nav-links
    # Note: we need to be careful not to remove it from elsewhere.
    # Actually, it's easier to just set it based on the file name.
    
    # Remove active class inside nav-links
    def clear_active(m):
        return m.group(0).replace('class="active"', '')
    content = re.sub(r'<div class="nav-links">.*?</div>', clear_active, content, flags=re.DOTALL)
    
    # Add active class to the right link
    if filepath == 'index.html':
        content = re.sub(r'<a href="/">Home</a>', '<a href="/" class="active">Home</a>', content)
        content = re.sub(r'<a href="/" style="color: white;">Home</a>', '<a href="/" class="active" style="color: white;">Home</a>', content)
    elif filepath == 'about.html':
        content = re.sub(r'<a href="about">About</a>', '<a href="about" class="active">About</a>', content)
        content = re.sub(r'<a href="about" style="color: white;">About</a>', '<a href="about" class="active" style="color: white;">About</a>', content)
    else:
        page_name = filepath.replace('.html', '')
        # e.g., href="films" -> href="films" class="active"
        content = re.sub(rf'<a href="{page_name}">', f'<a href="{page_name}" class="active">', content)
        content = re.sub(rf'<a href="{page_name}" style="color: white;">', f'<a href="{page_name}" class="active" style="color: white;">', content)
    
    with open(filepath, 'w') as f:
        f.write(content)

