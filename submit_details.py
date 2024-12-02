import openai
import json
import os
from openai import OpenAI

openai.api_key = ""
os.environ['OPENAI_API_KEY']=openai.api_key

folder_path = "gpt-4o/batchFiles"
folder_files = os.listdir(folder_path)

batc_output_files = [os.path.join(folder_path, file) for file in folder_files]
batc_output_files.sort()


client = OpenAI()

batch_ids = []
failed = []
for idx, batc_output_path in enumerate(batc_output_files):
    try:
        batch_input_file = client.files.create(
            file=open(f'{batc_output_path}', "rb"),
            purpose="batch"
        )

        batch_input_file_id = batch_input_file.id
        print(f"Batch input file created with id: {batch_input_file_id}")

        res = client.batches.create(
            input_file_id=batch_input_file_id,
            endpoint="/v1/chat/completions",
            completion_window="24h",
            metadata={
            "description": "GeoGPT_Evaluation"
            }
        )

        print(f"Batch_{idx} ID: {res.id}")
        # batch_ids.append({f'batch_{idx}': res.id})

        batch_ids.append({
            'batch': f'batch_{idx}',
            'file_id': batch_input_file_id,
            'batch_id': res.id
        })
    
    except Exception as e:
        print(f'FAILED: {batc_output_path}')
        failed.append(batc_output_path)
        pass

with open("failed_submitting_api.json", 'w') as file:
    json.dump(failed, file, indent=2)

with open("batch_ids.json", 'w') as file:
    json.dump(batch_ids, file, indent=2)
