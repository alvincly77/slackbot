import slack
import os 
from pathlib import Path
from dotenv import load_dotenv
from flask import Flask, request, Response
from slackeventsapi import SlackEventAdapter

env_path = Path('.') / '.env'
load_dotenv(dotenv_path=env_path)

app =  Flask(__name__)
slack_event_adapter = SlackEventAdapter(
  os.environ['SIGNING_SECRET'],'/slack/events', app)

client = slack.WebClient(token=os.environ['SLACK_TOKEN'])
BOT_ID = client.api_call("auth.test")['user_id']

#Event Based
@slack_event_adapter.on('message')
def message(payload):
    #print(payload)
    event = payload.get('event', {})
    channel_id = event.get('channel')
    user_id = event.get('user')
    text = event.get('text')
    if BOT_ID != user_id:
      if user_id in message_counts:
        message_counts[user_id] += 1
      else:
        message_counts[user_id] = 1
      client.chat_postMessage(channel='#test', text=text)

#Slack Commands
message_counts = {'user_id' : 0}

class WelcomeMessage:
    def __init__(self, channel, user):
        self.channel = channel
        self.user = user
        self.icon_emoji = ':robot_face'
          
        
        





@app.route('/message-count', methods=['POST'])
def message_count():
    data = request.form
    user_id = data.get('user_id')
    channel_id = data.get('channel_id')
    message_count = message_counts.get(user_id, 0)
    client.chat_postMessage(channel=channel_id, text=f"Messsage: {message_count}")
    # print(data)
    return Response(), 200

if __name__ == "__main__":
  app.run(debug=True)