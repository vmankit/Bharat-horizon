/* 
   Bharat Horizon - Map Controller
   Handles interactive node hover, clicks, region filter overlays, and tooltips on the SVG India Map
*/

document.addEventListener("DOMContentLoaded", () => {
    initIndiaMap();
});

async function initIndiaMap() {
    const mapSvg = document.getElementById("india-constellation-map");
    if (!mapSvg) return;

    // Create a floating tooltip element and add it to body if not already present
    let tooltip = document.getElementById("map-floating-tooltip");
    if (!tooltip) {
        tooltip = document.createElement("div");
        tooltip.id = "map-floating-tooltip";
        tooltip.className = "map-tooltip";
        document.body.appendChild(tooltip);
    }

    // Load states catalog for tooltips
    let statesCatalog = [];
    try {
        const pathDepth = window.location.pathname.includes("/states/") || window.location.pathname.includes("/destinations/") || window.location.pathname.includes("/blog/") ? "../../" : "";
        const response = await fetch(`${pathDepth}data/states.json`);
        statesCatalog = await response.json();
    } catch (e) {
        console.error("Failed to load map state metadata", e);
    }

    // Bind event listeners to all state nodes
    const nodes = mapSvg.querySelectorAll(".state-node");
    nodes.forEach(node => {
        const stateId = node.getAttribute("data-id");
        const stateMeta = statesCatalog.find(s => s.id === stateId) || {
            name: stateId.toUpperCase().replace(/-/g, " "),
            region: "India",
            vibe: "Explore this beautiful Indian destination."
        };

        // Hover In
        node.addEventListener("mouseenter", (e) => {
            tooltip.innerHTML = `
                <span class="region">${stateMeta.region}</span>
                <h4>${stateMeta.name}</h4>
                <p>${stateMeta.vibe}</p>
                <div class="cta">Fly to Destination &rarr;</div>
            `;
            tooltip.classList.add("active");
        });

        // Hover Move
        node.addEventListener("mousemove", (e) => {
            // Keep tooltip offset slightly from mouse pointer
            const tooltipWidth = tooltip.offsetWidth;
            const tooltipHeight = tooltip.offsetHeight;
            tooltip.style.left = `${e.pageX - tooltipWidth / 2}px`;
            tooltip.style.top = `${e.pageY - tooltipHeight - 20}px`;
        });

        // Hover Out
        node.addEventListener("mouseleave", () => {
            tooltip.classList.remove("active");
        });

        // Click Route
        node.addEventListener("click", () => {
            tooltip.classList.remove("active");
            const prefix = window.location.pathname.includes("/states/") || window.location.pathname.includes("/destinations/") || window.location.pathname.includes("/blog/") ? "../../" : "";
            window.location.href = `${prefix}state.html?id=${stateId}`;
        });
    });

    // Handle Regional Filter Tabs
    const filterTabs = document.querySelectorAll(".map-filter-tab");
    filterTabs.forEach(tab => {
        tab.addEventListener("click", () => {
            // Set active class
            filterTabs.forEach(t => t.classList.remove("active"));
            tab.classList.add("active");

            const selectedRegion = tab.getAttribute("data-region");

            // Toggle node visibilities/opacities based on region
            nodes.forEach(node => {
                const stateId = node.getAttribute("data-id");
                const stateMeta = statesCatalog.find(s => s.id === stateId);
                
                if (selectedRegion === "All") {
                    node.style.opacity = "1";
                    node.style.pointerEvents = "auto";
                } else if (stateMeta && stateMeta.region.trim() === selectedRegion.trim()) {
                    node.style.opacity = "1";
                    node.style.pointerEvents = "auto";
                    // Apply brief blink/glow effect
                    const circle = node.querySelector("circle");
                    if (circle) {
                        circle.style.animation = "none";
                        setTimeout(() => {
                            circle.style.animation = "pulseGlow 1.5s infinite alternate";
                        }, 10);
                    }
                } else {
                    node.style.opacity = "0.15";
                    node.style.pointerEvents = "none";
                }
            });
        });
    });

    // Add styles for region pulse animation to header/document dynamically
    if (!document.getElementById("map-animation-styles")) {
        const styleSheet = document.createElement("style");
        styleSheet.id = "map-animation-styles";
        styleSheet.innerText = `
            @keyframes pulseGlow {
                0% { stroke: rgba(212, 175, 55, 0.4); stroke-width: 8; }
                100% { stroke: rgba(212, 175, 55, 0.8); stroke-width: 18; }
            }
        `;
        document.head.appendChild(styleSheet);
    }
}
