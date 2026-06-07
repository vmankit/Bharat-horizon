/* 
   Bharat Horizon - Common JavaScript Logic
   Handles: Shared Header/Footer injection, Search indexer, Breadcrumbs, Skyscanner mock redirects
*/

document.addEventListener("DOMContentLoaded", () => {
    loadHeaderFooter();
    initGlobalSearch();
    handleScrollHeader();
});

// 1. Shared Header & Footer Loaders
function loadHeaderFooter() {
    const headerEl = document.querySelector("header");
    const footerEl = document.querySelector("footer");
    
    // Get current path to handle relative links on compiled pages
    const pathDepth = window.location.pathname.split("/").filter(p => p).length;
    let relPath = "";
    // If the path includes dist/states/ or similar, we adjust links
    if (window.location.pathname.includes("/states/") || window.location.pathname.includes("/destinations/") || window.location.pathname.includes("/blog/")) {
        relPath = "../../";
    }

    if (headerEl) {
        headerEl.innerHTML = `
            <div class="container nav-container">
                <a href="${relPath}index.html" class="logo">
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
                    <li><a href="${relPath}index.html">Home</a></li>
                    <li><a href="${relPath}explore.html">Explore India</a></li>
                    <li><a href="${relPath}diaries.html">Travel Diaries</a></li>
                    <li><a href="${relPath}itineraries.html">Itineraries</a></li>
                    <li><a href="${relPath}food-culture.html">Food & Culture</a></li>
                    <li><a href="${relPath}best-time.html">Best Seasons</a></li>
                    <li><a href="${relPath}tips.html">Travel Tips</a></li>
                    <li><a href="${relPath}about.html">About</a></li>
                    <li><a href="${relPath}contact.html" class="nav-cta">Plan Trip</a></li>
                </ul>
            </div>
        `;
        
        // Setup Active Class
        const currentFilename = window.location.pathname.split("/").pop() || "index.html";
        const navItems = headerEl.querySelectorAll(".nav-links li");
        navItems.forEach(item => {
            const link = item.querySelector("a");
            if (link && link.getAttribute("href").endsWith(currentFilename)) {
                item.classList.add("active");
            }
        });

        // Mobile Menu Interactions
        const mobBtn = headerEl.querySelector(".mobile-menu-btn");
        const navLinks = headerEl.querySelector(".nav-links");
        mobBtn.addEventListener("click", () => {
            mobBtn.classList.toggle("active");
            navLinks.classList.toggle("active");
            if(navLinks.classList.contains("active")) {
                navLinks.style.display = "flex";
                navLinks.style.flexDirection = "column";
                navLinks.style.position = "absolute";
                navLinks.style.top = "var(--nav-height)";
                navLinks.style.left = "0";
                navLinks.style.width = "100%";
                navLinks.style.background = "#050a18";
                navLinks.style.padding = "30px";
                navLinks.style.borderBottom = "1px solid var(--color-border)";
                navLinks.style.gap = "20px";
                navLinks.style.zIndex = "999";
            } else {
                navLinks.removeAttribute("style");
            }
        });
    }

    if (footerEl) {
        footerEl.innerHTML = `
            <div class="container">
                <div class="footer-grid">
                    <div class="footer-brand">
                        <a href="${relPath}index.html" class="logo">
                            <div class="logo-icon">
                                <svg viewBox="0 0 24 24">
                                    <path d="M21,16V14L13,9V3.5A1.5,1.5 0 0,0 11.5,2A1.5,1.5 0 0,0 10,3.5V9L2,14V16L10,13.5V19L8,20.5V22L11.5,21L15,22V20.5L13,19V13.5L21,16Z"/>
                                </svg>
                            </div>
                            <span class="logo-text">Bharat Horizon</span>
                        </a>
                        <p>Discover India's soul. An aviation-inspired premium travel diary and destination guide, carefully highlighting regional wonders, culinary routes, and pristine hidden getaways across 36 states and union territories.</p>
                        <div class="footer-socials">
                            <a href="#" class="social-icon" aria-label="Facebook">
                                <svg viewBox="0 0 24 24"><path d="M17,2H14A5,5 0 0,0 9,7V10H6V14H9V22H13V14H16L17,10H13V7A1,1 0 0,1 14,6H17V2Z"/></svg>
                            </a>
                            <a href="#" class="social-icon" aria-label="Twitter">
                                <svg viewBox="0 0 24 24"><path d="M22.46,6C21.69,6.35 20.86,6.58 20,6.69C20.88,6.16 21.56,5.32 21.88,4.31C21,4.83 20.08,5.22 19,5.41C18.17,4.53 17,4 15.7,4C13.19,4 11.16,6.04 11.16,8.55C11.16,8.91 11.2,9.26 11.28,9.6C7.5,9.41 4.12,7.59 1.88,4.82C1.48,5.5 1.25,6.3 1.25,7.15C1.25,8.73 2.05,10.12 3.28,10.95C2.53,10.93 1.84,10.72 1.25,10.4V10.45C1.25,12.65 2.81,14.48 4.88,14.9C4.5,15 4.09,15.07 3.67,15.07C3.37,15.07 3.08,15.04 2.8,14.97C3.38,16.78 5.06,18.1 7.05,18.14C5.49,19.36 3.53,20.09 1.39,20.09C1.02,20.09 0.66,20.07 0.3,20.03C2.32,21.33 4.71,22 7.28,22C15.65,22 20.22,15.07 20.22,9.05C20.22,8.85 20.22,8.65 20.2,8.45C21.1,7.8 21.88,7 22.46,6Z"/></svg>
                            </a>
                            <a href="#" class="social-icon" aria-label="Instagram">
                                <svg viewBox="0 0 24 24"><path d="M7.8,2H16.2C19.4,2 22,4.6 22,7.8V16.2A5.8,5.8 0 0,1 16.2,22H7.8C4.6,22 2,19.4 2,16.2V7.8A5.8,5.8 0 0,1 7.8,2M7.6,4A3.6,3.6 0 0,0 4,7.6V16.4A3.6,3.6 0 0,0 7.6,20H16.4A3.6,3.6 0 0,0 20,16.4V7.6A3.6,3.6 0 0,0 16.4,4H7.6M12,7A5,5 0 0,1 17,12A5,5 0 0,1 12,17A5,5 0 0,1 7,12A5,5 0 0,1 12,7M12,9A3,3 0 0,0 9,12A3,3 0 0,0 12,15A3,3 0 0,0 15,12A3,3 0 0,0 12,9M18,5.75A0.75,0.75 0 0,1 18.75,6.5A0.75,0.75 0 0,1 18,7.25A0.75,0.75 0 0,1 17.25,6.5A0.75,0.75 0 0,1 18,5.75Z"/></svg>
                            </a>
                        </div>
                    </div>
                    
                    <div class="footer-links">
                        <h4>Explore Regions</h4>
                        <ul>
                            <li><a href="${relPath}explore.html?region=North">North Region</a></li>
                            <li><a href="${relPath}explore.html?region=North East">North East Region</a></li>
                            <li><a href="${relPath}explore.html?region=East">East Region</a></li>
                            <li><a href="${relPath}explore.html?region=Central">Central Region</a></li>
                            <li><a href="${relPath}explore.html?region=West">West Region</a></li>
                            <li><a href="${relPath}explore.html?region=South">South Region</a></li>
                        </ul>
                    </div>

                    <div class="footer-links">
                        <h4>Resources</h4>
                        <ul>
                            <li><a href="${relPath}diaries.html">Travel Blogs</a></li>
                            <li><a href="${relPath}itineraries.html">Itineraries</a></li>
                            <li><a href="${relPath}best-time.html">Best Seasons</a></li>
                            <li><a href="${relPath}tips.html">Gear &amp; Tips</a></li>
                            <li><a href="${relPath}about.html">Our Story</a></li>
                            <li><a href="${relPath}contact.html">Support</a></li>
                        </ul>
                    </div>
                    
                    <div class="footer-newsletter">
                        <h4>Stay Inspired</h4>
                        <p>Subscribe to receive curated luxury travel diaries and flight itineraries monthly.</p>
                        <form class="newsletter-form" onsubmit="event.preventDefault(); alert('Thank you for subscribing to Bharat Horizon newsletter!');">
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
                        <a href="${relPath}affiliate-disclosure.html">Affiliate Disclosure</a>
                        <a href="${relPath}privacy.html">Privacy Policy</a>
                    </div>
                </div>
            </div>
        `;
    }
}

