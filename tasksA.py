import sqlite3
import subprocess
from dateutil.parser import parse
from fastapi import HTTPException
from datetime import datetime
import json
from pathlib import Path
import os
import requests
from scipy.spatial.distance import cosine
from dotenv import load_dotenv

load_dotenv()

AIPROXY_TOKEN = os.getenv('AIPROXY_TOKEN')


def A1(email="23f2001706@ds.study.iitm.ac.in"):
    
    try:
        data_dir = os.path.abspath("./data")
        
        process = subprocess.Popen(
            ["uv", "run", "https://raw.githubusercontent.com/sanand0/tools-in-data-science-public/tds-2025-01/project-1/datagen.py", email, "--root", data_dir],
            stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True
        )
        
        
        stdout, stderr = process.communicate()
        
        if process.returncode != 0:
            raise HTTPException(status_code=500, detail=f"Error: {stderr}")
        return stdout
    
    except subprocess.CalledProcessError as e:
        raise HTTPException(status_code=500, detail=f"Error: {e.stderr}")



# def A2(filename="./data/format.md"):
#     try:
#         filename = os.path.abspath(filename)
#         print(f"File path: {filename}")
        
#         # Use local prettier from node_modules
#         command = ["npx", "prettier", "--write", filename]
#         print(f"Running command: {' '.join(command)}")
        
#         process = subprocess.run(
#             command,
#             check=False,
#             stdout=subprocess.PIPE,
#             stderr=subprocess.PIPE,
#             text=True,
#             shell=False
#         )
        
#         print(f"Exit code: {process.returncode}")
#         print(f"stdout: {process.stdout}")
#         print(f"stderr: {process.stderr}")
        
#     except Exception as e:
#         print(f"Error: {e}")

# def A2(filename="./data/format.md"):
#     try:
#         filename = os.path.abspath(filename)
#         print(f"🔍 Validating file: {filename}")
        
#         if not os.path.exists(filename):
#             raise FileNotFoundError(f"File not found: {filename}")

#         # Use latest local prettier version
#         command = ["npx", "prettier", "--write", filename]
#         print(f"🚀 Executing: {' '.join(command)}")

#         process = subprocess.run(
#             command,
#             capture_output=True,
#             text=True,
#             check=True  # Raise exception on non-zero exit
#         )
        
#         print("✅ Formatting successful!")
#         print(f"📋 Output:\n{process.stdout}")
        
#     except subprocess.CalledProcessError as e:
#         print(f"❌ Formatting failed (Code {e.returncode})")
#         print(f"🔧 Error Details:\n{e.stderr}")
#     except Exception as e:
#         print(f"🚨 Unexpected error: {str(e)}")

def A2(prettier_version="prettier@3.4.2", filename="/data/format.md"):
    try:
        abs_filename = os.path.abspath(filename)
        
        print(f"📂 DEBUG: Using file path -> {abs_filename}")

        # Ensure the file exists
        if not os.path.isfile(abs_filename):
            raise FileNotFoundError(f"❌ Error: File {abs_filename} not found!")

        # Read original content
        with open(abs_filename, "r") as f:
            original_content = f.read()

        # Run Prettier with stdin (to match evaluation script)
        process = subprocess.run(
            ["npx", "prettier@3.4.2", "--stdin-filepath", abs_filename],
            input=original_content,
            capture_output=True,
            text=True,
            check=True,
            shell=True
        )

        formatted_content = process.stdout

        # Write formatted content back to the file
        with open(abs_filename, "w") as f:
            f.write(formatted_content)

        print("✅ Prettier executed successfully.")
        return True

    except FileNotFoundError as e:
        print(f"🚨 File Not Found: {e}")
    except subprocess.CalledProcessError as e:
        print(f"❌ Prettier failed:\n{e.stderr}")
    except Exception as e:
        print(f"⚠️ Unexpected error: {e}")






def A3(weekday: int, filename='data/dates.txt', targetfile='data/dates-wednesdays.txt'):
    
    input_file = '.'+os.path.abspath(filename)
    output_file = '.'+os.path.abspath(targetfile)
    weekday = weekday
    
    weekday_count = 0
    
    print("reached here")
    print(input_file)
    
    with open(input_file, 'r') as file:
        weekday_count = sum(1 for date in file if parse(date).weekday() == int(weekday)-1)
        # Ensure the file exists by touching it


    with open(output_file, 'w') as file:
        file.write(str(weekday_count))



def A4(filename="/data/contacts.json", targetfile="/data/contacts-sorted.json"):
    # Load the contacts from the JSON file
    
    filename = '.'+os.path.abspath(filename)
    targetfile = '.'+os.path.abspath(targetfile)
    
    with open(filename, 'r') as file:
        contacts = json.load(file)

    # Sort the contacts by last_name and then by first_name
    sorted_contacts = sorted(contacts, key=lambda x: (x['last_name'], x['first_name']))

    # Write the sorted contacts to the new JSON file
    with open(targetfile, 'w') as file:
        json.dump(sorted_contacts, file, indent=4)
        

