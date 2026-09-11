# Security and data boundaries

This starter contains no production data, provider keys, organization branding,
internal domains, or copied Git history. Generate fresh credentials with setup.sh.

- .env is private, ignored by Git, and created with mode 0600. Docker administrators
  can inspect container environments. Use a secret manager for stronger controls.
- PostgreSQL, Qdrant and Tika have no published ports and use an internal network.
  The application and gateway also have an outbound-capable network for providers.
- Qdrant requires an API key. PostgreSQL applications have distinct non-superuser
  roles and cannot connect to each other's application database.
- Open WebUI and LiteLLM listen on host loopback by default. Signup is disabled;
  setup generates an initial administrator password. Restrict new users deliberately.
- LiteLLM master keys are administrative credentials. Give Open WebUI a virtual
  key with explicit model access, budget and rate limits. Provider-side spend
  controls remain useful; budget checks are not a guarantee of zero overspend.
- Keep LITELLM_SALT_KEY with your encrypted backups. Changing it can make stored
  provider credentials unreadable. Do not regenerate .env on an existing database.
- Optional terminal and browser services execute actions and may retain sessions.
  Restrict them to trusted administrators. They are not per-user sandboxes.
- NPM's admin port stays on loopback even when public HTTP/HTTPS is enabled.
  TLS certificates and the proxy database are sensitive runtime data.
- Profiles and Docker networks are not comprehensive security boundaries. Apply
  egress controls or dedicated hosts for untrusted workloads.
- Never publish volumes, database dumps, log archives, or baseline snapshots.
  Report issues without real credentials or private page/chat content.

No automatic reset or volume-deletion scripts are included. A new project name
creates separate volumes; it does not migrate or erase an existing deployment.
