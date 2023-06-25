from slackeventsapi import SlackEventAdapter
from slack_sdk.web import WebClient
import openai
import json
import os

# Our app's Slack Event Adapter for receiving actions via the Events API
slack_signing_secret = "1565979a435515ba264939478921f35e"
slack_events_adapter = SlackEventAdapter(slack_signing_secret, "/slack/events")
openai.api_key = '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'
# Create a SlackClient for your bot to use for Web API requests
slack_bot_token = "xoxb-928934584657-5242865570663-BLtxYuzJ8yVrbo8JIQIU3osN"
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


# Example responder to bot mentions
@slack_events_adapter.on("app_mention")
def handle_mentions(event_data):
    event = event_data["event"]
    slack_client.chat_postMessage(
        channel=event["channel"],
        text=f"You said:\n>{event['text']}",
    )


# Example responder to greetings
@slack_events_adapter.on("message")
def handle_message(event_data):
    message = event_data["event"]
    # If the incoming message contains "hi", then respond with a "Hello" message
    if message.get("subtype") is None and "?" in message.get('text'):
        response = openaiapi(question=message.get('text'))
        channel = message["channel"]
        message = "<@{}> {} :tada:".format(message["user"], response)
        slack_client.chat_postMessage(channel=channel, text=message)


# Example reaction emoji echo
@slack_events_adapter.on("reaction_added")
def reaction_added(event_data):
    event = event_data["event"]
    emoji = event["reaction"]
    channel = event["item"]["channel"]
    text = ":%s:" % emoji
    slack_client.chat_postMessage(channel=channel, text=text)


# Error events
@slack_events_adapter.on("error")
def error_handler(err):
    print("ERROR: " + str(err))


# Once we have our event listeners configured, we can start the
# Flask server with the default `/events` endpoint on port 3000
slack_events_adapter.start(port=5000)