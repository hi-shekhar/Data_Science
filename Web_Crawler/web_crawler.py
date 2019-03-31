# Get the webpage from the provided url
import requests
# library for pulling data out of HTML and XML files
from bs4 import BeautifulSoup
# (Comma Separated Values) format is the most common import and export format for spreadsheets and databases
import csv
#  Import regular expression
import re

# url of  the website
url = 'https://www.imdb.com/chart/top?ref_=nv_mv_250'
# Recieved response from the provided url
response = requests.get(url)
'''
The BeautifulSoup constructor function takes in two string arguments:
1. The HTML string to be parsed
2. Optionally, the name of a parser
'''
soup = BeautifulSoup(response.text,'html.parser').body
print(type(soup))
# fina_all will return collection of tag whose name is table
table_data = soup.findAll(lambda tag: tag.name == 'table')

# List of variable used in code
imdb_header_list = []
imdb_filtered_header_list  = [];
rank_title_split = [];
header_found = False;
headers = []
tbody_found = False;

# Clean the  data after removing unwanted data
def clean_header(item):
    if(item == 'Rank & Title'):
        rank_title_split = re.split('[&]', item)
        return rank_title_split
    else:
        return item

#  open in imdb_movie_ranking.csv in write mode and with condition to override newline as empty
with open('imdb_movie_ranking.csv', 'w', newline='') as writeFile:
    writer = csv.writer(writeFile)
    for each_section in table_data:
        # if header is found one more time then do not enter in this code segment
        if(header_found == False):
            for headerIdx , th_section in enumerate(each_section.findAll('th')):
                header_found = True
                # get_text() returns all the text in a document or beneath a tag, as a single Unicode string:
                if (th_section.get_text()):
                    imdb_header_list.insert(headerIdx,th_section.get_text())
                else:
                    imdb_header_list.insert(headerIdx,False)
            # filter our false from imdb_header_list
            imdb_filtered_header_list =  filter(bool, imdb_header_list)
            # perform cleaning in imdb_header_list
            imdb_filtered_header_list = [clean_header(item) for item in imdb_filtered_header_list]
            # segregate the imdb_filtered_header_list into final list (headers)
            for data in imdb_filtered_header_list:
                if isinstance(data, list):
                    for split_data in data:
                        headers.append(split_data.replace(' ',''))
                elif(data == 'IMDb Rating'):
                    headers.append('Release Year')
                else:
                    headers.append('IMDb Rating')
            # print(headers)
            # write header into csv file
            writer.writerow(headers)
        # if tbody is found one more time then do not enter in this code segment
        if(tbody_found == False):
            for tbody_section in each_section.findAll("tbody", {"class": "lister-list"}):
                tbody_found = True
                for row in tbody_section.find_all('tr'):
                    rank_name_year = ''
                    split_rank_name_year = []
                    data = row.find_all("td")
                    # strip whitespace from the beginning and end of each bit of text:
                    rank_name_year = data[1].get_text(" ",strip=True)
                    imdb_rating = data[2].get_text(" ",strip=True);
                    # convert rank_name_year into list by splitting on the basis of . and ()
                    split_rank_name_year=  re.split('[.()]', rank_name_year)
                    movie_rank = split_rank_name_year[0]
                    movie_name = split_rank_name_year[1].replace(' ','')
                    release_year = split_rank_name_year[2].replace(' ','')
                    # print(movie_rank +' '+movie_name+' '+release_year+' '+imdb_rating)
                    # write tbody required data into csv file
                    writer.writerow([movie_rank,movie_name,release_year,imdb_rating])
