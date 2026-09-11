# Upstream components

Original configuration and helper scripts in this starter are MIT licensed.
Upstream applications, images, model weights and dependencies retain their own
licenses. No upstream source or image is relicensed by this repository.

- [Open WebUI](https://github.com/open-webui/open-webui) and its
  [license](https://github.com/open-webui/open-webui/blob/main/LICENSE)
- [LiteLLM](https://github.com/BerriAI/litellm)
- [PostgreSQL image](https://hub.docker.com/_/postgres)
- [Qdrant](https://github.com/qdrant/qdrant)
- [Apache Tika](https://tika.apache.org/)
- [Nginx Proxy Manager](https://github.com/NginxProxyManager/nginx-proxy-manager)
- [Ollama](https://github.com/ollama/ollama)
- [Open Terminal](https://github.com/open-webui/open-terminal)

The starter uses the unmodified upstream Open WebUI image and preserves branding
and attribution. No custom branding Dockerfile is required. Any later branding
changes must account for the applicable upstream license.

Core defaults use immutable image digests from images available during preparation
on 2026-09-11. These are reproducible selections, not a claim that the images are
free of vulnerabilities or the newest available versions. The optional NPM image
uses release tag 2.15.1. Verify architecture support and scan images for your target
environment before deployment. Update deliberately and repeat acceptance checks.

For human-readable versions and pinning details, see the
[version inventory](README.md#versions-and-update-policy). For changing versions,
follow the [upgrade procedure](README.md#upgrading-deliberately).
