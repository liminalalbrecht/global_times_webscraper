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
import json
import re
from dateutil.parser import parse




### (II) defining functions
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
               'begin_date': formatted_date_start,
               'end_date': formatted_date_end,
               'orderByTime': 'yes'}

    r = requests.post(url, data=payload)
    return r.text




### (III) Ask user for input data
#title search terms
print()
print("Please enter your search terms for the article title.")
search_title = input()
print(f"Your search term(s) for the title are: '{search_title}'")
print()

#body search terms
test = 0
while test == 0:
    print("Do you also want to look for specific words in the body of the articles?")
    print("Answer 'yes' or 'no'.")
    decision_search_body = input()
    if "yes" in decision_search_body.lower():
        print("Please enter the search terms for the article body.")
        search_body = input()
        print(f"Your body search term(s) are: '{search_body}'")
        test = 1
    elif "no" in decision_search_body.lower():
        search_body = ""
        print("You chose no criteria for the text body.")
        test = 1
    else:
        print("There appears to be a typo. Please type in either 'yes' or 'no'")

print()

###user date input
print("Please enter the start date of the time period you want to scrape.")
print("Required format is YYYY-MM-DD, but script will automatically transform other inputted date formats.")
date_start = input()
print()
print("Please enter the end date of the time period you want to scrape.")
print("Required format is YYYY-MM-DD, but script will automatically transform other inputted date formats.")
date_end = input()
print()

# Parse the date using dateutil
date_start = parse(date_start)
date_end = parse(date_end)

# Format the date into year-month-date format
formatted_date_start = date_start.strftime("%Y-%m-%d")
formatted_date_end = date_end.strftime("%Y-%m-%d")

# output the formatted date
print(f"The chosen start date is: {formatted_date_start}")
print(f"The chosen end date is: {formatted_date_end}")
print()

#checking date format
# Define the pattern for YYYY-MM-DD format
pattern = re.compile(r"\d{4}-\d{2}-\d{2}")

# Test if a string matches the pattern
if pattern.match(formatted_date_start):
    print()
else:
    print("The string of the start_date is not in the corrext format of YYYY-MM-DD. Please start process again and adjust the date input")

if pattern.match(formatted_date_end):
    print()
else:
    print("The string of the end_date is not in the correct format of YYYY-MM-DD. Please start process again and adjust the date input")



#testing return of results and extracting page number if there are results
#get yml
page_number_yml="""Number_of_Pages:
    css: 'div.row-fluid:nth-of-type(12)'
    xpath: null
    type: Text"""

no_content_yml="""no_results_text:
    css: 'div.container-fluid div'
    xpath: null
    type: Text"""

article_numbers="""number_of_articles:
    css: 'div.container-fluid div.row-fluid:nth-of-type(4)'
    xpath: null
    type: Text"""

article_numbers_many = """articles_many:
    css: 'div.row-fluid:nth-of-type(12)'
    xpath: null
    type: Text"""

results = search_global_times(search_title, 1, search_body)
page_data=extract(page_number_yml,results)
my_string = json.dumps(page_data)

#delay = randint(1, 2)
#sleep(delay)

if my_string == '{"Number_of_Pages": null}':
        try:
            page_data=extract(no_content_yml,results)
            dumped_text = json.dumps(page_data)
            if dumped_text == '{"no_results_text": "no results"}':
                print("Your search did not yield any results.")
                pages = 0
                articles = 0
            else:
                page_data = extract(article_numbers, results)
                dumped_article_num = json.dumps(page_data)
                match = re.search(r'Total:(\d+)', dumped_article_num)

                if match:
                    articles = int(match.group(1))
                pages = 1
        except:
            print("There seems to be an issue.")
else:
    match = re.search(r"(\d+) Next", my_string)
    if match:
        num_before_next = match.group(1)
        pages = num_before_next

        page_data = extract(article_numbers_many, results)
        dumped_article_num = json.dumps(page_data)
        match = re.search(r'Total:(\d+)', dumped_article_num)
        if match:
            articles = int(match.group(1))

print()
print(f"Number of pages on website matching criteria: {pages}")
print(f"Number of articles on website matching criteria: {articles}")
print()

#delay = randint(1, 2)
#sleep(delay)






# #(IV) loop extractings links
rounds = 1
link_list = list()

for i in range(1, (int(pages) + 1)):
    print(f"Downloading Links: {rounds}/{pages}")
    results = search_global_times(search_title, i, search_body)
    links=extract(yml_links,results)
    #print(links)
    #if links is not None:
        #link_list.extend(links["links"])
    link_list.extend(links["links"])

    rounds = rounds + 1
    #delay = randint(1, 2)
    #sleep(delay)
    print()


#print(link_list)
print(f"Links: {len(link_list)} out of {articles} found articles.")
print()

#duplicate check
if len(link_list) != len(set(link_list)):
    print("There are duplicates in the list")
else:
    print("There are no duplicates in the list")






### (V) extract articles content

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
df_global_times = pd.DataFrame({
    "Published": [],
    "Author(s)": [],
    "Title": [],
    "Text": [],
    "Link": []
})



#test for one article
#url = 'https://www.globaltimes.cn/page/202302/1285106.shtml'
#r = requests.get(url)
#r = r.text
#content_1=extract(yml_articles, r)
#print(content_1)


#loop for article content
round_number = 1

for link in link_list:

    print(f"Article {round_number}/{articles}")

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
    #delay = randint(1, 2)
    #sleep(delay)
    print()



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
df_global_times['Published'] = df_global_times['Published'].apply(lambda x: convert_timestamp_to_date_string(x) if x is not None else None)
df_global_times['Published'] = df_global_times['Published'].apply(lambda x: pd.to_datetime(x) if x is not None else None)


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

df_global_times['Author(s)'] = df_global_times['Author(s)'].apply(lambda x: split_string(x) if x is not None else None).apply(pd.Series, dtype='object')


### (V) save as excel
from datetime import date
df_global_times.to_excel(f'Global_Times_{date.today()}.xlsx', sheet_name='articles')

print("***SUCCESSFULLY FINISHED CODE***")







