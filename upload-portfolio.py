import json
import boto3
#from io import StringIO
import zipfile
import io
import mimetypes

def lambda_handler(event, context):
    try:
        s3 = boto3.resource('s3')
        portfolio_bucket = s3.Bucket('krishnaportfoliobucket')
        build_bucket = s3.Bucket('krishnabuildbucket')
        #build_bucket.download_file('portfoliobuild.zip','/tmp/portfoliobuild.zip')

        portfolio_zip = io.BytesIO()
        build_bucket.download_fileobj('portfoliobuild.zip',portfolio_zip)

        with zipfile.ZipFile(portfolio_zip) as myzip:
            for nm in myzip.namelist():
                obj = myzip.open(nm)
                portfolio_bucket.upload_fileobj(obj,nm,ExtraArgs={'ContentType': mimetypes.guess_type(nm)[0]})
                portfolio_bucket.Object(nm).Acl().put(ACL='public-read')
        sns = boto3.resource('sns')
        topic = sns.Topic('arn:aws:sns:us-east-1:535784091563:portfoliosns')
        topic.publish(Subject="Lambda successful",Message="Portfolio deployed")
    except:
        topic.publish(Subject="Lambda failure",Message="Portfolio deployment failed")
        raise

    return {
        'statusCode': 200,
        'body': json.dumps('Hello from Lambda!')
    }



# script which can dowload file to disk
# import boto3
# from botocore.client import Config
# import zipfile
#
# s3 = boto3.resource('s3', config=Config(signature_version='s3v4'))
#
# build_bucket = s3.Bucket('portfoliobuild.robinnorwood.info')
# portfolio_bucket = s3.Bucket('portfolio.robinnorwood.info')
#
# # On Windows, this will need to be a different location than /tmp
# build_bucket.download_file('portfolio.zip', '/tmp/portfolio.zip')
#
# with zipfile.ZipFile('/tmp/portfolio.zip') as myzip:
#     for nm in myzip.namelist():
#         obj = myzip.open(nm)
#         target_bucket.upload_fileobj(obj, nm)
#         target_bucket.Object(nm).Acl().put(ACL='public-read')
