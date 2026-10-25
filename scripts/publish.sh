#!/usr/bin/env bash
set -euo pipefail
: "${VERSION:?}" "${CHANNEL:?}" "${GITHUB_REPOSITORY:?}"
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
  --notes 'Native installers and CLI. Version, channel and source commit are recorded in the per-platform release manifests. Check SHA256SUMS.txt before installing. macOS builds are unsigned. Dev, Beta and stable use separate application identities and data directories.'
