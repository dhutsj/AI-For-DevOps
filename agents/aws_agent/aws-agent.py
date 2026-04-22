#!/usr/bin/env python3

import sys
import subprocess
import json
from openai import OpenAI

client = OpenAI()

ALLOWED_SERVICES = [
    "s3",
    "rds",
    "ec2",
    "secretsmanager",
    "dynamodb"
]

BLOCKED_WORDS = [
    "delete", "put", "create", "update", "modify", "remove"
]

def run_cmd(cmd):
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    return result.stdout if result.stdout else result.stderr

def is_safe(cmd):
    cmd_lower = cmd.lower()

    if not cmd_lower.startswith("aws"):
        return False, "Not an AWS command"

    if any(word in cmd_lower for word in BLOCKED_WORDS):
        return False, "Write operation blocked"

    if not any(f"aws {svc}" in cmd_lower for svc in ALLOWED_SERVICES):
        return False, "Service not allowed"

    return True, None

def generate_command(prompt):
    response = client.chat.completions.create(
        model="gpt-5.4",
        response_format={"type": "json_object"},
        messages=[
            {
                "role": "system",
                "content": """
You are an AWS CLI expert.

Convert user requests into a JSON object:

{
  "command": "full aws cli command"
}

Rules:
- ONLY generate valid AWS CLI commands
- ONLY READ-ONLY operations (describe, list, get)
- NEVER invent filters or fields that AWS CLI does not support
- Use --region when applicable (EC2, RDS, SSM, etc.)
- DO NOT use region filters for S3 (S3 is global)

Examples:

User: list rds clusters in us-west-2
Output:
{ "command": "aws rds describe-db-clusters --region us-west-2" }

User: list parameters in parameter store in us-west-2
Output:
{ "command": "aws ssm describe-parameters --region us-west-2" }

User: list s3 buckets
Output:
{ "command": "aws s3api list-buckets" }
"""
            },
            {"role": "user", "content": prompt}
        ]
    )

    data = json.loads(response.choices[0].message.content)
    return data["command"]

def summarize(output):
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "Summarize AWS CLI output briefly."},
            {"role": "user", "content": output[:8000]}
        ]
    )
    return response.choices[0].message.content

def refine_command(prompt, bad_cmd, error):
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        response_format={"type": "json_object"},
        messages=[
            {
                "role": "system",
                "content": """
Fix the AWS CLI command.

Return JSON:
{ "command": "fixed command" }

Do not explain.
"""
            },
            {
                "role": "user",
                "content": f"""
User request: {prompt}

Previous command:
{bad_cmd}

Error:
{error}

Fix it.
"""
            }
        ]
    )

    return json.loads(response.choices[0].message.content)["command"]


def main():
    if len(sys.argv) < 2:
        print("Usage: aws-agent \"your request\"")
        return

    prompt = " ".join(sys.argv[1:])
    print(f"\n🧠 Prompt: {prompt}")

    # Step 1: generate command
    cmd = generate_command(prompt)
    print(f"\n⚙️ Generated command:\n{cmd}\n")

    # Step 2: safety check
    ok, reason = is_safe(cmd)
    if not ok:
        print(f"❌ Blocked: {reason}")
        return

    # Step 3: execute command
    output = run_cmd(cmd)

    # Step 4: detect failure and refine once
    if any(err in output.lower() for err in ["error", "invalid", "unknown", "failed"]):
        print("⚠️ Detected error, refining command...\n")

        new_cmd = refine_command(prompt, cmd, output)
        print(f"🔁 Refined command:\n{new_cmd}\n")

        ok, reason = is_safe(new_cmd)
        if not ok:
            print(f"❌ Refined command blocked: {reason}")
            return

        cmd = new_cmd
        output = run_cmd(cmd)

    # Step 5: print raw output
    print("📦 Raw Output:\n")
    print(output)

    # Step 6: summarize (optional but useful)
    try:
        print("\n📝 Summary:\n")
        print(summarize(output))
    except Exception:
        print("\n⚠️ Summary failed, showing raw output only.")


if __name__ == "__main__":
    main()
