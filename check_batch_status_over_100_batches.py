# The OpenAI has a limit of retrieving 100 batches from openai, so we will use pagination to retrieve the remaining results.
# OpenAI version > 1.0.0

import openai
import json
import os

client = openai.OpenAI(
    api_key = ""
)

# The batch id looks like following, update the submit.py file to store the file_id as well.:
'''
[
  {
    "batch": "batch_0",
    "file_id": "file-xxx",
    "batch_id": "batch_xxx"
  },
'''

with open('/home/batch_ids.json', 'r') as file:
    batches = json.load(file)

retrieved_ids = []
for batch in client.batches.list(limit=100).data:
    for batch_ in batches:
        if batch.id == batch_['batch_id']:
            print('id:', batch.id)
            print('Status:', batch.status)
            print(f'Completed {batch.request_counts.completed} out of {batch.request_counts.total} with {batch.request_counts.failed} failed')
            print(f'Output fileid:', batch.output_file_id)
            print()

            if batch.status == 'completed':
                fileid = batch.output_file_id
                file_response = client.files.content(fileid)
            
                output_file = "batch_outputs/openai_" + str(batch.id) + '.jsonl'
                with open(f"{output_file}", 'w') as f:
                    f.write(file_response.text)

            retrieved_ids.append(batch.id)


for batch in client.batches.list(limit=96, after=retrieved_ids[-1]).data:
    for batch_ in batches:
        if batch.id == batch_['batch_id']:
            print('id:', batch.id)
            print('Status:', batch.status)
            print(f'Completed {batch.request_counts.completed} out of {batch.request_counts.total} with {batch.request_counts.failed} failed')
            print(f'Output fileid:', batch.output_file_id)
            print()

            if batch.status == 'completed':
                fileid = batch.output_file_id
                file_response = client.files.content(fileid)
            
                output_file = "batch_outputs/openai_" + str(batch.id) + '.jsonl'
                with open(f"{output_file}", 'w') as f:
                    f.write(file_response.text)

            retrieved_ids.append(batch.id)

print(len(set(retrieved_ids)))
