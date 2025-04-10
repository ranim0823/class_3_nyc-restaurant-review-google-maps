import json
from collections import defaultdict

def extract_primary_types(input_file, output_file=None):
    """
    Extract all unique primary_type values from a JSON file of restaurant data.
    
    Args:
        input_file (str): Path to the input JSON file
        output_file (str, optional): Path to save the list of primary types. 
                                   If None, prints to console.
    """
    try:
        # Load the JSON data
        with open(input_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        # Extract all primary_type values
        primary_types = set()
        type_counts = defaultdict(int)
        
        for restaurant in data:
            primary_type = restaurant.get('primary_type')
            if primary_type:
                primary_types.add(primary_type)
                type_counts[primary_type] += 1
        
        # Convert to sorted list
        sorted_types = sorted(primary_types)
        
        # Create a report
        report = {
            "total_restaurants": len(data),
            "unique_primary_types": len(sorted_types),
            "primary_types": sorted_types,
            "type_counts": {k: v for k, v in sorted(type_counts.items(), key=lambda item: item[1], reverse=True)}
        }
        
        # Output results
        if output_file:
            with open(output_file, 'w', encoding='utf-8') as f:
                json.dump(report, f, indent=2)
            print(f"Successfully saved primary types to {output_file}")
        else:
            print("Unique Primary Types:")
            for i, pt in enumerate(sorted_types, 1):
                print(f"{i}. {pt} (count: {type_counts[pt]})")
            
            print(f"\nTotal restaurants: {len(data)}")
            print(f"Unique primary types: {len(sorted_types)}")
        
        return sorted_types
        
    except Exception as e:
        print(f"Error processing file: {e}")
        return None

# Example usage
if __name__ == "__main__":
    input_json = "nyc-restaurant-review-google-maps/restaurants.json"
    output_json = "primary_types_report.json"
    
    # Extract and display primary types
    primary_types = extract_primary_types(input_json, output_json)
    
    # Optional: Print just the list of types for copying
    if primary_types:
        print("\nList of primary types:")
        print(json.dumps(primary_types, indent=2))


import json
from collections import defaultdict

def extract_unique_restaurants(input_file, output_file=None):
    """
    Process restaurant data to:
    1. Remove review texts
    2. Keep only unique entries (based on google_place_id)
    3. Focus on types ending with "_restaurant"
    
    Args:
        input_file (str): Path to the input JSON file
        output_file (str, optional): Path to save the cleaned data.
                                   If None, prints summary to console.
    
    Returns:
        dict: Processed restaurant data with unique entries
    """
    try:
        # Load the JSON data
        with open(input_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        # Track unique restaurants and types
        unique_restaurants = {}
        restaurant_types = set()
        type_counts = defaultdict(int)
        
        for restaurant in data:
            primary_type = restaurant.get('primary_type')
            place_id = restaurant.get('google_place_id')
            
            # Only process if it's a restaurant type and has a place ID
            if primary_type and primary_type.endswith('_restaurant') and place_id:
                # Create or update restaurant entry
                if place_id not in unique_restaurants:
                    unique_restaurants[place_id] = {
                        'google_place_id': place_id,
                        'name': restaurant.get('name'),
                        'primary_type': primary_type,
                        'overall_rating': restaurant.get('overall_rating'),
                        'user_rating_count': restaurant.get('user_rating_count'),
                        'price_level': restaurant.get('price_level'),
                        'latitude': restaurant.get('latitude'),
                        'longitude': restaurant.get('longitude'),
                        'generative_summary': restaurant.get('generative_summary'),
                        'serves_veg_food': restaurant.get('serves_veg_food')
                    }
                
                # Track types
                restaurant_types.add(primary_type)
                type_counts[primary_type] += 1
        
        # Convert to list and sort by name
        unique_list = sorted(unique_restaurants.values(), key=lambda x: x.get('name', ''))
        
        # Prepare results
        result = {
            "total_original_entries": len(data),
            "total_unique_restaurants": len(unique_list),
            "unique_restaurant_types": {
                "count": len(restaurant_types),
                "types": sorted(restaurant_types),
                "type_counts": dict(sorted(type_counts.items(), key=lambda item: item[1], reverse=True))
            },
            "restaurants": unique_list
        }
        
        # Output results
        if output_file:
            with open(output_file, 'w', encoding='utf-8') as f:
                json.dump(result, f, indent=2)
            print(f"Successfully saved {len(unique_list)} unique restaurants to {output_file}")
        else:
            print("\n=== RESTAURANT DATA PROCESSING RESULTS ===")
            print(f"Original entries: {len(data)}")
            print(f"Unique restaurants: {len(unique_list)}")
            print(f"Unique restaurant types: {len(restaurant_types)}")
            
            print("\nMost common restaurant types:")
            for i, (type_, count) in enumerate(sorted(type_counts.items(), key=lambda item: item[1], reverse=True)[:10], 1):
                print(f"{i}. {type_} (count: {count})")
        
        return result
        
    except Exception as e:
        print(f"Error processing file: {e}")
        return None

# Example usage
if __name__ == "__main__":
    input_json = "nyc-restaurant-review-google-maps/restaurants.json"
    output_json = "nyc-restaurant-review-google-maps/restaurants_wo_reviews.json"
    
    # Process the data
    cleaned_data = extract_unique_restaurants(input_json, output_json)
    
    # Optional: Print the first few entries as a sample
    if cleaned_data and 'restaurants' in cleaned_data:
        print("\nSample of processed restaurant data:")
        print(json.dumps(cleaned_data['restaurants'][:3], indent=2))