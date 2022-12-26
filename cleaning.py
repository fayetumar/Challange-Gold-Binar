import re

def lowercase(text):
    return text.lower()

def remove_unnecessary_char(text):
    text = re.sub(r'\\n',' ',text) # remove every '\n'
    text = re.sub('rt','',text) # Remove every retweet symbol
    text = re.sub('user','',text) # Remove every username
    text = re.sub('url','',text) # Remove every url
    text = re.sub(';',' ',text) #remove every';'
    text = re.sub('((www\.[^\s]+)|(https?://[^\s]+)(http?://[^\s]+))',' ',text) # Remove every URL
    text = re.sub(' +',' ',text) #Remove extra spaces
    text = re.sub('\d+\.\s',' ',text) #remove every '\d+\.\s'
    text = re.sub('[,1]{2,}','',text)
    text = re.sub('[,0]{2,}','',text)
    text = re.sub(r'x[a-z0-9][a-z0-9]',' ',text)
    return text
    
def remove_nonaplhanumeric(text):
    text = re.sub(r'[^0-9a-zA-Z\?!,.]+',' ',text)
    text = re.sub('"','',text)
    text = re.sub('\s\s+',' ',text)
    text = re.sub('^\s','',text)
    return text

def remove_duplicateexclamation(text):
    text = re.sub(r'[!]{2,}','!',text)
    text = re.sub(r'[\?]{2,}','?',text)
    text = re.sub(r'(! ){2,}','!',text)
    text = re.sub(r'(\? ){2,}','?',text)
    text = re.sub(r',{2,}',',',text)
    text = re.sub(r'\.{2,}',',',text)
    return text

def preprocess(text):
    text = lowercase(text)
    text = remove_unnecessary_char(text)
    text = remove_nonaplhanumeric(text)
    text = remove_duplicateexclamation(text)
    return text