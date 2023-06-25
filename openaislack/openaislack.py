from slack_sdk import WebClient
import slack
from flask import Flask
from slackeventsapi import SlackEventAdapter
from slack_sdk.errors import SlackApiError


class OpenAISlackBot(object):
    def __init__(self, **kwargs):
        self.client = WebClient(token=kwargs['token'])
        self.channel = kwargs['channel']

    def postmessage(self, message=None):
        response = self.client.chat_postMessage(channel=self.channel,
                                                text=message)


if __name__ == "__main__":
    slackbot = OpenAISlackBot(token="xoxb-928934584657-5242865570663-BLtxYuzJ8yVrbo8JIQIU3osN",
                              channel="openai_testing")
    slackbot.postmessage(message="Testing testing!")
