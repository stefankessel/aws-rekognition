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
        bucket_name = event['Records'][0]['bucket']['name']
        bucket_key = event['records'][0]['bucket']['key']

        res = index_user_image(bucket_name, bucket_key)
        print(res)

        # get image_id from dynamodb
        image_id = res['ResponseMetadata'][0]['Face'] #['Faceid']
    except Exception as e:
        print(e)
        print(f'error processing image {bucket_key} from bucket {bucket_name}')



def index_user_image(bucket_name, bucket_key):
    pass