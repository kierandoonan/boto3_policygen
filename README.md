# boto3_policygen

This module will record AWS API calls made by `boto3` / `botocore` and generate
an `iam` policy that would allow a user to make those calls.

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

```
