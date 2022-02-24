import numpy as np
import matplotlib.pyplot as plt
from PIL import Image
from operator import itemgetter
import base64
import webbrowser
import requests
import json

user_name = "tadpole"

'''
change ur name(above) so tj knows whos hitting his servers lmao
to get new data run getimages.py, then convert.py, then testing.py
idgaf if u cant understand my code
i wrote most of it after midnight drunk cuz of timezones
(fuck u america)
deal with it



sidenote: fuck russia too
'''

def compare(column, compare_col):
    header_score = np.sum(100 / (np.linalg.norm(column[:230] - compare_col[:230]) + 1))
    text_score = np.sum(100 / (np.linalg.norm(column[230:] - compare_col[230:]) + 1))
    return((-header_score) * 2 - text_score)

clus = "4"  # THIS IS WHICH CLUSTER U ARE MAKING RESULTS FOR (leave blank for all)

columns = np.loadtxt(f"cache{clus}.txt")
print(len(columns)/1033)
columns = columns.reshape(int(len(columns)/1033), 1033)

sorted_cols = columns

f = open(f'cache_files{clus}.txt', 'r')
new_names = f.readlines()
names = []
for name in new_names:
    names.append(name.rstrip("\n"))

s = sorted_cols
matched = []
strip_names = {}
for i in range(len(s)):    # my gcse compsci teacher would be proud

    column = s[0]
    matched.append(s[0])
    s = np.delete(s, 0, 0)

    strip_names[names.pop(0)] = i

    similarity_list = []
    for j, compare_col in enumerate(s):

        #total_difference = sum(abs(column - compare_col))
        '''
        thanks danzi for this comparison alg, my pea sized brain doesnt like thinking too hard
        '''
        total_difference = compare(column, compare_col)


        tupley_thing = (j, total_difference)
        similarity_list.append(tupley_thing)
    if len(similarity_list) != 0:
        highest_col = sorted(similarity_list, key=itemgetter(1))[0][0]

        temp = s[highest_col]
        temp2 = names.pop(highest_col)

        s = np.delete(s, highest_col, 0)
        s = np.insert(s, 0, temp, axis=0)
        names = [temp2] + names

        print("final", s.shape)




final = np.transpose(matched)
img = Image.fromarray(np.uint8(final) , 'L')
img.save(f"result{clus}.png")

print(strip_names)    #  this is 100% a dict
message = str(json.dumps(strip_names))
url = f'https://tjl.co/wqarg/arrange-save.php?source={user_name}'
x = requests.post(url, data=message)

webbrowser.get("C:/Program Files/Google/Chrome/Application/chrome.exe %s").open(x.json()["url"])

