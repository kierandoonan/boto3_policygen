import json
from botocore.stub import Stubber


class PolicyGenerator:

    def __init__(self):
        self.actions = set()

    def record(self):
        Stubber._get_response_handler = self._event_wrapper(
            Stubber._get_response_handler
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

    def _event_wrapper(self, method):
        def wrapper_method(*args, **kwargs):
            model = kwargs.get('model')
            if not model:
                import pdb; pdb.set_trace()

            action = '{}:{}'.format(
                model.metadata['endpointPrefix'],
                model.name
            )

            self.actions.add(action)

            return method(*args, **kwargs)

        return wrapper_method