def A5(log_dir_path='/data/logs', output_file_path='/data/logs-recent.txt', num_files=10):
    log_dir = Path('.' + os.path.abspath(log_dir_path))
    output_file = Path('.' + os.path.abspath(output_file_path))

    # Get list of .log files sorted by modification time (most recent first)
    log_files = sorted(log_dir.glob('*.log'), key=lambda p: p.stat().st_mtime, reverse=True)[:num_files]

    # Read first line of each file and write to the output file
    with output_file.open('w') as f_out:
        for log_file in log_files:
            with log_file.open('r') as f_in:
                first_line = f_in.readline().strip()
                f_out.write(f"{first_line}\n")

def A6(doc_dir_path='/data/docs', output_file_path='/data/docs/index.json'):
    
    docs_dir = Path('.' + os.path.abspath(doc_dir_path))
    output_file = Path('.' + os.path.abspath(output_file_path))
    
    index_data = {}

    # Walk through all files in the docs directory
    for root, _, files in os.walk(docs_dir):
        for file in files:
            if file.endswith('.md'):
                # print(file)
                file_path = os.path.join(root, file)
                # Read the file and find the first occurrence of an H1
                with open(file_path, 'r', encoding='utf-8') as f:
                    for line in f:
                        if line.startswith('# '):
                            # Extract the title text after '# '
                            title = line[2:].strip()
                            # Get the relative path without the prefix
                            relative_path = os.path.relpath(file_path, docs_dir).replace('\\', '/')
                            index_data[relative_path] = title
                            break  # Stop after the first H1
    # Write the index data to index.json
    # print(index_data)
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(index_data, f, indent=4)

def A7(filename='/data/email.txt', output_file='/data/email-sender.txt'):
    
    filename='.'+os.path.abspath(filename)
    output_file='.'+os.path.abspath(output_file)
    
    # Read the content of the email
    with open(filename, 'r') as file:
        email_content = file.readlines()

    sender_email = "sujay@gmail.com"
    for line in email_content:
        if "From" == line[:4]:
            sender_email = (line.strip().split(" ")[-1]).replace("<", "").replace(">", "")
            break

    # Get the extracted email address

    # Write the email address to the output file
    with open(output_file, 'w') as file:
        file.write(sender_email)

import base64
def png_to_base64(image_path):
    with open(image_path, "rb") as image_file:
        base64_string = base64.b64encode(image_file.read()).decode('utf-8')
    return base64_string
# def A8():
#     input_image = "data/credit_card.png"
#     output_file = "data/credit-card.txt"

#     # Step 1: Extract text using OCR
#     try:
#         image = Image.open(input_image)
#         extracted_text = pytesseract.image_to_string(image)
#         print(f"Extracted text:\n{extracted_text}")
#     except Exception as e:
#         print(f"❌ Error reading or processing {input_image}: {e}")
#         return

#     # Step 2: Pass the extracted text to the LLM to validate and extract card number
#     prompt = f"""Extract the credit card number from the following text. Respond with only the card number, without spaces:

#     {extracted_text}
#     """
#     try:
#         card_number = ask_llm(prompt).strip()
#         print(f"Card number extracted by LLM: {card_number}")
#     except Exception as e:
#         print(f"❌ Error processing with LLM: {e}")
#         return

#     # Step 3: Save the extracted card number to a text file
#     try:
#         with open(output_file, "w", encoding="utf-8") as file:
#             file.write(card_number + "\n")
#         print(f"✅ Credit card number saved to: {output_file}")
#     except Exception as e:
#         print(f"❌ Error writing {output_file}: {e}")

def A8(filename='/data/credit_card.txt', image_path='/data/credit_card.png'):
    
    
    filename='.'+os.path.abspath(filename)
    image_path='.'+os.path.abspath(image_path)
    
    # Construct the request body for the AIProxy call
    body = {
        "model": "gpt-4o-mini",
        "messages": [
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": "There is a 16 digit number in this image, with space after every 4 digit, only extract the those digits without spaces and return just the number without any other characters, i need exactly only those 16 digits."
                    },
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": f"data:image/png;base64,{png_to_base64(image_path)}"
                        }
                    }
                ]
            }
        ]
    }

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {AIPROXY_TOKEN}"
    }

    # Make the request to the AIProxy service
    response = requests.post("http://aiproxy.sanand.workers.dev/openai/v1/chat/completions",
                             headers=headers, data=json.dumps(body))
    # response.raise_for_status()

    # Extract the credit card number from the response
    result = response.json()
    # print(result); return None
    card_number = result['choices'][0]['message']['content'].replace(" ", "")

    # Write the extracted card number to the output file
    with open(filename, 'w') as file:
        file.write(card_number)
# A8()



