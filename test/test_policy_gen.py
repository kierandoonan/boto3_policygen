import boto3
import json
from botocore.stub import Stubber
from policy_gen.boto3 import BotoPolicyGen


class TestPolicyGen:

    def gen_client_and_stub(self, endpoint):
        session = boto3.Session(region_name='eu-west-1')
        client = session.client(endpoint)
        stub = Stubber(client)

        return (client, stub)

    def test_records_and_generates_policy(self):
        ec2, stub = self.gen_client_and_stub('ec2')

        stub.add_response('describe_instances', {}, {})
        stub.add_response('describe_images', {}, {})
        stub.activate()

        policy_gen = BotoPolicyGen([ec2])
        policy_gen.record()

        ec2.describe_instances()
        ec2.describe_images()

        policy = json.loads(policy_gen.generate())

        assert 'Statement' in policy
        assert len(policy['Statement']) == 1
        assert len(policy['Statement'][0]['Action']) == 2
        assert 'ec2:DescribeInstances' in policy['Statement'][0]['Action']
        assert 'ec2:DescribeImages' in policy['Statement'][0]['Action']

    def test_records_policy_from_multiple_clients(self):
        pass
