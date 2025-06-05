#!/usr/bin/env python3

import aws_cdk as cdk

from lib.cdk_python_stack import CdkPythonStack
from lib.cdk_dynamo_stack import DynamoDBStack
from lib.cdk_iam_stack import CdkIamStackRole

app = cdk.App()
CdkPythonStack(app, "CdkPythonStack")
DynamoDBStack(app, "DynamoDBStack")
# Iam role to be assumed by an ArnPrincipal to perform DynamoDB/Step Functions operations
CdkIamStackRole(app, "CdkIamStackRole")

app.synth()
