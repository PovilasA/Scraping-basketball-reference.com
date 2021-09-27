
# coding: utf-8

# In[78]:


# import needed libraries
from urllib.request import urlopen
from bs4 import BeautifulSoup
import pandas as pd# create a function to scrape team performance for multiple years


# In[84]:


# urllib.quote(".")

import urllib.parse

url = "https://www.basketball-reference.com/international/players/edgaras-ulanovas-1/gamelog/2021/euroleague.html"
urllib.parse.quote(url, safe='')


# In[23]:




def scrape_NBA_team_data(years = [2017, 2018]):
    
    final_df = pd.DataFrame(columns = ["Year", "Team", "W", "L",
                                       "W/L%", "GB", "PS/G", "PA/G",
                                       "SRS", "Playoffs",
                                       "Losing_season"])
    
    # loop through each year
    for y in years:        # NBA season to scrape
        year = y
        
        # URL to scrape, notice f string:
        url = f"https://www.basketball-reference.com/leagues/NBA_{year}_standings.html"
        
        # collect HTML data
        html = urlopen(url)
#         return(html)
        
        # create beautiful soup object from HTML
        soup = BeautifulSoup(html)#, features="lxml")
        
        # use getText()to extract the headers into a list
        titles = [th.getText() for th in soup.findAll('tr', limit=2)[0].findAll('th')]
        
        # first, find only column headers
        headers = titles[1:titles.index("SRS")+1]
        
        # then, exclude first set of column headers (duplicated)
        titles = titles[titles.index("SRS")+1:]
        
        # next, row titles (ex: Boston Celtics, Toronto Raptors)
        try:
            row_titles = titles[0:titles.index("Eastern Conference")]
        except: row_titles = titles
        # remove the non-teams from this list
        for i in headers:
            row_titles.remove(i)
        row_titles.remove("Western Conference")
        divisions = ["Atlantic Division", "Central Division",
                     "Southeast Division", "Northwest Division",
                     "Pacific Division", "Southwest Division",
                     "Midwest Division"]
        for d in divisions:
            try:
                row_titles.remove(d)
            except:
                print("no division:", d)
        
        # next, grab all data from rows (avoid first row)
        rows = soup.findAll('tr')[1:]
        team_stats = [[td.getText() for td in rows[i].findAll('td')]
                    for i in range(len(rows))]
        # remove empty elements
        team_stats = [e for e in team_stats if e != []]
        # only keep needed rows
        team_stats = team_stats[0:len(row_titles)]
        
        # add team name to each row in team_stats
        for i in range(0, len(team_stats)):
            team_stats[i].insert(0, row_titles[i])
            team_stats[i].insert(0, year)
            
        # add team, year columns to headers
        headers.insert(0, "Team")
        headers.insert(0, "Year")
        
        # create a dataframe with all aquired info
        year_standings = pd.DataFrame(team_stats, columns = headers)
        
        # add a column to dataframe to indicate playoff appearance
        year_standings["Playoffs"] = ["Y" if "*" in ele else "N" for ele in year_standings["Team"]]
        # remove * from team names
        year_standings["Team"] = [ele.replace('*', '') for ele in year_standings["Team"]]
        # add losing season indicator (win % < .5)
        year_standings["Losing_season"] = ["Y" if float(ele) < .5 else "N" for ele in year_standings["W/L%"]]
        
        # append new dataframe to final_df
        final_df = final_df.append(year_standings)
        
    # print final_df
    print(final_df.info)
    return(final_df)
    # export to csv
#     final_df.to_csv("nba_team_data.csv", index=False)


# In[82]:


# html = scrape_NBA_team_data(years = [
#                               2015, 2016, 2017, 2018, 2019])


# In[26]:


###################


# In[89]:


url


# In[130]:





# In[175]:


final_df = pd.DataFrame(columns = ["Year", "Team", "W", "L",
                               "W/L%", "GB", "PS/G", "PA/G",
                               "SRS", "Playoffs",
                               "Losing_season"])

player = 'Edgaras Ulanovas'

# URL to scrape, notice f string:
url = f"https://www.basketball-reference.com/leagues/NBA_{year}_standings.html"
player_for_url = player.replace(' ', '-').lower()
url = "https://www.basketball-reference.com/international/players/edgaras-ulanovas-1/gamelog/2021/euroleague/"
url = f"https://www.basketball-reference.com/international/players/{player_for_url}-1/gamelog/2021/euroleague/"
# url = urllib.parse.quote(url, safe='')
# url = "https://www.basketball-reference.com/international/euroleague/2021.html"



# collect HTML data
html = urlopen(url)

