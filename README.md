# docker-s3-generatepublicurl
## Generate S3 public URL with Flask & Python
A simple flask based service to generate public URLs for S3.

The format is:

http://{server:port}/{bucket}/{path}/{filename}?expire={expiration}

Expiration defaults to 1 minute, with parameters currently integers with duration declared in seconds

For example, calling the service with:

http://localhost:8080/mybucket/myfolder/myfile?expire=600

Will return the temporary url to S3 that expires after 10 minutes. 
If the time was 2016-12-01 00:00:00 and by using the example keys provided in the example docker compose the reponse should be:

https://mybucket.s3.amazonaws.com/myfolder/myfile?AWSAccessKeyId=ACCESSKEY11223344556&Expires=1480551000&Signature=vilskVpDawVpgSbpwq6oVROtt4A%3D

When running the Docker image, you can configure the Access and Secret ket using the environment configuration settings

S3PROXY_AWS_ACCESS_KEY

S3PROXY_AWS_SECRET_KEY


To setup and run in a development environment, install Pip, then install the dependencies like so:

```pip install -r requirements.txt```

You can execute using:

```python App/app.py --ACCESS_KEY=123 --SECRET_KEY=ABC```

Verify the port that it starts on, but it should be 5000, and test with curl:

```curl http://localhost:5000/mybucket/myfolder/myfile?expire=600```

And get a response like:

```https://mybucket.s3.amazonaws.com/myfolder/myfile?AWSAccessKeyId=123&Expires=1480551000&Signature=CH5Kz%2B9ljZWeBPdkFK%2FeYIR1ia4%3D```