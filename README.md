# s3bucketPolicySecurity:
This code will scan all s3 buckets and check bucket policy for security purpose.

# prerequisite:
1. python
2. boto3 (pip install boto3)
3. aws cli profile
4. requests module (pip install requests)

# usage: 
Type command in terminal<br>
``` s3fast.py default > report.html ``` [If aws-cli profile is default else change "default" with profile name]

# False-Positive
It show "may be public", when prnciple is * but condition set to limited access. 

# Future Update
1. Remove false-positive by checking condition as well
2. Add - role based access
s
