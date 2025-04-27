import json
import re
from collections import Counter

# Load the dataset
def load_data(file_path):
    with open(file_path, 'r') as file:
        return json.load(file)

# Save the processed data to a new file
def save_data(data, file_path):
    with open(file_path, 'w') as file:
        json.dump(data, file, indent=4)

# Keywords categorized by priority
CUISINE_KEYWORDS = {
    "nation_state": [
        "Afghan", "Albanian", "Algerian", "Andorran", "Angolan", "Antiguan", "Argentine", "Armenian", "Australian",
        "Austrian", "Azerbaijani", "Bahamian", "Bahraini", "Bangladeshi", "Barbadian", "Belarusian", "Belgian",
        "Belizean", "Beninese", "Bhutanese", "Bolivian", "Bosnian", "Botswanan", "Brazilian", "British", "Bruneian",
        "Bulgarian", "Burkinabe", "Burmese", "Burundian", "Cambodian", "Cameroonian", "Canadian", "Cape Verdean",
        "Central African", "Chadian", "Chilean", "Chinese", "Colombian", "Comoran", "Congolese", "Costa Rican",
        "Croatian", "Cuban", "Cypriot", "Czech", "Danish", "Djiboutian", "Dominican", "Dutch", "Ecuadorian",
        "Egyptian", "Emirati", "Equatorial Guinean", "Eritrean", "Estonian", "Eswatini", "Ethiopian", "Fijian",
        "Filipino", "Finnish", "French", "Gabonese", "Gambian", "Georgian", "German", "Ghanaian", "Greek", "Grenadian",
        "Guatemalan", "Guinean", "Guinea-Bissauan", "Guyanese", "Haitian", "Honduran", "Hungarian", "Icelandic",
        "Indian", "Indonesian", "Iranian", "Iraqi", "Irish", "Israeli", "Italian", "Ivorian", "Jamaican", "Japanese",
        "Jordanian", "Kazakh", "Kenyan", "Kiribati", "Korean", "Kosovar", "Kuwaiti", "Kyrgyz", "Lao", "Latvian",
        "Lebanese", "Liberian", "Libyan", "Liechtensteiner", "Lithuanian", "Luxembourgish", "Macedonian", "Malagasy",
        "Malawian", "Malaysian", "Maldivian", "Malian", "Maltese", "Marshallese", "Mauritanian", "Mauritian",
        "Mexican", "Micronesian", "Moldovan", "Monacan", "Mongolian", "Montenegrin", "Moroccan", "Mozambican",
        "Namibian", "Nauruan", "Nepalese", "New Zealander", "Nicaraguan", "Nigerien", "Nigerian", "North Korean",
        "Norwegian", "Omani", "Pakistani", "Palauan", "Palestinian", "Panamanian", "Papua New Guinean", "Paraguayan",
        "Peruvian", "Polish", "Portuguese", "Qatari", "Romanian", "Russian", "Rwandan", "Saint Lucian",
        "Salvadoran", "Samoan", "San Marinese", "Sao Tomean", "Saudi", "Senegalese", "Serbian", "Seychellois",
        "Sierra Leonean", "Singaporean", "Slovak", "Slovenian", "Solomon Islander", "Somali", "South African",
        "South Korean", "Spanish", "Sri Lankan", "Sudanese", "Surinamese", "Swazi", "Swedish", "Swiss", "Syrian",
        "Tajik", "Tanzanian", "Thai", "Timorese", "Togolese", "Tongan", "Trinidadian", "Tunisian", "Turkish",
        "Turkmen", "Tuvaluan", "Ugandan", "Ukrainian", "Uruguayan", "Uzbek", "Vanuatuan", "Vatican", "Venezuelan",
        "Vietnamese", "Yemeni", "Zambian", "Zimbabwean", "Persian", "Tibetan", "Mongolian", "Siberian", "taiwanese", "cantonese"
    ],
    "region": [
        "Caribbean", "Latin American", "West African", "Southeast Asian", "Mediterranean", "Middle Eastern", "East Asian",
        "South Asian", "Pan-Asian", "Asian", "American"
    ],
    "food_type": [
        "halal", "kosher", "noodle", "noodles", "dumpling", "dumplings", "hot pot", "hotpot", "chicken", "fried chicken", "sushi", 
        "health", "comfort food", "taco", "tacos", "food court", "vegetarian", "soul food", "vegan", "lounge",
        "bar", "poke", "Coffee", "cafe", "hookahs", "hookah", "teriyaki", "pizza"
    ]
}

# Prioritize less commonly-known cuisines
PRIORITY_ORDER = {
    "nation_state": 1,
    "region": 2,
    "food_type": 3
}

