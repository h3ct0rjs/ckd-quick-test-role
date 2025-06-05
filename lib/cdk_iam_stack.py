from constructs import Construct
from aws_cdk import (
    Stack,
    aws_iam as iam,
)
class CdkIamStackRole(Stack):
    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)
        # Use current cdk context : 
        account_id = self.account   # AWS Account ccp. 
        
        # Create an IAM role to be assumed by an ArnPrincipal and  do Scans/Queries/ List DynamoDB Tables
        self.dynamo_role = iam.Role(
            self,
            "DynamoDBRole",
            assumed_by=iam.ArnPrincipal(f"arn:aws:iam::{account_id}:user/cloud-dev"),
            description="Role for performing DynamoDB operations",
            role_name="DynamoDBOperationsRole"
        )

        # Attach policies to the role
        self.dynamo_role.add_to_policy(iam.PolicyStatement(
            actions=[
                "dynamodb:Scan", 
                "dynamodb:Query", 
                "dynamodb:ListTables", 
                "dynamodb:DescribeTable",
                "dynamodb:GetItem",
                "dynamodb:PutItem",
                "dynamodb:UpdateItem"
                ],
            resources=["*"]
        ))
        # Attach step functions policy to the role 
        self.dynamo_role.add_to_policy(iam.PolicyStatement(
            actions=[
                "states:StartExecution", 
                "states:DescribeExecution", 
                "states:ListExecutions",
                "states:ListActivities",
                "states:DescribeStateMachine",
                "states:DescribeStateMachineForExecution",
                "states:StopExecution",
                "states:ListStateMachines"
            ],
            resources=["arn:aws:states:*:*:stateMachine:*"]
        ))

