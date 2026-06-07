import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DIST_DIR = os.path.join(BASE_DIR, 'dist')

def run_verification():
    print("--- Starting Build Verification for Bharat Horizon ---")
    
    # Check core files
    core_files = [
        'index.html', 'explore.html', 'diaries.html', 'itineraries.html',
        'food-culture.html', 'best-time.html', 'tips.html', 'about.html',
        'contact.html', 'privacy.html', 'affiliate-disclosure.html',
        'sitemap.xml', 'robots.txt'
    ]
    
    missing_cores = []
    for file in core_files:
        path = os.path.join(DIST_DIR, file)
        if not os.path.exists(path):
            missing_cores.append(file)
            
    if missing_cores:
        print(f"[ ERROR ] Missing core files: {missing_cores}")
    else:
        print("[ OK ] All core support pages, sitemap, and robots.txt exist.")

    # Check directories
    states_dir = os.path.join(DIST_DIR, 'states')
    dest_dir = os.path.join(DIST_DIR, 'destinations')
    blog_dir = os.path.join(DIST_DIR, 'blog')
    assets_dir = os.path.join(DIST_DIR, 'assets')
    
    # Count states
    state_folders = [f for f in os.listdir(states_dir) if os.path.isdir(os.path.join(states_dir, f))]
    print(f"[ INFO ] States count: {len(state_folders)} / 36")
    
    # Count destinations
    dest_folders = [f for f in os.listdir(dest_dir) if os.path.isdir(os.path.join(dest_dir, f))]
    print(f"[ INFO ] Destinations count: {len(dest_folders)} / 720 (Expected: >= 500)")
    
    # Count blog posts
    blog_folders = [f for f in os.listdir(blog_dir) if os.path.isdir(os.path.join(blog_dir, f))]
    print(f"[ INFO ] Blog posts count: {len(blog_folders)} / 144")
    
    # Verify Assets
    css_main = os.path.join(assets_dir, 'css', 'main.css')
    css_pages = os.path.join(assets_dir, 'css', 'pages.css')
    js_main = os.path.join(assets_dir, 'js', 'main.js')
    map_svg = os.path.join(assets_dir, 'images', 'map-india.svg')
    placeholder_svg = os.path.join(assets_dir, 'images', 'placeholder.svg')
    
    assets_ok = True
    for asset in [css_main, css_pages, js_main, map_svg, placeholder_svg]:
        if not os.path.exists(asset):
            print(f"[ ERROR ] Missing asset file: {os.path.relpath(asset, DIST_DIR)}")
            assets_ok = False
            
    if assets_ok:
        print("[ OK ] All key stylesheets, scripts, and SVG map assets exist.")
        
    print("--- Build Verification Completed ---")

if __name__ == '__main__':
    run_verification()
