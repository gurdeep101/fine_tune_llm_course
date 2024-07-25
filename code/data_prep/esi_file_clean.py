import os
import pdfplumber

# helper functions
from helper_esi_file_clean import figure_text_clean, group_adjacent_rectangles

# parameters - move to argparse later
distance_threshold = 5
print(os.getcwd())
# load data - move to argparse later
esi = pdfplumber.open('../../data/esi/esi2023.pdf')

# # target directory
# if not os.path.exists('../data/esi/esi2023_clean'):
#     os.mkdir('../data/esi/esi2023_clean')

# target directory
path = '../../data/esi/esi2023_clean/images'
os.makedirs(path, exist_ok=True)

# extract text from each page and clean
esi_pages = [esi.pages[num].extract_text() for num in range(len(esi.pages))]

print("text loaded")
esi_text = " ".join(esi_pages)

print('text joined')

esi_text = esi_text.replace("\n", "")

print('newlines replaced')

esi_text = figure_text_clean(esi_text)

# save cleaned text for chunking later
with open('../../data/esi/esi2023_clean/esi_text_clean.txt', 'w') as file:
    file.write(esi_text)

print('text saved')
  
# extract tables and images and save into a new folder
for page in esi.pages:
    all_rects = page.rects
    rect_tuple = [(rect['x0'], rect['y0'], rect['x1'], rect['y1']) for rect in all_rects]
    adjacent_groups = group_adjacent_rectangles(rect_tuple, distance_threshold)
    print(f'{len(adjacent_groups)} adjacent groups found on page {page.page_number} done')
    
    if len(adjacent_groups) <= 2: 
        continue
    
    outer_rects = []
    for group in adjacent_groups:
        x0 = min(group, key=lambda x: x[0])[0]
        y0 = min(group, key=lambda x: x[1])[1]
        x1 = max(group, key=lambda x: x[2])[2]
        y1 = max(group, key=lambda x: x[3])[3]
        outer_rects.append([x0, y0, x1, y1])
    bbox_rects = []
    for rect in outer_rects:
        x0 = rect[0]
        top = page.height-rect[3]
        x1 = rect[2]
        bottom = page.height-rect[1]
        bbox_rects.append([x0, top, x1, bottom])
    for i, rect in enumerate(bbox_rects):
        bbox = (rect[0], rect[1], rect[2], rect[3])
        bbox_cropped = page.crop(bbox)
        ia = bbox_cropped.to_image(resolution=350)
        ia.save(f'{path}/pg_{page.page_number}_img_{i+1}.jpg')
    print(f'{page.page_number} done')