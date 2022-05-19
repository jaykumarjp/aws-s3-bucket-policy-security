import logging, boto3, json, requests, sys
from botocore.exceptions import ClientError
from urllib3.exceptions import InsecureRequestWarning
from multiprocessing.pool import ThreadPool as Pool

requests.packages.urllib3.disable_warnings(category=InsecureRequestWarning)

profile = sys.argv[1]
pool_size = 10 # your "parallelness"
session = boto3.Session(profile_name=profile) #Set session in boto3 according profile.
s3 = session.client('s3') #AWS resource to execute, S3.
response = s3.list_buckets() #CLI action on resource, List Bucket.
final = 0

def worker(item):
    global final
    ispub = ""
    try: #Using try for aws response error handeling
        policy = s3.get_bucket_policy(Bucket=item) #Get Bucket policy of bucket name from array.
        policy = policy["Policy"] #Filtered json response and removed un-neccesory items.

        if ('"Effect":"Allow","Principal":"*"' in policy): 
            ispub = '<p style="color:red">MayBePublic</p>'
        else :
            ispub = "NotPublic"
            
    except ClientError as e:
        policy = ("Unexpected error: %s" % e)
        ispub = "NotPublic"
    
    s3url = "https://"+item+".s3.amazonaws.com"
    pubreq = str(requests.get(s3url, verify=False))
    pubreq = pubreq.strip('<')
    pubreq = pubreq.strip('>')
    if ('403' in pubreq):
        pubcheck = "403"
    else :
        pubcheck = "<a href="+s3url+">"+s3url+"</a>"     
    
    final = str(final)+"<tr><td>"+item+"</td><td>"+pubcheck+"</td><td>"+ispub+"</td><td>"+str(policy)+"</td></tr>"

pool = Pool(pool_size)
for bucket in response['Buckets']:
    pool.apply_async(worker, (bucket["Name"],))
    
pool.close()
pool.join()
            
            
# To send this Alert on telegram uncomment next line        
#requests.get("https://api.telegram.org/bot1491210791:AAGzexKdzO4-TwfE28UGFCKwGJmo5cMRxU/sendmessage?chat_id=-508514152&text="+final)

header = '''<!DOCTYPE html>
<html>
<head>
<style>
table {
  font-family: arial, sans-serif;
  border-collapse: collapse;
  width: 100%;
}

td, th {
  border: 1px solid black;
  text-align: left;
  padding: 8px;
  word-break: break-all;
  min-width:180px;
}

tr:nth-child(even) {
  background-color: #dddddd;
}
</style>
</head>
<body>


<table>
  <tr>
    <th>BucketName</th>
    <th>Accessible</th>
    <th>IsPublic</th>
    <th>BucketPolicy</th>
  </tr>'''

footer = '''</table>

</body>
</html>
'''
print(header+final+footer) #Print "Final" result.

