/* 
   Bharat Horizon - State Page Controller
   Loads state details dynamically from JSON based on URL search query "?id=state-slug"
*/

document.addEventListener("DOMContentLoaded", () => {
    loadStateDetails();
});

async function loadStateDetails() {
    const urlParams = new URLSearchParams(window.location.search);
    let stateId = urlParams.get("id");
    
    // Default fallback to delhi if ID is missing or invalid
    if (!stateId) {
        stateId = "delhi";
    }

    // Aliases for state slug -> filename mismatches
    const STATE_ALIASES = {
        "jammu-kashmir": "jammu-and-kashmir"
    };

    // Use aliased filename when available
    let fetchId = STATE_ALIASES[stateId] || stateId;

    try {
        let response = await fetch(`data/states/${fetchId}.json`);

        // If the direct file wasn't found, try to resolve via the states index
        if (!response.ok) {
            const idxResp = await fetch('data/states.json');
            if (idxResp.ok) {
                const statesIndex = await idxResp.json(); // array of {id,...}
                const candidates = statesIndex.map(s => s.id);
                const tokens = stateId.split('-').filter(Boolean);

                // Find a candidate that contains all tokens from the requested id
                const match = candidates.find(c => tokens.every(t => c.includes(t)));
                if (match) {
                    fetchId = match;
                    response = await fetch(`data/states/${fetchId}.json`);
                    if (response.ok) {
                        stateId = fetchId; // update for UI and links
                    }
                }
            }
        }

        if (!response.ok) throw new Error("State data not found");

        const stateData = await response.json();
        
        // 1. Update Document Title and SEO Metadata
        document.title = `${stateData.name} Travel Diaries & Tourism Guide | Bharat Horizon`;
        
        // Update Meta Description
        let metaDesc = document.querySelector('meta[name="description"]');
        if (!metaDesc) {
            metaDesc = document.createElement('meta');
            metaDesc.name = "description";
            document.head.appendChild(metaDesc);
        }
        metaDesc.content = `Plan your ultimate trip to ${stateData.name}. Discover top 20 places to visit, hidden gems, local food specialties, custom itineraries, and expert travel tips for ${stateData.name}.`;

        // 2. Set Breadcrumbs
        renderBreadcrumbs([
            { name: "Explore", link: "explore.html" },
            { name: stateData.name, link: `state.html?id=${stateData.id}` }
        ]);

        // 3. Inject Content Areas
        document.getElementById("state-title").innerText = stateData.name;
        document.getElementById("state-vibe").innerText = stateData.vibe;
        document.getElementById("state-overview").innerText = stateData.overview;
        document.getElementById("state-best-time").innerText = stateData.bestTimeToVisit;
        
        // Sidebar Quick Facts
        document.getElementById("fact-capital").innerText = stateData.capital;
        document.getElementById("fact-region").innerText = stateData.region;
        document.getElementById("fact-budget").innerText = stateData.budgetGuide.level;
        document.getElementById("fact-reach").innerText = `Air, Rail & Road Access`;

        // How to Reach Details
        document.getElementById("reach-air").innerText = stateData.howToReach.air;
        document.getElementById("reach-rail").innerText = stateData.howToReach.rail;
        document.getElementById("reach-road").innerText = stateData.howToReach.road;

        // Populate Airports & Railways
        const airportList = document.getElementById("airports-list");
        airportList.innerHTML = stateData.airports_railways.map(item => `<li>${item}</li>`).join("");

        // Budget Guide Details
        document.getElementById("budget-cost").innerText = stateData.budgetGuide.costPerDay;
        document.getElementById("budget-rating").innerText = "★".repeat(stateData.budgetGuide.rating) + "☆".repeat(5 - stateData.budgetGuide.rating);
        document.getElementById("budget-desc").innerText = stateData.budgetGuide.description;

        // Render Travel Tips List
        const tipsList = document.getElementById("tips-list");
        tipsList.innerHTML = stateData.travelTips.map(tip => `
            <div style="display:flex; gap:10px; margin-bottom:12px; font-size:0.95rem; color:var(--color-text-muted);">
                <span style="color:var(--color-gold); font-weight:bold;">✔</span>
                <span>${tip}</span>
            </div>
        `).join("");

        // 4. Render Top 20 Places to Visit Grid
        const placesGrid = document.getElementById("places-grid");
        placesGrid.innerHTML = stateData.places.map((place, idx) => `
            <div class="diary-card">
                <div class="diary-card-img-container">
                    <img src="assets/images/placeholder.svg" alt="${place.name}" class="diary-card-img" />
                    <span class="diary-card-tag">Spot #${idx + 1}</span>
                </div>
                <div class="diary-card-content">
                    <div>
                        <div class="diary-card-meta">
                            <span>Ranked #${idx + 1}</span>
                            <span>&bull;</span>
                            <span>Sightseeing</span>
                        </div>
                        <h3 class="diary-card-title">${place.name}</h3>
                        <p class="diary-card-summary">Explore the historic site of ${place.name}, one of the key landmarks within ${stateData.name}. Find how to reach, entry times, and details.</p>
                    </div>
                    <a href="destination.html?id=${place.slug}" class="diary-card-readmore">
                        Read Travel Diary 
                        <svg viewBox="0 0 24 24"><path d="M4,11V13H16L10.5,18.5L11.92,19.92L19.84,12L11.92,4.08L10.5,5.5L16,11H4Z"/></svg>
                    </a>
                </div>
            </div>
        `).join("");

        // 5. Render Famous Food Cuisines
        const foodList = document.getElementById("famous-foods-list");
        foodList.innerHTML = stateData.famousFoods.map((food, idx) => `
            <div class="food-card">
                <div class="food-card-number">0${idx + 1}</div>
                <div class="food-card-content">
                    <h4>${food.name}</h4>
                    <p>${food.description}</p>
                </div>
            </div>
        `).join("");

        // Render Festivals list
        const festivalList = document.getElementById("festivals-list");
        festivalList.innerHTML = stateData.festivals.map(fest => `
            <div style="background:rgba(255,255,255,0.02); border:1px solid rgba(255,255,255,0.05); padding:20px; border-radius:8px;">
                <div style="display:flex; justify-content:space-between; margin-bottom:10px;">
                    <h4 style="color:var(--color-gold); font-size:1.15rem;">${fest.name}</h4>
                    <span style="font-size:0.85rem; background:rgba(212,175,55,0.15); color:var(--color-gold); padding:2px 8px; border-radius:4px; height:fit-content;">${fest.month}</span>
                </div>
                <p style="font-size:0.9rem; color:var(--color-text-muted); line-height:1.5;">${fest.vibe}</p>
            </div>
        `).join("");

        // 6. Setup Itineraries Tabs and Timeline Rendering
        setupItineraries(stateData);

        // 7. Render FAQ Section
        const faqList = document.getElementById("faqs-list");
        faqList.innerHTML = stateData.faqs.map(faq => `
            <div class="faq-item-block">
                <div class="faq-question">
                    <span>${faq.q}</span>
                    <svg viewBox="0 0 24 24"><path d="M7.41,8.58L12,13.17L16.59,8.58L18,10L12,16L6,10L7.41,8.58Z"/></svg>
                </div>
                <div class="faq-answer">
                    <p>${faq.a}</p>
                </div>
            </div>
        `).join("");

        // Bind FAQ expand triggers
        document.querySelectorAll(".faq-question").forEach(q => {
            q.addEventListener("click", () => {
                const block = q.parentElement;
                block.classList.toggle("active");
            });
        });

        // 8. Inject Schema Markup (SEO)
        const schema = {
            "@context": "https://schema.org",
            "@type": "TouristDestination",
            "name": stateData.name,
            "description": stateData.overview,
            "containedInPlace": {
                "@type": "Country",
                "name": "India"
            },
            "touristType": stateData.style.split(", "),
            "estimatedCost": {
                "@type": "MonetaryAmount",
                "currency": "INR",
                "value": stateData.budgetGuide.costPerDay
            }
        };
        injectSchemaMarkup(schema);

        // 9. Render Related Articles (Sample dynamic sidebar suggestions)
        renderRelatedArticles(stateData);

    } catch (err) {
        console.error(err);
        document.getElementById("state-main-wrapper").innerHTML = `
            <div class="container" style="padding: 100px 0; text-align:center;">
                <h2>Destination Portal Loading Error</h2>
                <p style="color:var(--color-text-muted); margin-bottom:30px;">Could not retrieve the travel data for state ID: <strong>${stateId}</strong>.</p>
                <a href="explore.html" class="btn btn-primary">Return to Exploration portal</a>
            </div>
        `;
    }
}

