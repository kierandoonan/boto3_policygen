# boto3_policygen

This module will record AWS API calls made by `boto3` / `botocore` and generate an `iam` policy that would allow a user to make those calls.

## Installation

Install via pip

```bash
$ [sudo] pip install boto3_policygen
```

## Usage

```python
from boto3_policygen.iam import PolicyGenerator
import boto3

policy_gen = PolicyGenerator()  # Create a new policy generator
policy_gen.record()

# Call some AWS APIs form boto3
ec2 = boto3.client('ec2')
ec2.describe_instances()

# Call generate() to get the IAM policy as a string
print policy_gen.generate()

# >> {"Version": "2012-10-17", "Statement": [{"Action": ["ec2:DescribeInstances"], "Resource": "*", "Effect": "Allow"}]}
```

Only the actions section of the policy will be created, any extra conditions or resource constraints will have to be added manually.

Recording should work when the API is stubbed with the `botocore.Stubber` class, the only condition is that `PolicyGenerator.record()` must be called before `Stubber.activate()`.

i.e. This will work:
```python
ec2 = boto3.client('ec2')
stub = Stubber(ec2)
stub.add_response('describe_instances', {}, {})
policy_gen = PolicyGenerator()

policy_gen.record()
stub.activate()
```

This won't work:
```python
ec2 = boto3.client('ec2')
stub = Stubber(ec2)
stub.add_response('describe_instances', {}, {})
policy_gen = PolicyGenerator()

stub.activate()
policy_gen.record()
```
