## AWS Agent

I leverage the idea of agent and cli everything to do this aws agent using cli `aws-agent`.

How to set it up?
```shell
# firstly login on your local
aws sso login 

# run the agent with prompt
export OPENAI_API_KEY="your-key"
mv aws-agent.py aws-agent
mv aws-agent /usr/local/bin/
aws-agent "list all the s3 bucket"
aws-agent "how many s3 buckets in total"
```

You can easily extend this script, for example, context saving, session management etc.
