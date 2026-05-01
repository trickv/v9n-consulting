#!/usr/bin/env bash
#
# Smoke-test the .htaccess protections against a deployed site.
#
# Usage:
#   scripts/smoke_test_htaccess.sh                    # tests https://v9n.us
#   scripts/smoke_test_htaccess.sh --host https://staging.example.com
#   scripts/smoke_test_htaccess.sh --verbose          # show every request
#
# Exit code is 0 if every assertion holds, 1 otherwise.

set -u

HOST="https://v9n.us"
VERBOSE=0

while [ $# -gt 0 ]; do
    case "$1" in
        --host) HOST="$2"; shift 2 ;;
        --verbose|-v) VERBOSE=1; shift ;;
        -h|--help)
            sed -n '3,11p' "$0" | sed 's/^# \{0,1\}//'
            exit 0
            ;;
        *) echo "unknown arg: $1" >&2; exit 2 ;;
    esac
done

HOST="${HOST%/}"
PASS=0
FAIL=0
FAILED_DETAIL=()

# fetch <path> -> echoes HTTP status code, follows no redirects
fetch() {
    curl -sS -o /dev/null -w '%{http_code}' --max-time 10 "$HOST$1"
}

# assert_blocked <path> [label]
#   passes if status is 401/403/404 (anything that says "not getting it")
assert_blocked() {
    local path="$1"
    local label="${2:-$path}"
    local code
    code=$(fetch "$path")
    case "$code" in
        401|403|404)
            PASS=$((PASS+1))
            [ "$VERBOSE" = 1 ] && printf '  ok  %-50s blocked (%s)\n' "$label" "$code"
            ;;
        *)
            FAIL=$((FAIL+1))
            FAILED_DETAIL+=("BLOCKED check failed: $label -> $code (expected 401/403/404)")
            printf '  FAIL %-50s expected blocked, got %s\n' "$label" "$code"
            ;;
    esac
}

# assert_public <path> [label]
#   passes if status is 2xx
assert_public() {
    local path="$1"
    local label="${2:-$path}"
    local code
    code=$(fetch "$path")
    case "$code" in
        2??)
            PASS=$((PASS+1))
            [ "$VERBOSE" = 1 ] && printf '  ok  %-50s public  (%s)\n' "$label" "$code"
            ;;
        *)
            FAIL=$((FAIL+1))
            FAILED_DETAIL+=("PUBLIC check failed: $label -> $code (expected 2xx)")
            printf '  FAIL %-50s expected public, got %s\n' "$label" "$code"
            ;;
    esac
}

# assert_redirect <path> [label]
#   passes if status is 301/302/307/308 — for paths intentionally redirected
#   via .htaccess (e.g. renamed pages), where the test should confirm the
#   URL is reachable, not silently broken or denied.
assert_redirect() {
    local path="$1"
    local label="${2:-$path}"
    local code
    code=$(fetch "$path")
    case "$code" in
        301|302|307|308)
            PASS=$((PASS+1))
            [ "$VERBOSE" = 1 ] && printf '  ok  %-50s redirect (%s)\n' "$label" "$code"
            ;;
        *)
            FAIL=$((FAIL+1))
            FAILED_DETAIL+=("REDIRECT check failed: $label -> $code (expected 3xx)")
            printf '  FAIL %-50s expected redirect, got %s\n' "$label" "$code"
            ;;
    esac
}

echo "Host: $HOST"
echo

echo "Should be blocked:"
# Dotfiles / dotdirs -- root .htaccess handles via RedirectMatch 404
assert_blocked "/.htaccess"
assert_blocked "/.git/config"
assert_blocked "/.git/HEAD"
assert_blocked "/.claude/settings.local.json"
assert_blocked "/.pre-commit-config.yaml"

# Repo scripts at root
assert_blocked "/pull"
assert_blocked "/webhook.cgi"

# Root-level markdown docs
assert_blocked "/CLAUDE.md"
assert_blocked "/DEPLOYMENT.md"
assert_blocked "/README-website.md"
assert_blocked "/SEO-SOCIAL-TAGS-SUMMARY.md"

# Per-directory deny rules
assert_blocked "/scripts/check_ga_tracking.py"
assert_blocked "/scripts/smoke_test_htaccess.sh"
assert_blocked "/scripts/.htaccess"
assert_blocked "/just-do-ai/b-cards/qr-generator.html"
assert_blocked "/just-do-ai/b-cards/business_cards_front.html"
assert_blocked "/just-do-ai/b-cards/README.md"
assert_blocked "/just-do-ai/input-images/IMG_4566.jpg"
assert_blocked "/just-do-ai/input-images/convert_heic.py"

echo
echo "Should be public:"
# Core public pages
assert_public "/"                                                  "/ (root site)"
assert_public "/just-do-ai/"                                       "/just-do-ai/"
assert_public "/just-do-ai/index.html"
assert_public "/just-do-ai/ai_tools_landscape.html"
assert_public "/just-do-ai/ai_tools_landscape_beta.html"
assert_public "/just-do-ai/bootcamp.html"
assert_public "/just-do-ai/cli-crib-sheet.html"
assert_public "/just-do-ai/claude-code-tools.html"
assert_public "/just-do-ai/coding-with-ai-setup-guide.html"
assert_public "/just-do-ai/coding/journey-to-agentic-ai-engineering.html"
assert_public "/just-do-ai/coding/claude-code-field-guide.html"
assert_public "/just-do-ai/coding/claude-code-fundamentals-crib-sheet.html"
assert_public "/just-do-ai/coding/claude-code-to-codex-crib-sheet.html"
assert_public "/look-up/privacy.html"

# Deliberately-public markdown (NOT at repo root, so root .htaccess shouldn't touch it)
assert_public "/apps/baby-monitor/PRIVACY.md"

# Public images
assert_public "/just-do-ai/images/sunset-0.5x-crop.jpg"

echo
echo "Should redirect (intentional .htaccess redirects):"
# choosing-an-ai-coding-tool was renamed to journey-to-agentic-ai-engineering;
# just-do-ai/coding/.htaccess preserves the old URL via 302.
assert_redirect "/just-do-ai/coding/choosing-an-ai-coding-tool.html"
# bootcamp/ -> /just-do-ai/bootcamp.html
assert_redirect "/bootcamp/"

echo
echo "Results: $PASS passed, $FAIL failed"
if [ "$FAIL" -gt 0 ]; then
    echo
    echo "Failures:"
    for d in "${FAILED_DETAIL[@]}"; do echo "  - $d"; done
    exit 1
fi
exit 0