// Render dynamic itineraries timelines
function setupItineraries(stateData) {
    const itineraryContainer = document.getElementById("itinerary-timeline");
    const tab2 = document.getElementById("tab-2day");
    const tab3 = document.getElementById("tab-3day");
    const tab5 = document.getElementById("tab-5day");
    
    const renderTimeline = (daysList) => {
        itineraryContainer.innerHTML = daysList.map((day, idx) => `
            <div class="timeline-item ${idx === 0 ? 'active' : ''}">
                <div class="timeline-day">Day 0${day.day}</div>
                <h3 class="timeline-title">${day.theme}</h3>
                <ul class="timeline-activities">
                    ${day.activities.map(act => `<li>${act}</li>`).join("")}
                </ul>
            </div>
        `).join("");
    };

    // Initial default render (3 Day Itinerary)
    renderTimeline(stateData.itinerary3Day);
    tab3.classList.add("active");

    // Click tabs triggers
    tab2.addEventListener("click", () => {
        [tab2, tab3, tab5].forEach(t => t.classList.remove("active"));
        tab2.classList.add("active");
        renderTimeline(stateData.itinerary2Day);
    });

    tab3.addEventListener("click", () => {
        [tab2, tab3, tab5].forEach(t => t.classList.remove("active"));
        tab3.classList.add("active");
        renderTimeline(stateData.itinerary3Day);
    });

    tab5.addEventListener("click", () => {
        [tab2, tab3, tab5].forEach(t => t.classList.remove("active"));
        tab5.classList.add("active");
        renderTimeline(stateData.itinerary5Day);
    });
}

// Generate related articles list dynamically for sidebar linkings
function renderRelatedArticles(stateData) {
    const relatedList = document.getElementById("related-blogs-list");
    if (!relatedList) return;

    const blogs = [
        { title: `Best Places to Visit in ${stateData.name}`, slug: `best-places-to-visit-in-${stateData.id}` },
        { title: `Best Time to Visit ${stateData.name}`, slug: `best-time-to-visit-${stateData.id}` },
        { title: `7 Day Road Trip Itinerary for ${stateData.name}`, slug: `7-day-itinerary-for-${stateData.id}` },
        { title: `Hidden Gems in ${stateData.name} Unveiled`, slug: `hidden-gems-in-${stateData.id}` }
    ];

    relatedList.innerHTML = blogs.map(b => `
        <div style="margin-bottom:15px; border-bottom:1px solid rgba(255,255,255,0.03); padding-bottom:10px;">
            <a href="diaries.html?article=${b.slug}" style="font-size:0.95rem; font-weight:600; color:var(--color-text-main);">
                ${b.title}
            </a>
            <p style="font-size:0.8rem; color:var(--color-text-muted); margin-top:3px;">Travel Guide &bull; A must-read blog</p>
        </div>
    `).join("");
}
