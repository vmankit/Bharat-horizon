/* 
   Bharat Horizon - Destination Article Page Controller
   Loads destination specific detail articles dynamically from data/destinations/[id].json
*/

document.addEventListener("DOMContentLoaded", () => {
    loadDestinationDetails();
});

async function loadDestinationDetails() {
    const urlParams = new URLSearchParams(window.location.search);
    let destId = urlParams.get("id");
    
    // Default fallback to hawa mahal if ID is missing or invalid
    if (!destId) {
        destId = "jaipur-hawa-mahal";
    }

    try {
        const response = await fetch(`data/destinations/${destId}.json`);
        if (!response.ok) throw new Error("Destination data not found");
        
        const destData = await response.json();
        
        // 1. Update Document Title and SEO Metadata
        document.title = `${destData.name} Travel Diary - Places to Visit in ${destData.stateName} | Bharat Horizon`;
        
        // Update Meta Description
        let metaDesc = document.querySelector('meta[name="description"]');
        if (!metaDesc) {
            metaDesc = document.createElement('meta');
            metaDesc.name = "description";
            document.head.appendChild(metaDesc);
        }
        metaDesc.content = `Read our premium travel diary for ${destData.name}. Find why to visit, top things to do, travel budgets, accommodation recommendations, and nearby getaways in ${destData.stateName}.`;

        // 2. Set Breadcrumbs
        renderBreadcrumbs([
            { name: "Explore", link: "explore.html" },
            { name: destData.stateName, link: `state.html?id=${destData.stateId}` },
            { name: destData.name, link: `destination.html?id=${destData.id}` }
        ]);

        // 3. Inject Content Areas
        document.getElementById("dest-title").innerText = destData.name;
        document.getElementById("dest-vibe").innerText = destData.vibe;
        document.getElementById("dest-state-link").innerHTML = `<a href="state.html?id=${destData.stateId}">${destData.stateName} Guide</a>`;
        document.getElementById("dest-why-visit").innerText = destData.whyVisit;
        document.getElementById("dest-season").innerText = destData.bestSeason;
        document.getElementById("dest-budget-idea").innerText = destData.budgetTripIdea;
        document.getElementById("dest-reach").innerText = destData.howToReach;

        // Update Affiliate Skyscanner forms
        const flightDestInput = document.getElementById("flight-dest");
        if (flightDestInput) {
            flightDestInput.value = `${destData.name} (${destData.name.substring(0,3).toUpperCase()})`;
        }

        // 4. Render Travel Angles List
        document.getElementById("angle-family").innerText = destData.travelAngles.family;
        document.getElementById("angle-solo").innerText = destData.travelAngles.solo;
        document.getElementById("angle-couple").innerText = destData.travelAngles.couple;

        // 5. Render Top Things To Do List
        const thingsList = document.getElementById("dest-things-list");
        thingsList.innerHTML = destData.topThingsToDo.map(thing => `
            <div class="faq-item-block" style="border-color:rgba(212,175,55,0.1); margin-bottom:15px; padding:20px;">
                <p style="font-size:1rem; color:var(--color-text-main); line-height:1.6;">${thing}</p>
            </div>
        `).join("");

        // 6. Render Where to Stay List
        const stayList = document.getElementById("dest-stay-list");
        stayList.innerHTML = `
            <div class="stay-card">
                <div class="stay-badge">
                    <svg viewBox="0 0 24 24"><path d="M7,14A2,2 0 0,0 5,16A2,2 0 0,0 7,18H17A2,2 0 0,0 19,16A2,2 0 0,0 17,14H7M19,7H12V11H19V7M21,5A2,2 0 0,1 23,7V16A2,2 0 0,1 21,18H19V21H17V18H7V21H5V18H3A2,2 0 0,1 1,16V7A2,2 0 0,1 3,5H21Z"/></svg>
                    <span>Luxury</span>
                </div>
                <div class="stay-details">
                    <h4>${destData.whereToStay.luxury.split(" - ")[0]}</h4>
                    <p>${destData.whereToStay.luxury.split(" - ")[1] || "A luxury boutique property offering premium local hospitality and heritage views."}</p>
                </div>
                <a href="https://booking.com/?aid=bharathorizon-mock" target="_blank" class="gear-cta-link" style="text-align:center;">Book Room</a>
            </div>
            
            <div class="stay-card">
                <div class="stay-badge">
                    <svg viewBox="0 0 24 24"><path d="M19,5V7H12V5H19M21,3H3A2,2 0 0,0 1,5V16A2,2 0 0,0 3,18H5V21H7V18H17V21H19V18H21A2,2 0 0,0 23,16V5A2,2 0 0,0 21,3M21,16H3V11H21V16M21,9H3V5H21V9Z"/></svg>
                    <span>Mid-Range</span>
                </div>
                <div class="stay-details">
                    <h4>${destData.whereToStay.midRange.split(" - ")[0]}</h4>
                    <p>${destData.whereToStay.midRange.split(" - ")[1] || "A clean and comfortable hotel located centrally near key sightseeing structures."}</p>
                </div>
                <a href="https://booking.com/?aid=bharathorizon-mock" target="_blank" class="gear-cta-link" style="text-align:center;">Book Room</a>
            </div>
            
            <div class="stay-card">
                <div class="stay-badge">
                    <svg viewBox="0 0 24 24"><path d="M5,8.5C5,7.67 5.67,7 6.5,7C7.33,7 8,7.67 8,8.5C8,9.33 7.33,10 6.5,10C5.67,10 5,9.33 5,8.5M19,10H12V5H19M21,3H3A2,2 0 0,0 1,5V16A2,2 0 0,0 3,18H5V21H7V18H17V21H19V18H21A2,2 0 0,0 23,16V5A2,2 0 0,0 21,3Z"/></svg>
                    <span>Budget</span>
                </div>
                <div class="stay-details">
                    <h4>${destData.whereToStay.budget.split(" - ")[0]}</h4>
                    <p>${destData.whereToStay.budget.split(" - ")[1] || "Cozy, friendly dorm spaces ideal for backpackers, solo travelers, and students."}</p>
                </div>
                <a href="https://booking.com/?aid=bharathorizon-mock" target="_blank" class="gear-cta-link" style="text-align:center;">Book Room</a>
            </div>
        `;

        // 7. Render What to Eat List
        const foodList = document.getElementById("dest-food-list");
        foodList.innerHTML = destData.whatEat ? destData.whatEat.map((food, idx) => `
            <div class="food-card" style="margin-bottom:12px; background:rgba(255,255,255,0.01);">
                <div class="food-card-number">0${idx+1}</div>
                <div class="food-card-content">
                    <h4>${food}</h4>
                    <p>Sample regional culinary creation highly recommended to try when exploring local street food joints.</p>
                </div>
            </div>
        `).join("") : destData.whatToEat.map((food, idx) => `
            <div class="food-card" style="margin-bottom:12px; background:rgba(255,255,255,0.01);">
                <div class="food-card-number">0${idx+1}</div>
                <div class="food-card-content">
                    <h4>${food}</h4>
                    <p>Sample regional culinary creation highly recommended to try when exploring local street food joints.</p>
                </div>
            </div>
        `).join("");

        // 8. Render Nearby Destinations
        const nearbyGrid = document.getElementById("dest-nearby-grid");
        nearbyGrid.innerHTML = destData.nearbyDestinations.map(nearby => `
            <div style="border: 1px solid var(--color-border); border-radius: 8px; padding: 20px; text-align: center; background: rgba(255,255,255,0.02);">
                <h4 style="font-size:1.15rem; color:var(--color-text-main); margin-bottom:12px;">${nearby.name}</h4>
                <a href="destination.html?id=${nearby.slug}" class="diary-card-readmore" style="justify-content:center;">
                    View Entry &rarr;
                </a>
            </div>
        `).join("");

        // 9. Render Hourly Sample Itinerary
        const itineraryList = document.getElementById("dest-itinerary-timeline");
        itineraryList.innerHTML = destData.sampleItinerary.map(item => `
            <div style="display:grid; grid-template-columns:120px 1fr; gap:15px; margin-bottom:20px; border-bottom:1px dashed rgba(255,255,255,0.03); padding-bottom:12px;">
                <div style="font-family:var(--font-heading); color:var(--color-gold); font-weight:bold; font-size:0.9rem;">${item.time}</div>
                <div style="font-size:0.95rem; color:var(--color-text-muted);">${item.activity}</div>
            </div>
        `).join("");

        // 10. Inject Schema Markup (SEO - Article / Attraction)
        const schema = {
            "@context": "https://schema.org",
            "@type": "TouristAttraction",
            "name": destData.name,
            "description": destData.whyVisit,
            "containedInPlace": {
                "@type": "TouristDestination",
                "name": destData.stateName
            },
            "touristType": ["Sightseeing", "Tourism", "Travel Diary"],
            "offers": {
                "@type": "Offer",
                "priceCurrency": "INR",
                "description": destData.budgetTripIdea
            }
        };
        injectSchemaMarkup(schema);

    } catch (err) {
        console.error(err);
        document.getElementById("dest-main-wrapper").innerHTML = `
            <div class="container" style="padding: 100px 0; text-align:center;">
                <h2>Destination Diary Loading Error</h2>
                <p style="color:var(--color-text-muted); margin-bottom:30px;">Could not retrieve travel diary details for destination ID: <strong>${destId}</strong>.</p>
                <a href="explore.html" class="btn btn-primary">Return to Exploration portal</a>
            </div>
        `;
    }
}
