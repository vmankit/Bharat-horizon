import os
import json
import shutil
import re

# Base paths
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, 'data')
STATES_DIR = os.path.join(DATA_DIR, 'states')
DEST_DIR = os.path.join(DATA_DIR, 'destinations')
BLOG_DIR = os.path.join(DATA_DIR, 'blog')
DIST_DIR = os.path.join(BASE_DIR, 'dist')

# Re-create dist directory
if os.path.exists(DIST_DIR):
    shutil.rmtree(DIST_DIR)
os.makedirs(DIST_DIR, exist_ok=True)
os.makedirs(os.path.join(DIST_DIR, 'states'), exist_ok=True)
os.makedirs(os.path.join(DIST_DIR, 'destinations'), exist_ok=True)
os.makedirs(os.path.join(DIST_DIR, 'blog'), exist_ok=True)

# Copy Assets to dist
if os.path.exists(os.path.join(BASE_DIR, 'assets')):
    shutil.copytree(os.path.join(BASE_DIR, 'assets'), os.path.join(DIST_DIR, 'assets'))

# Load global states catalog
with open(os.path.join(DATA_DIR, 'states.json'), 'r', encoding='utf-8') as f:
    states_catalog = json.load(f)

# Helper: Update links in compiled pages to be relative based on directory depth
def fix_links(html, depth):
    prefix = "../" * depth
    # Fix standard nav and layout links
    html = html.replace('href="index.html"', f'href="{prefix}index.html"')
    html = html.replace('href="explore.html"', f'href="{prefix}explore.html"')
    html = html.replace('href="diaries.html"', f'href="{prefix}diaries.html"')
    html = html.replace('href="itineraries.html"', f'href="{prefix}itineraries.html"')
    html = html.replace('href="food-culture.html"', f'href="{prefix}food-culture.html"')
    html = html.replace('href="best-time.html"', f'href="{prefix}best-time.html"')
    html = html.replace('href="tips.html"', f'href="{prefix}tips.html"')
    html = html.replace('href="about.html"', f'href="{prefix}about.html"')
    html = html.replace('href="contact.html"', f'href="{prefix}contact.html"')
    html = html.replace('href="privacy.html"', f'href="{prefix}privacy.html"')
    html = html.replace('href="affiliate-disclosure.html"', f'href="{prefix}affiliate-disclosure.html"')
    
    html = html.replace('src="assets/', f'src="{prefix}assets/')
    html = html.replace('href="assets/', f'href="{prefix}assets/')
    html = html.replace('data="assets/', f'data="{prefix}assets/')
    
    # Fix dynamic link references
    # state.html?id=xxx -> states/xxx/index.html
    html = re.sub(r'href="state\.html\?id=([a-z0-9-]+)"', r'href="' + prefix + r'states/\1/index.html"', html)
    # destination.html?id=xxx -> destinations/xxx/index.html
    html = re.sub(r'href="destination\.html\?id=([a-z0-9-]+)"', r'href="' + prefix + r'destinations/\1/index.html"', html)
    # diaries.html?article=xxx -> blog/xxx/index.html
    html = re.sub(r'href="diaries\.html\?article=([a-z0-9-]+)"', r'href="' + prefix + r'blog/\1/index.html"', html)
    
    return html

# 1. Compile Main Support Pages
support_pages = [
    'index.html', 'explore.html', 'diaries.html', 'itineraries.html', 
    'food-culture.html', 'best-time.html', 'tips.html', 'about.html', 
    'contact.html', 'privacy.html', 'affiliate-disclosure.html'
]

