---
title: "Exploring Secure Remote Access: Tailscale, Sunshine, and Cloudflare Tunnel"
date: 2025-07-03T12:00:00+02:00
draft: false
---

Today, I dove into the world of secure remote access for my digital devices. My goal is to connect to my development machine from anywhere, without compromising security. I started by considering the traditional approach of opening ports on my router, but I want to avoid the potential security risks that come with that method. This led me to explore some popular alternatives.

Here's a brief overview of the tools I've been looking at:

*   **[Tailscale](https://tailscale.com/)**: This tool creates a secure network between your devices, making them accessible to each other as if they were on the same local network. It's built on top of WireGuard, a modern and fast VPN protocol. Setting up Tailscale seems straightforward, and it's known for its ease of use.

*   **[Sunshine](https://lizardbyte.dev/projects/sunshine/)**: Sunshine is a self-hosted game streaming host that can be used for remote desktop access. It's often used with the Moonlight client. While it's primarily for game streaming, it can also provide low-latency remote desktop access.

*   **[Cloudflare Tunnel](https://developers.cloudflare.com/cloudflare-one/connections/connect-apps/use-cases/ssh/)**: This service from Cloudflare allows you to expose a local server to the internet without opening any ports. It creates a secure tunnel from your server to the Cloudflare network, and you can then access it through a public hostname.

I haven't made a final decision yet, but I'm leaning towards Tailscale due to its simplicity and focus on secure networking. I'll continue to explore these options and will share my final choice and setup process in a future post.

In the meantime, I've created a new [Tools](/tools) page on the blog to keep track of all the tools I'm evaluating during this journey. Each tool will have a brief description and a link to its official website.