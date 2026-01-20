import os

root_dir = '/Users/koushithamin/Desktop/personal/interview/clueso-mock'
enterprise_dir = os.path.join(root_dir, 'enterprise')

def update_file(filepath, is_enterprise):
    with open(filepath, 'r') as f:
        content = f.read()

    # Determine link content
    if is_enterprise:
        link_html = '''
                <a href="../index.html" class="nav-item" style="color: var(--brand-primary); margin-top: 1rem; margin-bottom: 0.5rem;">
                    <i data-lucide="rotate-ccw"></i>
                    Switch to Original
                </a>'''
    else:
        link_html = '''
                <a href="enterprise/index.html" class="nav-item" style="color: var(--brand-primary); margin-top: 1rem; margin-bottom: 0.5rem;">
                    <i data-lucide="layout"></i>
                    Switch to Enterprise
                </a>'''

    # Check if a switch link already exists (simple check)
    if 'Switch to' in content:
        # Remove existing likely variations to ensure clean slate (or just replace)
        # However, regex replacement is risky without careful patterns. 
        # Since I know I added one with 5rem margin in index.html, let's try to remove that specifc one first
        # But for other files where sed failed, it won't be there.
        # Let's simple-replace the one I added in index.html
        content = content.replace('style="color: var(--brand-primary); margin-top: 5rem;"', 'style="color: var(--brand-primary); margin-top: 1rem; margin-bottom: 0.5rem;"')
        
    # If it's NOT in the content (after potential fix above), insert it
    if 'Switch to' not in content:
        # Insert before user-profile
        target_str = '<div class="user-profile">'
        if target_str in content:
            content = content.replace(target_str, link_html + '\n                ' + target_str)
        else:
            print(f"Warning: Could not find user-profile in {filepath}")
            return

    with open(filepath, 'w') as f:
        f.write(content)
    print(f"Updated {filepath}")

# Update root files
for filename in os.listdir(root_dir):
    if filename.endswith('.html'):
        update_file(os.path.join(root_dir, filename), is_enterprise=False)

# Update enterprise files
for filename in os.listdir(enterprise_dir):
    if filename.endswith('.html'):
        update_file(os.path.join(enterprise_dir, filename), is_enterprise=True)
