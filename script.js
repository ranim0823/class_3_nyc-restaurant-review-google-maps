// Mapbox API access token
mapboxgl.accessToken = 'pk.eyJ1IjoicmFuLW1hcCIsImEiOiJjbTlicmp4YXQwa2IyMmtxMWpvbTI1Y3MxIn0.648gkZUHOMLe8Nxww67Yww';

// Initialize the map
const map = new mapboxgl.Map({
    container: 'map',
    style: 'mapbox://styles/mapbox/light-v11',
    center: [-74.006, 40.7128],
    zoom: 13
});

// Process restaurant data - only include types ending with "_restaurant"
function processRestaurantData(rawData) {
    const uniqueRestaurants = {};
    const cuisineTypes = new Set();
    
    rawData.forEach(restaurant => {
        const primaryType = restaurant.primary_type;
        
        if (primaryType && primaryType.endsWith('_restaurant')) {
            const cuisineType = primaryType;
            cuisineTypes.add(cuisineType);
            
            if (!uniqueRestaurants[restaurant.google_place_id]) {
                uniqueRestaurants[restaurant.google_place_id] = {
                    id: restaurant.google_place_id,
                    name: restaurant.name,
                    primary_type: primaryType,
                    cuisine: cuisineType,
                    rating: parseFloat(restaurant.overall_rating),
                    review_count: parseInt(restaurant.user_rating_count),
                    price_level: restaurant.price_level,
                    latitude: parseFloat(restaurant.latitude),
                    longitude: parseFloat(restaurant.longitude),
                    summary: restaurant.generative_summary,
                    serves_veg: restaurant.serves_veg_food === "TRUE",
                    coordinates: [parseFloat(restaurant.longitude), parseFloat(restaurant.latitude)],
                    reviews: []
                };
            }
            
            if (uniqueRestaurants[restaurant.google_place_id].reviews.length < 3) {
                uniqueRestaurants[restaurant.google_place_id].reviews.push({
                    text: restaurant.review_text,
                    rating: parseInt(restaurant.review_rating),
                    date: new Date(restaurant.publish_time)
                });
            }
        }
    });
    
    return {
        restaurants: Object.values(uniqueRestaurants),
        cuisineTypes: Array.from(cuisineTypes).sort()
    };
}

// Format cuisine type for display
function formatCuisineType(type) {
    return type
        .replace(/_restaurant$/, '')
        .replace(/_/g, ' ')
        .replace(/(?:^|\s)\S/g, a => a.toUpperCase());
}

// Emoji mapping for cuisine types
function getEmojiForCuisine(cuisineType) {
    // Country-based emojis
    const countryEmojis = {
        'american_restaurant': '🇺🇸',
        'afghani_restaurant': '🇦🇫',
        'african_restaurant': '🌍',
        'brazilian_restaurant': '🇧🇷',
        'chinese_restaurant': '🇨🇳',
        'french_restaurant': '🇫🇷',
        'greek_restaurant': '🇬🇷',
        'indian_restaurant': '🇮🇳',
        'indonesian_restaurant': '🇮🇩',
        'italian_restaurant': '🇮🇹',
        'japanese_restaurant': '🇯🇵',
        'korean_restaurant': '🇰🇷',
        'lebanese_restaurant': '🇱🇧',
        'mediterranean_restaurant': '🌍',
        'mexican_restaurant': '🇲🇽',
        'middle_eastern_restaurant': '🌍',
        'spanish_restaurant': '🇪🇸',
        'thai_restaurant': '🇹🇭',
        'turkish_restaurant': '🇹🇷',
        'vietnamese_restaurant': '🇻🇳'
    };

    // Dish-based emojis
    const dishEmojis = {
        'barbecue_restaurant': '🍖',
        'breakfast_restaurant': '🥞',
        'brunch_restaurant': '🥑',
        'buffet_restaurant': '🍽️',
        'dessert_restaurant': '🍰',
        'diner': '🍽️',
        'fast_food_restaurant': '🍟',
        'fine_dining_restaurant': '🍷',
        'hamburger_restaurant': '🍔',
        'pizza_restaurant': '🍕',
        'ramen_restaurant': '🍜',
        'sandwich_shop': '🥪',
        'seafood_restaurant': '🦞',
        'steak_house': '🥩',
        'sushi_restaurant': '🍣',
        'vegan_restaurant': '🌱',
        'vegetarian_restaurant': '🥗'
    };

    return countryEmojis[cuisineType] || dishEmojis[cuisineType] || '🍽️';
}

