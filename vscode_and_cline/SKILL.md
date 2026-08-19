# Name: argocd-fix-degraded-app

# SKILL: Auto fix degraded apps in argocd

## Description
This skill logs into a specified argocd cluster, switches to the corresponding argocd cluster, and grep the apps in **Degraded** state, then try to find the reason why the app is in **Degraded** state. If there is failed pods, auto delete these pods in the app.

---

## Inputs
- **argocd_cluster**: The argocd cluster name (e.g., `argocd.dev.demo.is`, `argocd.staging.demo.is`)

---

## Steps

### 1. Login to argocd cluster
Use the provided argocd_cluster name to authenticate:

```bash
argocd login <argocd_cluster> --sso
```

Example:
```bash
argocd login argocd.dev.demo.is --sso
```

---

### 2. Switch argocd Context if needed
Switch to the corresponding argocd context if the current context is not the target argocd cluster:

```bash
argocd context <argocd_cluster>
```

Example:
```bash
argocd context argocd.dev.demo.is
```

---

### 3. Grep Degraded Apps
Run the following command to list and grep degraded apps:

```bash
argocd app list | grep -E "Degraded"
```

---

## Output
- Returns these in **Degraded** state apps' name in the argocd cluster.

Example:
```
chat-backend
```

---
