import json

# Load missing_data.json
with open("missing_data.json", "r", encoding="utf-8") as file1:
    data1 = json.load(file1)

# Load utd_d.json
with open("utd_data.json", "r", encoding="utf-8") as file2:
    data2 = json.load(file2)

# Merge the two lists (assuming both files contain lists of dictionaries)
merged_data = data1 + data2  # Combine lists

# Remove duplicates if needed (based on URL)
unique_data = {item["url"]: item for item in merged_data}.values()

# Save the merged file
with open("merged_data.json", "w", encoding="utf-8") as output:
    json.dump(list(unique_data), output, indent=4)

print("Merging complete. Saved as merged_data.json")