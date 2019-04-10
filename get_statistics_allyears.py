import numpy as np
import scholarly
from bs4 import BeautifulSoup
from urllib.request import urlopen
import pandas as pd
import pickle
import argparse

# global definition of Google Scholar's author page, sorted by date
_AUTHPAGE = '/citations?hl=en&user={0}&view_op=list_works&sortby=pubdate&cstart=0&pagesize=200'

def get_html(url):
    # gets the raw html for the webpage
    return urlopen(url)

def get_name_and_authors(html):
    # takes in html, parses with beautiful soup
    # adds paper name/author names to dataframe
    output = pd.DataFrame(columns=["name", "authors", "citations", "affiliations"])
    
    soup = BeautifulSoup(html, 'html.parser')
    clumped_tags = soup.find_all('div', attrs={"class": "maincard narrower Poster"})
    for t in clumped_tags:
        pname = t.find('div', attrs={"class": "maincardBody"}).text.strip()
        araw = t.find('div', attrs={"class": "maincardFooter"}).text.strip()
        anames = araw.split(' · ')
        output = output.append({"name" : pname, "authors" : anames},ignore_index=True)
    
    return output

def author_paper_citations(df, adata, pname, i):
    # helper function to try and get citations for one paper
    updated = False
    url = _AUTHPAGE.format(scholarly.requests.utils.quote(adata.id))
    soup = scholarly._get_soup(scholarly._HOST+url)
    
    clumped_tags = soup.find_all('tr', attrs={"class":"gsc_a_tr"})
    for t in clumped_tags:
        cname = t.find('a', attrs={"class":"gsc_a_at"}).text.strip().lower().replace(" ","")
        if cname == pname:
            # try to find citations
            try:
                cites = t.find('a', attrs={"class":"gsc_a_ac gs_ibl"}).text.strip()
                if cites == "":
                    cites = 0
                else:
                    cites = int(cites)
                df['citations'][i] = cites
                df['affiliations'][i] = adata.affiliation
                updated = True
            except AttributeError:
                if t.find('a', attrs={"class":"gsc_a_ac gs_ibl"}) == None:
                    print("couldn't find citations for, author", adata.name) 
                    print("source paper name, found name", pname, cname)
            break
    return df, updated 

def get_citations(df):
    # get paper citations from Google Scholar using paper and author names
    for i in range(len(df)):
        praw = str(df["name"][i])
        pname = praw.lower().replace(" ", "")
        authors = df["authors"][i]
        print("step , paper name, authors", i, praw, authors)
    
        for author in authors:
            try:
                adata = next(scholarly.search_author(author))
                print("Found author data", adata.name)
                df, updated = author_paper_citations(df, adata, pname, i)
            except StopIteration:
                continue
            if updated:
                print("Successfully updated df for paper, with author", pname, adata.name)
                break
        print("")
    return df
                    
                
if __name__ == "__main__":
    
    # parse command line args
    parser = argparse.ArgumentParser()
    parser.add_argument("--year", help="Conference year", 
                        default="2018")
    parser.add_argument("--conference", help="Either ICML or NeurIPS",
                        default="NeurIPS")
    args = parser.parse_args()

    if args.conference == "NeurIPS":
        _URL = "https://nips.cc/Conferences/%s/Schedule"%str(args.year)
    if args.conference == "ICML":
        _URL = "https://icml.cc/Conferences/%s/Schedule"%str(args.year)

    html = get_html(_URL)
    df = get_name_and_authors(html)
    df = get_citations(df)

    with open("./results_%s_%s.p"%(args.conference, args.year), "wb") as f:
        pickle.dump(df, f)
                
            
        
