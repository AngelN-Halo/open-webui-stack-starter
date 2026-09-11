# Validation record

Validated on 2026-09-11 on a Linux x86-64 Docker host. Testing used a separate
Compose project, new volumes, and dynamically allocated localhost ports.
The existing deployment was not reconfigured or restarted.

## Passed

- Compose validation for the core stack and all optional profiles.
- Network/storage checks: no database, vector, extraction, terminal or Ollama host
  ports; default web/admin bindings on loopback; private data network; proxy only
  on the edge network; project-scoped volumes and no fixed container names.
- Four setup regression tests: independent random credentials and mode 0600,
  preservation of an existing .env, preservation of symlinks without following
  them, and rejection of configuration-injection input.
- Fresh PostgreSQL initialization and both applications' database migrations.
- Separate application logins, non-superuser roles, and cross-database denial.
- Open WebUI 0.11.1 health, generated administrator login, and disabled signup.
- LiteLLM authenticated model listing and rejection of unauthenticated access.
- Authenticated Qdrant access and rejection of unauthenticated access.
- Tika extraction of a synthetic text document.
- Synthetic file upload through Open WebUI, file processing, and embeddings stored
  in Qdrant using the bundled local embedding model.
- Full stack stop/start followed by repeated infrastructure checks, administrator
  login, and confirmation that document vectors persisted.
- Shell syntax, staged whitespace checks, and source comparison against generated
  secrets and known original-deployment identifiers.
- Pre-publication scan of the staged source using Gitleaks 8.30.1: no leaks found.
  The scanner download was checked against its published SHA-256 checksum.
- Documentation shell examples passed Bash syntax checking; all optional Compose
  profiles and setup regression tests were rechecked before publication.

Embedding downloads were disabled during the isolated test with
HF_HUB_OFFLINE=1. The pinned image's bundled embedding model was available.
The normal starter does not force offline mode.

## Not tested

- Real provider credentials, paid inference, virtual-key budgets, or chat answers
  and citations. Configure a model and complete the README's user-facing tests.
- NPM deployment, public DNS, certificate issuance, or reverse-proxy browser flows.
- Optional Ollama inference/GPU configuration, Open Terminal, or browser add-on
  integration with this new stack. Those profiles received configuration checks;
  browsers are supplied by the separate Browser Workspace repository.
- Other CPU architectures, PostgreSQL major upgrades, or backup restoration.
- A vulnerability audit of upstream images. Source scanning does not audit image
  dependencies or guarantee that every possible secret pattern is detected.

Run `python3 -m unittest discover -s tests -v` for local setup regression tests.
Run `./scripts/check.sh` after starting the core stack for infrastructure checks.
That script performs read-only checks and does not call a model or upload files.