// Color mapping for cuisine types
function getColorForCuisine(cuisineType) {
    // Country-based colors
    const countryColors = {
        'american_restaurant': '#3c78d8',
        'afghani_restaurant': '#6aa84f',
        'african_restaurant': '#e69138',
        'brazilian_restaurant': '#6aa84f',
        'chinese_restaurant': '#cc0000',
        'french_restaurant': '#3d85c6',
        'greek_restaurant': '#0b5394',
        'indian_restaurant': '#ff9900',
        'indonesian_restaurant': '#cc0000',
        'italian_restaurant': '#009e73',
        'japanese_restaurant': '#bcbcbc',
        'korean_restaurant': '#3d85c6',
        'lebanese_restaurant': '#cc0000',
        'mediterranean_restaurant': '#e69138',
        'mexican_restaurant': '#6aa84f',
        'middle_eastern_restaurant': '#990000',
        'spanish_restaurant': '#cc0000',
        'thai_restaurant': '#990000',
        'turkish_restaurant': '#e69138',
        'vietnamese_restaurant': '#cc0000'
    };

    // Dish-based colors
    const dishColors = {
        'barbecue_restaurant': '#8b0000',
        'breakfast_restaurant': '#ffd700',
        'brunch_restaurant': '#ffa500',
        'buffet_restaurant': '#9370db',
        'dessert_restaurant': '#ff69b4',
        'diner': '#a0522d',
        'fast_food_restaurant': '#ff0000',
        'fine_dining_restaurant': '#800080',
        'hamburger_restaurant': '#8b4513',
        'pizza_restaurant': '#dc143c',
        'ramen_restaurant': '#ff8c00',
        'sandwich_shop': '#d2b48c',
        'seafood_restaurant': '#1e90ff',
        'steak_house': '#8b0000',
        'sushi_restaurant': '#ff6347',
        'vegan_restaurant': '#2e8b57',
        'vegetarian_restaurant': '#228b22'
    };

    return countryColors[cuisineType] || dishColors[cuisineType] || '#666666';
}

// Group cuisine types into country-based and dish-based categories
function groupCuisineTypes(types) {
    const countryBased = [
        'american_restaurant', 'afghani_restaurant', 'african_restaurant',
        'brazilian_restaurant', 'chinese_restaurant', 'french_restaurant',
        'greek_restaurant', 'indian_restaurant', 'indonesian_restaurant',
        'italian_restaurant', 'japanese_restaurant', 'korean_restaurant',
        'lebanese_restaurant', 'mediterranean_restaurant', 'mexican_restaurant',
        'middle_eastern_restaurant', 'spanish_restaurant', 'thai_restaurant',
        'turkish_restaurant', 'vietnamese_restaurant'
    ];

    const dishBased = [
        'barbecue_restaurant', 'breakfast_restaurant', 'brunch_restaurant',
        'buffet_restaurant', 'dessert_restaurant', 'diner',
        'fast_food_restaurant', 'fine_dining_restaurant', 'hamburger_restaurant',
        'pizza_restaurant', 'ramen_restaurant', 'sandwich_shop',
        'seafood_restaurant', 'steak_house', 'sushi_restaurant',
        'vegan_restaurant', 'vegetarian_restaurant'
    ];

    const availableCountry = types.filter(type => countryBased.includes(type));
    const availableDish = types.filter(type => dishBased.includes(type));

    return [
        { name: 'By Country/Region', types: availableCountry },
        { name: 'By Dish Type', types: availableDish }
    ].filter(group => group.types.length > 0);
}

// Add markers to the map
function addMarkers(restaurants) {
    document.querySelectorAll('.mapboxgl-marker').forEach(marker => marker.remove());
    
    restaurants.forEach(restaurant => {
        const el = document.createElement('div');
        el.className = 'marker';
        el.innerHTML = getEmojiForCuisine(restaurant.cuisine);
        el.style.fontSize = '16px';
        el.style.textAlign = 'center';
        el.style.textShadow = '0 0 3px white';
        el.style.cursor = 'pointer';
        
        const marker = new mapboxgl.Marker({
            element: el,
            anchor: 'center'
        })
        .setLngLat(restaurant.coordinates)
        .addTo(map);
        
        function updateMarkerSize() {
            const zoom = map.getZoom();
            const scale = Math.min(1.5, Math.max(0.7, zoom / 15));
            el.style.fontSize = `${16 * scale}px`;
        }
        
        map.on('zoom', updateMarkerSize);
        updateMarkerSize();
        
        const popupContent = `
            <div class="popup-content">
                <h3>${restaurant.name}</h3>
                <p><strong>Cuisine:</strong> ${formatCuisineType(restaurant.cuisine)}</p>
                <div class="rating-container">
                    <span class="rating">${restaurant.rating.toFixed(1)}</span>
                    <span class="stars">${'★'.repeat(Math.round(restaurant.rating))}</span>
                    <span class="review-count">(${restaurant.review_count} reviews)</span>
                </div>
                ${restaurant.price_level ? `<p><strong>Price:</strong> ${restaurant.price_level.replace('PRICE_LEVEL_', '')}</p>` : ''}
                <button class="more-info" data-id="${restaurant.id}">More Info</button>
            </div>
        `;
        
        marker.setPopup(new mapboxgl.Popup({ offset: 25 }).setHTML(popupContent));
    });
}

