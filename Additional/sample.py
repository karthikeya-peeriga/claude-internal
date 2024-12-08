import anthropic
import csv
import json

# Initialize the client
client = anthropic.Anthropic(
    api_key="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"
)

# Path to your CSV file and output file
input_file = "input.csv"
output_file = "output.json"  # Use JSON for structured data storage

# List to store all outputs
all_responses = []





# Read the CSV file
with open(input_file, mode='r', encoding='utf-8') as file:
    csv_reader = csv.DictReader(file)
    for row in csv_reader:
        # Extract data from the row
        product_name = row.get("Brief Product Descirption", "Unknown Product")
        brand = row.get("Brand Name", "Unknown Brand")
        category = row.get("Category", "Unknown Category")
        sub_category = row.get("Sub-Category", "Unknown Sub-Category")
        model_number = row.get("Model Number", "Unknown Model")
        color = row.get("Color", "Unknown Color")
        material = row.get("Material", "Unknown Material")
        size = row.get("Size (If applicable)", "N/A")
        key_attr_1 = row.get("Key Attribute 1", "No details")
        key_attr_2 = row.get("Key Attribute 2", "No details")
        key_attr_3 = row.get("Key Attribute 3", "No details")
        key_attr_4 = row.get("Key Attribute 4", "No details")
        key_attr_5 = row.get("Key Attribute 5", "No details")
        keywords = row.get("Keywords", "")
        
        # Construct the message content dynamically
        message_content = f''' 

Create an Amazon Detailed Page content for the product below, using the following structured format:

|||Title: [Detailed SEO-Optimized Product Title Goes Here]|||
|||Description: [Comprehensive Product Description]|||
|||Bullets: [Bullet1 =|= Bullet2 =|= Bullet3 =|= Bullet4 =|= Bullet5]|||

Product Details:
Product Name: {product_name}
Brand: {brand}
Category: {category}
Sub-Category: {sub_category}
Model Number: {model_number}
Color: {color}
Material: {material}
Size: {size}
Key Features:
1. {key_attr_1}
2. {key_attr_2}
3. {key_attr_3}
4. {key_attr_4}
5. {key_attr_5}

Keywords: {keywords}

Detailed Content Generation Guidelines:

1. Title Guidelines:
   - Length: Minimum 175 characters, maximum 200 characters
   - Utilize the full allowed length
   - Load the title with keywords (provided + SEO-relevant keywords)
   - First 100 characters should completely inform the customer about the product
   - Use "--" as a separator between different sections of the title without spaces

2. Bullet Points Requirements:
   - Create exactly 5 bullet points
   - Each bullet point must:
     a) Start with a capitalized summary/punch line
     b) Be keyword-rich
     c) Explain the feature and its problem-solving capability
     d) Provide real-life applications and benefits
     e) Illustrate usage in different scenarios (home, office, specific user types)
     f) Relate features to everyday situations to increase relatability
   - Sequence bullet points to optimize conversion rate and address customer requirements
   - Format the 5 bullet points to be separated by " =|= " when outputting

3. Product Description Specifications:
   - Length: 600-1000 characters
   - Include:
     a) Brand background and specialties
     b) Product's unique selling points
     c) Maximum keyword phrase integration
     d) Context of product in daily life
     e) Potential use cases and scenarios
     f) Solutions to common pain points
     g) Vision of improved lifestyle/work environment with the product

4. Keyword and Market Considerations:
   - Focus on high-relevance search keywords for the Indian market
   - Optimize for both Amazon and Google search

5. Feature Description Approach:
   - Always connect features to tangible benefits
   - Provide real-world application context
   - Help customers understand the value proposition

6. User Persona Targeting:
   - Consider diverse user groups (homeowners, business owners, tech enthusiasts)
   - Address specific needs of different customer segments

7. Storytelling Technique:
   - Use narrative elements in the product description
   - Help customers visualize themselves using the product

IMPORTANT INSTRUCTIONS:
- Use Simple English (High school level comprehension)
- Strictly maintain the |||Label: Content||| format
- Bullets should be formatted as: Bullet1 =|= Bullet2 =|= Bullet3 =|= Bullet4 =|= Bullet5
- Do not use "|||" or "=|=" elsewhere in the content
- Ensure each section is clear, compelling, and informative
- Prioritize clarity, benefit communication, and customer engagement

'''

        # Make the API call
        message = client.messages.create(
            model="claude-3-5-sonnet-20241022",
            max_tokens=1000,
            temperature=0,
            system=(
                "You are an expert Amazon and Ecommerce product listing copy writer and content generator. "
                "You have expert knowledge on consumer behaviour and understand how the copy and content flow and storytelling "
                "affect Indian consumer behavior. Your objective is to ensure better shopping experiences by providing accurate, "
                "tailor-made details for each product type, increasing conversion rates, and boosting organic visibility using SEO."
            ),
            messages=[
                {
                    "role": "user",
                    "content": message_content
                }
            ]
        )

        # Append the response to the list
        all_responses.append({
            "product_name": product_name,
            "response": str(message.content)
        })

# Save all responses to a JSON file
with open(output_file, mode='w', encoding='utf-8') as file:
    json.dump(all_responses, file, indent=4, ensure_ascii=False)

#Rewrie Ouput file
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
output_file = "./Parsed.json"  # Replace with the desired output file path

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





print(f"All responses have been saved to {output_file}")
