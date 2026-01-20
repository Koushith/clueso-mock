import os
import re

root_dir = '/Users/koushithamin/Desktop/personal/interview/clueso-mock'
light_mode_dir = os.path.join(root_dir, 'light-mode')

def get_nav_block(current_location):
    # current_location: 'root', 'light'
    
    links = []
    
    # Dark Mode Link
    path_dark = "#"
    style_dark = "opacity: 0.5; cursor: default;"
    if current_location == 'light':
        path_dark = "../index.html"
        style_dark = "margin-top: 0.25rem;"
    
    links.append(f'''
                <a href="{path_dark}" class="nav-item" style="{style_dark}">
                    <i data-lucide="moon"></i>
                    Dark Mode
                </a>''')

    # Light Mode Link
    path_light = "#"
    style_light = "opacity: 0.5; cursor: default;" 
    if current_location == 'root':
        path_light = "light-mode/index.html"
        style_light = "margin-top: 0.25rem;"
        
    links.append(f'''
                <a href="{path_light}" class="nav-item" style="{style_light}">
                    <i data-lucide="sun"></i>
                    Light Mode
                </a>''')

    return '\n'.join(links)

def update_file(filepath, location):
    with open(filepath, 'r') as f:
        content = f.read()

    # 1. Regex to remove the existing Themes block
    # Pattern looks for the div with border-top -> Themes -> ... -> closing div
    # This matches the structure we added previously
    content = re.sub(
        r'<div style="margin-top: 1rem; padding-top: 1rem; border-top: 1px solid var(--border-base);">\s*<div.*?>Themes</div>[\s\S]*?</div>', 
        '', 
        content
    )

    # 2. Regex to remove any old "Switch to" links that might still be there
    content = re.sub(r'<a href="[^"]*".*?>\s*<i data-lucide="(layout|rotate-ccw)"></i>\s*Switch to.*?\s*</a>', '', content, flags=re.DOTALL)
    
    # 3. Insert new Nav Block
    trash_link_marker = 'Trash\n                </a>'
    
    nav_block = get_nav_block(location)
    
    full_block = f'''{trash_link_marker}
                
                <div style="margin-top: 1rem; padding-top: 1rem; border-top: 1px solid var(--border-base);">
                    <div style="font-size: 0.7rem; color: var(--text-tertiary); padding-left: 0.75rem; margin-bottom: 0.5rem; text-transform: uppercase; letter-spacing: 0.05em;">Themes</div>
                    {nav_block}
                </div>'''

    if trash_link_marker in content:
        content = content.replace(trash_link_marker, full_block)
    
    with open(filepath, 'w') as f:
        f.write(content)
    print(f"Updated {filepath}")

# Update Root Files
for filename in os.listdir(root_dir):
    if filename.endswith('.html'):
        update_file(os.path.join(root_dir, filename), 'root')

# Update Light Mode Files
for filename in os.listdir(light_mode_dir):
    if filename.endswith('.html'):
        update_file(os.path.join(light_mode_dir, filename), 'light')
