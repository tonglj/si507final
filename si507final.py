## SI 507 Final
## unique name: tonglj

from dash import Dash, dcc, html, Input, Output
import plotly.express as px
import plotly as plt
import json
from pip._vendor import requests
from urllib.request import urlopen
import time
import pandas as pd
import plotly.graph_objs as go
from plotly import io
from collections import Counter

# Cache
CACHE_FILENAME = "cache.json"

def open_cache():
    try:
        cache_file = open(CACHE_FILENAME, 'r')
        cache_contents = cache_file.read()
        cache_dict = json.loads(cache_contents)
        cache_file.close()
    except:
        cache_dict = {}
    return cache_dict

def save_cache(cache_dict):
    dumped_json_cache = json.dumps(cache_dict)
    fw = open(CACHE_FILENAME,"w")
    fw.write(dumped_json_cache)
    fw.close()

FIB_CACHE = open_cache()

def get_url_with_cache(url):
    if url in FIB_CACHE:
        return FIB_CACHE[url]
    else:
        FIB_CACHE[url] = get_url(url)
        save_cache(FIB_CACHE)
        return FIB_CACHE[url]

def get_url(url):
    source = requests.get(url).text
    data = json.loads(source)
    return data

# Get the file with API with Cache
badminton_url = "http://api.sportradar.us/badminton/trial/v2/en/rankings.json?api_key=vy9zvdhsewfzfrg7j9xcrwcn"
start_time_cache = time.time()
badmintonData = get_url_with_cache(badminton_url)
print("With Cache takes %s seconds" % (time.time() - start_time_cache))

# Read the male and female single data
male_single = badmintonData['rankings'][0]['competitor_rankings']
female_single = badmintonData['rankings'][2]['competitor_rankings']


# This function fixes issues of missing country key for certain players in male group
def checkNone(dic, key):
    for i in range(len(male_single)):
        if key not in dic[i]['competitor']:
            dic[i]['competitor']['country'] = "Not Available"

# Fix male_single data
checkNone(male_single, 'country')


def checkNoneBirth(dic, key):
    new_dic = []
    for i in range(len(dic)):
        if key in dic[i]['competitor']:
            new_dic.append(dic[i])
    return new_dic

# Fix male_single birth date data
age_male_single = checkNoneBirth(male_single, 'date_of_birth')
age_female_single = checkNoneBirth(female_single, 'date_of_birth')

def get_age(lst):
    age_list = []
    for i in range(len(lst)):
        birth_year = lst[i]['competitor']['date_of_birth'][0:4]
        age = 2022 - int(birth_year)
        age_list.append(age)
    return age_list

age_male_single_done = get_age(age_male_single)
age_female_single_done = get_age(age_female_single)

age_male_single_df = pd.DataFrame(age_male_single_done, columns = ['age'])

age_female_single_df = pd.DataFrame(age_female_single_done, columns = ['age'])


# Tree structure based on name abbreviation
class Node:
    def __init__(self, data):
        self.left = None
        self.right = None
        self.data = data
        self.abb = data['competitor']['abbreviation']

    def insert(self, data):
        if self.data is None:
            self.data = data
        else:
            if data['competitor']['abbreviation'] < self.abb:
                if self.left is None:
                    self.left = Node(data)
                else:
                    self.left.insert(data)
            elif data['competitor']['abbreviation'] > self.abb:
                if self.right is None:
                    self.right = Node(data)
                else:
                    self.right.insert(data)

    def findval(self, lkpval):
        if lkpval < self.data['competitor']['abbreviation']:
            if self.left is None:
                return str(lkpval)+" Not Found"
            return self.left.findval(lkpval)
        elif lkpval > self.data['competitor']['abbreviation']:
            if self.right is None:
                return str(lkpval)+" Not Found"
            return self.right.findval(lkpval)
        else:
            return self.data

def printTree(node, level=0):
    if node != None:
        printTree(node.left, level + 1)
        print(' ' * 4 * level + '-> ' + str(node.data))
        printTree(node.right, level + 1)


# Male single tree
male_root = Node(male_single[0])
for i in range(1, len(male_single)):
    male_root.insert(male_single[i])
printTree(male_root)

# Female single tree
female_root = Node(female_single[0])
for i in range(1, len(female_single)):
    female_root.insert(female_single[i])
# printTree(female_root)

# Get all player's name abbreviation by gender
def get_name_abb_list(lst):
    abb_list = []
    for i in range(len(lst)):
        abb_list.append(lst[i]['competitor']['abbreviation'])
    return abb_list

male_single_name_abb_list = get_name_abb_list(male_single)
female_single_name_abb_list = get_name_abb_list(female_single)

def get_country_list(lst):
    country_list = []
    for i in range(len(lst)):
        country_list.append(lst[i]['competitor']['country'])
    return country_list

