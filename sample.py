import anthropic
import csv

# Initialize the client
client = anthropic.Anthropic(
    api_key="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"
)

# Path to your CSV file
input_file = "input.csv"

# Read the CSV file
with open(input_file, mode='r', encoding='utf-8') as file:
    csv_reader = csv.DictReader(file)  # Using DictReader for column-based access
    for row in csv_reader:
        # Extract data from the row (assuming relevant fields are present)
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
Create an Amazon Detailed Page content for the product below: 

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

General Guidelines for content generation:
1. Use Simple English (High school level)
2. Title should be at least 175 characters but not exceed 200 characters. Utilize maximum length. Load the title with keywords (provided + use SEO logic to come up with relevant keywords). The first 100 characters of the title should inform the customer completely about the product. Use separator "--" without space between different sections of the title.

3. Total 5 bullet points. Each bullet point should:
   - Have a capitalized summary / punch line
   - Be keyword rich
   - Discuss the feature and how it solves a specific problem
   - Provide real-life applications and benefits
   - Illustrate how the feature can be used in different scenarios (e.g., home, office, specific user types)
   - Relate the feature to everyday situations to make it more relatable
   Sequence the bullet points based on customer requirements and to boost conversion rate.

4. Product description should:
   - Be 600-1000 characters long
   - Talk about the Brand and its specialties
   - Highlight the product's uniqueness
   - Include as many keyword phrases as possible with logic
   - Provide context on how the product fits into users' daily lives
   - Illustrate potential use cases and scenarios
   - Address common pain points and how the product solves them
   - Paint a picture of the improved lifestyle or work environment with the product

5. Use high relevant search keywords for the Indian market (Amazon + Google).

6. When describing features, always tie them to benefits and real-world applications to help customers understand the value proposition.

7. Consider different user personas (e.g., homeowners, business owners, tech enthusiasts) and address their specific needs throughout the listing.

8. Use storytelling elements in the product description to help customers envision themselves using the product.
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

        # Print or save the response
        print(f"Response for {product_name}:")
        print(message.content)
        print("\n" + "="*50 + "\n")
