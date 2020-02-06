from flask import Flask, request
#from twilio import twiml
from twilio.twiml.messaging_response import Message, MessagingResponse
from newsapi import NewsApiClient

app = Flask(__name__)

class Articles:
    def __init__(self, title, content, url):
        self.title = title
        self.content = content
        self.url = url

    def getTitle(self):
        return self.title

    def getContent(self):
        return self.content

    def getURL(self):
        return self.url


@app.route('/sms', methods=['POST'])
def sms():
    number = request.form['From']   #phone number from where message is recieved
    message_body = request.form['Body']   #contents of the message

    if '-' in message_body:
        region = message_body[message_body.find('-')+1:]
        topic = message_body[:message_body.find('-')]
    else:
        topic = message_body

    country_code_map = {"+1": "us", "+91": "in"}

    country = country_code_map[number[:2]]

    resp = MessagingResponse()  #MessagingResponse allows sending SMS back to the user

    # Initialize news api
    news = NewsApiClient(api_key='37e3b46e93db4c4fb65d31d1b677f131')

    top_headlines = news.get_everything(q=message_body, sources='bbc-news, bbc-sport, bleacher-report, bloomberg, cnbc, espn, the-new-york-times, the-wall-street-journal, the-washington-post', language='en', sort_by='relevancy', page=1, page_size=5)   #get the headlines related to the topic in the message
    #print(top_headlines)
    #print(news.get_sources())

    response_message = 'Top headlines about {} are as follows:\n '.format(topic)

    i = 0
    while ( i < 4 ):

        article = Articles(top_headlines["articles"][i]["title"], top_headlines["articles"][i]["content"], top_headlines["articles"][i]["url"])

        #add the contents for the first article
        response_message += str(i) + ". {} \n".format(article.getTitle()) + "-> {}\n".format(article.getContent())
        response_message += "Source: {}\n\n".format(article.getURL())

        i += 1

    resp.message(response_message)     #send back the SMS with the following content

    return str(resp)

if __name__ == '__main__':
    app.run()
