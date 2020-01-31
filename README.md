# Coffee shop sentiment analysis

# Introduction:

Sentiment Analysis of yelp reviews using bs4 for web scrapping to analyze customers reviews and make a sentiment analysis.

1. Libraries:

* pandas
* numpy
* string module
* matplotlib
* seaborn
* from functions import clean_data
* nltk
* from nltk import pos_tag
* from nltk import FreqDist
* from nltk.corpus import stopwords
* from nltk.tokenize import WhitespaceTokenizer
* from nltk.stem import WordNetLemmatizer
* from nltk.corpus import wordnet
* from nltk.sentiment.vader import SentimentIntensityAnalyzer
* from sklearn.feature_extraction.text import CountVectorizer
* #nltk.download('vader_lexicon')
* from textblob import TextBlob

For web scrapping:

* BeautifulSoup
from urllib.request import urlopen as uReq
* requests
* re
* csv
* time
* random

2. Project Motivation

I've been working in coffee shops for the last 6 years and I'm always interested in what customers think about the customer service, coffee flavor, location, etc. I constantly check for customer reviews to get an idea of what's happening on the other side of the counter, that's why, for my last project of the Data Science NanoDegree I decided to work on a sentiment analysis using the customers reviews from Yelp. I'm basing this project on simple questions:

* What is the distribution of good reviews vs bad reviews using VADER S.A.
* What is the polarity and subjectivity of all the reviews
* Compared to the initial data exploration, does the metrics match the models metrics?


3. Files Description

* functions.py -> this script contains the function that cleans the raw dataset scrapped from Yelp
* web_scrapping.py -> contains the code used to scrape the reviews from yelp
* reviews.csv -> csv file with the reviews
* sentiment_analysis.ipynb -> contains the data analysis and modeling of the project.

4. How to interact with the project

The way to go through this notebook is to start with the loading data setup. Run the exploratory data analysis code lines, proceed to modeling for an understanding of the distributions of the data. There is no need to use the web_scrapping.py file since the dataset is already included in the package. 

I'm happy to receive feedback and suggestions for better readability, cleaner code or even more analysis ideas or ML model suggestions.

5. Authors

I'm the only one who has contributed to this repository so far, but I want to mention some sources where I got the ideas for this repository, starting with Bluebeard Coffee Roasters in Tacoma that provided the inspiration for this project and to Yelp.

You can also see my Medium analysis of this project on this link: 

https://medium.com/@GonzandRobles25/coffee-shop-sentiment-analysis-dbf8d3c333e

6. License

MIT license
License
Copyright 2020 © Eduardo González.

## License

[![License](http://img.shields.io/:license-mit-blue.svg?style=flat-square)](http://badges.mit-license.org)

- **[MIT license](http://opensource.org/licenses/mit-license.php)**
- Copyright 2020 © <a href="https://medium.com/@GonzandRobles25" target="_blank">Eduardo Gonzalez</a>.