# Mapping to normalize primary_type values
PRIMARY_TYPE_NORMALIZATION = {
    "middle eastern_restaurant": "middle_eastern_restaurant",
    "bar": "bar/pub",
    "bar_restaurant": "bar/pub",
    "pub": "bar/pub",
    "cafe": "cafe",
    "coffee_shop": "cafe",
    "cafe_restaurant": "cafe",
    "coffee_restaurant": "cafe",
    "hookahs_restaurant": "hookah_bar",
    "hookah_restaurant": "hookah_bar",
    "noodles_restaurant": "noodle_restaurant",
    "noodle_restaurant": "noodle_restaurant",
    "sushi": "sushi_restaurant",
    "health_restaurant": "health_food",
    "food court_restaurant": "food_court",
    "meal_takeaway" : "takeout",
    "meal_delivery" : "takeout",
    "dumplings_restaurant" : "dumpling_restaurant",
    "tacos_restaurant" : "taco_restaurant",
    "philippine_restaurant" : "filipino_restaurant",
    "soul food_restaurant" : "comfort food_restaurant",
    "dessert_restaurant" : "dessert_shop",
    "hotpot_restaurant" : "hot pot_restaurant",
}

# Identify keywords in text
def identify_keywords(text):
    keywords_found = {"nation_state": [], "region": [], "food_type": []}
    for category, keywords in CUISINE_KEYWORDS.items():
        for keyword in keywords:
            if re.search(rf"\b{re.escape(keyword)}\b", text, re.IGNORECASE):
                keywords_found[category].append(keyword)
    return keywords_found

# Select the most appropriate keyword based on priority
def select_keyword(keywords_found):
    for category in sorted(PRIORITY_ORDER, key=lambda x: PRIORITY_ORDER[x]):
        if keywords_found[category]:
            # Prioritize less commonly-known cuisines by sorting alphabetically
            return sorted(keywords_found[category])[0]
    return None

# Normalize primary_type values
def normalize_primary_type(primary_type):
    return PRIMARY_TYPE_NORMALIZATION.get(primary_type.lower(), primary_type)

# Remove non-restaurant businesses
def filter_restaurants(data):
    # List of non-restaurant types to exclude
    NON_RESTAURANT_TYPES = [
        "hotel", "grocery_store", "event_venue", "market", "catering_service", "supermarket", "shopping_mall",
        "banquet_hall", "wholesaler", "apartment_building", "night_club", "park", "sports_complex", "food_store",
        "hospital", "condominium_complex", "asian_grocery_store", "wedding_venue", "subway_station", "corporate_office",
        "real_estate_agency", "bowling_alley", "convenience_store", "apartment_complex", "cafeteria", "movie_theater",
        "playground", "museum", "sports_club", "ice_skating_rink", "store", "butcher_shop", "spa", "marina", "comedy_club",
        "historical_landmark", "performing_arts_theater", "book_store", "food", "point_of_interest", "clothing_store", "gym",
        "athletic_field", "consultant", "cultural_center", "child_care_agency", "parking", "department_store", "concert_hall",
        "government_office", "sports_activity_location", "gas_station", "synagogue", "amusement_center", "tour_agency",
        "wellness_center", "transit_depot", "plaza", "international_airport", "bus_station", "health",
        "local_government_office", "confectionery", "farm", "motel", "zoo", "golf_course", "drugstore", "tourist_attraction",
        "liquor_store", "train_station", "finantial_services", "karaoke", "observation_deck", "ferry_terminal", "arena",
        "light_rail_station", "transit_station", "school", "art_gallery", "sporting_goods_store", "post_office",
        "botanical_garden", "laundry", "casino", "fitness_center", "dentist", "library", "university", "pet_store",
        "general_contractor", "nail_salon", "rest_stop", "place_of_worship", "courier_service", "hostel", "amphitheatre",
        "gift_shop", ""
    ]

    # Filter out restaurants with primary_type matching any type in NON_RESTAURANT_TYPES
    return [
        restaurant for restaurant in data
        if normalize_primary_type(restaurant.get("primary_type", "")) not in NON_RESTAURANT_TYPES
    ]

