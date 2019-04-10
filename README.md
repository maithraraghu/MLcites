# MLcites

## Repository Overview
This repository contains:
1. Citation and author affiliation data of published papers in NeurIPS (2014 to 2018) and ICML (2017, 2018), collected March 31st 2019.
2. The script used to collect this data, which can be rerun or repurposed to collect data from other publication venues and years.

### Blogpost and Jupyter Notebook
For a detailed overview of the data and statistics on top cited papers, citation distributions, topic trends and academia/industry splits, check out the [blog post](TODO)!

The repository also contains a [jupyter notebook](https://github.com/rubai5/MLcites/blob/master/Paper_Statistics_Analysis.ipynb) with the code for the simple analyses outlined in the blogpost.

## Some Example Results: Accepted Papers, Top Cited Papers, Topic Trends
Below are some of the simpel results we can compute, taken from the [blog post]() and [jupyter notebook](https://github.com/rubai5/MLcites/blob/master/Paper_Statistics_Analysis.ipynb).

### Accepted Papers and Finding Citation Information
Collecting the data is a somewhat involved and noisy process (overviewed in detail below), and we can't find citation information for all the papers. But we don't do _too_ badly -- below is a plot of the total number of accepted papers, and the number we find citation information for:

![alt text](https://github.com/rubai5/MLcites/blob/master/Accepted_Paper_Statistics.png "NeurIPS Accepted Papers and Papers with Citations Data")

There's approximately 50 or so papers in any conference that we don't find citation information for.

### Top Cited Papers
We can also see what the top cited papers in our collected data are. Below is a picture of the top cited papers in our dataset from NeurIPS 2014, 2015 and 2016:

![alt text](https://github.com/rubai5/MLcites/blob/master/Most_Cited_Papers.png "The top cited papers from NeurIPS 2014, 2015, 2016.")

We can see the original GAN paper, seq2seq, Faster R-CNN for object detection and several others.

### Topic Trends
We can use the title information to study trends in different topics through the years. GANs are a nice case study, because as we saw above, the original paper was published in NeurIPS 2014, and since then the topic has been of huge interest to the community.

![alt text](https://github.com/rubai5/MLcites/blob/master/GAN_Trends.png "Number of GAN papers at NeurIPS over the years.")

Above are plots showing the total number of GAN papers and fraction of GAN papers at different years in NeurIPS. In 2014, there is only one paper, the original GAN paper, but by 2017, there are around _25_ GAN papers, comprising 3.5% of the conference!

### Further Results
Additional results on citation distributions and academia/industry breakdowns can be found in the blogpost and jupyter notebook.


## Details on the Data and Scraping Method
Here we overview the data as well as the scraping method and code.

### Data
The data was collected on March 31st 2019 (from running `get_statistics_allyears.py`) and is in files of form `results_<conference name>_<year>.p`, which are pickled pandas dataframes. 

### Scraping the Data
For each paper, the citation information and author affiliation is scraped from Google Scholar. It is somewhat tricky to scrape paper information directly (involves parsing javascript), but author profiles are much easier to search. Therefore, the script sequentially looks up the authors of a paper on Google Scholar, and goes through their publication list to try and see if they have a publication matching the name of the conference paper. Note the number of papers to search also has to be specificed, and currently the script looks at 200 of the most recent papers. 

If a match is found, the script updates the paper with the citation count and the found author's affiliation. To save time, the script does not look up all the authors of a paper, only the minimum number needed to find a citation. Note that the affiliation of the author is their _current_ affiliation, not necessarily the affiliation they had when they wrote the paper. We study this in detail when analyzing academia/industry breakdowns in the [blogpost](). 

The script to perform this scraping, `get_statistics_allyears.py` broadly consists of two parts. Two of the functions, `get_html` and `get_name_and_authors` are used to parse the [accepted papers](https://nips.cc/Conferences/2018/Schedule?type=Poster) page of NeurIPS and ICML. The `get_citations` function then tries to find citation and affilation information for each paper in turn.

Note that it should be relatively easy to scrape paper lists from other conferences, such as CVPR or ICLR. The `get_citations` function can then be used in conjunction with these to find citation information about these papers too. 

### Code Dependencies and Setup
The code to scrape the data is written for Python 3, and besides standard packages such as pandas, relies on the [scholarly](https://github.com/OrganicIrradiation/scholarly) package. **Note:** unfortunately, several functions in scholarly don't seem to be working anymore, due to changes in Google Scholar. We will make some edits to the installation to ensure it can retrieve author information. 

Instructions for Scraping the Data:
1. Install [scholarly](https://github.com/OrganicIrradiation/scholarly) and its dependencies.
2. In the `Author` class in `/usr/local/lib/python3.5/dist-packages/scholarly.py`, edit all occurences of `gsc_oai_<text>` to `gs_ai_<text>`.
3. Run the scraping script: e.g. `python3 get_statistics_allyears.py --conference=NeurIPS --year=2016`


## Open Questions and Future Work
We overview several open questions in the blogpost. Some scraper specific ones: it would be very interesting to see this analysis applied to other publishing venues. It would also be interesting to see if affiliations at time of publishing could be scraped to get a better sense of the shift from academia/industry.

I hope this is a useful resource for the community!
