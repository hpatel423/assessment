import argparse
import boto3
import unittest

class S3BucketCLI:
    def __init__(self):
        self.parser = argparse.ArgumentParser(description='S3 Bucket CLI')
        self.parser.add_argument('command', choices=['list_files', 'list_task_versions'], help='Command to execute')
        
        self.s3_client = boto3.client('s3')
        self.ecs_client = boto3.client('ecs')

    def list_files(self, bucket_name):
        response = self.s3_client.list_objects_v2(Bucket=bucket_name)
        
        if 'Contents' in response:
            for obj in response['Contents']:
                print(obj['Key'])
        else:
            print('Bucket is empty.')

    def list_task_versions(self, cluster_name, service_name):
        response = self.ecs_client.list_task_definitions(familyPrefix=service_name)
        
        if 'taskDefinitionArns' in response:
            for arn in response['taskDefinitionArns']:
                print(arn)
        else:
            print('No task definitions found.')

    def run(self):
        args = self.parser.parse_args()

        if args.command == 'list_files':
            bucket_name = input('Enter S3 bucket name: ')
            self.list_files(bucket_name)

        elif args.command == 'list_task_versions':
            cluster_name = input('Enter ECS cluster name: ')
            service_name = input('Enter ECS service name: ')
            self.list_task_versions(cluster_name, service_name)


class S3BucketCLITest(unittest.TestCase):
    def setUp(self):
        self.s3bucket = S3BucketCLI()

    def test_list_files(self):
        Bucket = 'my-test-bucket'
        objects = [{'Key': 'file1.txt'}, {'Key': 'file2.txt'}, {'Key': 'file3.txt'}]
        self.s3bucket.s3_client.list_objects_v2 = lambda Bucket: {'Contents': objects}
        self.s3bucket.list_files(Bucket)
        self.assertEqual(self.s3bucket.s3_client.list_objects_v2.call_count, 1)

    def test_list_task_versions(self):
        cluster_name = 'my-ecs-cluster'
        service_name = 'my-ecs-service'
        task_definitions = ['arn:aws:ecs:us-east-1:123456789012:task-definition/def1', 'arn:aws:ecs:us-east-1:123456789012:task-definition/def2']
        self.s3bucket.ecs_client.list_task_definitions = lambda familyPrefix: {'taskDefinitionArns': task_definitions}
        self.s3bucket.list_task_versions(cluster_name, service_name)
        self.assertEqual(self.s3bucket.ecs_client.list_task_definitions.call_count, 1)


if __name__ == "__main__":
    S3BucketCLI().run()
