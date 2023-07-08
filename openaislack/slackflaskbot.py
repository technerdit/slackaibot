from slackeventsapi import SlackEventAdapter
from slack_sdk.web import WebClient
import openai
import os

# Our app's Slack Event Adapter for receiving actions via the Events API
slack_signing_secret = os.environ['SLACK_SIGNING_SECRET']
slack_events_adapter = SlackEventAdapter(slack_signing_secret, "/slack/events")
openai.api_key = os.environ['OPENAI_API_KEY']
# Create a SlackClient for your bot to use for Web API requests
slack_bot_token = os.environ['SLACK_BOT_TOKEN']
slack_client = WebClient(slack_bot_token)


def openaiapi(question=None):
    response = openai.Completion.create(
        model="text-davinci-003",
        prompt=question,
        temperature=0.5,
        max_tokens=150,
        top_p=1.0,
        frequency_penalty=0.0,
        presence_penalty=0.0
    )
    for line in response['choices']:
        return line['text']


@slack_events_adapter.on("app_mention")
def handle_mentions(event_data):
    event = event_data["event"]
    if "?" in event['text']:
        print(event['text'])
        response = openaiapi(question=event['text'])
        channel = event["channel"]
        message = "<@{}> {}".format(event["user"], response)
        slack_client.chat_postMessage(channel=channel, text=message)


# Error events
@slack_events_adapter.on("error")
def error_handler(err):
    print("ERROR: " + str(err))


# Once we have our event listeners configured, we can start the
# Flask server with the default `/events` endpoint on port 3000
slack_events_adapter.start(port=8000)
