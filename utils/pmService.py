from pmClient import PMClient
import json

class PMService():
    def __init__(self):
        self.pmClient = None

    def getPmClient(self):
        if self.pmClient == None:
            with open('API_Keys.json', "r") as file:
                api_keys = json.load(file)

            self.pmClient = PMClient(api_key=api_keys['api_key'], api_secret=api_keys['api_secret'])
            self.pmClient.set_access_token(api_keys['access_token'])
            self.pmClient.set_public_access_token(api_keys['public_access_token'])
            self.pmClient.set_read_access_token(api_keys['read_access_token'])

        return self.pmClient

