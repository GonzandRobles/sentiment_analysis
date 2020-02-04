import pandas as pd
import seaborn as sns
import matplotlib.ticker as ticker
from wordcloud import WordCloud
import matplotlib.pyplot as plt
import string
import matplotlib.ticker as ticker
import nltk
from nltk import pos_tag
from nltk import FreqDist
from nltk.corpus import stopwords
from nltk.tokenize import WhitespaceTokenizer
from nltk.stem import WordNetLemmatizer
from nltk.corpus import wordnet
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from sklearn.feature_extraction.text import CountVectorizer
#nltk.download('vader_lexicon')
from textblob import TextBlob

df = pd.read_csv('/Users/gonzandrobles/Desktop/Python/ipynb_notebooks/other_projects/nlp_projects/capstone_project/reviews.csv')


def column_cleaner(df):
    '''
    Takes a df as input and:
    1. deletes de index column since it's unnecessary
    2. changes the format of date to datatime
    3. add a "," next to the city removing "|" 
    4. some reviesw have the string "\ao" so it needs to be removed from the review.
    '''
    del df['index']
    # rename columns to delete white space from the column names
    df.columns = ['username', 'location', 'date', 'rating', 'content']
    df['date'] = pd.to_datetime(df['date'])
    df['location'] = df['location'].apply(lambda x: x.replace('|', ','))
    df['content'] = df['content'].apply(lambda x: x.replace('\xa0', ''))
    return df

def clean_data(df):
    '''unifies all the column changes from column_cleaner
    to be applied to the dataframe'''
    df = column_cleaner(df)
    return df

def dist_chart(df):
    '''
    This function creates a plot where on the left side
    we have the percentage distribution and on the right side
    the count distribution
    
    input:
    df
    
    output:
    bar plot
    '''
# checking for the ratio of rating
    # event column dimensions
    ncount = df['rating'].shape[0]

    # setting figure size to 8 by 4
    plt.figure(figsize=(8,4))
    # countplot where x is 'rating' and the data is 'df'
    ax = sns.countplot(x="rating", data=df)
    # setting the title of the chart
    plt.title('Distribution of Ratings')
    plt.xlabel('Ratings')

    # Make twin axis
    ax2=ax.twinx()

    # switch so count axis is on right, frequency on left
    ax2.yaxis.tick_left()
    ax.yaxis.tick_right()

    # switch the labels over
    ax.yaxis.set_label_position('right')
    ax2.yaxis.set_label_position('left')

    # frrequency label
    ax2.set_ylabel('Frequency [%]')

    for p in ax.patches:
        x=p.get_bbox().get_points()[:,0]
        y=p.get_bbox().get_points()[1,1]
        ax.annotate('{:.1f}%'.format(100.*y/ncount), (x.mean(), y), 
                ha='center', va='bottom') # set the alignment of the text


    # Use a LinearLocator to ensure the correct number of ticks
    ax.yaxis.set_major_locator(ticker.LinearLocator(10))

    # Fix the frequency range to 0-100
    ax2.set_ylim(0,100)
    ax.set_ylim(0,ncount)

    # And use a MultipleLocator to ensure a tick spacing of 10
    ax2.yaxis.set_major_locator(ticker.MultipleLocator(10))

    # Need to turn the grid on ax2 off, otherwise the gridlines end up on top of the bars
    ax2.grid(None)
    
def count_punct(text):
    '''
    Counts the number of punctuations the corpus has
    input:
    str
    
    output:
    str
    '''
    count = sum([1 for char in text if char in string.punctuation])
    return round(count/(len(text) - text.count(" ")), 3)*100

def show_wordcloud(data, title = None):
    '''
    Returns a wordcloud with the most common words in the corpus
    
    input:
    dataset -> dataset where the words are coming out 
    str -> title of the word cloud
    
    output:
    words cloud with words
    '''
    wordcloud = WordCloud(
        background_color = 'white',
        max_words = 200,
        max_font_size = 40, 
        scale = 3,
        random_state = 42
    ).generate(str(data))

    fig = plt.figure(1, figsize = (20, 20))
    plt.axis('off')
    if title: 
        fig.suptitle(title, fontsize = 20)
        fig.subplots_adjust(top = 2.3)

    plt.imshow(wordcloud)
    plt.show()
    

def get_wordnet_pos(pos_tag):
    '''
    return the wordnet object value corresponding to the POS tag
    '''
    if pos_tag.startswith('J'):
        return wordnet.ADJ
    elif pos_tag.startswith('V'):
        return wordnet.VERB
    elif pos_tag.startswith('N'):
        return wordnet.NOUN
    elif pos_tag.startswith('R'):
        return wordnet.ADV
    else:
        return wordnet.NOUN    

    
def clean_text(text):
    '''
    Returns the corpus in lowercase, without punctuation marks, 
    stopwords and lemmatize.
    '''
    # lower text
    text = text.lower()
    # tokenize text and removes puncutation
    text = [word.strip(string.punctuation) for word in text.split(" ")]
    # remove words that contain numbers
    text = [word for word in text if not any(c.isdigit() for c in word)]
    # remove stop words
    stop = stopwords.words('english')
    text = [x for x in text if x not in stop]
    # remove empty tokens
    text = [t for t in text if len(t) > 0]
    # pos tag text
    pos_tags = pos_tag(text)
    # lemmatize text
    text = [WordNetLemmatizer().lemmatize(t[0], get_wordnet_pos(t[1])) for t in pos_tags]
    # remove words with only one letter
    text = [t for t in text if len(t) > 1]
    # join all
    text = " ".join(text)
    return(text)

def pie_chart(df, col):
    '''
    Pie chart of sentiment Polarity
    Categorize Polarity into Positive, Neutral or Negative
    
    input:
    
    df -> dataframe
    col -> str name of column
    '''
    labels = ["Negative", "Neutral", "Positive"]
    #Initialize count array
    values =[0,0,0]

    #Categorize each review
    for review in df[col]:
        sentiment = TextBlob(review)

        #Custom formula to convert polarity 
        # 0 = (Negative) 1 = (Neutral) 2=(Positive)
        polarity = round(( sentiment.polarity + 1 ) * 3 ) % 3

        #add the summary array
        values[polarity] = values[polarity] + 1

    print("Final summarized counts :", values)

    #Set colors by label
    colors=["Green","Blue","Red"]

    print("\n Pie Representation \n-------------------")
    #Plot a pie chart
    plt.pie(values, labels=labels, colors=colors, \
            autopct='%1.1f%%', shadow=True, startangle=140)
    plt.axis('equal')
    plt.show()


def get_top_n_words(corpus, n=None):
    """
    List the top n words in a vocabulary according to occurrence in a text corpus.
    """
    vec = CountVectorizer().fit(corpus)
    bag_of_words = vec.transform(corpus)
    sum_words = bag_of_words.sum(axis=0) 
    words_freq = [(word, sum_words[0, idx]) for word, idx in     vec.vocabulary_.items()]
    words_freq =sorted(words_freq, key = lambda x: x[1], reverse=True)
    return words_freq[:n]