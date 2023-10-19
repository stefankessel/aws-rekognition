from boto3 import client, resource

# get resources
s3 = client('s3')
rekognition = client('rekognition', region_name='eu-central-1')
dynamodb = resource('dynamodb', region_name= 'eu-central-1')
dynamodb_table_name = 'users'
table = dynamodb.Table(dynamodb_table_name)

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
            face_id = res['FaceRecords'][0]['Face']['Faceid']

            # register user in dynamodb
            register_user(face_id, firstname, lastname)
    except Exception as e:
        print(e)
        print(f'error processing image {object_key} from bucket {bucket_name}')



def index_user_image(bucket_name, object_key):
    pass