male_single_country_list = get_country_list(male_single)
male_single_country_counter = Counter(male_single_country_list)

female_single_country_list = get_country_list(female_single)
female_single_country_counter = Counter(female_single_country_list)

# Number of players who made into the ranking list by country
## Male by country
male_country_player = pd.DataFrame.from_dict(male_single_country_counter, orient='index').reset_index()
male_country_player = male_country_player.rename(columns={'index':'country', 0:'# of player'})
male_country_player_top_10 = male_country_player[0:10]

## Female by country
female_country_player = pd.DataFrame.from_dict(female_single_country_counter, orient='index').reset_index()
female_country_player = female_country_player.rename(columns={'index':'country', 0:'# of player'})
female_country_player_top_10 = female_country_player[0:10]

app = Dash(__name__)

# The html that displays the contents
app.layout = html.Div([
    html.H2('Number of players who made into the ranking list by country'),
    html.P('You might wonder what country is known for badminton? You might have your answers. But let\'s take a look at the number of players who made in to the world ranking by country.'),
    dcc.Graph(id="graph"),
    html.P("Player Group:"),
    dcc.Dropdown(id='playerGroup',
        options=['Man Single', 'Woman Single'],
        value='Man Single',
        clearable=False,
    ),

    html.Br() ,
    html.Br() ,

    html.H2('You must know everything about your faviorite player. But do you know what their official name abbreviations are? Let\' learn them again but with name abbreviation this time. (Tree Search)'),
    html.Br() ,
    html.H4('Man Single Player\'s information by name abbreviation'),
    html.P("Man Single Player Name"),
    dcc.Dropdown(id='malePlayerName',
        options=male_single_name_abb_list,
        clearable=False,
        value="AXE"
    ),
    html.P(id="maleInfo"),

    html.Br() ,
    html.Br() ,


    html.H4('Woman Single Player\'s information by name abbreviation'),
    html.P("Woman Single Player Name"),
    dcc.Dropdown(id='femalePlayerName',
        options=female_single_name_abb_list,
        clearable=False,
        value="YAM"
    ),
    html.P(id="femaleInfo"),

    html.Br() ,
    html.Br() ,
    html.Br() ,
    html.Br() ,

    html.H2('Number of players by gender (single)'),
    dcc.Graph(
        figure={
            'data': [
                {'x': ["Man", "Woman"], 'y': [len(male_single_name_abb_list), len(female_single_name_abb_list)], 'type': 'bar', 'name': 'SF'}
            ],
            'layout': {
                'title': 'Number of players by gender (single)'
            }
        }
    ),

    html.Br() ,
    html.Br() ,
    html.Br() ,
    html.Br() ,

    html.H2('Player\' age spread by gender'),
    dcc.Graph(id="graph3"),
    html.P("Player Age:"),
    dcc.Dropdown(id='playerAge',
        options=['Man Single', 'Woman Single'],
        value='Man Single',
        clearable=False,
    ),

    html.Br() ,
    html.Br() ,
    html.Br() ,
    html.Br() ,
    html.Br() ,
    html.Br() ,
    html.Br() ,

])

# This part is for the first pie chart
@app.callback(
    Output("graph", "figure"),
    Input("playerGroup", "value"))

def generate_top10_player(value):
    if value == 'Man Single':
        df = male_country_player_top_10
    else:
        df = female_country_player_top_10
    fig = px.pie(df, values='# of player', names='country', hole=.2)
    return fig

# This part is for name abbreviation (man)
@app.callback(
    Output("maleInfo", "children"),
    Input("malePlayerName", "value"))

def generate_male_info(value):
    value = male_root.findval(value)
    maleInfo = (f"""
    Name: {value['competitor']['name']}, \n
    Abbreviation: {value['competitor']['abbreviation']},\n
    Date of Birth: {value['competitor']['date_of_birth']},\n
    Country: {value['competitor']['country']},\n
    Ranking: {value['rank']},
    Points: {value['points']}""")
    return maleInfo


# This part is for name abbreviation (woman)
@app.callback(
    Output("femaleInfo", "children"),
    Input("femalePlayerName", "value"))

def generate_male_info(value):
    value = female_root.findval(value)
    femaleInfo = (f"Name: {value['competitor']['name']},\
                Abbreviation: {value['competitor']['abbreviation']},\
                Date of Birth: {value['competitor']['date_of_birth']},\
                Country: {value['competitor']['country']},\
                Ranking: {value['rank']},\
                Points: {value['points']}")
    return femaleInfo


@app.callback(
    Output("graph3", "figure"),
    Input("playerAge", "value"))

def generate_age(value):
    if value == 'Man Single':
        df = age_male_single_df
    else:
        df = age_female_single_df
    fig = px.scatter(df, x='age')
    return fig


if __name__ == '__main__':
    app.run_server(debug=True)
    print("Web Running")

