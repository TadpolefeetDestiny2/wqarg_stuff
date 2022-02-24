import requests
import json
import webbrowser
import numpy as np
import urllib
#strip_names = {"0-1": 0, "7q-2": 1, "3q-1": 2}
#print(strip_names)    #  this is 100% a dict
#message = str(json.dumps(strip_names))
#url = 'https://tjl.co/wqarg/arrange-save.php?source=tadpole'
#x = requests.post(url, data=message)
#print(x.json())
#webbrowser.get("C:/Program Files/Google/Chrome/Application/chrome.exe %s").open(x.json()["url"])
with urllib.request.urlopen("https://tjl.co/wqarg/mapping.json") as url:
    mapping = json.loads(url.read().decode())
print(mapping)
with urllib.request.urlopen("https://tjl.co/wqarg/clustered2.json") as url:
    clusters = json.loads(url.read().decode())
f = open('cache_files.txt', 'r')
names = f.readlines()
temp = []
for name in names:
    name = name.rstrip('\n')
    temp.append(name)
names = temp

columns = np.loadtxt("cache.txt")
print(len(columns)/1033)
columns = columns.reshape(int(len(columns)/1033), 1033)


print(names)

new_clusters_files = []
new_clusters_data = []
for cluster in clusters:
    cluster_files = []
    cluster_data = []
    for strip in cluster:
        filename = strip[:-2]
        if filename in mapping.keys():
            short_name = f'{mapping[filename]}{strip[-2:]}'
            if short_name in names:
                cluster_files.append(short_name)
                data_index = names.index(short_name)
                strip = columns[data_index]
                cluster_data.append(strip)
    new_clusters_files.append(cluster_files)
    new_clusters_data.append(cluster_data)

for i, cluster in enumerate(new_clusters_data):
    with open(f"cache{i}.txt", "w") as f:
        for strip in cluster:
            np.savetxt(f, strip)

    with open(f"cache_files{i}.txt", "w") as f:
        for strip in new_clusters_files[i]:
            f.write(f'{strip}\n')



