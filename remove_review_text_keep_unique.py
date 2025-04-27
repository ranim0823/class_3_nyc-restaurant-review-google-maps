import json
from collections import Counter

# Load the dataset
def load_data(file_path):
    with open(file_path, 'r') as file:
        return json.load(file)

# Remove "review_text" from each restaurant
def remove_review_text(data):
    for restaurant in data:
        if "review_text" in restaurant:
            del restaurant["review_text"]
    return data

# Keep only unique restaurants by "google_place_id"
def get_unique_restaurants(data):
    unique_restaurants = {}
    for restaurant in data:
        unique_restaurants[restaurant["google_place_id"]] = restaurant
    return list(unique_restaurants.values())

# Save the processed data to a new file
def save_data(data, file_path):
    with open(file_path, 'w') as file:
        json.dump(data, file, indent=4)

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

# Main function
def main():
    input_file = "/Users/ranmei/Documents/GitHub/class_3_nyc-restaurant-review-google-maps/restaurants.json"  # Replace with your input file path
    output_file = "/Users/ranmei/Documents/GitHub/class_3_nyc-restaurant-review-google-maps/restaurants_unique.json"  # Replace with your output file path

    # Load the dataset
    data = load_data(input_file)

    # Step 1: Remove "review_text"
    data = remove_review_text(data)

    # Step 2: Keep only unique restaurants by "google_place_id"
    unique_restaurants = get_unique_restaurants(data)

    # Print the total number of unique restaurants
    print(f"Total unique restaurants: {len(unique_restaurants)}")

    # Save the processed data
    save_data(unique_restaurants, output_file)
    print(f"\nProcessed data saved to {output_file}")

    # Step 3: Rank primary types
    primary_type_ranking = rank_primary_types(unique_restaurants)
    print("Ranked Primary Types:")
    for rank, (primary_type, count) in enumerate(primary_type_ranking, start=1):
        print(f"{rank}. {primary_type}: {count}")

     # Step 4: Get a ranked list of all unique values under "types"
    types_ranking = rank_types(unique_restaurants)
    print("\nRanked Types:")
    for rank, (type_value, count) in enumerate(types_ranking, start=1):
        print(f"{rank}. {type_value}: {count}")

if __name__ == "__main__":
    main()



