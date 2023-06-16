from flask import Flask, render_template, request
from bs4 import BeautifulSoup
import json
import urllib.parse
import requests
import re

app = Flask(__name__)

@app.route('/', methods=['GET'])
def index():
    return render_template('chart.html')

@app.route('/chart', methods=['POST'])
def chart():
    song_name = request.form['song_name']
    return search_charts(song_name)

@app.route('/chartsearch', methods=['GET'])
def chart_search():
    query = request.args.get('query')
    return search_charts(query)

def search_charts(query):
    num_results = 10

    njamp_query = urllib.parse.quote(query)
    njamp_url = f'https://njamp.us/search/{njamp_query}'
    njamp_response = requests.get(njamp_url)
    njamp_paths = []

    if njamp_response.status_code == 200:
        for item in njamp_response.json():
            njamp_paths.append(urllib.parse.quote(item['path']))

    njamp_header = "<h3>NJamp Links:</h3>"
    njamp_links = ""

    if len(njamp_paths) > 0:
        for path in njamp_paths:
            njamp_url = f'https://njamp.us/{path}'
            njamp_links += f"<a href='{njamp_url}'>{njamp_url}</a><br>"
    else:
        njamp_links = f"No results found for '{query}' on NJamp."

    search_string = '+'.join(query.split())
    url = f"https://www.ultimate-guitar.com/search.php?title={search_string}&rating%5B0%5D=4&rating%5B1%5D=5&page=1&order=myweight&type=300"
    ug_header = "<h3>Ultimate Guitar Links:</h3>"

    response = requests.get(url)
    soup = BeautifulSoup(response.content, "html.parser")

    js_store_div = soup.find("div", class_="js-store")
    data_content = js_store_div.get("data-content")
    json_data = json.loads(data_content)
    store_data = json_data.get("store")
    page_data = store_data.get("page")
    page_data = page_data.get("data")
    results = page_data.get("results")

    chord_tabs = []

    for tab in results:
        tab_url = tab.get("tab_url")
        if "-chords-" in tab_url:
            chord_tabs.append(tab_url)

    chord_tabs_str = ""

    if chord_tabs:
        chord_tabs_str = "<ul>"
        for tab in chord_tabs[:10]:
            chord_tabs_str += f"<li><a href='{tab}'>{tab}</a></li>"
        chord_tabs_str += "</ul>"

    return render_template('result.html', njamp_links=njamp_links, ug_links=chord_tabs_str)

if __name__ == '__main__':
    app.run()
