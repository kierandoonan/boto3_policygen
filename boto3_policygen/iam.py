import json
from botocore.model import OperationModel
from botocore.hooks import HierarchicalEmitter


class PolicyGenerator:

    def __init__(self):
        self.actions = set()

    def record(self):
        HierarchicalEmitter.emit_until_response = self._event_wrapper(
            HierarchicalEmitter.emit_until_response
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
            """ Looks for an OperationModel in the args and kwargs and if it is
                found then it will add it as an action to PolicyGenerator
            """
            model = kwargs.get('model')

            # If model isn't in kwargs, check for it in args
            if not model:
                try:
                    model = next(a for a in args if type(a) is OperationModel)
                except StopIteration:
                    pass  # No model found

            if model:
                action = '{}:{}'.format(
                    model.metadata['endpointPrefix'],
                    model.name
                )

                self.actions.add(action)

            return method(*args, **kwargs)

        return wrapper_method
