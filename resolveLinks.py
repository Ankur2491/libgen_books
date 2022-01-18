from libgen_api import LibgenSearch
import json
import requests
import collections
book_name = input("Enter the book name: ")
extension = input("What format you want? (pdf, epub, mobi): ")
author_name = input(
    "Do you know the author name? If yes, please enter here else press enter:  ")
author_entered = False
s = LibgenSearch()
final_map = {}
size_map = {}
filtr = {"Extension": extension}
results = s.search_title_filtered(book_name, filtr)
if len(author_name) > 0:
    author_entered = True
if author_entered:
    for i in range(0, len(results)):
        if len(results[i]["Author"]) > 0:
            if author_name.strip().lower() == results[i]["Author"].strip().lower():
                item_to_download = results[i]
                download_links = s.resolve_download_links(item_to_download)
                if(len(results[i]["Year"]) == 4):
                    final_map[int(results[i]["Year"])] = download_links
                    file_size_arr = results[i]['Size'].split(" ")
                    if file_size_arr[1] == 'Kb':
                        size_map[download_links['Cloudflare']] = int(
                            file_size_arr[0]) * 1024
                    elif file_size_arr[1] == 'Mb':
                        size_map[download_links['Cloudflare']] = int(
                            file_size_arr[0]) * 1024 * 1024
else:
    for i in range(0, len(results)):
        item_to_download = results[i]
        download_links = s.resolve_download_links(item_to_download)
        if(len(results[i]["Year"]) == 4):
            final_map[int(results[i]["Year"])] = download_links
            file_size_arr = results[i]['Size'].split(" ")
            if file_size_arr[1] == 'Kb':
                size_map[download_links['Cloudflare']] = int(
                    file_size_arr[0]) * 1024
            elif file_size_arr[1] == 'Mb':
                size_map[download_links['Cloudflare']] = int(
                    file_size_arr[0]) * 1024 * 1024
ordered_final_map = collections.OrderedDict(
    sorted(final_map.items(), reverse=True))
selected_size = 0
url = ""
for k, v in ordered_final_map.items():
    url = v["Cloudflare"]
    selected_size = size_map[url]
    break
if url != "":
    with open('%s.%s' % (book_name, extension), 'wb') as fd:
        print('Downloading %s.%s' % (book_name, extension))
        response = requests.get(url, stream=True)
        total_length = selected_size
        dl = 0
        for chunk in response.iter_content(2000):
            dl += len(chunk)
            fd.write(chunk)
            done = round((dl/total_length) * 100, 2)
            if done < 101:
                print(done, "%")
