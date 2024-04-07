import os
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
from main import *

async def save_file(websocket, path):
    try:
        # Receive the file name from the client
        file_name = await websocket.recv()
        file_path = os.path.join(path, file_name)

        # Receive and save the file data from the client
        with open(file_path, "wb") as file:
            while True:
                data = await websocket.recv()
                if data == "EndOfFile":
                    break
                file.write(data)

        await websocket.send(f"File '{file_name}' uploaded successfully")
    except Exception as e:
        await websocket.send(f"Error uploading file: {str(e)}")

async def handle_client(websocket, path):
    # Specify the directory where files will be saved
    file_dir = "user1"
    os.makedirs(file_dir, exist_ok=True)
    
    try:
        while True:
            message = await websocket.recv()
            if message.startswith("user1"):
                file_dir = "user1"
                os.makedirs(file_dir, exist_ok=True)
                await save_file(websocket, file_dir)
            elif message.startswith("user2"):
                file_dir = "user2"
                os.makedirs(file_dir, exist_ok=True)
                await save_file(websocket, file_dir)
            elif message.startswith("user3"):
                file_dir = "user3"
                os.makedirs(file_dir, exist_ok=True)
                await save_file(websocket, file_dir)
            elif message.startswith("user4"):
                file_dir = "user4"
                os.makedirs(file_dir, exist_ok=True)
                await save_file(websocket, file_dir)
            elif message.startswith("user5"):
                file_dir = "user5"
                os.makedirs(file_dir, exist_ok=True)
                await save_file(websocket, file_dir)
            elif message.startswith("user6"):
                file_dir = "user6"
                os.makedirs(file_dir, exist_ok=True)
                await save_file(websocket, file_dir)
            elif message.startswith("user7"):
                file_dir = "user7"
                os.makedirs(file_dir, exist_ok=True)
                await save_file(websocket, file_dir)
            elif message.startswith("user8"):
                file_dir = "user8"
                os.makedirs(file_dir, exist_ok=True)
                await save_file(websocket, file_dir)
            elif message.startswith("user9"):
                file_dir = "user9"
                os.makedirs(file_dir, exist_ok=True)
                await save_file(websocket, file_dir)
            elif message.startswith("user10"):
                file_dir = "user1"
                os.makedirs(file_dir, exist_ok=True)
                await save_file(websocket, file_dir)

            else:
                print("Received message:", message)
                user = message[:5]
                message = message[5:]
                msg = message[-4:]
                past_conversation = append_to_csv(user, "user response " + message)
                if "generate" in message:
                    text = image_gen(message, user)
                    text = extract_file_name(text)[0]

                elif "see" in message:
                    text = extract_file_name(message)[0]
                elif "delete" in message:
                    text = extract_file_name(message)[0]
                    delete_file(f"{user}/data/{text}")
                    text = text + " file is deleted "
                elif "rename" in message:
                    text = extract_file_name(message)[0]
                    directory = f"{user}/data"
                    old_name = text
                    new_name = extract_text_after_string(message, "filename")
                    rename_files(directory, old_name, new_name)
                    return new_name
                elif "commands" in message:
                    text = " keyword [generate] = generating images, [see]= see the file, [delete] = delete the file, [rename] = rename the file, [commands] = see the commands, [all files] = print list of files, [describe the image] = it will describe the image"
                    
                elif "all files" in message:
                    create_file_list_csv(f"{user}/data")
                    df = pd.read_csv(f"{user}/data/file_list.csv")
                    text = ' ; '.join(df.to_string(index=False).split('\n'))
                elif "describe the image" in message:
                    text = extract_file_name(message)[0]
                    img = Image.open(f"{user}/data/{text}")
                    text = gv_model("describe the image in detail", img)
                else:
                    prompt = f"You've engaged with a highly advanced personal assistant designed to emulate human-like interactions effectively. Please treat our conversation as you would with a human assistant. Let's ensure our conversation flows smoothly without repeating the same questions or formalities. If we've discussed something previously, let's continue from where we left off. If this is our first interaction, feel free to start with a greeting or your query.To enhance our interaction: 1. Be concise and clear in your queries. 2. Avoid repeating the same questions unless necessary for clarification. 3. If you need to reference previous topics, provide context to help me understand.Remember, I'm here to assist you professionally and efficiently. Now, let's dive into our conversation. Please proceed with your message or inquiry. this is our past fonversation {past_conversation} and this is next message {message}"

                    # Combine prompt and context with the new message
                    text = g_model(prompt)

                    past_conversation = append_to_csv(user, " elon  " + text)
                
                await websocket.send(text)
    except websockets.exceptions.ConnectionClosedOK:
        print("Client connection closed")

def start_server(host, port):
    server = websockets.serve(handle_client, host, port)
    print(f"Server is listening on {host}:{port}")
    asyncio.get_event_loop().run_until_complete(server)
    asyncio.get_event_loop().run_forever()

if __name__ == "__main__":
    start_server('127.0.0.1', 12345)