# Process restaurants to update "primary_type"
def process_restaurants(data):
    updated_restaurants = []
    for restaurant in data:
        primary_type = restaurant.get("primary_type", "").strip()
        
        # If primary_type is "restaurant" or empty, attempt to update it
        if not primary_type or primary_type.lower() in ["restaurant", "meal_takeaway", "meal_delivery"]:
            # Combine "generative_summary", "name", and "types" for keyword search
            text = f"{restaurant.get('generative_summary', '')} {restaurant.get('name', '')}"
            if "types" in restaurant and isinstance(restaurant["types"], list):
                text += " " + " ".join(restaurant["types"])
            
            # Identify keywords in the combined text
            keywords_found = identify_keywords(text)
            
            # Select the most appropriate keyword
            selected_keyword = select_keyword(keywords_found)
            
            # Update primary_type if a keyword is found
            if selected_keyword:
                primary_type = f"{selected_keyword.lower()}_restaurant"
        
        # Normalize the primary_type
        restaurant["primary_type"] = normalize_primary_type(primary_type)
        updated_restaurants.append(restaurant)
    
    return updated_restaurants


# Get a ranked list of all unique "primary_type"
def rank_primary_types(data):
    primary_types = [restaurant["primary_type"] for restaurant in data if "primary_type" in restaurant]
    return Counter(primary_types).most_common()

# Get a ranked list of all unique values under "types"
def rank_types(data):
    all_types = []
    for restaurant in data:
        if "types" in restaurant:
            if isinstance(restaurant["types"], list):
                all_types.extend(restaurant["types"])
            elif isinstance(restaurant["types"], str):
                # Handle JSON-like strings
                try:
                    parsed_types = json.loads(restaurant["types"].replace("'", '"'))
                    if isinstance(parsed_types, list):
                        all_types.extend(parsed_types)
                except json.JSONDecodeError:
                    pass
    return Counter(all_types).most_common()

# Remove unwanted subtypes from the "types" field
def remove_unwanted_subtypes(data, unwanted_subtypes):
    for restaurant in data:
        if "types" in restaurant:
            if isinstance(restaurant["types"], list):
                # Filter out unwanted subtypes
                restaurant["types"] = [subtype for subtype in restaurant["types"] if subtype not in unwanted_subtypes]
            elif isinstance(restaurant["types"], str):
                # Handle JSON-like strings
                try:
                    parsed_types = json.loads(restaurant["types"].replace("'", '"'))
                    if isinstance(parsed_types, list):
                        # Filter out unwanted subtypes
                        restaurant["types"] = [subtype for subtype in parsed_types if subtype not in unwanted_subtypes]
                except json.JSONDecodeError:
                    pass
    return data

# Main function
def main():
    input_file = "/Users/ranmei/Documents/GitHub/class_3_nyc-restaurant-review-google-maps/restaurants_unique.json"  # Replace with your input file path
    output_file = "/Users/ranmei/Documents/GitHub/class_3_nyc-restaurant-review-google-maps/restaurants_filtered.json"  # Replace with your output file path

    # Load the dataset
    data = load_data(input_file)

    # Filter out non-restaurant businesses
    filtered_data = filter_restaurants(data)

    # Remove unwanted subtypes
    unwanted_subtypes = [
        "point_of_interest", "establishment", "store", "event_venue", "night_club", "banquet_hall", "karaoke",
        "wedding_venue", "health", "internet_cafe", "video_arcade", "airport", "barbecue_area",
        "sports_activity_location", "performing_arts_theater", "sports_club", "garden", "park", "sports_complex",
        "wholesaler", "market", "amusement_center", "comedy_club", "art_gallery", "farm", "gift_shop", "lodging",
        "home_goods_store", "tourist_attraction", "museum", "hotel", "clothing_store", "historical_landmark",
        "historical_place", "consultant", "dance_hall", "bowling_alley", "florist", "hospital", "wellness_center",
        "athletic_field", "community_center", "atm", "finance", "veterinary_care", "cultural_center", "playground",
        "truck_stop", "courier_service", "discount_store", "furniture_store", "home_improvement_store", "parking",
        "fitness_center", "gym", "bed_and_breakfast", "pet_store", "book_store", "barber_shop", "hair_salon",
        "hair_care", "massage", "car_repair"
    ]
    filtered_data = remove_unwanted_subtypes(filtered_data, unwanted_subtypes)

    # Process restaurants to update "primary_type"
    updated_data = process_restaurants(filtered_data)

    # Save the updated dataset
    save_data(updated_data, output_file)
    print(f"Updated data saved to {output_file}")

    # Rank primary types
    primary_type_ranking = rank_primary_types(updated_data)
    print("Ranked Primary Types:")
    for rank, (primary_type, count) in enumerate(primary_type_ranking, start=1):
        print(f"{rank}. {primary_type}: {count}")

    # Rank subtypes
    subtype_ranking = rank_types(updated_data)
    print("\nRanked Subtypes:")
    for rank, (subtype, count) in enumerate(subtype_ranking, start=1):
        print(f"{rank}. {subtype}: {count}")

if __name__ == "__main__":
    main()