// 2. Header Scroll Styling Toggle
function handleScrollHeader() {
    const header = document.querySelector("header");
    window.addEventListener("scroll", () => {
        if (window.scrollY > 50) {
            header.classList.add("scrolled");
        } else {
            header.classList.remove("scrolled");
        }
    });
}

// 3. Global Search & Autocomplete
let statesSearchIndex = [];

async function initGlobalSearch() {
    const searchInputs = document.querySelectorAll(".search-input-trigger");
    if (searchInputs.length === 0) return;

    // Load main states metadata index file
    try {
        const pathDepth = window.location.pathname.split("/").filter(p => p).length;
        let prefixPath = "";
        if (window.location.pathname.includes("/states/") || window.location.pathname.includes("/destinations/") || window.location.pathname.includes("/blog/")) {
            prefixPath = "../../";
        }
        
        const response = await fetch(`${prefixPath}data/states.json`);
        statesSearchIndex = await response.json();
    } catch (e) {
        console.error("Failed to load states search index", e);
    }

    searchInputs.forEach(input => {
        const wrapper = input.closest(".hero-search-wrapper") || input.parentElement;
        // Create result container dynamically if it doesn't exist
        let resultsContainer = wrapper.querySelector(".search-dropdown-results");
        if (!resultsContainer) {
            resultsContainer = document.createElement("div");
            resultsContainer.className = "search-dropdown-results";
            wrapper.appendChild(resultsContainer);
        }

        input.addEventListener("input", (e) => {
            const query = e.target.value.toLowerCase().trim();
            if (query.length < 2) {
                resultsContainer.innerHTML = "";
                resultsContainer.classList.remove("active");
                return;
            }

            // Filter states
            const matches = statesSearchIndex.filter(state => 
                state.name.toLowerCase().includes(query) ||
                state.capital.toLowerCase().includes(query) ||
                state.region.toLowerCase().includes(query) ||
                state.style.toLowerCase().includes(query)
            );

            resultsContainer.innerHTML = "";
            if (matches.length === 0) {
                resultsContainer.innerHTML = `<div class="search-result-item" style="cursor:default;"><span class="name">No destinations found</span></div>`;
            } else {
                matches.slice(0, 6).forEach(state => {
                    const item = document.createElement("div");
                    item.className = "search-result-item";
                    item.innerHTML = `
                        <div>
                            <span class="name">${state.name}</span>
                            <span class="meta">${state.capital}, ${state.region}</span>
                        </div>
                        <span class="type">${state.type}</span>
                    `;
                    item.addEventListener("click", () => {
                        resultsContainer.classList.remove("active");
                        const linkDepth = window.location.pathname.includes("/states/") || window.location.pathname.includes("/destinations/") || window.location.pathname.includes("/blog/") ? "../../" : "";
                        window.location.href = `${linkDepth}state.html?id=${state.id}`;
                    });
                                        <p>Discover India's soul. An aviation-inspired premium travel diary and destination guide, carefully highlighting regional wonders, culinary routes, and pristine hidden getaways across 36 states and union territories.</p>
                                        <div style="margin-top:12px; font-size:0.95rem; color:var(--color-text-muted);">
                                            <div>Office: Shubhash Nagar, Dehradun, 248002</div>
                                            <div style="margin-top:6px;">Email: <a href="mailto:ankitrajvm@gmail.com" style="color:var(--color-gold);">ankitrajvm@gmail.com</a></div>
                                        </div>
                                        <div class="footer-socials">
                                            <a href="https://www.instagram.com/bharathorizon.travel/" target="_blank" rel="noopener noreferrer" class="social-icon" aria-label="Instagram">
            resultsContainer.classList.add("active");
        });

        // Close dropdown when clicking outside
        document.addEventListener("click", (e) => {
            if (!wrapper.contains(e.target)) {
                resultsContainer.classList.remove("active");
            }
        });
    });
}

// 4. Skyscanner Flight Booking Mock Redirect Action
function mockSearchFlights(event) {
    if (event) event.preventDefault();
    
    const origin = document.getElementById("flight-origin")?.value || "Delhi (DEL)";
    const destination = document.getElementById("flight-dest")?.value || "Goa (GOI)";
    const date = document.getElementById("flight-date")?.value || "";
    
    alert(`Searching flights from ${origin} to ${destination} for ${date || 'upcoming date'} via Skyscanner...\n\n(This redirects to Skyscanner live flight rates with affiliate sub ID tags)`);
    
    const cleanOrigin = encodeURIComponent(origin.split(" ")[0]);
    const cleanDest = encodeURIComponent(destination.split(" ")[0]);
    
    // Open Skyscanner affiliate redirect link mockup
    window.open(`https://www.skyscanner.co.in/transport/flights/${cleanOrigin}/${cleanDest}/?utm_source=bharathorizon&utm_medium=affiliate`, '_blank');
}

// Helper to inject Breadcrumbs dynamically
function renderBreadcrumbs(crumbs) {
    const container = document.getElementById("breadcrumb-container");
    if (!container) return;
    
    const pathDepth = window.location.pathname.includes("/states/") || window.location.pathname.includes("/destinations/") || window.location.pathname.includes("/blog/") ? "../../" : "";
    
    let html = `<a href="${pathDepth}index.html">Home</a>`;
    crumbs.forEach((crumb, idx) => {
        html += `<span class="separator"></span>`;
        if (idx === crumbs.length - 1) {
            html += `<span class="current">${crumb.name}</span>`;
        } else {
            html += `<a href="${pathDepth}${crumb.link}">${crumb.name}</a>`;
        }
    });
    container.innerHTML = html;
}

// Dynamic injection of structured Schema.org JSON-LD
function injectSchemaMarkup(schemaData) {
    let script = document.getElementById("dynamic-jsonld-schema");
    if (!script) {
        script = document.createElement("script");
        script.type = "application/ld+json";
        script.id = "dynamic-jsonld-schema";
        document.head.appendChild(script);
    }
    script.textContent = JSON.stringify(schemaData);
}
