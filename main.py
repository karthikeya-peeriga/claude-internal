import anthropic
import pandas as pd
import time
from dotenv import load_dotenv
import os
import re

# Load environment variables from the .env file
load_dotenv()

# Retrieve API key from the .env file
api_key = os.getenv("ANTHROPIC_API_KEY")
if not api_key:
    raise ValueError("API key not found. Please ensure it is set in the .env file.")

# Initialize the Anthropic client
client = anthropic.Anthropic(api_key=api_key)

# Function to generate product listing with token tracking
def generate_product_listing(product_details):
    start_time = time.time()
    
    try:
        # Create API call
        message = client.messages.create(
            model="claude-3-5-sonnet-20241022",
            max_tokens=1000,
            temperature=0,
            system="You are an expert Amazon and Ecommerce product listing copy writer and content generator for the Indian market. Focus on creating compelling, SEO-optimized content that drives conversions and provides clear product information.",
            messages=[
                {
                    "role": "user",
                    "content": f'''
Create a comprehensive Amazon product listing based on the following product details:

{product_details}

Guidelines:
1. Create a keyword-rich title (175-200 characters)
2. Generate 5 compelling bullet points highlighting key features and benefits
3. Write a product description that tells a story and addresses customer needs
4. Ensure content is optimized for the Indian e-commerce market
5. Focus on clear, simple language that explains the product's value proposition
'''
                }
            ]
        )
        
        # Calculate runtime
        end_time = time.time()
        runtime = end_time - start_time
        
        # Token usage details
        input_tokens = message.usage.input_tokens
        output_tokens = message.usage.output_tokens
        
        # Print token and runtime information
        print(f"Row Processing:")
        print(f"  Input Tokens: {input_tokens}")
        print(f"  Output Tokens: {output_tokens}")
        print(f"  Total Tokens: {input_tokens + output_tokens}")
        print(f"  API Call Runtime: {runtime:.2f} seconds\n")
        
        # Extract and return the generated content
        return {
            'content': message.content[0].text,
            'input_tokens': input_tokens,
            'output_tokens': output_tokens,
            'total_tokens': input_tokens + output_tokens
        }
    except Exception as e:
        print(f"Error generating listing: {e}")
        return None

# Function to process the CSV
def process_product_listings(input_file, output_file):
    # Overall process start time
    process_start_time = time.time()
    
    # Read the input CSV
    df = pd.read_csv(input_file)
    
    # Add new columns for generated content
    df['Generated Title'] = ''
    df['Generated Bullet Points'] = ''
    df['Generated Description'] = ''
    
    # Track total tokens
    total_input_tokens = 0
    total_output_tokens = 0
    total_tokens = 0
    
    # Process each row
    for index, row in df.iterrows():
        # Prepare product details string
        product_details = "\n".join([
            f"{col}: {row[col]}" for col in df.columns 
            if pd.notna(row[col]) and col not in ['Generated Title', 'Generated Bullet Points', 'Generated Description']
        ])
        
        # Generate listing
        generated_listing = generate_product_listing(product_details)
        
        if generated_listing:
            # Update total token tracking
            total_input_tokens += generated_listing['input_tokens']
            total_output_tokens += generated_listing['output_tokens']
            total_tokens += generated_listing['total_tokens']
            
            # Assign generated content
            content = generated_listing['content']
            
            # Extract Title (first line, limited to 200 characters)
            title_match = re.search(r'^(.{10,200})(?:\n|$)', content, re.MULTILINE)
            if title_match:
                df.at[index, 'Generated Title'] = title_match.group(1).strip()[:200]
            
            # Extract Bullet Points
            bullet_points_match = re.findall(r'•\s*([^\n]+)', content)
            if bullet_points_match:
                df.at[index, 'Generated Bullet Points'] = '\n'.join(bullet_points_match[:5])
            
            # Extract Description (everything after bullet points)
            description_match = re.search(r'(?:•\s*[^\n]+\n){5,}(.*)', content, re.DOTALL)
            if description_match:
                df.at[index, 'Generated Description'] = description_match.group(1).strip()[:1000]
    
    # Calculate total process runtime
    process_end_time = time.time()
    total_process_runtime = process_end_time - process_start_time
    
    # Print final summary
    print("\nFinal Token Usage Summary:")
    print(f"Total Input Tokens: {total_input_tokens}")
    print(f"Total Output Tokens: {total_output_tokens}")
    print(f"Total Tokens Used: {total_tokens}")
    print(f"Total Process Runtime: {total_process_runtime:.2f} seconds")
    
    # Save to output CSV
    df.to_csv(output_file, index=False, encoding='utf-8')
    print(f"\nProcessing complete. Output saved to {output_file}")

# Usage
input_file = './input.csv'
output_file = 'output_product_listings.csv'
process_product_listings(input_file, output_file)