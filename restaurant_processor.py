import json
from collections import defaultdict

# Define food-and-drink-related keywords
FOOD_AND_DRINK_KEYWORDS = [
    "restaurant", "bar", "cafe", "shop", "diner", "bakery", "pub", "grill",
    "deli", "buffet", "brunch", "breakfast", "fine_dining", "steak", "sandwich",
    "pizza", "sushi", "seafood", "coffee", "tea", "ice_cream", "juice", "confectionery", 
    "food", "meal", "acai", "butcher", "cafeteria", "catering", "chocolate", 
    "convenience", "dessert", "donut", "wine", "bagel", "candy"
]

# Define explicitly non-food-and-drink-related types
NON_FOOD_AND_DRINK_TYPES = [
    "gift_shop", "butcher_shop", "grocery_store", "food_store", 
    "shopping_mall", "convenience_store", "public_bath", "bed_and_breakfast",
    "barber_shop"  # Added barber_shop to the list of non-food-related types
]

# Exclude specific types from "types"
EXCLUDED_TYPES = {"food", "restaurant"}

def is_food_related(value):
    """
    Check if a primary type or type is food-and-drink related based on keywords.
    """
    if value in NON_FOOD_AND_DRINK_TYPES or value in EXCLUDED_TYPES:
        return False
    return any(keyword in value for keyword in FOOD_AND_DRINK_KEYWORDS)


def summarize_and_filter_restaurant_data(input_file, summary_output_file, filtered_output_file):
    """
    Summarize and filter the restaurant dataset.

    Args:
        input_file (str): Path to the input JSON file.
        summary_output_file (str): Path to save the summary JSON file.
        filtered_output_file (str): Path to save the filtered dataset JSON file.

    Returns:
        None
    """
    try:
        # Load the JSON data
        with open(input_file, 'r', encoding='utf-8') as f:
            data = json.load(f)

        # Initialize data structures
        unique_restaurants = {}
        primary_type_counts = defaultdict(set)
        type_counts = defaultdict(set)
        primary_type_type_counts = defaultdict(lambda: defaultdict(set))
        unique_primary_types = set()
        unique_types = set()

        # Process each restaurant entry
        for restaurant in data:
            place_id = restaurant.get('google_place_id')
            primary_type = restaurant.get('primary_type')
            types = restaurant.get('types')

            if place_id:
                # Remove "review_text" if it exists
                if "review_text" in restaurant:
                    del restaurant["review_text"]

                # Add unique restaurants
                if place_id not in unique_restaurants:
                    unique_restaurants[place_id] = restaurant

                # Count primary types
                if primary_type and is_food_related(primary_type):
                    primary_type_counts[primary_type].add(place_id)
                    unique_primary_types.add(primary_type)

                # Process types
                if types:
                    if isinstance(types, list):
                        filtered_types = [t for t in types if is_food_related(t)]
                    elif isinstance(types, str):
                        try:
                            parsed_types = json.loads(types.replace("'", '"'))
                            filtered_types = [t for t in parsed_types if is_food_related(t)]
                        except json.JSONDecodeError:
                            print(f"Failed to parse types for restaurant: {place_id}")
                            filtered_types = []
                    else:
                        filtered_types = []

                    restaurant["types"] = filtered_types  # Update the restaurant's types

                    for t in filtered_types:
                        type_counts[t].add(place_id)
                        unique_types.add(t)

                        # Count combinations of food-related primary type and type
                        if primary_type and is_food_related(primary_type) and is_food_related(t):
                            primary_type_type_counts[primary_type][t].add(place_id)

        # Extract food-and-drink-related and non-food-related primary types and types
        food_related_primary_types = {pt for pt in unique_primary_types if is_food_related(pt)}
        food_related_types = {t for t in unique_types if is_food_related(t)}

        # Prepare summary
        summary = {
            "unique_restaurant_count": len(unique_restaurants),
            "primary_types": {
                "food_related": {
                    pt: len(primary_type_counts[pt]) for pt in food_related_primary_types
                }
            },
            "types": {
                "food_related": {
                    t: len(type_counts[t]) for t in food_related_types
                }
            },
            "primary_type_type_combinations": {
                primary: {t: len(ids) for t, ids in types.items()}
                for primary, types in primary_type_type_counts.items()
            }
        }

        # Save the summary to a JSON file
        with open(summary_output_file, 'w', encoding='utf-8') as f:
            json.dump(summary, f, indent=2)
        print(f"Summary saved to {summary_output_file}")

        # Filter the dataset to include only food-and-drink-related primary types
        filtered_restaurants = [
            restaurant for restaurant in unique_restaurants.values()
            if is_food_related(restaurant.get('primary_type', ''))
        ]

        # Save the filtered dataset to a JSON file
        with open(filtered_output_file, 'w', encoding='utf-8') as f:
            json.dump(filtered_restaurants, f, indent=2)
        print(f"Filtered dataset saved to {filtered_output_file}")

    except Exception as e:
        print(f"Error processing file: {e}")


def extract_unique_food_related_types(input_file, output_file):
    """
    Extract a list of all unique primary_type and types related to food and drink combined.

    Args:
        input_file (str): Path to the input JSON file.
        output_file (str): Path to save the list of unique types.

    Returns:
        None
    """
    try:
        # Load the JSON data
        with open(input_file, 'r', encoding='utf-8') as f:
            data = json.load(f)

        # Initialize a set to store unique types
        unique_food_related_types = set()

        # Process each restaurant entry
        for restaurant in data:
            # Add primary_type to the set if it's food-related
            primary_type = restaurant.get('primary_type')
            if primary_type and is_food_related(primary_type):
                unique_food_related_types.add(primary_type)

            # Add types to the set if they're food-related
            types = restaurant.get('types')
            if types:
                if isinstance(types, list):
                    unique_food_related_types.update([t for t in types if is_food_related(t)])
                elif isinstance(types, str):
                    try:
                        parsed_types = json.loads(types.replace("'", '"'))
                        unique_food_related_types.update([t for t in parsed_types if is_food_related(t)])
                    except json.JSONDecodeError:
                        print(f"Failed to parse types for restaurant: {restaurant.get('google_place_id')}")

        # Convert the set to a sorted list
        unique_food_related_types_list = sorted(unique_food_related_types)

        # Save the list to a JSON file
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(unique_food_related_types_list, f, indent=2)
        print(f"Unique food-related types saved to {output_file}")

    except Exception as e:
        print(f"Error processing file: {e}")


# Example usage
if __name__ == "__main__":
    input_json = "/Users/ranmei/Documents/GitHub/class_3_nyc-restaurant-review-google-maps/restaurants.json"  # Replace with your input JSON file
    summary_output_json = "/Users/ranmei/Documents/GitHub/class_3_nyc-restaurant-review-google-maps/restaurant_summary.json"  # Replace with your summary JSON file
    filtered_output_json = "/Users/ranmei/Documents/GitHub/class_3_nyc-restaurant-review-google-maps/filtered_restaurants.json"  # Replace with your filtered JSON file
    unique_food_related_types_output_json = "/Users/ranmei/Documents/GitHub/class_3_nyc-restaurant-review-google-maps/unique_food_related_types.json"  # Replace with your unique types JSON file

    # Summarize and filter the dataset
    summarize_and_filter_restaurant_data(input_json, summary_output_json, filtered_output_json)

    # Extract unique food-related types
    extract_unique_food_related_types(input_json, unique_food_related_types_output_json)