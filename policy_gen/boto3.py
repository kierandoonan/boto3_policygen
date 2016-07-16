from botocore.endpoint import Endpoint
import json

class BotoPolicyGen:
    def __init__(self, clients=[]):
        self.actions = set()
        self.clients = clients

    def add_client(self, client):
        self.clients.append(client)

    def record(self):
        for client in self.clients:
            client.meta.events.register_first(
                'before-call.*.*',
                self._get_response_handler,
                id(self)
            )

    def generate(self):
        policy = {
            "Version": "2012-10-17",
            "Statement": [
                {
                    "Action": list(self.actions),
                    "Effect": "Allow",
                    "Resource": "*"
                }
            ]
        }

        return json.dumps(policy)

    def clear_actions(self):
        self.actions = set()

    def _get_response_handler(self, model, params, **kwargs):
        action = '{}:{}'.format(
            model.metadata['endpointPrefix'],
            model.name
        )

        self.actions.add(action)
