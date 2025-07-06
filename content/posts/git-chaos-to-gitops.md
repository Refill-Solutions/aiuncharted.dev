---
title: "From Git Chaos to GitOps: Building a Local Development Platform"
date: 2025-07-06
draft: false
description: "How a massive YAML file led to building a complete k3s + ArgoCD GitOps setup for local development"
tags: ["GitOps", "k3s", "ArgoCD", "Development", "Infrastructure"]
---

# From Git Chaos to GitOps: Building a Local Development Platform

**TL;DR**: A 26,657-line YAML file was killing git performance, so I spent the past week building a complete GitOps infrastructure with k3s + ArgoCD + NATS running locally. Perfect for cost-controlled development without API dependencies.

## The Problem: When Git Commits Take Forever

It started with a simple git commit that took forever. Investigation revealed the culprit: a massive `argocd.yaml` file with 26,657 lines making every git operation crawl. 

But fixing git performance was just the beginning. The real goal was building an environment for local development that gives me full control over costs and dependencies.

## Technology Decisions

### Container Orchestration: k3s

Why [k3s](/tools/software/#infrastructure--devops) over full Kubernetes?
- **Lightweight**: Perfect for single-node development
- **Resource efficient**: Ideal for dedicated hardware
- **Production compatible**: Can migrate to full K8s later  
- **WSL2 friendly**: Works great on Windows dev setups

### GitOps: ArgoCD

The heart of the operation with [ArgoCD](/tools/software/#infrastructure--devops):
- **Git-driven deployments**: Push to git, everything updates automatically
- **Declarative**: Infrastructure and applications as code
- **GitHub App integration**: Secure repository access
- **Visual dashboard**: Clear overview of what's running

### Packaging: Helm vs Kustomize

Initially went with Kustomize + [Helm](/tools/software/#infrastructure--devops) hybrid with environment overlays (base/development/production).

Final decision: Pure Helm after realizing we were over-engineering for a single-environment setup:
- Simpler mental model
- Better templating for dynamic values
- Easier to share and reuse charts
- ArgoCD ApplicationSet handles multiple deployments elegantly

### Access Strategy: Cloud vs Local

Explored Cloudflare Tunnel + Zero Trust for external access.

Chose localhost + port-forwarding for development:
- **Portability**: Works on any machine that clones the repo
- **Simplicity**: No DNS configuration or tunnel setup
- **[Tailscale](/tools/software/#infrastructure--devops) compatible**: Remote desktop access gives full GUI experience
- **Cost effective**: No external dependencies

### Messaging: NATS

For inter-service communication, [NATS](/tools/software/#infrastructure--devops) won because:
- Sub-millisecond latency
- JetStream for persistent messaging
- Tiny resource footprint
- Simple to configure and maintain

## Final Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                   Development Setup                        │
├─────────────────────────────────────────────────────────────┤
│  Linux Machine (k3s cluster)          Windows (via Tailscale) │
│  ├── ArgoCD (GitOps)                  ├── Remote Desktop    │
│  ├── NATS (Messaging)                 ├── Cursor IDE        │
│  ├── Shared Storage                   └── Browser           │
│  └── Application Platform                                   │
└─────────────────────────────────────────────────────────────┘
```

## Repository Structure

**gitops-factory** (Infrastructure):
- k3s installation scripts
- ArgoCD configuration with GitHub App integration
- NATS messaging system
- Shared storage setup
- Base Helm charts (nginx, shared-storage, application-base)

**application-platform** (Separate repo):
- Application orchestration platform
- Dynamic service spawning/scaling
- [FastAPI](/tools/software/#web-development) management interface

## Key Design Decisions

### 1. Localhost-First Development

Instead of complex DNS/tunnel setups:

```bash
# Simple access pattern
kubectl port-forward svc/argocd-server -n argocd 8080:443
# Open https://localhost:8080
```

Works identically whether you're:
- Working directly on the Linux machine
- Using Tailscale remote desktop access
- Running on WSL2 on Windows

### 2. Separate Infrastructure vs Application

- **gitops-factory**: Stable infrastructure (ArgoCD, NATS, storage)
- **application-platform**: Rapid iteration application code

This separation prevents accidentally breaking the cluster while developing applications.

### 3. Production-Ready but Simple

Each Helm chart includes:
- Development values (optimized for k3s)
- Production values (security contexts, resource limits)
- The ability to scale from laptop to cloud

## What's Next

- Complete the application platform implementation
- Build service templates for different use cases
- Scale up the hardware for more serious workloads
- Document everything for the community

## Technologies Used

- **[k3s](/tools/software/#infrastructure--devops)**: Lightweight Kubernetes distribution
- **[ArgoCD](/tools/software/#infrastructure--devops)**: GitOps continuous delivery
- **[Helm](/tools/software/#infrastructure--devops)**: Kubernetes package manager
- **[NATS](/tools/software/#infrastructure--devops)**: Cloud native messaging system
- **[Tailscale](/tools/software/#infrastructure--devops)**: Zero-config VPN for remote access
- **[FastAPI](/tools/software/#web-development)**: Modern Python web framework
- **[GitHub Apps](/tools/software/#development-environment)**: Secure repository integration

## Key Takeaways

- **Start simple, add complexity when needed** - We almost over-engineered with Kustomize overlays
- **Local development can be production-ready** - Proper Helm charts scale from laptop to cloud
- **Separate concerns cleanly** - Infrastructure vs application repositories
- **Choose boring technology** - NATS over Kafka, localhost over DNS complexity
- **Cost-effective development is possible** - No need for expensive external dependencies

The result? A completely functional GitOps environment for local development with remote access via Tailscale. Git commits are fast again, and we have a solid platform for future projects.

---

*All the technologies mentioned in this post are documented with detailed information and links on the [Tools](/tools) page.* 