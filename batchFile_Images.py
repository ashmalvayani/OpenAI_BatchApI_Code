import os
import json
import base64
from PIL import Image
from io import BytesIO
from openai import OpenAI
import openai
from tqdm import tqdm
 
openai.api_key = ""
os.environ['OPENAI_API_KEY']=openai.api_key

client= OpenAI()

def encode_image(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode('utf-8')

def generate_batch_json_files(image_clues_path):
    batch = []
    failed = []

    with open(image_clues_path, 'r') as file:
        image_files = json.load(file)

    for idx, data in enumerate(tqdm(image_files)):
        try: 
            image_path = data['img_path']
            base64_image = encode_image(image_path)

            if 'clues' in data.keys():
                user_text = f"Image's Location: {data['location']} \n\nClues of that country: {data['clues']}"
            else:
                user_text = f"Image's Location: {data['location']}"

            PROMPT_MESSAGES = [
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "text",
                            "text": user_text
                        },
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": f"data:image/jpeg;base64,{base64_image}"
                            }
                        }
                    ]
                },
                {
                    "role": "system",
                    "content": 
                        '''You are a helpful Assistant. Provide detailed response to the user's question.'''
                        '''Given an image, it's location where it is located and some geolocalizable clues of that location, write the detailed description of image.  Answer in one detailed paragraph of 200-300 words.'''
                    
                }
            ]

            bat = {
            "custom_id": f"{data['id']}", 
            "method": "POST", 
            "url": "/v1/chat/completions", 
            "body": {
                "model": "gpt-4o-mini", 
                "messages": PROMPT_MESSAGES,
                "max_tokens": 1000
                }
            }
            batch.append(bat)

        except Exception as e:
            failed.append(data)
            print(e)
            pass

    # the number of batches will depend upon your length of data in each chunk, it can be 30k-50k per batch or even 1k per batch.
    sub_batches = [batch[i:i + 1000] for i in range(0, len(batch), 1000)]

    os.makedirs('batch_files', exist_ok=True)

    for idx, sub_batch in enumerate(sub_batches):
        with open(f'batch_files/json_batch_{idx}.jsonl', 'w') as f:
            for entry in sub_batch:
                f.write(json.dumps(entry))
                f.write('\n')
            # json.dump(sub_batch, f, indent=2)

    with open('failed_jsons.json', 'w') as f:
        json.dump(failed, f, indent=2)
    

if __name__ == "__main__":
    image_clues_path = 'Image_Locations_Clues.json'
    generate_batch_json_files(image_clues_path)
    
