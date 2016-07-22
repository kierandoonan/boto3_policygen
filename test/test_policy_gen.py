import boto3
import json
from botocore.stub import Stubber
from boto3_policygen.iam import PolicyGenerator
from moto import mock_ec2

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

        policy_gen = PolicyGenerator()
        policy_gen.record()

        stub.activate()

        ec2.describe_instances()
        ec2.describe_images()

        policy = json.loads(policy_gen.generate())

        assert 'Statement' in policy
        assert len(policy['Statement']) == 1
        assert len(policy['Statement'][0]['Action']) == 2
        assert 'ec2:DescribeInstances' in policy['Statement'][0]['Action']
        assert 'ec2:DescribeImages' in policy['Statement'][0]['Action']

    def test_records_policy_from_multiple_clients(self):
        ec2, ec2_stub = self.gen_client_and_stub('ec2')
        rds, rds_stub = self.gen_client_and_stub('rds')
        s3, s3_stub = self.gen_client_and_stub('s3')

        ec2_stub.add_response('describe_instances', {}, {})
        rds_stub.add_response('describe_db_instances', {}, {})
        s3_stub.add_response('list_buckets', {}, {})

        policy_gen = PolicyGenerator()
        policy_gen.record()

        ec2_stub.activate()
        rds_stub.activate()
        s3_stub.activate()

        ec2.describe_instances()
        rds.describe_db_instances()
        s3.list_buckets()

        policy = json.loads(policy_gen.generate())

        assert len(policy['Statement'][0]['Action']) == 3
        assert 'ec2:DescribeInstances' in policy['Statement'][0]['Action']
        assert 's3:ListBuckets' in policy['Statement'][0]['Action']
        assert 'rds:DescribeDBInstances' in policy['Statement'][0]['Action']

    def test_actions_in_policy_are_unique(self):
        ec2, stub = self.gen_client_and_stub('ec2')

        for i in range(10):
            stub.add_response('describe_instances', {}, {})

        policy_gen = PolicyGenerator()
        policy_gen.record()

        stub.activate()

        for i in range(10):
            ec2.describe_instances()

        policy = json.loads(policy_gen.generate())

        assert len(policy['Statement'][0]['Action']) == 1
        assert 'ec2:DescribeInstances' in policy['Statement'][0]['Action']

    def test_stub_can_be_activated_before_policy_gen(self):
        ec2, stub = self.gen_client_and_stub('ec2')

        stub.add_response('describe_instances', {}, {})
        stub.activate()

        policy_gen = PolicyGenerator()
        policy_gen.record()

        ec2.describe_instances()

        policy = json.loads(policy_gen.generate())

        assert len(policy['Statement'][0]['Action']) == 1
        assert 'ec2:DescribeInstances' in policy['Statement'][0]['Action']

    @mock_ec2
    def test_policy_is_recorded_when_not_stubbed(self):
        session = boto3.Session(region_name='eu-west-1')
        ec2 = session.client('ec2')

        policy_gen = PolicyGenerator()
        policy_gen.record()

        ec2.describe_instances()

        policy = json.loads(policy_gen.generate())

        assert len(policy['Statement'][0]['Action']) == 1
        assert 'ec2:DescribeInstances' in policy['Statement'][0]['Action']
