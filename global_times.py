### (I) import
import time
from random import randint
from selectorlib import Extractor
import requests
import pandas as pd
desired_width = 200
pd.set_option('display.width', desired_width)
pd.set_option("display.max_columns", 5)
from time import sleep



### (II) Extracting links
#get yml
yml_links="""links:
    css: null
    xpath: '/html/body/div[4]/div[1]/div/div[2]/blockquote/a[1]'
    multiple: true
    type: Link"""

#define functions
def extract(yml_source, source):
    e = Extractor.from_yaml_string(yml_source)
    return e.extract(source)

# this endpoint returns the paginated html results for a POST search request in global times
def search_global_times(title, page, body=''):
    url = "https://search.globaltimes.cn/SearchCtrl"
    payload = {'page_no': page,
               'title': title,
               'col<umn': '0',
               'sub_column': '0',
               'author': '',
               'source': '',
               'textPage': body,
               'begin_date': '',
               'end_date': '',
               'orderByTime': 'yes'}

    r = requests.post(url, data=payload)
    return r.text



#loop extractings links
rounds = 1
link_list = list()

for i in range(1, 3):
    print(f"Round{rounds} of Link-Loop")
    results = search_global_times('European Union', i)
    links=extract(yml_links,results)
    #print(links)
    link_list.extend(links["links"])

    rounds = rounds + 1
    delay = randint(1, 4)
    sleep(delay)
    print(f"Sleeping for {delay} s")


print(link_list)
print(len(link_list))

#duplicate check
if len(link_list) != len(set(link_list)):
    print("There are duplicates in the list")
else:
    print("There are no duplicates in the list")






### (III) extract articles content

#yml for each article content
yml_articles = """title:
    css: div.article_title
    xpath: null
    type: Text
author:
    css: 'body > div.container.article_section > div > div > div.article > div.article_top > div.author_share > div > span.byline'
    xpath: null
    multiple: true
    type: Text
published:
    css: 'body > div.container.article_section > div > div > div.article > div.article_top > div.author_share > div > span.pub_time'
    xpath: null
    type: Text
body_text:
    css: 'body > div.container.article_section > div > div > div.article > div.article_content > div'
    xpath: null
    type: Text
"""

#data table
text_article = []
link = []
title = []
author = []
date = []

dictionary_yt = {
    "Published": date,
    "Author(s)": author,
    "Title": title,
    "Text": text_article,
    "Link": link}

df_global_times = pd.DataFrame(dictionary_yt)



#test for one article
#url = 'https://www.globaltimes.cn/page/202302/1285106.shtml'
#r = requests.get(url)
#r = r.text
#content_1=extract(yml_articles, r)
#print(content_1)


#loop for article content
round_number = 1

for link in link_list:

    print(f"Round {round_number} for Content-Loop")

    url = link
    r = requests.get(url)
    e = Extractor.from_yaml_string(yml_articles)
    text = e.extract(r.text)

    for key, value in text.items():
        title_a = list(text.values())[0]
        author_a = list(text.values())[1]
        published_a = list(text.values())[2]
        body_a = list(text.values())[3]
        url_of_a = url

    length = len(df_global_times)

    df_global_times.loc[length] = [published_a, author_a, title_a, body_a, url_of_a]
    round_number = round_number + 1
    delay = randint(1, 4)
    sleep(delay)
    print(f"Sleeping system for {delay}s")



### (IV) clean data table
df_global_times.dtypes
df_global_times.shape
df_global_times


#clean time
from datetime import datetime

def convert_timestamp_to_date_string(string):
    if "Updated:" in string:
        string = string.split(" Updated:")[0]
        #print(string)
    datetime_object = datetime.strptime(string, "Published: %b %d, %Y %I:%M %p")
    date_object = datetime_object.date()
    formatted_date = date_object.strftime("%Y-%m-%d")
    return formatted_date

# Apply the function to the date column
df_global_times['Published'] = df_global_times['Published'].apply(lambda x: convert_timestamp_to_date_string(x))
df_global_times['Published'] = df_global_times['Published'].apply(lambda x: pd.to_datetime(x))



#clean author
def split_string(s_list):
    output_list = []
    for s in s_list:
        words = s.split()
        if len(words) > 3 and words[3] == "and":
            # If the fourth word is "and", split after the sixth word
            split_index = 6
        else:
            # Otherwise, split after the third word
            split_index = 3
        first_part = " ".join(words[:split_index])
        first_part = first_part.replace('By', '').strip()
        output_list.append([first_part])
        output_list = output_list[0]
    return output_list

df_global_times['Author(s)'] = df_global_times['Author(s)'].apply(split_string).apply(pd.Series)



### (V) save as excel
from datetime import date
df_global_times.to_excel(f'Global_Times_{date.today()}.xlsx', sheet_name='articles')







