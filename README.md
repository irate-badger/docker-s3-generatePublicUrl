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






