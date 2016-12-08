from nose.tools import *
import unittest
import os

# Setting environment variables before App.app attempts to access them. We should probably just set app in a before
os.environ['S3PROXY_AWS_ACCESS_KEY'] = 'ACCESSKEY11223344556'
os.environ['S3PROXY_AWS_SECRET_KEY'] = 'SECRETKEY1122334455667788990011223344556'

import App.app as app

class TestApp(unittest.TestCase):

    def test_always_true(self):
        self.assertTrue(True)

    def test_calculate(self):
        example_url = "https://mybucket.s3.amazonaws.com/myfolder/myfile?AWSAccessKeyId=ACCESSKEY11223344556&Expires=1480551000&Signature=vilskVpDawVpgSbpwq6oVROtt4A%3D"
        bucket = "mybucket"
        file_path = "myfolder/myfile"
        expiry = app._calculate_expiration(600, 1480550400)
        response = app._calculate(bucket, file_path, expiry)
        self.assertEqual(response, example_url, "The response wasn't expected. Recieved {response} expected {example_url}".format(response=response, example_url=example_url))

    def test_calculate_expiration(self):
        expiry = app._calculate_expiration(600, 1480550400)
        self.assertEqual(expiry, 1480551000, "Times were not added correctly")

    def test_split_paths_in_folder(self):
        path = "mybucket/myfolder/myfile"
        bucket, file = app._splitPaths(path)
        self.assertEqual(bucket, "mybucket", "Bucket is not expected")
        self.assertEqual(file, "myfolder/myfile", "Filename and path is not expected")

    def test_split_paths(self):
        path = "mybucket/myfile"
        bucket, file = app._splitPaths(path)
        self.assertEqual(bucket, "mybucket", "Bucket is not expected")
        self.assertEqual(file, "myfile", "Filename and path is not expected")

    @raises(AttributeError)
    def test_split_paths_missing_bucket(self):
        path = "myfile"
        bucket, file = app._splitPaths(path)
