#!/usr/bin/env bash
set -euo pipefail
: "${WEBUI_DB_PASSWORD:?Missing WEBUI_DB_PASSWORD}"
: "${LITELLM_DB_PASSWORD:?Missing LITELLM_DB_PASSWORD}"

# psql's literal quoting prevents passwords from becoming SQL syntax.
psql --username "$POSTGRES_USER" --dbname postgres --set=ON_ERROR_STOP=1 \
  --set=webui_password="$WEBUI_DB_PASSWORD" \
  --set=litellm_password="$LITELLM_DB_PASSWORD" <<'SQL'
CREATE ROLE openwebui LOGIN PASSWORD :'webui_password' NOSUPERUSER NOCREATEDB NOCREATEROLE;
CREATE ROLE litellm LOGIN PASSWORD :'litellm_password' NOSUPERUSER NOCREATEDB NOCREATEROLE;
CREATE DATABASE openwebui OWNER openwebui;
CREATE DATABASE litellm OWNER litellm;
REVOKE ALL ON DATABASE openwebui FROM PUBLIC;
REVOKE ALL ON DATABASE litellm FROM PUBLIC;
SQL
