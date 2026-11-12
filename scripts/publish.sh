#!/usr/bin/env bash
set -euo pipefail
: "${VERSION:?}" "${CHANNEL:?}" "${GITHUB_REPOSITORY:?}"
# Independent public-repository fence: an older source ref cannot authorize stable.
# Read policy relative to this script, not the caller's working directory.
POLICY_FILE="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")/.." && pwd)/release-policy.json"
node - "$POLICY_FILE" "$CHANNEL" <<'JS'
const fs = require('node:fs');
const { maximumChannel } = JSON.parse(fs.readFileSync(process.argv[2], 'utf8'));
const ranks = { dev: 0, beta: 1, stable: 2 };
if (!Object.hasOwn(ranks, maximumChannel) || !Object.hasOwn(ranks, process.argv[3]) || ranks[process.argv[3]] > ranks[maximumChannel]) {
  console.error(`Release channel ${process.argv[3]} is blocked by release policy (${maximumChannel})`);
  process.exit(1);
}
JS
# This script runs in the public release repo; source code is never uploaded.
case "$CHANNEL" in
  dev|beta)
    [[ "$VERSION" =~ ^(0|[1-9][0-9]*)\.(0|[1-9][0-9]*)\.(0|[1-9][0-9]*)-${CHANNEL}\.[1-9][0-9]*$ ]] || exit 1
    classification=(--prerelease --latest=false)
    ;;
  stable)
    [[ "$VERSION" =~ ^(0|[1-9][0-9]*)\.(0|[1-9][0-9]*)\.(0|[1-9][0-9]*)$ ]] || exit 1
    classification=(--latest)
    ;;
  *) exit 1 ;;
esac
if gh release view "v$VERSION" --repo "$GITHUB_REPOSITORY" >/dev/null 2>&1; then
  echo "Release v$VERSION already exists; refusing to replace its assets" >&2
  exit 1
fi
shopt -s nullglob
assets=(dist/*)
((${#assets[@]} > 0)) || { echo 'No release artifacts' >&2; exit 1; }
gh release create "v$VERSION" "${assets[@]}" "${classification[@]}" \
  --repo "$GITHUB_REPOSITORY" --title "EOS Media $VERSION ($CHANNEL)" \
  --notes 'Native installers and CLI. Version, channel and source commit are recorded in the per-platform release manifests. Check SHA256SUMS.txt before installing. macOS builds use ad-hoc signatures with hardened runtime and are not Developer ID notarized. Dev, Beta and stable use separate application identities and data directories.'