// Setup filter controls with grouped cuisine types
function setupCuisineFilters(types) {
    const filterContainer = document.getElementById('filters-container');
    filterContainer.innerHTML = '';
    
    const cuisineGroups = groupCuisineTypes(types);
    
    cuisineGroups.forEach(group => {
        const groupDiv = document.createElement('div');
        groupDiv.className = 'filter-group';
        groupDiv.innerHTML = `<h3>${group.name}</h3>`;
        
        group.types.forEach(type => {
            const div = document.createElement('div');
            div.className = 'filter-item';
            div.innerHTML = `
                <input type="checkbox" id="filter-${type}" checked>
                <label for="filter-${type}">
                    ${getEmojiForCuisine(type)} ${formatCuisineType(type)}
                </label>
            `;
            groupDiv.appendChild(div);
            
            div.querySelector('input').addEventListener('change', filterRestaurants);
        });
        
        filterContainer.appendChild(groupDiv);
    });
}

// Filter restaurants based on selected cuisine types
function filterRestaurants() {
    const selectedTypes = [];
    document.querySelectorAll('#filters-container input[type="checkbox"]:checked').forEach(checkbox => {
        selectedTypes.push(checkbox.id.replace('filter-', ''));
    });
    
    const filtered = window.restaurantData.filter(restaurant => 
        selectedTypes.includes(restaurant.cuisine)
    );
    
    addMarkers(filtered);
}

// Show restaurant details
function showRestaurantDetails(restaurant) {
    const detailsContent = document.getElementById('details-content');
    detailsContent.innerHTML = `
        <h3>${restaurant.name}</h3>
        <div class="rating-container">
            <span class="rating">${restaurant.rating.toFixed(1)}</span>
            <span class="stars">${'★'.repeat(Math.round(restaurant.rating))}</span>
            <span class="review-count">(${restaurant.review_count} reviews)</span>
        </div>
        <p><strong>Cuisine:</strong> ${formatCuisineType(restaurant.cuisine)}</p>
        ${restaurant.price_level ? `<p><strong>Price:</strong> ${restaurant.price_level.replace('PRICE_LEVEL_', '')}</p>` : ''}
        ${restaurant.serves_veg ? '<p>✓ Vegetarian options available</p>' : ''}
        
        ${restaurant.summary ? `<div class="summary"><p>${restaurant.summary}</p></div>` : ''}
        
        ${restaurant.reviews.length > 0 ? `
        <div class="reviews-section">
            <h4>Recent Reviews</h4>
            ${restaurant.reviews.map(review => `
                <div class="review">
                    <div class="review-rating">${'★'.repeat(review.rating)}</div>
                    <p class="review-text">"${review.text}"</p>
                    <p class="review-date">${review.date.toLocaleDateString()}</p>
                </div>
            `).join('')}
        </div>
        ` : ''}
    `;
    
    document.getElementById('restaurant-details').classList.add('visible');
}

function getMarkerSize(currentZoom) {
    // More exponential scaling
    const minSize = 1;
    const maxSize = 10;
    const scaleFactor = 3;
    
    // Exponential growth based on zoom level
    let size = minSize * Math.pow(scaleFactor, currentZoom - 10);
    
    return Math.min(maxSize, Math.max(minSize, size));
  }

// Load restaurant data
async function loadRestaurantData() {
    try {
        const response = await fetch('restaurants_wo_reviews.json');
        if (!response.ok) throw new Error('Failed to load data');
        const rawData = await response.json();
        return processRestaurantData(rawData);
    } catch (error) {
        console.error('Error loading restaurant data:', error);
        return { restaurants: [], cuisineTypes: [] };
    }
}

// Initialize app
async function initializeApp() {
    const { restaurants, cuisineTypes } = await loadRestaurantData();
    
    if (restaurants.length > 0) {
        window.restaurantData = restaurants;
        addMarkers(restaurants);
        setupCuisineFilters(cuisineTypes);
        
        // Setup select/deselect all buttons
        document.getElementById('select-all').addEventListener('click', () => {
            document.querySelectorAll('#filters-container input[type="checkbox"]').forEach(checkbox => {
                checkbox.checked = true;
            });
            filterRestaurants();
        });
        
        document.getElementById('deselect-all').addEventListener('click', () => {
            document.querySelectorAll('#filters-container input[type="checkbox"]').forEach(checkbox => {
                checkbox.checked = false;
            });
            filterRestaurants();
        });
        
        // Close details panel
        document.getElementById('close-details').addEventListener('click', () => {
            document.getElementById('restaurant-details').classList.remove('visible');
        });
        
        // Handle info button clicks
        document.addEventListener('click', (e) => {
            if (e.target.classList.contains('more-info')) {
                const restaurantId = e.target.getAttribute('data-id');
                const restaurant = restaurants.find(r => r.id === restaurantId);
                if (restaurant) showRestaurantDetails(restaurant);
            }
        });
    }
}

// Start the app
map.on('load', initializeApp);