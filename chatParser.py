import argparse
import re
import json
import urllib2

def getTitle(url):
    """
    Gets title from webpage
    """
    title = None
    try:
        page = urllib2.urlopen(url).read()
    except Exception, err:
        print err
        return "Title not found"

    title = re.search(r'<title>(.+)</title>', page)
    return title.group(1)

def chatstring2JSON(chatstring):
    """
    Parses chat string and returns details as JSON string
    """
    results = {}

    # Find mentions
    mentions = []
    for mention in re.finditer(r'@\w+', chatstring):
        mentions.append(mention.group(0).replace('@',''))

    # Add mentions to result
    if len(mentions) > 0:
        results['mentions'] = mentions

    # Find emoticons
    emoticons = []
    for emoticon in re.finditer(r'\((\w{,15})\)', chatstring):
        emoticons.append(emoticon.group(1))
    
    # Add emoticons to result
    if len(emoticons) > 0:
        results['emoticons'] = emoticons

    # Find links
    links = []
    for link in re.finditer(r'https?://\S+', chatstring):
        url = link.group(0)
        title = getTitle(url)
        links.append({'url': url, 'title': title})

    # Add links to result
    if len(links) > 0:
        results['links'] = links

    return json.dumps(results, indent=4)
        

if __name__ == '__main__':
    argparser = argparse.ArgumentParser(description='Parses chat string and returns details as JSON string')
    argparser.add_argument('chatstring', type=str, help='Chat string to parse')

    args = argparser.parse_args()

    print chatstring2JSON(args.chatstring)
    
