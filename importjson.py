import json
import os
from PIL import Image, ImageDraw
from collections import Counter
import pandas as pd
import matplotlib.pyplot as plt
from operator import itemgetter

input_dir = "image directory"
target_dir = "annotation directory"

input_img_paths = sorted(
    [
        os.path.join(input_dir, fname)
        for fname in os.listdir(input_dir)
    ]
)

target_img_paths = sorted(
    [
        os.path.join(target_dir, fname)
        for fname in os.listdir(target_dir)
    ]
)

def ann_load(target_img_paths):
    for i in target_img_paths:
        f=open(i)
        data = json.load(f)
        return data     

data = ann_load(target_img_paths)
size=[data['size']['height'],data['size']['width']]
outline=[]
class_name=[]
for i in data['objects']:
        class_name.append(i['classTitle'])
        x=(i['points']['exterior'])
        line=[]
        for j in range(len(x)):
            line.append(tuple(x[j]))
        outline.append(line)
#x=outline[1:][0]
#print(x)
#print(max(x,key=itemgetter(0))[0])
#print(max(x,key=itemgetter(1))[1])
#print(min(x,key=itemgetter(0))[0])
#print(min(x,key=itemgetter(1))[1])

img=Image.open(input_img_paths[0])
img.show()

#im=Image.new('RGB', tuple(size))
draw = ImageDraw.Draw(img)
class_color={'amacrine':'yellow', 'bipolar':'green', 'cone':'orange', 'ganglion': 'blue', 'horizontal':'pink', 'muller':'brown', 'rod':'grey', 'rpe':'violet'}
for i,j in zip(range(1,len(outline)),range(1, len(class_name))):   
    #img=Image.open(input_img_paths[0])
    draw.polygon(tuple(outline[i]),fill=class_color[class_name[j]])
    x=outline[i]
    #print(x)
    draw.rectangle([((min(x,key=itemgetter(0))[0]), (min(x,key=itemgetter(1))[1])), ((max(x,key=itemgetter(0))[0]), (max(x,key=itemgetter(1))[1]))], fill=None, outline='red')
img.show()


x=Counter(class_name[1:])
summary=pd.DataFrame.from_dict(x, orient='index', columns=['number'])
print(summary)

