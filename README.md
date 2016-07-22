# boto3_policygen

This module will record AWS API calls made by `boto3` / `botocore` and generate an `iam` policy that would allow a user to make those calls.

## Setup

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

Recording should work when the API is stubbed or mocked (it's currently tested against `botocore.Stubber` and `moto` but should work with others).
