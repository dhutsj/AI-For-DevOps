## Using Skills in vscode with cline
Refer to this doc https://docs.cline.bot/customization/skills for using Skills in cline.
The path of `SKILL.md` is in `~/.agents/skills/eks-failed-pod-counter/` or `~/.agents/skills/argocd-fix-degraded-app/` etc.

Then you can use below template.

````md

# Name: eks-failed-pod-counter

# SKILL: Count Failed Pods in EKS

## Description
This skill logs into a specified AWS account, switches to the corresponding EKS cluster, and counts the number of pods in **Failed** state across all namespaces.

---

## Inputs
- **account**: The AWS account / environment name (e.g., `dev`, `staging(aka stg)`, `prod`)

---

## Steps

### 1. Login to AWS Account
Use the provided account name to authenticate:

```bash
awslogin <account>
```

Example:
```bash
awslogin dev
```

---

### 2. Switch Kubernetes Context
Switch to the corresponding EKS cluster context:

```bash
kubectx <account>
```

Example:
```bash
kubectx arn:aws:eks:region:account_id:cluster/cluster_name
```

---

### 3. Count Failed Pods
Run the following command to list and count all failed pods:

```bash
kubectl get pods --all-namespaces \
  --field-selector=status.phase=Failed \
  --no-headers | wc -l
```

---

## Output
- Returns a single integer representing the total number of pods in **Failed** state.

Example:
```
5
```

---

## Notes
- Ensure `awslogin` is configured and authenticated properly.
- Ensure `kubectx` contexts are named consistently with the account (e.g., `dev`, `staging`, `prod`).
- The command filters only pods with `status.phase=Failed`.

---

## Optional Enhancements

### Show Failed Pods with Details
```bash
kubectl get pods --all-namespaces \
  --field-selector=status.phase=Failed -o wide
```

### Group by Namespace
```bash
kubectl get pods --all-namespaces \
  --field-selector=status.phase=Failed \
  --no-headers | awk '{print $1}' | sort | uniq -c
```

````


