import urllib

from PIL import Image
import matplotlib.pyplot as plt
import numpy as np
from numpy import asarray
import sys
import os
import statistics
import urllib.request, json
with urllib.request.urlopen("https://tjl.co/wqarg/mapping.json") as url:
    mapping = json.loads(url.read().decode())

columns = []
filenames = []

np.set_printoptions(threshold=sys.maxsize)
for file_index, filename in enumerate(os.listdir('C:/Users/Louis/PycharmProjects/pythonProject2/imgs')):

    if filename.endswith('.png'):#
        image = Image.open(f'./imgs/{filename}')
        data = asarray(image)
        if data.shape == (10536, 1250, 4):
            data = np.transpose(data, (1, 0, 2))
        else:
            data = np.transpose(data, (1, 0))
        print(file_index)

        count = 1
        for i, column in enumerate(data):
            if i in [200, 410, 620, 830, 1040]:
                new_column = []
                column = column[103:-103]
                column = np.split(column, 1033)
                for pixel in column:
                    if data.shape == (1250, 10536, 4):
                        pixel = statistics.mean(pixel[0][:-1])
                    else:
                        pixel = pixel[0]
                    new_column.append(pixel)
                columns.append(new_column)

                filenames.append(f'{mapping[filename.strip(".png")]}-{count}')
                count += 1

print(len(columns))

with open("cache.txt", "w") as f:
    for col in columns:
        np.savetxt(f, col)

with open("cache_files.txt", "w") as f:
    for strip in filenames:
        f.write(f'{strip}\n')

