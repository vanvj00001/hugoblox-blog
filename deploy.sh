#!/usr/bin/env bash
set -euo pipefail

RED='\033[0;31m'
GREEN='\033[0;32m'
BLUE='\033[0;34m'
NC='\033[0m'

echo_info() { echo -e "${GREEN}✓ $1${NC}"; }
echo_error() { echo -e "${RED}✗ $1${NC}"; }
echo_blue() { echo -e "${BLUE}→ $1${NC}"; }

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REMOTE="https://github.com/vanvj00001/hugoblox-blog.git"
BRANCH="gh-pages"

# ── Build ────────────────────────────────────────────────────────────────────
echo_blue "🚀 构建 Hugo 站点..."
rm -rf "${SCRIPT_DIR}/public"
export HUGO_POSTCSS_ARGS="--allow-fs-read"
hugo --minify --source "${SCRIPT_DIR}"
echo_info "站点构建完成"

# ── Deploy (isolated clone) ──────────────────────────────────────────────────
DEPLOY_DIR=$(mktemp -d)
trap 'rm -rf "$DEPLOY_DIR"' EXIT

echo_blue "⚙️ 克隆部署仓库..."
if ! git clone --single-branch --branch "${BRANCH}" "${REMOTE}" "${DEPLOY_DIR}" 2>/dev/null; then
  git init "${DEPLOY_DIR}"
  cd "${DEPLOY_DIR}"
  git remote add origin "${REMOTE}" 2>/dev/null || true
fi

cd "${DEPLOY_DIR}"
git checkout -B "${BRANCH}"

# Clean everything except .git
find . -maxdepth 1 -not -name '.git' -not -name '.' -delete

# Copy built site
cp -r "${SCRIPT_DIR}/public/"* .
touch .nojekyll

# Commit and force-push
git add -A
if git diff --cached --quiet; then
  echo_info "没有新内容需要部署"
else
  git commit -m "Deploy: $(date +'%Y-%m-%d %H:%M:%S')"
  git push origin "HEAD:${BRANCH}" --force
  echo_info "部署已推送到 ${REMOTE}"
fi

echo ""
echo_info "完成！"
echo_blue "访问: https://vanvj00001.github.io/hugoblox-blog/"
