import os
import json
from datetime import datetime
from flask import Flask, request, jsonify, render_template
import anthropic

app = Flask(__name__)

# Ensure the uploads directory exists
UPLOAD_FOLDER = 'product_submissions'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Initialize Anthropic client
client = anthropic.Anthropic(
    api_key=os.getenv('ANTHROPIC_API_KEY', 'your-api-key-here')  # Use environment variable
)

@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')

@app.route('/submit_products', methods=['POST'])
def submit_products():
    try:
        # Get form data
        brand_names = request.form.getlist('brand_name[]')
        categories = request.form.getlist('category[]')
        sub_categories = request.form.getlist('sub_category[]')
        descriptions = request.form.getlist('brief_product_description[]')
        ean_numbers = request.form.getlist('ean_number[]')
        model_numbers = request.form.getlist('model_number[]')
        colors = request.form.getlist('color[]')
        materials = request.form.getlist('material[]')
        sizes = request.form.getlist('size[]')
        keywords = request.form.getlist('keywords[]')

        # Prepare product list and Claude API responses
        products = []
        claude_responses = []

        for i in range(len(brand_names)):
            # Prepare key attributes
            key_attributes = []
            for j in range(1, 6):
                attr_value = request.form.get(f'key_attribute_{j}[]', '')[i] if i < len(request.form.get(f'key_attribute_{j}[]', '')) else ''
                if attr_value:
                    key_attributes.append(attr_value)

            # Construct product dictionary
            product = {
                "brand_name": brand_names[i],
                "category": categories[i],
                "sub_category": sub_categories[i],
                "description": descriptions[i],
                "ean_number": ean_numbers[i],
                "model_number": model_numbers[i],
                "color": colors[i],
                "material": materials[i],
                "size": sizes[i],
                "keywords": keywords[i].split(',') if keywords[i] else [],
                "key_attributes": key_attributes
            }
            products.append(product)

            # Prepare Claude API call content
            message_content = f''' 
Create an Amazon Detailed Page content for the product below, using the following structured format:

|||Title: [Detailed SEO-Optimized Product Title Goes Here]|||
|||Description: [Comprehensive Product Description]|||
|||Bullets: [Bullet1 =|= Bullet2 =|= Bullet3 =|= Bullet4 =|= Bullet5]|||

Product Details:
Product Name: {descriptions[i]}
Brand: {brand_names[i]}
Category: {categories[i]}
Sub-Category: {sub_categories[i]}
Model Number: {model_numbers[i]}
Color: {colors[i]}
Material: {materials[i]}
Size: {sizes[i]}
Key Features:
1. {key_attributes[0] if len(key_attributes) > 0 else 'No details'}
2. {key_attributes[1] if len(key_attributes) > 1 else 'No details'}
3. {key_attributes[2] if len(key_attributes) > 2 else 'No details'}
4. {key_attributes[3] if len(key_attributes) > 3 else 'No details'}
5. {key_attributes[4] if len(key_attributes) > 4 else 'No details'}

Keywords: {keywords[i]}

[Rest of the previous prompt content remains the same...]
'''
            
            # Make Claude API call
            try:
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
                
                # Parse the response
                response_text = str(message.content[0].text)
                
                # Extract sections
                sections = response_text.split("|||")
                parsed_response = {
                    "title": "",
                    "description": "",
                    "bullets": []
                }
                
                for section in sections:
                    if section.startswith("Title:"):
                        parsed_response["title"] = section.replace("Title:", "").strip()
                    elif section.startswith("Description:"):
                        parsed_response["description"] = section.replace("Description:", "").strip()
                    elif section.startswith("Bullets:"):
                        parsed_response["bullets"] = [
                            bullet.strip() for bullet in 
                            section.replace("Bullets:", "").strip().split("=|=")
                        ]
                
                claude_responses.append({
                    "product": product,
                    "claude_output": parsed_response
                })
            
            except Exception as api_error:
                claude_responses.append({
                    "product": product,
                    "claude_output": {"error": str(api_error)}
                })

        # Generate unique filename with timestamp
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = os.path.join(UPLOAD_FOLDER, f'products_{timestamp}.json')

        # Write to JSON file
        with open(filename, 'w') as f:
            json.dump(products, f, indent=4)

        # Render results page with Claude API responses
        return render_template('results.html', responses=claude_responses)

    except Exception as e:
        return jsonify({
            "status": "error", 
            "message": str(e)
        }), 500

if __name__ == '__main__':
    app.run(debug=True)