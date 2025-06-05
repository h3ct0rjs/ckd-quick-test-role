#!/usr/bin/env python3

import aws_cdk as cdk

from cdk_python.cdk_python_stack import CdkPythonStack


app = cdk.App()
CdkPythonStack(app, "CdkPythonStack")

app.synth()
