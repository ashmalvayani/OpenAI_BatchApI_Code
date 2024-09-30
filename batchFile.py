import openai
import json
import pandas as pd
import os
import re
import pandas as pd
import concurrent.futures


openai.api_key = ""
os.environ['OPENAI_API_KEY']=openai.api_key



file_path = 'filtered_mistakes.csv'
df = pd.read_csv(file_path)
# df_sampled = df.sample(frac = 1).reset_index(drop=True)

batch = []
for index, row in df.iterrows():
    question = row['English_Question']
    lang = row['Language']
    id = row['Question_Number']
    # print(row['Language'], row['Question_Number'], row['English_Question'], row['English_Answer'], sep=', ')

    content = ('''You are an expert in designing tasks that require visual and linguistic reasoning. Your goal is to ensure that each question provided is specifically designed to be answered only by analyzing the given image, making it necessary for a Vision Language Model (VLM) to be used.\n\n'''
    '''Instructions:\n'''
    '''1. Analyze the given question.\n'''
    '''2. Determine if the question can be answered without using the image (i.e., using text-based knowledge alone or by searching through commonly accessible data such as the internet, databases, or general public knowledge).\n'''
    '''3. If the question can be answered without visual input, even if additional textual information is required or if it can be found using general sources, say "requires modification" and give the updated question.\n'''
    '''4. If the question does not explicitly include visual-specific language such as "in this image", "as referred to this image", or similar phrases, say "requires modification" and give the updated question.\n'''
    '''5. If the question is about general information or a common query that could be answered by non-visual means (e.g., searching for public knowledge), say "requires modification" and give the updated question.\n'''
    '''6. If the question requires modification and if question has name of famous places, site, sports, dishes, famous person names, remove it so the model tries to identify that from the image.\n'''
    '''7. If the question explicitly requires visual input to answer (e.g., contains words like "this", "in this image", or asks for specific visual details that cannot be inferred from text alone), say "no modification."\n'''
    '''8. Consider only the information given in the question. Do not make any assumptions beyond what is provided.\n\n'''

    '''**Examples:**\n'''

    '''Original Question: "What type of traditional attire is being worn in the image?"\n'''
    '''Your Response: {"answer": "no modification", "reason": "A VLM can not tell about traditional attire of the image without analyzing the image.", "updated_question": "None"}\n\n'''

    '''Original Question: "Are the individuals in the image wearing modern Western clothing?"\n'''
    '''Your Response: {"answer": "no modification", "reason": "A VLM can not tell if individuals or people in the image are weaning moderl Western Clothing without analyzing the visual data so both question and image are necessary.", "updated_question": "None"}\n\n'''

    '''Original Question: "Discuss the cultural significance of traditional Zulu attire and how it represents the heritage and identity of the Zulu people, particularly in ceremonies and daily life.\n"'''
    '''Your Response: {"answer": "requires modification", "reason": "Cultural significance of traditional Zulu attire can be directly answered, we should be expressing about cultural significance about the cultural, ceremony and people shown in the image only.", "updated_question": "Discuss the cultural significance of the traditional Zulu attire that's shown in the image and how it represents the heritage and identity of the Zulu people, particularly in ceremonies and daily life."}\n\n'''

    '''Original Question: "Where is the Church of Abuna Aregawi located?"\n'''
    '''Your Response: {"answer": "requires modification", "reason": "this information can be answered from google or LLM's data, doesn't require image input to be answered.", "updated_question": "Where is this church that's shown in the image located?"}}\n\n'''

    '''Original Question: "From which period does Fasil Ghebbi date back to?"\n'''
    '''Your Response: {"answer": "requires modification", "reason": "The question does not contain pointers to look at the image specifically. It is a historical question and can be answered very easily.", "updated_question": "From which period does the building shown in the image date back to?"}}\n\n'''

    '''Original QuestionL=: "Discuss the architectural and cultural significance of the Petronas Towers, including their design elements, symbolism, and how they represent Malaysia's advancement and modernity."\n'''
    '''Your Response: {"answer": "requires modification", "reason": "The question discusses the architectural and cultural significance of the Petronas Towers, which can be answered using general knowledge about the towers rather than needing to analyze an image of them.", "updated_question": "Discuss the architectural and cultural significance of the place shown in the image, including their design elements, symbolism, and how they represent Malaysia's advancement and modernity."}}\n\n'''


    '''Remember: '''
    '''- A question should be flagged for modification if it can clearly be answered without analyzing the image.\n'''
    '''- Questions that refer directly to the image (e.g., with words like 'this', 'in this image') should not be marked as requiring modification, as they inherently require visual context to answer.\n\n'''

    '''Provide your answer in JSON format: {"answer": ANSWER HERE, "reason": REASONING HERE, "updated_question": UPDATED QUESTION IF NEEDED OTHERWISE NONE}.\n''')
    
    user_content = f"Question: {question}\n"

    bat = {
        "custom_id": f"{lang}-{id}", 
        "method": "POST", 
        "url": "/v1/chat/completions", 
        "body": {
            "model": "gpt-4o-mini", 
            "messages": [{"role": "system", "content": content},{"role": "user", "content": user_content}],
            "max_tokens": 1000
            }
        }
    batch.append(bat)


model_id = "Revised_Questions"
with open(f'{model_id}.jsonl', 'w') as f:
    for entry in batch:
        f.write(json.dumps(entry))
        f.write('\n')
