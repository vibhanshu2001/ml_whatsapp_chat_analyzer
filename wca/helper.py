from urlextract import URLExtract
import pandas as pd
from collections import Counter
import emoji
import re
extract = URLExtract()

def fetch_stats(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]
    num_messages = df.shape[0]
        #number of words
    words = []
    for message in df['message']:
        words.extend(message.split())


    num_stickers = df[df['message'] == 'sticker omitted\n'].shape[1]
    num_images = df[df['message'] == 'image omitted\n'].shape[1]
    num_docs = df[df['message'].str.contains("document omitted")]
    links = []
    for message in df['message']:
        links.extend(extract.find_urls(message))
    
    return num_messages, len(words), num_stickers, num_images, len(links), len(num_docs)


def most_busy_users(df):
    x = df['user'].value_counts().head()
    df = round((df['user'].value_counts()/df.shape[0])*100,2).reset_index().rename(columns={'index':'name','user':'percent'})
    return x,df


def most_common_words(selected_user, df):
    f = open('stop_words.txt','r')
    stop_words = f.read()
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]
    
    temp = df[df['message']!='sticker omitted\n']
    temp = temp[temp['message']!='image omitted\n']
    words = []
    for message in temp['message']:
        for word in message.lower().split():
            if word not in stop_words:
                words.append(word)
                    
                  
    most_common_df = pd.DataFrame(Counter(words).most_common(20))
    return most_common_df

