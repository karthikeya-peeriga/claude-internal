import json

# Function to parse the response field
def parse_response_field(response_text):
    # Split by "|||" to separate the sections
    sections = response_text.split("|||")
    data = {"Title": None, "Description": None, "Bullets": [], "Keywords": []}

    for section in sections:
        if section.startswith("Title:"):
            data["Title"] = section.replace("Title:", "").strip()
        elif section.startswith("Description:"):
            data["Description"] = section.replace("Description:", "").strip()
        elif section.startswith("Bullets:"):
            bullets = section.replace("Bullets:", "").strip()
            # Split bullets by " =|= " to create a list
            data["Bullets"] = [bullet.strip() for bullet in bullets.split("=|=")]
    
    # Generate keywords from Title and Description (basic approach: split by spaces and deduplicate)
    if data["Title"]:
        title_keywords = data["Title"].split()
    else:
        title_keywords = []

    if data["Description"]:
        description_keywords = data["Description"].split()
    else:
        description_keywords = []

    # Combine and deduplicate keywords
    data["Keywords"] = list(set(title_keywords + description_keywords))
    
    return data

# Load the input JSON file
input_file = "./output.json"  # Replace with the path to your input file
output_file = "output-parsed.json"  # Replace with the desired output file path

with open(input_file, "r") as infile:
    input_data = json.load(infile)

# Process the data
output_data = []
for item in input_data:
    product_name = item.get("product_name")
    response = item.get("response", "")
    # Extract the response text (if it's wrapped in a TextBlock structure)
    if "text=" in response:
        response = response.split('text="', 1)[-1].rsplit('",', 1)[0]
    parsed_data = parse_response_field(response)
    output_data.append({
        "Product Name": product_name,
        "Title": parsed_data["Title"],
        "Description": parsed_data["Description"],
        "Bullets": parsed_data["Bullets"],
        "Keywords": parsed_data["Keywords"]
    })

# Save the processed data to an output JSON file
with open(output_file, "w") as outfile:
    json.dump(output_data, outfile, indent=4)

print(f"Processed data saved to {output_file}")
