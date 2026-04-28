#!/usr/bin/env bash
set -euo pipefail

# Color helpers
RED='\033[0;31m'
GREEN='\033[0;32m'
BLUE='\033[0;34m'
NC='\033[0m'

echo_info() { echo -e "${GREEN}✓ $1${NC}"; }
echo_error() { echo -e "${RED}✗ $1${NC}"; }
echo_blue() { echo -e "${BLUE}→ $1${NC}"; }

# -----------------------------------------------------------------------------
# Configuration
# -----------------------------------------------------------------------------
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
BUILD_DIR="${SCRIPT_DIR}/public"
REMOTE="https://github.com/vanvj00001/hugoblox-blog.git"
BRANCH="main"   # GitHub Pages serves the repository root on this branch

# -----------------------------------------------------------------------------
# Build the Hugo site
# -----------------------------------------------------------------------------
echo_blue "🚀 构建 Hugo 站点..."
# Use the extended version with minify for production
hugo --minify
echo_info "站点构建完成"

# -----------------------------------------------------------------------------
# Deploy
# -----------------------------------------------------------------------------
if [ -d "${SCRIPT_DIR}/.git" ]; then
  echo_blue "⚙️ 检测到本目录已是 Git 仓库，使用本地仓库部署"
  cd "${SCRIPT_DIR}"
  # Ensure we are on the correct branch
  git checkout "${BRANCH}" 2>/dev/null || git checkout -b "${BRANCH}"
  # Remove everything except .git (ignore errors for missing files)
  git rm -r . --ignore-unmatch || true
else
  echo_blue "⚙️ 未检测到 Git 仓库，克隆远程仓库进行部署"
  TMPDIR=$(mktemp -d)
  git clone "${REMOTE}" "${TMPDIR}"
  cd "${TMPDIR}"
  git checkout -B "${BRANCH}"  # create/force branch
  # Clean repo (keep .git only)
  git rm -r . --ignore-unmatch || true
  # Remove any stray submodule entries (PaperMod is not needed for hugo_book)
  git rm -f --cached themes/PaperMod 2>/dev/null || true
  rm -rf .gitmodules 2>/dev/null || true
fi

# Copy generated site into the repository root
cp -r "${BUILD_DIR}/"* .
# Ensure GitHub Pages ignores Hugo pipelines
touch .nojekyll

# Commit and push
git add -A
if git diff --cached --quiet; then
  echo_info "没有新内容需要部署"
else
  git commit -m "Deploy: $(date +'%Y-%m-%d %H:%M:%S')"
  git push "${REMOTE}" "${BRANCH}" --force
  echo_info "部署已推送到 ${REMOTE}" 
fi

echo ""
echo_info "完成！"
echo_blue "访问: https://vanvj00001.github.io/hugoblox-blog/"
