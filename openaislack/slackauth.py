from slack_sdk import WebClient

class SlackAuth(object):
    def __init__(self, **kwargs):
        self.client_id = kwargs['client_id']
        self.client_secret = kwargs['client_secret']
        self.code = kwargs['code_param']

    def gettoken(self):
