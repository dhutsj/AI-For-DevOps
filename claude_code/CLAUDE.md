# AWS Agent Rules

## AWS Access Policy

This agent is operating in READ-ONLY mode.

The agent MUST NOT perform any AWS resource modification actions.

### Forbidden AWS operations

Never call any AWS API that can:

- create resources
- update resources
- modify resources
- delete resources
- terminate resources
- restart resources
- change configurations
- change permissions
- change networking
- change security settings

Examples of forbidden operations:

- Create*
- Put*
- Update*
- Modify*
- Delete*
- Remove*
- Attach*
- Detach*
- Authorize*
- Revoke*
- Associate*
- Disassociate*
- Start*
- Stop*
- Reboot*
- Terminate*

### Allowed operations

Only perform read-only operations:

Examples:

- Describe*
- Get*
- List*

Allowed examples:

- List S3 buckets
- List S3 objects
- Get S3 bucket configuration
- Describe RDS clusters
- Describe EC2 instances
- List IAM roles
- Get Secrets Manager metadata
- Get CloudWatch metrics
- Describe EKS clusters

### Execution rules

Before executing any AWS command:

1. Check that the command is read-only.
2. If the command contains a write operation, refuse.
3. Do not suggest replacing a read-only command with a write command.
4. Never ask the user for confirmation to perform a write action.
5. If a write action is requested, explain that this agent is read-only.

### Examples

Allowed:
aws ec2 describe-instances
aws rds describe-db-clusters
aws s3api list-buckets
aws secretsmanager list-secrets
Not allowed:
aws ec2 terminate-instances
aws s3 rm
aws rds modify-db-cluster
aws iam attach-role-policy


## General Cloud/Infra MCP Policy

When using any cloud/infra MCP server (AWS, Cast.ai, Datadog, etc.), treat all actions
as read-only by default. Never call create/update/delete/terminate/scale
operations unless I explicitly ask for a specific change in that message.
