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
    except Exception:
        return "Error opening url"

    title = re.search(r'<title>(.+)</title>', page)
    if title is None:
        return "Title not found"

    return title.group(1)

def chatstring2JSON(chatstring):
    """
    Parses chat string and returns details as JSON string
    """
    results = {}
    mentions = []
    emoticons = []
    links = []

    # Find metions, emoticons, and links
    for token in chatstring.split():
        mention = re.match(r'@(\w+)', token)
        if mention is not None:
            mentions.append(mention.group(1))
            continue
        
        emoticon = re.match(r'\((\w{,15})\)', token)
        if emoticon is not None:
            emoticons.append(emoticon.group(1))
            continue

        link = re.match(r'https?://\S+', token)
        if link is not None:
            url = link.group(0)
            title = getTitle(url)
            links.append({'url': url, 'title': title})
            continue

    # Add mentions to result
    if len(mentions) > 0:
        results['mentions'] = mentions

    # Add emoticons to result
    if len(emoticons) > 0:
        results['emoticons'] = emoticons

    # Add links to result
    if len(links) > 0:
        results['links'] = links

    return json.dumps(results, indent=4)
        

if __name__ == '__main__':
    argparser = argparse.ArgumentParser(description='Parses chat string and returns details as JSON string')
    argparser.add_argument('chatstring', type=str, help='Chat string to parse')

    args = argparser.parse_args()

    print chatstring2JSON(args.chatstring)
    