# Simple layouts injection for local templates
def load_template_with_layout(filename):
    with open(os.path.join(BASE_DIR, filename), 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Inject Mock Header & Footer HTML if the file expects dynamic injection
    # In index.html, state.html etc. they have empty <header> and <footer> tags which we loaded via main.js.
    # To make it truly SEO-first and fully indexable without JS, we inject the HTML directly into the static output!
    header_html = """
    <div class="container nav-container">
        <a href="index.html" class="logo">
            <div class="logo-icon">
                <svg viewBox="0 0 24 24">
                    <path d="M21,16V14L13,9V3.5A1.5,1.5 0 0,0 11.5,2A1.5,1.5 0 0,0 10,3.5V9L2,14V16L10,13.5V19L8,20.5V22L11.5,21L15,22V20.5L13,19V13.5L21,16Z"/>
                </svg>
            </div>
            <span class="logo-text">Bharat Horizon</span>
        </a>
        <button class="mobile-menu-btn" aria-label="Toggle Menu">
            <span></span>
            <span></span>
            <span></span>
        </button>
        <ul class="nav-links">
            <li><a href="index.html">Home</a></li>
            <li><a href="explore.html">Explore India</a></li>
            <li><a href="diaries.html">Travel Diaries</a></li>
            <li><a href="itineraries.html">Itineraries</a></li>
            <li><a href="food-culture.html">Food &amp; Culture</a></li>
            <li><a href="best-time.html">Best Seasons</a></li>
            <li><a href="tips.html">Travel Tips</a></li>
            <li><a href="about.html">About</a></li>
            <li><a href="contact.html" class="nav-cta">Plan Trip</a></li>
        </ul>
    </div>
    """
    
    footer_html = """
    <div class="container">
        <div class="footer-grid">
            <div class="footer-brand">
                <a href="index.html" class="logo">
                    <div class="logo-icon">
                        <svg viewBox="0 0 24 24">
                            <path d="M21,16V14L13,9V3.5A1.5,1.5 0 0,0 11.5,2A1.5,1.5 0 0,0 10,3.5V9L2,14V16L10,13.5V19L8,20.5V22L11.5,21L15,22V20.5L13,19V13.5L21,16Z"/>
                        </svg>
                    </div>
                    <span class="logo-text">Bharat Horizon</span>
                </a>
                <p>Discover India's soul. An aviation-inspired premium travel diary and destination guide, carefully highlighting regional wonders, culinary routes, and pristine hidden getaways across 36 states and union territories.</p>
            </div>
            <div class="footer-links">
                <h4>Explore Regions</h4>
                <ul>
                    <li><a href="explore.html?region=North">North Region</a></li>
                    <li><a href="explore.html?region=North East">North East Region</a></li>
                    <li><a href="explore.html?region=East">East Region</a></li>
                    <li><a href="explore.html?region=Central">Central Region</a></li>
                    <li><a href="explore.html?region=West">West Region</a></li>
                    <li><a href="explore.html?region=South">South Region</a></li>
                </ul>
            </div>
            <div class="footer-links">
                <h4>Resources</h4>
                <ul>
                    <li><a href="diaries.html">Travel Blogs</a></li>
                    <li><a href="itineraries.html">Itineraries</a></li>
                    <li><a href="best-time.html">Best Seasons</a></li>
                    <li><a href="tips.html">Gear &amp; Tips</a></li>
                    <li><a href="about.html">Our Story</a></li>
                    <li><a href="contact.html">Support</a></li>
                </ul>
            </div>
            <div class="footer-newsletter">
                <h4>Stay Inspired</h4>
                <p>Subscribe to receive curated luxury travel diaries and flight itineraries monthly.</p>
                <form class="newsletter-form" onsubmit="event.preventDefault(); alert('Thank you for subscribing!');">
                    <input type="email" placeholder="Your email address" required aria-label="Email address">
                    <button type="submit" aria-label="Subscribe">
                        <svg viewBox="0 0 24 24"><path d="M2,21L23,12L2,3V10L17,12L2,14V21Z"/></svg>
                    </button>
                </form>
            </div>
        </div>
        <div class="footer-bottom">
            <p>&copy; 2026 Bharat Horizon. All rights reserved. Crafted for explorers.</p>
            <div class="footer-bottom-links">
                <a href="affiliate-disclosure.html">Affiliate Disclosure</a>
                <a href="privacy.html">Privacy Policy</a>
            </div>
        </div>
    </div>
    """
    
    content = content.replace('<header></header>', f'<header class="scrolled">{header_html}</header>')
    content = content.replace('<footer></footer>', f'<footer>{footer_html}</footer>')
    return content

for page in support_pages:
    compiled_html = load_template_with_layout(page)
    compiled_html = fix_links(compiled_html, 0)
    with open(os.path.join(DIST_DIR, page), 'w', encoding='utf-8') as f:
        f.write(compiled_html)

print("Compiled core support pages.")

# 2. Compile State Pages (36 pages)
state_template = load_template_with_layout('state.html')

for state_meta in states_catalog:
    state_id = state_meta['id']
    with open(os.path.join(STATES_DIR, f"{state_id}.json"), 'r', encoding='utf-8') as f:
        s_data = json.load(f)
        
    s_name = s_data['name']
    
    # Render fields
    html = state_template
    html = html.replace('<title>State Travel Guide | Bharat Horizon</title>', f'<title>{s_name} Travel Diaries &amp; Tourism Guide | Bharat Horizon</title>')
    html = html.replace('<h1 id="state-title">Indian State</h1>', f'<h1 id="state-title">{s_name}</h1>')
    html = html.replace('<p id="state-vibe">Explore regional wonders</p>', f'<p id="state-vibe">{s_data["vibe"]}</p>')
    html = html.replace('<p id="state-overview" style="font-size:1.1rem; color:var(--color-text-muted); line-height:1.7; margin-bottom:30px;"></p>', f'<p id="state-overview" style="font-size:1.1rem; color:var(--color-text-muted); line-height:1.7; margin-bottom:30px;">{s_data["overview"]}</p>')
    html = html.replace('<p id="state-best-time" style="font-size:0.95rem; color:var(--color-text-muted); line-height:1.6;"></p>', f'<p id="state-best-time" style="font-size:0.95rem; color:var(--color-text-muted); line-height:1.6;">{s_data["bestTimeToVisit"]}</p>')
    
    html = html.replace('<p id="fact-capital">City Name</p>', f'<p id="fact-capital">{s_data["capital"]}</p>')
    html = html.replace('<p id="fact-region">North India</p>', f'<p id="fact-region">{s_data["region"]}</p>')
    html = html.replace('<p id="fact-budget">Economy</p>', f'<p id="fact-budget">{s_data["budgetGuide"]["level"]}</p>')
    
    html = html.replace('<span id="budget-cost" style="font-weight:bold; color:var(--color-gold);">INR 3,500</span>', f'<span id="budget-cost" style="font-weight:bold; color:var(--color-gold);">{s_data["budgetGuide"]["costPerDay"]}</span>')
    stars = "★" * s_data["budgetGuide"]["rating"] + "☆" * (5 - s_data["budgetGuide"]["rating"])
    html = html.replace('<span id="budget-rating" style="color:var(--color-gold);">★★★★☆</span>', f'<span id="budget-rating" style="color:var(--color-gold);">{stars}</span>')
    html = html.replace('<p id="budget-desc" style="font-size:0.88rem; color:var(--color-text-muted); line-height:1.5; border-top:1px solid rgba(255,255,255,0.05); padding-top:12px;"></p>', f'<p id="budget-desc" style="font-size:0.88rem; color:var(--color-text-muted); line-height:1.5; border-top:1px solid rgba(255,255,255,0.05); padding-top:12px;">{s_data["budgetGuide"]["description"]}</p>')
    
    html = html.replace('<p id="reach-air" style="margin-top:3px;"></p>', f'<p id="reach-air" style="margin-top:3px;">{s_data["howToReach"]["air"]}</p>')
    html = html.replace('<p id="reach-rail" style="margin-top:3px;"></p>', f'<p id="reach-rail" style="margin-top:3px;">{s_data["howToReach"]["rail"]}</p>')
    html = html.replace('<p id="reach-road" style="margin-top:3px;"></p>', f'<p id="reach-road" style="margin-top:3px;">{s_data["howToReach"]["road"]}</p>')
    
    # Airports list
    airports_li = "".join([f"<li>{item}</li>" for item in s_data["airports_railways"]])
    html = html.replace('<ul id="airports-list" style="padding-left:15px; font-size:0.85rem;">\n                                <!-- Populated dynamically -->\n                            </ul>', f'<ul id="airports-list" style="padding-left:15px; font-size:0.85rem;">{airports_li}</ul>')
    
    # Tips list
    tips_html = "".join([f'<div style="display:flex; gap:10px; margin-bottom:12px; font-size:0.95rem; color:var(--color-text-muted);"><span style="color:var(--color-gold); font-weight:bold;">✔</span><span>{tip}</span></div>' for tip in s_data["travelTips"]])
    html = html.replace('<div id="tips-list">\n                        <!-- Populated dynamically -->\n                    </div>', f'<div id="tips-list">{tips_html}</div>')
    
    # Top 20 Places Cards
    places_html = ""
    for idx, p in enumerate(s_data['places']):
        places_html += f"""
        <div class="diary-card">
            <div class="diary-card-img-container">
                <img src="../../assets/images/placeholder.svg" alt="{p['name']}" class="diary-card-img" />
                <span class="diary-card-tag">Spot #{idx+1}</span>
            </div>
            <div class="diary-card-content">
                <div>
                    <div class="diary-card-meta">
                        <span>Ranked #{idx+1}</span>
                        <span>&bull;</span>
                        <span>Sightseeing</span>
                    </div>
                    <h3 class="diary-card-title">{p['name']}</h3>
                    <p class="diary-card-summary">Explore the historic site of {p['name']}, one of the key landmarks within {s_name}. Find how to reach, entry times, and details.</p>
                </div>
                <a href="../../destinations/{p['slug']}/index.html" class="diary-card-readmore">
                    Read Travel Diary 
                    <svg viewBox="0 0 24 24"><path d="M4,11V13H16L10.5,18.5L11.92,19.92L19.84,12L11.92,4.08L10.5,5.5L16,11H4Z"/></svg>
                </a>
            </div>
        </div>
        """
    html = html.replace('<div id="places-grid" class="cards-grid">\n                        <!-- Populated dynamically via state.js -->\n                    </div>', f'<div id="places-grid" class="cards-grid">{places_html}</div>')

    # Foods list
    foods_html = "".join([f'<div class="food-card"><div class="food-card-number">0{idx+1}</div><div class="food-card-content"><h4>{food["name"]}</h4><p>{food["description"]}</p></div></div>' for idx, food in enumerate(s_data["famousFoods"])])
    html = html.replace('<div id="famous-foods-list" class="food-grid-list">\n                        <!-- Populated dynamically via state.js -->\n                    </div>', f'<div id="famous-foods-list" class="food-grid-list">{foods_html}</div>')

    # Festivals
    festivals_html = "".join([f'<div style="background:rgba(255,255,255,0.02); border:1px solid rgba(255,255,255,0.05); padding:20px; border-radius:8px;"><div style="display:flex; justify-content:space-between; margin-bottom:10px;"><h4 style="color:var(--color-gold); font-size:1.15rem;">{fest["name"]}</h4><span style="font-size:0.85rem; background:rgba(212,175,55,0.15); color:var(--color-gold); padding:2px 8px; border-radius:4px; height:fit-content;">{fest["month"]}</span></div><p style="font-size:0.9rem; color:var(--color-text-muted); line-height:1.5;">{fest["vibe"]}</p></div>' for fest in s_data["festivals"]])
    html = html.replace('<div id="festivals-list" style="display:grid; grid-template-columns:1fr 1fr; gap:20px;">\n                        <!-- Populated dynamically via state.js -->\n                    </div>', f'<div id="festivals-list" style="display:grid; grid-template-columns:1fr 1fr; gap:20px;">{festivals_html}</div>')

    # FAQs
    faqs_html = "".join([f'<div class="faq-item-block"><div class="faq-question"><span>{faq["q"]}</span><svg viewBox="0 0 24 24"><path d="M7.41,8.58L12,13.17L16.59,8.58L18,10L12,16L6,10L7.41,8.58Z"/></svg></div><div class="faq-answer"><p>{faq["a"]}</p></div></div>' for faq in s_data["faqs"]])
    html = html.replace('<div id="faqs-list" class="faq-accordion">\n                        <!-- Populated dynamically via state.js -->\n                    </div>', f'<div id="faqs-list" class="faq-accordion">{faqs_html}</div>')

    # Itinerary timeline (Defaulting to 3-day view)
    itineraries_html = "".join([f'<div class="timeline-item"><div class="timeline-day">Day 0{day["day"]}</div><h3 class="timeline-title">{day["theme"]}</h3><ul class="timeline-activities">' + "".join([f'<li>{act}</li>' for act in day["activities"]]) + '</ul></div>' for day in s_data["itinerary3Day"]])
    html = html.replace('<div id="itinerary-timeline" class="timeline">\n                        <!-- Populated dynamically via state.js -->\n                    </div>', f'<div id="itinerary-timeline" class="timeline">{itineraries_html}</div>')

    # Related blogs sidebar
    blogs = [
        { "title": f"Best Places to Visit in {s_name}", "slug": f"best-places-to-visit-in-{state_id}" },
        { "title": f"Best Time to Visit {s_name}", "slug": f"best-time-to-visit-{state_id}" },
        { "title": f"7 Day Road Trip Itinerary for {s_name}", "slug": f"7-day-itinerary-for-{state_id}" },
        { "title": f"Hidden Gems in {s_name} Unveiled", "slug": f"hidden-gems-in-{state_id}" }
    ]
    related_html = "".join([f'<div style="margin-bottom:15px; border-bottom:1px solid rgba(255,255,255,0.03); padding-bottom:10px;"><a href="../../blog/{b["slug"]}/index.html" style="font-size:0.95rem; font-weight:600; color:var(--color-text-main);">{b["title"]}</a><p style="font-size:0.8rem; color:var(--color-text-muted); margin-top:3px;">Travel Guide &bull; A must-read blog</p></div>' for b in blogs])
    html = html.replace('<div id="related-blogs-list">\n                        <!-- Populated dynamically -->\n                    </div>', f'<div id="related-blogs-list">{related_html}</div>')

    # Breadcrumbs
    bread_html = f'<a href="../../index.html">Home</a><span class="separator"></span><a href="../../explore.html">Explore</a><span class="separator"></span><span class="current">{s_name}</span>'
    html = html.replace('<div id="breadcrumb-container" class="breadcrumbs"></div>', f'<div id="breadcrumb-container" class="breadcrumbs">{bread_html}</div>')

    # Fill default input value for flights destination
    html = html.replace('value="Delhi (DEL)" style="padding:8px;"', f'value="{s_name} Airport" style="padding:8px;"')

    # Inject SEO schema script tag
    schema = {
        "@context": "https://schema.org",
        "@type": "TouristDestination",
        "name": s_name,
        "description": s_data["overview"],
        "containedInPlace": {
            "@type": "Country",
            "name": "India"
        },
        "estimatedCost": {
            "@type": "MonetaryAmount",
            "currency": "INR",
            "value": s_data["budgetGuide"]["costPerDay"]
        }
    }
    html = html.replace('</head>', f'<script type="application/ld+json">{json.dumps(schema)}</script>\n</head>')

    # Write output
    os.makedirs(os.path.join(DIST_DIR, 'states', state_id), exist_ok=True)
    html = fix_links(html, 2)
    with open(os.path.join(DIST_DIR, 'states', state_id, 'index.html'), 'w', encoding='utf-8') as f:
        f.write(html)

print("Compiled 36 state portals.")

# 3. Compile Destination Pages (720 pages!)
dest_template = load_template_with_layout('destination.html')

for filename in os.listdir(DEST_DIR):
    if not filename.endswith('.json'):
        continue
    
    with open(os.path.join(DEST_DIR, filename), 'r', encoding='utf-8') as f:
        d_data = json.load(f)
        
    d_id = d_data['id']
    d_name = d_data['name']
    s_name = d_data['stateName']
    s_id = d_data['stateId']
    
    html = dest_template
    html = html.replace('<title>Destination Details | Bharat Horizon</title>', f'<title>{d_name} Travel Diary - Sights in {s_name} | Bharat Horizon</title>')
    html = html.replace('<h1 id="dest-title" style="font-size:3.5rem; text-transform:uppercase; margin:15px 0 10px 0;">Destination Spot</h1>', f'<h1 id="dest-title" style="font-size:3.5rem; text-transform:uppercase; margin:15px 0 10px 0;">{d_name}</h1>')
    html = html.replace('<p id="dest-vibe" style="font-size:1.2rem; color:var(--color-text-muted); font-family:var(--font-heading); letter-spacing:1px;"></p>', f'<p id="dest-vibe" style="font-size:1.2rem; color:var(--color-text-muted); font-family:var(--font-heading); letter-spacing:1px;">{d_data["vibe"]}</p>')
    html = html.replace('<span id="dest-state-link" style="font-size:0.85rem; background:rgba(212,175,55,0.15); color:var(--color-gold); padding:4px 12px; border-radius:30px; font-weight:700; text-transform:uppercase; letter-spacing:1px; width:fit-content; display:block;">\n                State Tourism\n            </span>', f'<span id="dest-state-link" style="font-size:0.85rem; background:rgba(212,175,55,0.15); color:var(--color-gold); padding:4px 12px; border-radius:30px; font-weight:700; text-transform:uppercase; letter-spacing:1px; width:fit-content; display:block;"><a href="../../states/{s_id}/index.html">{s_name} Guide</a></span>')
    
    html = html.replace('<p id="dest-why-visit" style="font-size:1.1rem; color:var(--color-text-muted); line-height:1.7;"></p>', f'<p id="dest-why-visit" style="font-size:1.1rem; color:var(--color-text-muted); line-height:1.7;">{d_data["whyVisit"]}</p>')
    html = html.replace('<p id="dest-season" style="font-size:0.95rem; color:var(--color-text-muted); line-height:1.6;"></p>', f'<p id="dest-season" style="font-size:0.95rem; color:var(--color-text-muted); line-height:1.6;">{d_data["bestSeason"]}</p>')
    html = html.replace('<p id="dest-budget-idea" style="font-size:0.95rem; color:var(--color-text-muted); line-height:1.6;"></p>', f'<p id="dest-budget-idea" style="font-size:0.95rem; color:var(--color-text-muted); line-height:1.6;">{d_data["budgetTripIdea"]}</p>')
    html = html.replace('<p id="dest-reach" style="font-size:0.95rem; color:var(--color-text-muted); line-height:1.6;"></p>', f'<p id="dest-reach" style="font-size:0.95rem; color:var(--color-text-muted); line-height:1.6;">{d_data["howToReach"]}</p>')
    
    # Perspectives
    html = html.replace('<p id="angle-family"></p>', f'<p id="angle-family">{d_data["travelAngles"]["family"]}</p>')
    html = html.replace('<p id="angle-solo"></p>', f'<p id="angle-solo">{d_data["travelAngles"]["solo"]}</p>')
    html = html.replace('<p id="angle-couple"></p>', f'<p id="angle-couple">{d_data["travelAngles"]["couple"]}</p>')
    
    # Things to do
    things_html = "".join([f'<div class="faq-item-block" style="border-color:rgba(212,175,55,0.1); margin-bottom:15px; padding:20px;"><p style="font-size:1rem; color:var(--color-text-main); line-height:1.6;">{thing}</p></div>' for thing in d_data["topThingsToDo"]])
    html = html.replace('<div id="dest-things-list">\n                        <!-- Populated dynamically -->\n                    </div>', f'<div id="dest-things-list">{things_html}</div>')
    
    # Itinerary schedule
    timeline_html = "".join([f'<div style="display:grid; grid-template-columns:120px 1fr; gap:15px; margin-bottom:20px; border-bottom:1px dashed rgba(255,255,255,0.03); padding-bottom:12px;"><div style="font-family:var(--font-heading); color:var(--color-gold); font-weight:bold; font-size:0.9rem;">{item["time"]}</div><div style="font-size:0.95rem; color:var(--color-text-muted);">{item["activity"]}</div></div>' for item in d_data["sampleItinerary"]])
    html = html.replace('<div id="dest-itinerary-timeline" style="background:var(--color-bg-card); border:1px solid var(--color-border); border-radius:12px; padding:30px; box-shadow:var(--shadow-premium);">\n                        <!-- Populated dynamically -->\n                    </div>', f'<div id="dest-itinerary-timeline" style="background:var(--color-bg-card); border:1px solid var(--color-border); border-radius:12px; padding:30px; box-shadow:var(--shadow-premium);">{timeline_html}</div>')
    
    # What to eat
    foods_html = "".join([f'<div class="food-card" style="margin-bottom:12px; background:rgba(255,255,255,0.01);"><div class="food-card-number">0{idx+1}</div><div class="food-card-content"><h4>{food}</h4><p>Sample regional culinary creation highly recommended to try when exploring local street food joints.</p></div></div>' for idx, food in enumerate(d_data["whatToEat"])])
    html = html.replace('<div id="dest-food-list" class="food-grid-list">\n                        <!-- Populated dynamically -->\n                    </div>', f'<div id="dest-food-list" class="food-grid-list">{foods_html}</div>')
    
    # Accommodation
    stay_html = f"""
    <div class="stay-card">
        <div class="stay-badge">
            <svg viewBox="0 0 24 24"><path d="M7,14A2,2 0 0,0 5,16A2,2 0 0,0 7,18H17A2,2 0 0,0 19,16A2,2 0 0,0 17,18H7M19,7H12V11H19V7M21,5A2,2 0 0,1 23,7V16A2,2 0 0,1 21,18H19V21H17V18H7V21H5V18H3A2,2 0 0,1 1,16V7A2,2 0 0,1 3,5H21Z"/></svg>
            <span>Luxury</span>
        </div>
        <div class="stay-details">
            <h4>{d_data['whereToStay']['luxury'].split(' - ')[0]}</h4>
            <p>{d_data['whereToStay']['luxury'].split(' - ')[1]}</p>
        </div>
        <a href="https://booking.com/?aid=bharathorizon" target="_blank" class="gear-cta-link">Book Room</a>
    </div>
    <div class="stay-card">
        <div class="stay-badge">
            <svg viewBox="0 0 24 24"><path d="M19,5V7H12V5H19M21,3H3A2,2 0 0,0 1,5V16A2,2 0 0,0 3,18H5V21H7V18H17V21H19V18H21A2,2 0 0,0 23,16V5A2,2 0 0,0 21,3M21,16H3V11H21V16M21,9H3V5H21V9Z"/></svg>
            <span>Mid-Range</span>
        </div>
        <div class="stay-details">
            <h4>{d_data['whereToStay']['midRange'].split(' - ')[0]}</h4>
            <p>{d_data['whereToStay']['midRange'].split(' - ')[1]}</p>
        </div>
        <a href="https://booking.com/?aid=bharathorizon" target="_blank" class="gear-cta-link">Book Room</a>
    </div>
    <div class="stay-card">
        <div class="stay-badge">
            <svg viewBox="0 0 24 24"><path d="M5,8.5C5,7.67 5.67,7 6.5,7C7.33,7 8,7.67 8,8.5C8,9.33 7.33,10 6.5,10C5.67,10 5,9.33 5,8.5M19,10H12V5H19M21,3H3A2,2 0 0,0 1,5V16A2,2 0 0,0 3,18H5V21H7V18H17V21H19V18H21A2,2 0 0,0 23,16V5A2,2 0 0,0 21,3Z"/></svg>
            <span>Budget</span>
        </div>
        <div class="stay-details">
            <h4>{d_data['whereToStay']['budget'].split(' - ')[0]}</h4>
            <p>{d_data['whereToStay']['budget'].split(' - ')[1]}</p>
        </div>
        <a href="https://booking.com/?aid=bharathorizon" target="_blank" class="gear-cta-link">Book Room</a>
    </div>
    """
    html = html.replace('<div id="dest-stay-list" class="stay-options-container" style="margin:0;">\n                        <!-- Populated dynamically -->\n                    </div>', f'<div id="dest-stay-list" class="stay-options-container" style="margin:0;">{stay_html}</div>')

    # Nearby destinations
    nearby_html = "".join([f'<div style="border: 1px solid var(--color-border); border-radius: 8px; padding: 20px; text-align: center; background: rgba(255,255,255,0.02);"><h4 style="font-size:1.15rem; color:var(--color-text-main); margin-bottom:12px;">{nearby["name"]}</h4><a href="../../destinations/{nearby["slug"]}/index.html" class="diary-card-readmore" style="justify-content:center;">View Entry &rarr;</a></div>' for nearby in d_data["nearbyDestinations"]])
    html = html.replace('<div id="dest-nearby-grid" style="display:grid; grid-template-columns:1fr 1fr; gap:20px;">\n                        <!-- Populated dynamically -->\n                    </div>', f'<div id="dest-nearby-grid" style="display:grid; grid-template-columns:1fr 1fr; gap:20px;">{nearby_html}</div>')

    # Breadcrumbs
    bread_html = f'<a href="../../index.html">Home</a><span class="separator"></span><a href="../../explore.html">Explore</a><span class="separator"></span><a href="../../states/{s_id}/index.html">{s_name}</a><span class="separator"></span><span class="current">{d_name}</span>'
    html = html.replace('<div id="breadcrumb-container" class="breadcrumbs" style="padding:0 0 20px 0;"></div>', f'<div id="breadcrumb-container" class="breadcrumbs" style="padding:0 0 20px 0;">{bread_html}</div>')

    # Pre-fill Skyscanner flight form input
    html = html.replace('id="flight-dest" value=""', f'id="flight-dest" value="{d_name} ({d_name[:3].upper()})"')

    # Inject SEO Schema
    schema = {
        "@context": "https://schema.org",
        "@type": "TouristAttraction",
        "name": d_name,
        "description": d_data["whyVisit"],
        "containedInPlace": {
            "@type": "TouristDestination",
            "name": s_name
        }
    }
    html = html.replace('</head>', f'<script type="application/ld+json">{json.dumps(schema)}</script>\n</head>')

    # Write output
    os.makedirs(os.path.join(DIST_DIR, 'destinations', d_id), exist_ok=True)
    html = fix_links(html, 2)
    with open(os.path.join(DIST_DIR, 'destinations', d_id, 'index.html'), 'w', encoding='utf-8') as f:
        f.write(html)

print("Compiled 720 destination pages.")

# 4. Compile Blog Pages (144 pages)
blog_template = load_template_with_layout('diaries.html')

for filename in os.listdir(BLOG_DIR):
    if not filename.endswith('.json'):
        continue
    
    with open(os.path.join(BLOG_DIR, filename), 'r', encoding='utf-8') as f:
        b_data = json.load(f)
        
    b_id = b_data['slug']
    b_title = b_data['title']
    s_name = b_data['stateName']
    s_id = b_data['stateId']
    
    html = blog_template
    html = html.replace('<title>Travel Diaries Hub | Bharat Horizon Blog</title>', f'<title>{b_title} | Bharat Horizon Diaries</title>')
    
    # Activate detail view and deactivate hub view in template HTML directly!
    html = html.replace('<div id="blog-hub-view">', '<div id="blog-hub-view" style="display:none;">')
    html = html.replace('<div id="blog-detail-view" style="display:none; grid-template-columns: 2fr 1fr; gap:40px; align-items:start;">', '<div id="blog-detail-view" style="display:grid; grid-template-columns: 2fr 1fr; gap:40px; align-items:start;">')
    html = html.replace('<section class="container" id="blog-breadcrumbs-wrapper" style="display:none; padding-top:15px;">', '<section class="container" id="blog-breadcrumbs-wrapper" style="display:block; padding-top:15px;">')
    
    # Replacements
    html = html.replace('<span id="blog-category-tag" style="font-size:0.85rem; background:rgba(212,175,55,0.15); color:var(--color-gold); padding:4px 12px; border-radius:30px; font-weight:700; text-transform:uppercase; letter-spacing:1px; display:inline-block; margin-bottom:15px;">\n                    Travel Blog\n                </span>', f'<span id="blog-category-tag" style="font-size:0.85rem; background:rgba(212,175,55,0.15); color:var(--color-gold); padding:4px 12px; border-radius:30px; font-weight:700; text-transform:uppercase; letter-spacing:1px; display:inline-block; margin-bottom:15px;">{b_data["category"]}</span>')
    html = html.replace('<h1 id="blog-main-title" style="font-size: 3rem; margin-bottom: 15px; text-transform: uppercase;">Travel <span>Diaries</span></h1>', f'<h1 id="blog-main-title" style="font-size: 2.2rem; margin-bottom: 15px; text-transform: uppercase;">{b_title}</h1>')
    html = html.replace('<p id="blog-main-subtitle" style="color: var(--color-text-muted); max-width: 700px; margin: 0 auto; font-size: 1.1rem;">Read real, detailed guides on top places, itineraries, and best times to visit across every state and union territory.</p>', f'<p id="blog-main-subtitle" style="color: var(--color-text-muted); max-width: 700px; margin: 0 auto; font-size: 1.1rem;">{b_data["summary"]}</p>')
    
    # Body Writeup
    article_body = f"""
    <p style="font-size:1.2rem; color:var(--color-text-main); font-weight:500; margin-bottom:20px; line-height:1.6;">{b_data["summary"]}</p>
    <p style="margin-bottom:20px;">{b_data["content"]}</p>
    <p style="margin-bottom:25px;">Exploring {s_name} offers an incredible glance into India's historical diversity. From standard local cooking systems like traditional spices to pristine hidden getaways, you will find details that will wow any traveler. Book flights early and seek registered guides to experience local life.</p>
    """
    html = html.replace('<div id="blog-detail-content" style="font-size:1.1rem; color:var(--color-text-muted); line-height:1.8; text-align:justify;">\n                        <!-- Injected dynamically -->\n                    </div>', f'<div id="blog-detail-content" style="font-size:1.1rem; color:var(--color-text-muted); line-height:1.8; text-align:justify;">{article_body}</div>')

    # Breadcrumbs
    bread_html = f'<a href="../../index.html">Home</a><span class="separator"></span><a href="../../diaries.html">Diaries</a><span class="separator"></span><span class="current">{b_title}</span>'
    html = html.replace('<div id="breadcrumb-container" class="breadcrumbs"></div>', f'<div id="breadcrumb-container" class="breadcrumbs">{bread_html}</div>')

    # Pre-fill sidebar flights form destination
    html = html.replace('id="flight-dest" value=""', f'id="flight-dest" value="{s_name} Airport"')

    # Inject SEO Schema
    schema = {
        "@context": "https://schema.org",
        "@type": "BlogPosting",
        "headline": b_title,
        "description": b_data["summary"],
        "articleBody": b_data["content"],
        "author": {
            "@type": "Organization",
            "name": "Bharat Horizon"
        }
    }
    html = html.replace('</head>', f'<script type="application/ld+json">{json.dumps(schema)}</script>\n</head>')

    # Write output
    os.makedirs(os.path.join(DIST_DIR, 'blog', b_id), exist_ok=True)
    html = fix_links(html, 2)
    with open(os.path.join(DIST_DIR, 'blog', b_id, 'index.html'), 'w', encoding='utf-8') as f:
        f.write(html)

print("Compiled 144 blog articles.")

# 5. Generate Sitemap & Robots.txt
# Sitemap
sitemap_urls = [
    "", "explore.html", "diaries.html", "itineraries.html", 
    "food-culture.html", "best-time.html", "tips.html", 
    "about.html", "contact.html", "privacy.html", "affiliate-disclosure.html"
]

sitemap_xml = '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
for url in sitemap_urls:
    sitemap_xml += f'  <url>\n    <loc>https://bharathorizon.com/{url}</loc>\n    <changefreq>weekly</changefreq>\n    <priority>0.8</priority>\n  </url>\n'

# Add states
for state_meta in states_catalog:
    sitemap_xml += f'  <url>\n    <loc>https://bharathorizon.com/states/{state_meta["id"]}/index.html</loc>\n    <changefreq>monthly</changefreq>\n    <priority>0.9</priority>\n  </url>\n'

# Add destinations
for filename in os.listdir(DEST_DIR):
    if filename.endswith('.json'):
        d_id = filename[:-5]
        sitemap_xml += f'  <url>\n    <loc>https://bharathorizon.com/destinations/{d_id}/index.html</loc>\n    <changefreq>monthly</changefreq>\n    <priority>0.7</priority>\n  </url>\n'

# Add blogs
for filename in os.listdir(BLOG_DIR):
    if filename.endswith('.json'):
        b_id = filename[:-5]
        sitemap_xml += f'  <url>\n    <loc>https://bharathorizon.com/blog/{b_id}/index.html</loc>\n    <changefreq>monthly</changefreq>\n    <priority>0.6</priority>\n  </url>\n'

sitemap_xml += '</urlset>\n'

with open(os.path.join(DIST_DIR, 'sitemap.xml'), 'w', encoding='utf-8') as f:
    f.write(sitemap_xml)

# Robots.txt
robots_txt = """User-agent: *
Allow: /

Sitemap: https://bharathorizon.com/sitemap.xml
"""

with open(os.path.join(DIST_DIR, 'robots.txt'), 'w', encoding='utf-8') as f:
    f.write(robots_txt)

print("Generated sitemap.xml and robots.txt.")
print("Static site compilation completed successfully under the 'dist/' folder!")