# create beautiful soup object from HTML
soup = BeautifulSoup(html)#, features="lxml")

# use getText()to extract the headers into a list
headers = [th.getText() for th in soup.findAll('tr', limit=2)[0].findAll('th')]
headers[3] = 'H/A'
headers[5] = 'W/L'

# next, grab all data from rows (avoid first row)
rows = soup.findAll('tr')[1:]
team_stats = [[td.getText() for td in rows[i].findAll('td')]
            for i in range(len(rows))]

# remove empty elements
team_stats = [e for e in team_stats if e != []]
# only keep needed rows
# team_stats = team_stats[0:len(row_titles)]

# add team name to each row in team_stats
for i in range(0, len(team_stats)):
    team_stats[i].insert(0, player)
#     team_stats[i].insert(0, year)

# create a dataframe with all aquired info
player_stats = pd.DataFrame(team_stats, columns = headers).apply(pd.to_numeric, errors='ignore')


# player_stats


# In[176]:


d = player_stats


# In[177]:


d


# In[ ]:


# Fantasy žaidimo taškai duodami už:

#     Pelnytas taškas +1
#     Gynyboje atkovotas kamuolys +1
#     Puolime atkovotas kamuolys +1.5
#     Rezultatyvus perdavimas +1.5
#     Perimtas kamuolys +1.5
#     Klaida -1.5
#     Blokuotas metimas +1.5
#     Gautas blokas -0.5
#     Dvigubas dublis +10
#     Trigubas dublis +30
#     Keturgubas dublis +100
#     Penki vienetai trijose skirtingose kategorijos (iš šių: taškai, perdavimai, atkovoti kamuoliai, perimti kamuoliai, blokuoti metimai) +10 (pvz.: 7 taškai, 5 perimti kam., 6 atkovot kam.)
#     Penki vienetai keturiose skirtingose kategorijos +20 (pvz.: 7 taškai, 5 perimti kam., 6 atkovot kam., 8 rez. perdavimai)
#     Penki vienetai penkiose skirtingose kategorijos +50 (pvz.: 7 taškai, 5 perimti kam., 6 atkovot kam., 8 rez. perdavimai, 5 blokai)
#     Komandos pergalė +3
#     Komandos pralaimėjimas -3
#     Pramestas metimas -1
#     Pramestas baudos metimas -1
#     Išprovokuota pražanga +1
#     Išnaudotas asmeninių pražangų limitas (5)-5


# In[301]:


p = 11
r = 1
a = 7
s = 5
b = 5

def count_number_of_5(p,r,a,s,b):
    return(
           (1 if len(str(p))==2 else 0) + \
           (1 if len(str(r))==2 else 0) + \
           (1 if len(str(a))==2 else 0) + \
           (1 if len(str(s))==2 else 0) + \
           (1 if len(str(b))==2 else 0)
    )

def count_number_of_5(p,r,a,s,b):
    return(
           (1 if (p >= 5 and p < 10) else 0) + \
           (1 if (r >= 5 and r < 10) else 0) + \
           (1 if (a >= 5 and a < 10) else 0) + \
           (1 if (s >= 5 and s < 10) else 0) + \
           (1 if (b >= 5 and b < 10) else 0)
    )

count_number_of_5(p,r,a,s,b)    
    
# 50 if () else 0



# In[316]:


d['PTS'] + d['DRB']+ 1.5*d['ORB'] + 1.5*d['AST'] + 1.5*d['STL'] - 1.5*d['TOV'] + 1.5*d['BLK'] + [10 if (min(p,r)>=10 and a<10) | (min(p,a)>=10 and r<10) |(min(r,a)>=10 and p<10) else 0 for p,r,a  in zip(d['PTS'],d['TRB'],d['AST'])] + [30 if (min(p,r,a)>=10) else 0 for p,r,a in zip(d['PTS'],d['TRB'],d['AST'])] + [10 if (count_number_of_5(p,r,a,s,b)==3) else 0 for p,r,a,s,b in zip(d['PTS'],d['TRB'],d['AST'],d['STL'],d['BLK'])] + [20 if (count_number_of_5(p,r,a,s,b)==4) else 0 for p,r,a,s,b in zip(d['PTS'],d['TRB'],d['AST'],d['STL'],d['BLK'])] + [50 if (count_number_of_5(p,r,a,s,b)==4) else 0 for p,r,a,s,b in zip(d['PTS'],d['TRB'],d['AST'],d['STL'],d['BLK'])] + [3 if x == 'W' else -3 for x in d['W/L']] - (d['FGA'] - d['FG']) - (d['FTA'] - d['FT']) - d['PF'] + d['FTA']*3/4 # instead of fouls received


# missing gautas blokas

