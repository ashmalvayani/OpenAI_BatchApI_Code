import openai
import json
import pandas as pd
import os
import re
import concurrent.futures
from openai import OpenAI

openai.api_key = ""
os.environ['OPENAI_API_KEY']=openai.api_key

batc_output_path = "Revised_Questions.jsonl"

model_id = ""


client = OpenAI()

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
      "description": "Cultural Requires Modification"
    }
)

print(f"Batch ID: {res.id}")
