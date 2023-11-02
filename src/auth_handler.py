from boto3 import client, resource
import json

"""
define resources:  s3, dynamodb table, rekognition
"""

rekognition = client('rekognition', region_name = 'eu-central-1')

dynamodb = resource('dynamodb', region_name = 'eu-central-1')
table = dynamodb.Table('users')

s3 = client('s3')
bucket_name = 'steftech_guest_users_image'

# handler
def lambda_handler(event, context):
    print(event)

    object_key = 'todo' # todo
    # get s3 object, Response Syntax: 'Body': StreamingBody()
    """
    response = client.get_object(
    Bucket='string',
    IfMatch='string',
    IfModifiedSince=datetime(2015, 1, 1),
    IfNoneMatch='string',
    IfUnmodifiedSince=datetime(2015, 1, 1),
    Key='string',
    Range='string',
    ResponseCacheControl='string',
    ResponseContentDisposition='string',
    ResponseContentEncoding='string',
    ResponseContentLanguage='string',
    ResponseContentType='string',
    ResponseExpires=datetime(2015, 1, 1),
    VersionId='string',
    SSECustomerAlgorithm='string',
    SSECustomerKey='string',
    RequestPayer='requester',
    PartNumber=123,
    ExpectedBucketOwner='string',
    ChecksumMode='ENABLED'
)
    """
    s3_response = s3.get_object(Bucket=bucket_name, Key='object_key')
    image_bytes = s3_response['Body'].read()

    # Upload image to rekognition, search_users_by_image API

    """
    https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/rekognition/client/search_faces_by_image.html
    You pass the input image either as base64-encoded image bytes or as a reference to an image in an Amazon S3 bucket. If you use the AWS CLI to call Amazon Rekognition operations, passing image bytes is not supported. The image must be either a PNG or JPEG formatted file.

    The response returns an array of faces that match, ordered by similarity score with the highest similarity first. More specifically, it is an array of metadata for each face match found. Along with the metadata, the response also includes a similarity indicating how similar the face is to the input face. In the response, the operation also returns the bounding box (and a confidence level that the bounding box contains a face) of the face that Amazon Rekognition used for the input image.

    If no faces are detected in the input image, SearchFacesByImage returns an InvalidParameterException error.
    """

    rekognition_response = rekognition.search_faces_by_image(
                    CollectionId='employees',
                    Image={
                        'Bytes': image_bytes,
                    },
                )
    print(f'rekognition response: {rekognition_response}')

    for face in rekognition_response['FaceMatches']:
        if face['Similarity'] > 80:
            face_id = face['Face']['FaceId']
            print(f'face_id if Similarity > 80: {face_id}')
        