# def get_embeddings(texts):
#     headers = {
#         "Content-Type": "application/json",
#         "Authorization": f"Bearer {AIPROXY_TOKEN}"
#     }
#     data = {
#         "model": "text-embedding-3-small",
#         "input": texts
#     }
#     response = requests.post("http://aiproxy.sanand.workers.dev/openai/v1/embeddings", headers=headers, data=json.dumps(data))
#     response.raise_for_status()
#     return [item["embedding"] for item in response.json()["data"]]

# async def A9(filename='/data/comments.txt', output_filename='/data/comments-similar.txt'):
    
#     filename = '.' + os.path.abspath(filename)
#     output_filename = '.' + os.path.abspath(output_filename)
    
#     # Read comments
#     with open(filename, 'r') as f:
#         comments = [line.strip() for line in f.readlines()]

#     # Batch the comments to reduce the number of API calls
#     batch_size = 2
#     embeddings = []
#     for i in range(0, len(comments), batch_size):
#         batch = comments[i:i + batch_size]
#         batch_embeddings = await get_embeddings(batch) # Fetch embeddings for the batch
#         embeddings.extend(batch_embeddings)

#     # Find the most similar pair
#     min_distance = float('inf')
#     most_similar = (None, None)

#     for i in range(len(comments)):
#         for j in range(i + 1, len(comments)):
#             distance = cosine(embeddings[i], embeddings[j])
#             if distance < min_distance:
#                 min_distance = distance
#                 most_similar = (comments[i], comments[j])

#     # Write the most similar pair to file
#     with open(output_filename, 'w') as f:
#         f.write(most_similar[0] + '\n')
#         f.write(most_similar[1] + '\n')

# ✅ Function to get embeddings
def get_embeddings(texts):
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {AIPROXY_TOKEN}"
    }
    data = {
        "model": "text-embedding-3-small",
        "input": texts
    }
    
    response = requests.post("https://aiproxy.sanand.workers.dev/openai/v1/embeddings", 
                             headers=headers, data=json.dumps(data))
    
    if response.status_code != 200:
        print(f"🔴 Error fetching embeddings: {response.text}")
        return None

    return [item["embedding"] for item in response.json().get("data", [])]

# ✅ Main function
async def A9(filename='/data/comments.txt', output_filename='/data/comments-similar.txt'):
    
    # Convert relative paths to absolute paths
    filename = os.path.abspath(filename)
    output_filename = os.path.abspath(output_filename)

    print(f"📂 Reading from: {filename}")
    print(f"📂 Writing to: {output_filename}")

    # ✅ Step 1: Read comments
    try:
        with open(filename, 'r') as f:
            comments = [line.strip() for line in f.readlines()]
        print(f"✅ Loaded {len(comments)} comments")
    except FileNotFoundError:
        print(f"❌ Error: File {filename} not found!")
        return

    if not comments:
        print("⚠️ No comments found in the file!")
        return

    # ✅ Step 2: Get embeddings in batches
    batch_size = 2
    embeddings = []
    for i in range(0, len(comments), batch_size):
        batch = comments[i:i + batch_size]
        batch_embeddings = get_embeddings(batch)
        
        if batch_embeddings is None:
            print("❌ Error fetching embeddings! Aborting.")
            return
        
        embeddings.extend(batch_embeddings)

    # ✅ Step 3: Find the most similar pair
    min_distance = float('inf')
    most_similar = (None, None)

    for i in range(len(comments)):
        for j in range(i + 1, len(comments)):
            distance = cosine(embeddings[i], embeddings[j])
            if distance < min_distance:
                min_distance = distance
                most_similar = (comments[i], comments[j])

    if most_similar == (None, None):
        print("⚠️ No similar comments found!")
        return

    print(f"✅ Most similar comments found: {most_similar}")

    # ✅ Step 4: Write the most similar comments to file
    try:
        with open(output_filename, 'w') as f:
            f.write(most_similar[0] + '\n')
            f.write(most_similar[1] + '\n')

        print(f"✅ Successfully written to: {output_filename}")

        # ✅ Step 5: Verify the file exists after writing
        if os.path.exists(output_filename):
            print(f"🎉 File successfully created: {output_filename}")
        else:
            print("🚨 File was not created for some reason!")
    except Exception as e:
        print(f"❌ Error writing file: {e}")

def A10(filename='data/ticket-sales.db', output_filename='data/ticket-sales-gold.txt', query="SELECT SUM(units * price) FROM tickets WHERE type = 'Gold'"):
    # Connect to the SQLite database
    filename='.'+os.path.abspath(filename)
    output_filename='.'+os.path.abspath(output_filename)
    conn = sqlite3.connect(filename)
    print("Connected to SQLite")
    cursor = conn.cursor()

    # Calculate the total sales for the "Gold" ticket type
    cursor.execute(query)
    total_sales = cursor.fetchone()[0]

    # If there are no sales, set total_sales to 0
    total_sales = total_sales if total_sales else 0

    # Write the total sales to the file
    with open(output_filename, 'w') as file:
        file.write(str(total_sales))

    # Close the database connection
    conn.close()