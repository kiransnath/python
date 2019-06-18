# Function to create EMR cluster programmatically

import boto3
import json
import os
from datetime import datetime
from dateutil import tz
from boto3.dynamodb.conditions import Key, Attr

client = boto3.client('emr', region_name=os.environ['region'])

def lambda_handler(event, context):

 s3 = boto3.resource('s3')

 dynamodb = boto3.resource('dynamodb')
 table_name = os.environ['app_env'] + "-" + "application-status"
 table = dynamodb.Table(table_name)

 application_name = os.environ['app_env'] + '-' + os.environ['app_config_name']

 ## Get the status for the latest run
 response = table.query(
               Limit = 1,
               ScanIndexForward = False,
               KeyConditionExpression=Key('application_name').eq(application_name)
            )

 if response['Items']:
     for i in response['Items']:
         print("most recent record: ", i['application_name'], " ", i['status'], " ", i['start_time_utc'])
     most_recent_status = i['status']
     most_recent_start_time = i['start_time_utc']

 else:
     print("No records in DynamoDB table for application:", application_name, " NEW CLUSTER WILL BE CREATED.")
     most_recent_status = ''

 ## Intitialize variables spinup_cluster, start_time, start_time_str
 spinup_cluster = 0

 start_time = datetime.utcnow()
 start_time_str = start_time.strftime("%Y-%m-%dT%H:%M:%S")

 if most_recent_status != 'running':
     status = 'running'

     table.put_item(
         Item={
             'application_name':application_name,
             'start_time_utc':start_time_str,
             'status':status
         }
     )
     print("New CLUSTER WILL BE CREATED.")
     #Spin-up new cluster
     spinup_cluster = 1
 else:
     print("CLUSTER IS ALREADY RUNNING. CLUSTER WILL NOT BE CREATED.")
      #DO NOT spin-up new cluster
     spinup_cluster = 0

 if spinup_cluster == 0:
  return {
   'message' : 'Another EMR cluster is running. Exiting'
  }
 else:
  try:
    ##drop the emrfs metadata table
    dynamodb_client = boto3.client('dynamodb')
    print("Spinning up a new cluster...")
    cluster_name_with_prefix = os.environ['app_env'] + '_' + os.environ['cluster_name']
    env_region_concat = os.environ['app_env'] + '-' + os.environ['region']
    obj1 = env_region_concat + '-' + 'paybi-platform'

    content_object = s3.Object(obj1, 'config/hive-site-spark.json')
    file_content = content_object.get()['Body'].read().decode('utf-8')
    json_content = json.loads(file_content)

    steps = [
        {
         'Name': 'Step 1: Read Kinesis Stream',
         'ActionOnFailure': 'TERMINATE_JOB_FLOW',
         'HadoopJarStep': {
             'Jar': 'command-runner.jar',
             'Args':
               [
                 "spark-submit",
                 "--conf","spark.driver.maxResultSize=0",
                 "--conf","spark.streaming.stopGracefullyOnShutdown=true",
                 "--class", "run_jar",
                 "--packages","org.apache.spark:spark-streaming-kinesis-asl_2.11:2.3.0",
                 "s3://" +  env_region_concat + "-paybi-platform/jars/" + os.environ['kinesis_stream_jar'],
                 os.environ['app_env'],
                 os.environ['app_config_table'],
                 "sca"
               ]
             }
        },


    ]

    response = client.run_job_flow(
    Name=cluster_name_with_prefix,
    ReleaseLabel='emr-5.13.0',
    Instances={
            'MasterInstanceType': os.environ['master_instance_type'],
            'SlaveInstanceType': os.environ['slave_instance_type'],
            'InstanceCount': int(os.environ['instance_count']),
            'Ec2KeyName': os.environ['ec2_key_name'],
            'EmrManagedMasterSecurityGroup': os.environ['emr_managed_master_security_group'],
            'EmrManagedSlaveSecurityGroup': os.environ['emr_managed_slave_security_group'],
            'ServiceAccessSecurityGroup': os.environ['service_access_security_group'],
            'Ec2SubnetId': os.environ['ec2_subnet_Id'],
            'KeepJobFlowAliveWhenNoSteps': False,
            'TerminationProtected': False,
            },
    Applications=[{
            'Name': 'Spark',
             },
             {
             'Name': 'Hive'
             },
             {
              'Name':'Hue'
             }
    ],
    Configurations=[
    {
     "Classification":"spark",
     "Properties":{
       "maximizeResourceAllocation":"true"
     }
    },
    {
     "Classification":"hive-site",
     "Properties":{
       "javax.jdo.option.ConnectionUserName":os.environ['connectionUserName'],
       "hive.merge.tezfiles":"true",
       "javax.jdo.option.ConnectionPassword":os.environ['connectionPassword'],
       "javax.jdo.option.ConnectionURL":os.environ['connectionURL']
       }
    },
    {"Classification":"spark-log4j",
    "Properties":{
        "log4j.rootCategory":"WARN, console"
       }
    }
    ],
    BootstrapActions=[
            {
                'Name': 'boto3 install',
                'ScriptBootstrapAction': {
                    'Path': 's3://' + env_region_concat + '-paybi-platform/shell-scripts/install-boto3.sh'
                }
            }
        ],
    Steps=steps,
    VisibleToAllUsers=True,
    LogUri=os.environ['emr_s3_log'],
    JobFlowRole=os.environ['Job_Flow_Role'],
    ServiceRole='EMR_DefaultRole'
)
  except Exception as e:

        raise Exception("Function: " + context.function_name + "\t\n" + str(e))
