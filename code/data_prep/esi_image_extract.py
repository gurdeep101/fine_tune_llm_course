# imports
import os
from PIL import Image
import csv

from llama_index.core import SimpleDirectoryReader
from llama_index.multi_modal_llms.openai import OpenAIMultiModal

# define variables - replace with argparse later

# output tokens
max_tokens = 1500
# input image folder
img_path = 'GitHub/fine_tune_llm_course/data/esi/test'
# output path
filename = '../data/esi/test/image_chunks.csv'
# dictionary to store response
image_descr = {}

# instantiate model
gpt4o = OpenAIMultiModal(model="gpt-4o", max_new_tokens=max_tokens)

prompt="""
    you are an analyst reading tables and charts with the objective of extracting information from them for analysis.
    Identify the image as a table or a chart. 
    If the image is a table then return the table in markdown format.
    If the image is a chart then extract the information in the chart from the image in as much detail as possible. Do not draw any interpretaions but focus solely on extracting information from the image
    If you are unable to classify the image as either a table or a chart, please summarize the image and return the summary.
"""

# for item in os.listdir(img_path):
#     if item.endswith(".jpg") or item.endswith(".png"):
#         image_list.append(os.path.join(img_path, item))

# # process images and store response in a dictionary
# image_descr = {}
# for img_file in image_list:
#     image_documents = SimpleDirectoryReader(input_files=[image_file]).load_data()
#     response = llm.complete(prompt=prompt, image_documents=image_documents)
#     # print(restponse.text)
#     image_descr_t2[image_file].append(response.text)
#     print(f'{img_file} done!')

# process images and store response in a dictionary
for item in os.listdir(os.path.join(os.getcwd(),img_path)):
    if item.endswith(".jpg") or item.endswith(".png"):
        item_path = os.path.join(img_path, item)
        image_documents = SimpleDirectoryReader(input_files=[item_path]).load_data()
        response = gpt4o.complete(prompt=prompt, image_documents=image_documents)
        # print(restponse.text)
        image_descr[item].append(response.text)
        print(f'{item} done!')
        break
        

# open the file for writing
headers = ['filename','description']
# open the file for writing
with open(filename, mode='w', newline='')as file:
    writer = csv.writer(file)
    
    # write the header - dictionary keys
    writer.writerow(headers)
    
    # write rows - dictionary values
    for key, value in image_descr.items():
        writer.writerow([key, value[0]])
    
print(f"image descriptions saved as csv")
