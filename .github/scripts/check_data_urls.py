import json
import requests
import sys
import os
from urllib.parse import urlparse
from concurrent.futures import ThreadPoolExecutor, as_completed

def check_url(entry, category):
    """Check if a URL is accessible"""
    name = entry['name']
    url = entry['url']
    
    # Skip GitHub URLs as they're less likely to go down and may have rate limiting
    if 'github.com' in url:
        print(f"🔧 Skipping {name} (GitHub repository): {url}")
        return entry, True
    
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        
        response = requests.get(
            url, 
            headers=headers, 
            timeout=15,
            allow_redirects=True
        )
        
        # Consider 2xx and 3xx status codes as working
        if response.status_code < 400:
            print(f"✅ [{category}] {name} is working: {url}")
            return entry, True
        else:
            print(f"❌ [{category}] {name} returned status {response.status_code}: {url}")
            return entry, False
            
    except requests.exceptions.RequestException as e:
        print(f"❌ [{category}] {name} failed with error: {e}")
        return entry, False

def check_category(category_name, entries):
    """Check all URLs in a category"""
    print(f"\n🔍 Checking {category_name}...")
    working_entries = []
    
    with ThreadPoolExecutor(max_workers=8) as executor:
        future_to_entry = {
            executor.submit(check_url, entry, category_name): entry 
            for entry in entries
        }
        
        for future in as_completed(future_to_entry):
            entry, is_working = future.result()
            if is_working:
                working_entries.append(entry)
    
    return working_entries

def main():
    # Read the current data.json file
    with open('data.json', 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    print("Starting URL health check for data.json...")
    
    # Track original counts
    original_counts = {category: len(entries) for category, entries in data.items()}
    
    # Check URLs in each category
    updated_data = {}
    removed_count = 0
    
    for category, entries in data.items():
        working_entries = check_category(category, entries)
        updated_data[category] = working_entries
        removed_count += (len(entries) - len(working_entries))
    
    # Print summary
    print(f"\n📊 Summary:")
    for category in data.keys():
        original = original_counts[category]
        updated = len(updated_data[category])
        print(f"  {category}: {updated}/{original} working")
    
    print(f"  Total removed: {removed_count}")
    
    # Write the updated data back to the file
    with open('data.json', 'w', encoding='utf-8') as f:
        json.dump(updated_data, f, indent=4, ensure_ascii=False)
    
    # Set exit code based on whether changes were made
    if removed_count > 0:
        print("Changes detected - file will be updated")
        sys.exit(0)  # Success with changes
    else:
        print("No changes needed")
        sys.exit(0)  # Success without changes

if __name__ == "__main__":
    main()
