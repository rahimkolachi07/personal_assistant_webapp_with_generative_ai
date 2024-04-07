import asyncio
import websockets
from gemini.gemini import g_model
from gemini.geminivision import*
import requests
import io
from PIL import Image
import time
import re
import csv
import pandas as pd
import os

def extract_text_after_string(filename, string):
    try:
        index = filename.index(string)
        return filename[index + len(string):].strip()
    except ValueError:
        print(f"'{string}' not found in the filename.")
        return None


def rename_files(directory, old_name, new_name):
    try:
        old_file_path = os.path.join(directory, old_name)
        new_file_path = os.path.join(directory, new_name)
        
        if os.path.exists(old_file_path):
            os.rename(old_file_path, new_file_path)
            print(f"File '{old_name}' renamed to '{new_name}' successfully.")
        else:
            print(f"File '{old_name}' not found in the directory '{directory}'.")
    except PermissionError:
        print(f"Permission denied to rename file '{old_name}'.")
    except Exception as e:
        print(f"An error occurred: {str(e)}")

def delete_file(file_path):
    try:
        os.remove(file_path)
        print(f"File '{file_path}' deleted successfully.")
    except FileNotFoundError:
        print(f"File '{file_path}' not found.")
    except PermissionError:
        print(f"Permission denied to delete file '{file_path}'.")
    except Exception as e:
        print(f"An error occurred: {str(e)}")



def create_file_list_csv(folder_path):
    # Get list of files in the folder
    file_list = os.listdir(folder_path)
    
    # Remove the CSV file itself if it exists in the list
    if 'file_list.csv' in file_list:
        file_list.remove('file_list.csv')
    
    # Write the file list to a CSV file
    with open(os.path.join(folder_path, 'file_list.csv'), 'w', newline='') as csvfile:
        csv_writer = csv.writer(csvfile)
        for file_name in file_list:
            csv_writer.writerow([file_name])

def query(payload,API_URL,headers):
    response = requests.post(API_URL, headers=headers, json=payload)
    return response.content
def image_gen(prompts,user):
    unique_number = int(time.time())
    path=f"{user}/data/image{unique_number}.png"

    try:
        API_URL = "https://api-inference.huggingface.co/models/EK12317/Ekmix-Diffusion"
        headers = {"Authorization": "Bearer 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"}

        image_bytes = query({"inputs": f"{prompts}",},API_URL,headers)
        # Attempt to open the image
        image = Image.open(io.BytesIO(image_bytes))
        # Display or process the image as needed
        image.save(path)
        print("part one")
    except:
        try:
            API_URL = "https://api-inference.huggingface.co/models/stabilityai/stable-diffusion-2-1"
            headers = {"Authorization": "Bearer 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"}
            image_bytes = query({"inputs": f"{prompts}",},API_URL,headers)
            # Attempt to open the image
            image = Image.open(io.BytesIO(image_bytes))
            # Display or process the image as needed
            image.save(path)
            print("part two")
        except:

            API_URL = "https://api-inference.huggingface.co/models/sayakpaul/diffusion-sdxl-orpo"
            headers = {"Authorization": "Bearer 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"}
            image_bytes = query({"inputs": f"{prompts}",},API_URL,headers)
            # Attempt to open the image
            image = Image.open(io.BytesIO(image_bytes))
            
        
            # Display or process the image as needed
            image.save(path)
            print("part third")


    return f"your file name is = image{unique_number}.png"

import pandas as pd
import os

def append_to_csv(user,text):
    # Create DataFrame with a single column 'Text'
    df = pd.DataFrame({'Text': [text]})
    # Append DataFrame to the CSV file
    df.to_csv(f'{user}/data/conversation.csv', mode='a', index=False, header=False)
    txt=read_csv(user)
    return txt


def read_csv(user):
    if not os.path.exists(f'{user}/data/conversation.csv'):
        print("CSV file not found. Creating a new file.")
        # If CSV file doesn't exist, return an empty list
        return []
    # Read CSV file into a DataFrame
    df = pd.read_csv(f'{user}/data/conversation.csv')
    # Extract 'Text' column and convert it to a list
    return df

def extract_file_name(text):
    # Define a regex pattern to match file names with common extensions
    pattern = r'\b\w+\.(?:png|jpg|jpeg|gif|mp4|mp3|wav|txt|pdf|doc|docx|xls|xlsx|ppt|pptx|csv)\b'

    
    # Use findall to search for all occurrences of file names in the text
    file_names = re.findall(pattern, text)
    
    # Return the list of file names found
    return file_names

