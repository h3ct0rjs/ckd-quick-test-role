import aws_cdk as core
import aws_cdk.assertions as assertions
from lib.cdk_dynamo_stack import DynamoDBStack

def test_dynamodb_table_created():
    app = core.App()
    stack = DynamoDBStack(app, "DynamoDBStack")
    template = assertions.Template.from_stack(stack)

    template.has_resource_properties("AWS::DynamoDB::Table", {
        "AttributeDefinitions": [
            {
                "AttributeName": "id",
                "AttributeType": "S"
            }, 
            {
                "AttributeName": "timestamp",
                "AttributeType": "S"
            }
        ]
    })