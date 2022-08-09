# Publish Amazon DevOps Guru Insights to Slack

Amazon DevOps Guru is a machine learning (ML) powered service that gives you a simpler way to improve an application’s availability and reduce expensive downtime. Without involving any complex configuration setup, DevOps Guru automatically ingests operational data in your AWS cloud. When DevOps Guru identifies a critical issue, it automatically alerts you with a summary of related anomalies, the likely root cause, and context on when and where the issue occurred. DevOps Guru also, when possible, provides prescriptive recommendations on how to remediate the issue.

Amazon DevOps Guru also integrates with Amazon EventBridge to notify you of events relating to insights and corresponding insight updates. DevOps Guru generates insights when it detects anomalous behavior in your operational applications and can alert you of a potential issue in near real-time when you set up notifications. With this integration, you can set up routing rules to determine where to send notifications, use pre-defined DevOps Guru patterns to only send notifications or trigger actions that match that pattern (e.g., only send for “New Insights Open”), or create custom patterns to send notifications. For example, you may only want to be notified when a new insight is opened that DevOps Guru has marked as high severity which could then trigger an action that sends it to a specific ticketing queue so you can immediately address the issue.

You can select any of the following pre-defined patterns to filter Events to trigger actions in a supported AWS resource. 

    "DevOps Guru New Insight Open"
    "DevOps Guru New Anomaly Association"
    "DevOps Guru Insight Severity Upgraded"
    "DevOps Guru New Recommendation Created"
    "DevOps Guru Insight Closed"

This template deploys an AWS Lambda function that is triggered by an Amazon EventBridge rule when Amazon DevOps Guru notifies event relating to "DevOps Guru New Insight Open". It also deploys AWS Secret Manager, Amazon EventBridge Rule and required permission to invoke this specific function. AWS Lambda function  retrieves Slack Webhook URL from AWS Secret Manager and posts a message to Slack using webhook API call. It also deploys 

## Requirements

* [Create an AWS account](https://portal.aws.amazon.com/gp/aws/developer/registration/index.html) if you do not already have one and log in. The IAM user that you use must have sufficient permissions to make necessary AWS service calls and manage AWS resources.
* [AWS CLI](https://docs.aws.amazon.com/cli/latest/userguide/install-cliv2.html) installed and configured
* [Git Installed](https://git-scm.com/book/en/v2/Getting-Started-Installing-Git)
* [AWS Serverless Application Model](https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/serverless-sam-cli-install.html) (AWS SAM) installed
* Amazon DevOps Guru is enabled and generates insight. Please check [this blog](https://aws.amazon.com/blogs/devops/gaining-operational-insights-with-aiops-using-amazon-devops-guru/) to generate insight 

We recommend using [AWS Cloud9](https://aws.amazon.com/cloud9/) to create an environment to get access to the AWS CLI and SAM CLI from a bash terminal. AWS Cloud9 is a browser-based IDE that provides a development environment in the cloud. While creating the new environment, ensure you choose Linux2 as the operating system. Alternatively, you can use your bash terminal in your favorite IDE and configure your AWS credentials in your terminal.

### Deployment Instructions

1. Create a Slack Webhook URL

    **You will need to have access to add a new channel and app to your Slack Workspace.**

   - Create a new [channel](https://slack.com/help/articles/201402297-Create-a-channel) for events (i.e. devopsguru_events)
   - Within Slack **click** on your workspace name drop down arrow in the upper left. **click on Tools > Workflow Builder**  
   - **Click** Create in the upper right hand corner of the Workflow Builder and give your workflow a name **click** next.
   - **Click** on *select* next to **Webhook** and then **click** *add variable* add the following variables one at a time in the *Key* section. All *data type* will be *text*:  
            -text  
            -account  
            -region  
            -startTime  
            -insightType
            -severity  
            -description
            -insightUrl  
            -numOfAnomalies  
   - When done you should have 9 variables, double check them as they are case sensitive and will be referenced. When checked **click** on *done* and *next*.
   - **Click** on *add step* and then on the add a workflow step **click** *add* next to *send a message*.
   - Under *send this message to:* select the channel you created in Step 1 in *message text* you  should recreate this following:  
       ![](https://gitlab.aws.dev/aws-blogs/devops-guru-integration-with-slack/raw/ba7f77bb4cd97a4f3d984dc1bb9bdc85a0d4cb06/images/slack_workflow.PNG)
   - **Click** *save* and **click** *publish*
   - For the deployment we will need the *Webhook URL*

2. Create a new directory, navigate to that directory in a terminal and clone the GitHub repository:
    ``` 
    git clone https://gitlab.aws.dev/aws-blogs/devops-guru-integration-with-slack.git
    ```
3. Change directory to the directory where you cloned the Github repository:
    ```
    cd devops-guru-integration-with-slack
    ```
4. From the command line, use AWS SAM to build the serverless application with its dependencies
    ```
    sam build
    ```
5. From the command line, use AWS SAM to deploy the AWS resources for the pattern as specified in the template.yml file:
    ```
    sam deploy --guided
    ```
6. During the prompts:
    * Enter a stack name
    * Enter the desired AWS Region
    * Enter the Secret name to store Slack Channel Webhook URL
    * Enter the Slack Channel Webhook URL that you copied in Step #1
    * Allow SAM CLI to create IAM roles with the required permissions.

    Once you have run `sam deploy --guided` mode once and saved arguments to a configuration file (samconfig.toml), you can use `sam deploy` in future to use these defaults.

7. Note the outputs from the SAM deployment process. This contains the Lambda function name for testing

## How it works

* Amazon DevOps Guru notifies of events relating to "DevOps Guru New Insight Open" in Amazon EventBridge.
* Amazon EventBridge triggers AWS Lambda function.
* AWS Lambda function retrieves Slack Channel Webhook URL from AWS Secret Manager and publishes the message to Slack by calling Webhook API.

## License

This library is licensed under the MIT-0 License. See the [LICENSE](/LICENSE) file.

