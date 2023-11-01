from boto3 import client, resource

# get resources
s3 = client('s3')
rekognition = client('rekognition', region_name='eu-central-1')
dynamodb = resource('dynamodb', region_name= 'eu-central-1')
dynamodb_table_name = 'users'
# table = dynamodb.Table(dynamodb_table_name)

def handler(event, context):
    print(event)

    
    try:
        # get s3 trigger event data
        bucket_name = event['Records'][0]['s3']['bucket']['name']
        object_key = event['records'][0]['s3']['object']['key']

        # get face data from rekognition
        res = index_user_image(bucket_name, object_key)
        print(res)

        # expected name: john_doe.jpg
        firstname, lastname = object_key.split('.')[0].split('_')

        if res['ResponseMetadata']['HTTPStatusCode'] == 200:
            # return data reference: https://docs.aws.amazon.com/rekognition/latest/APIReference/API_IndexFaces.html
            face_id = res['FaceRecords'][0]['Face']['Faceid']

            # save user data in dynamodb
            register_user(face_id, firstname, lastname)

            return res
    except Exception as e:
        print(e)
        print(f'error processing image {object_key} from bucket {bucket_name}')



def index_user_image(bucket_name, object_key):
    # send to rekognition
    # Request Syntax: https://docs.aws.amazon.com/rekognition/latest/APIReference/API_IndexFaces.html#API_IndexFaces_Request
    res = rekognition.index_faces(
            Image={
                    "S3Object": { 
                        "Bucket": bucket_name,
                        "Name": object_key,
                    }
            },
            CollectionId='employees' # Todo
        )
    return res
    
# put user into dynamodb
def register_user(face_id, firstname, lastname):
    # dynamodb API reference: https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dynamodb.html
    # put_item API reference: https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dynamodb/client/put_item.html
    dynamodb.put_item(
        TableName=dynamodb_table_name,
        Item={
            'face_id': face_id,
            'firstname': firstname,
            'lastname': lastname
        }
    )