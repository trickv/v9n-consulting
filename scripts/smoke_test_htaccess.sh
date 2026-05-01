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
        --host) HOST="${2:?--host requires a URL}"; shift 2 ;;
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

# fetch <path> -> echoes HTTP status code.
# Deliberately does NOT follow redirects: assert_redirect needs to see the
# 3xx, and following redirects in assert_blocked/assert_public would mask
# misconfigurations that 302 a sensitive path to a public page.
fetch() {
    curl -sS -o /dev/null -w '%{http_code}' --max-time 10 "$HOST$1"
}

# assert_status <path> <expected_code> [label]
#   passes only on the exact status code. Use this when 403 vs 404 matters
#   (e.g. dotfile rule must produce 404 specifically; <Files> deny rule must
#   produce 403). Catches regressions where a rule "blocks" but via the
#   wrong mechanism — which is itself a sign the rule is broken.
assert_status() {
    local path="$1"
    local expected="$2"
    local label="${3:-$path}"
    local code
    code=$(fetch "$path")
    if [ "$code" = "$expected" ]; then
        PASS=$((PASS+1))
        [ "$VERBOSE" = 1 ] && printf '  ok  %-50s status %s\n' "$label" "$code"
    else
        FAIL=$((FAIL+1))
        FAILED_DETAIL+=("STATUS check failed: $label -> $code (expected $expected)")
        printf '  FAIL %-50s expected %s, got %s\n' "$label" "$expected" "$code"
    fi
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

echo "Strict status (403 vs 404 matters — 403 = <Files>/Require denied, 404 = RedirectMatch):"
# Dotfile rule (root .htaccess: RedirectMatch 404 /\..*$). Must be 404, not
# 403, or the rule has been replaced by something weaker.
# Note: /.htaccess is NOT tested here because Apache has a built-in global
# rule (<FilesMatch "^\.ht">) that 403s any .ht* file before our rule ever
# runs. Tested separately below as a 403.
assert_status "/.git/config"                            404
assert_status "/.git/HEAD"                              404
assert_status "/.claude/settings.local.json"            404
# Nested dotdir — proves the regex is unanchored and catches dotpaths at
# any depth, not just the root.
assert_status "/just-do-ai/.claude/settings.local.json" 404
# .pre-commit-config.yaml: starts with ".", so the dotfile RedirectMatch
# wins and returns 404.
assert_status "/.pre-commit-config.yaml"                404
# Apache's built-in <FilesMatch "^\.ht"> rule returns 403 for any .ht* file
# regardless of our config — verify the global protection is active.
assert_status "/.htaccess"                              403

# <Files>/<FilesMatch> deny rules at root must produce 403.
assert_status "/pull"                                   403
assert_status "/webhook.cgi"                            403
assert_status "/CLAUDE.md"                              403
assert_status "/DEPLOYMENT.md"                          403
assert_status "/README-website.md"                      403
assert_status "/SEO-SOCIAL-TAGS-SUMMARY.md"             403
# <FilesMatch "\.(py|ya?ml)$"> at root.
assert_status "/just-do-ai/build_landscape.py"          403
assert_status "/just-do-ai/ai_tools_landscape.yaml"     403

# Per-directory "Require all denied" must produce 403.
assert_status "/scripts/check_ga_tracking.py"           403
assert_status "/just-do-ai/b-cards/qr-generator.html"   403
assert_status "/just-do-ai/input-images/IMG_4566.jpg"   403

echo
echo "Other blocked paths (any 4xx is fine):"
# Broader sample of files inside protected directories. If a Require all
# denied rule were ever replaced by a too-narrow FilesMatch, these would
# leak even though the strict-status assertions above still pass.
assert_blocked "/scripts/smoke_test_htaccess.sh"
assert_blocked "/scripts/.htaccess"
# b-cards: cover binary, SVG, MD, and an additional HTML beyond the strict probe.
assert_blocked "/just-do-ai/b-cards/qr-code.png"
assert_blocked "/just-do-ai/b-cards/qr-code-v9n.png"
assert_blocked "/just-do-ai/b-cards/v9n_back.svg"
assert_blocked "/just-do-ai/b-cards/example_front.svg"
assert_blocked "/just-do-ai/b-cards/business-card-template.md"
assert_blocked "/just-do-ai/b-cards/business_cards_back_v9n.html"
assert_blocked "/just-do-ai/b-cards/README.md"
assert_blocked "/just-do-ai/b-cards/.htaccess"
# input-images: cover the venv (would expose Python internals if leaked)
# and a couple more raw photos.
assert_blocked "/just-do-ai/input-images/convert_heic.py"
assert_blocked "/just-do-ai/input-images/convert_heic_portable.py"
assert_blocked "/just-do-ai/input-images/heic_converter/pyvenv.cfg"
assert_blocked "/just-do-ai/input-images/heic_converter/bin/python3"
assert_blocked "/just-do-ai/input-images/.htaccess"

echo
echo "Directory listings:"
# If Options +Indexes were ever enabled and a deny rule got narrowed,
# requesting the bare directory would return an autoindex with a 200.
# Per-dir deny rules must block these.
assert_blocked "/scripts/"
assert_blocked "/just-do-ai/b-cards/"
assert_blocked "/just-do-ai/input-images/"
assert_blocked "/just-do-ai/input-images/heic_converter/"
# Dotdirs — listing must 404 like other dotpaths.
assert_status "/.git/"        404 "/.git/"
assert_status "/.claude/"     404 "/.claude/"

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
    for d in "${FAILED_DETAIL[@]:-}"; do [ -n "$d" ] && echo "  - $d"; done
    exit 1
fi
exit 0
