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