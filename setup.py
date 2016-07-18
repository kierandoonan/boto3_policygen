from setuptools import setup

setup(
    name='boto3_policygen',
    version='0.1',
    description='Generates policy documents from calls to boto3 / botocore',
    url='https://github.com/kierandoonan/boto3_policygen',
    download_url='https://github.com/kierandoonan/boto3_policygen/archive/0.1.tar.gz',
    author='Kieran Doonan',
    author_email='kieran@doonan.net',
    license='MIT',
    packages=['boto3_policygen'],
    install_requires=['boto3', 'botocore'],
    keywords=['boto', 'boto3', 'iam', 'policy']
)
