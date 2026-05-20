import glob

files = glob.glob("*.html")
for f in files:
    with open(f, 'r') as file:
        content = file.read()
    
    new_content = content.replace(' style="color: white;"', '')
    new_content = new_content.replace(' style="padding: 20px;"', '')
    new_content = new_content.replace('  style="color: white;"', '')
    
    if new_content != content:
        with open(f, 'w') as file:
            file.write(new_content)
        print(f"Updated {f}")
