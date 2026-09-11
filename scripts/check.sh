#!/usr/bin/env bash
set -euo pipefail
cd -- "$(dirname -- "$0")/.."
docker compose config --quiet
docker compose exec -T postgres bash -euo pipefail -c '
  PGPASSWORD="$WEBUI_DB_PASSWORD" psql -h 127.0.0.1 -U openwebui -d openwebui -v ON_ERROR_STOP=1 -Atc "SELECT 1" >/dev/null
  PGPASSWORD="$LITELLM_DB_PASSWORD" psql -h 127.0.0.1 -U litellm -d litellm -v ON_ERROR_STOP=1 -Atc "SELECT 1" >/dev/null
  result=$(psql -U postgres -d postgres -Atc "SELECT count(*) FROM pg_roles WHERE rolname IN ('\''openwebui'\'', '\''litellm'\'') AND NOT rolsuper AND NOT rolcreatedb AND NOT rolcreaterole")
  test "$result" = 2
  if PGPASSWORD="$WEBUI_DB_PASSWORD" psql -h 127.0.0.1 -U openwebui -d litellm -c "SELECT 1" >/dev/null 2>&1; then
    echo "FAIL: Open WebUI role can access LiteLLM database"; exit 1
  fi
  if PGPASSWORD="$LITELLM_DB_PASSWORD" psql -h 127.0.0.1 -U litellm -d openwebui -c "SELECT 1" >/dev/null 2>&1; then
    echo "FAIL: LiteLLM role can access Open WebUI database"; exit 1
  fi
  echo "PASS: database logins, restricted roles, cross-database denial"
'
docker compose exec -T open-webui python - <<'PY'
import os
import urllib.error
import urllib.request

def get(url, headers=None):
    with urllib.request.urlopen(urllib.request.Request(url, headers=headers or {}), timeout=15) as response:
        assert response.status == 200

get('http://127.0.0.1:8080/health')
get('http://tika:9998/tika')
get('http://litellm:4000/health/liveliness')
get('http://qdrant:6333/collections', {'api-key': os.environ['QDRANT_API_KEY']})
try:
    get('http://qdrant:6333/collections')
except urllib.error.HTTPError as error:
    assert error.code in (401, 403)
else:
    raise SystemExit('FAIL: Qdrant allowed unauthenticated access')
print('PASS: Open WebUI, Tika, LiteLLM, and Qdrant connectivity and Qdrant authentication')
PY
docker compose exec -T litellm python - <<'PY'
import os
import urllib.request
import urllib.error
url = 'http://127.0.0.1:4000/v1/models'
request = urllib.request.Request(url, headers={'Authorization': 'Bearer ' + os.environ['LITELLM_MASTER_KEY']})
with urllib.request.urlopen(request, timeout=15) as response:
    assert response.status == 200
try:
    urllib.request.urlopen(url, timeout=15)
except urllib.error.HTTPError as error:
    assert error.code in (401, 403)
else:
    raise SystemExit('FAIL: LiteLLM allowed unauthenticated model listing')
print('PASS: LiteLLM authenticated access and unauthenticated denial')
PY
printf 'Infrastructure checks passed. Test a configured model and document ingestion separately.\n'
