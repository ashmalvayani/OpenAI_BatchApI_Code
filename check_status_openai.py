import openai
import json
import os


client = openai.OpenAI(
    api_key = ""
)

# Replace the 'id_from_previous_code' below from running the previous submit code. If you have accidentally deleted it, comment on the if batch.id code, in that case, it will print all the opener's batch submissions.
for batch in client.batches.list().data:
    if batch.id == 'id_from_previous_code':
        print('id:', batch.id)
        print('Status:', batch.status)
        print(f'Completed {batch.request_counts.completed} out of {batch.request_counts.total} with {batch.request_counts.failed} failed')
        print(f'Output fileid:', batch.output_file_id)
        print()

        # fileid = batch.output_file_id
        # file_response = client.files.content(fileid)
        
        # output_file = "revised_questions_openai_" + str(batch.id) + '.jsonl'
        # with open(f"{output_file}", 'w') as f:
        #     f.write(file_response.text)
