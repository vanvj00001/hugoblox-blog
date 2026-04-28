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
cd "$SCRIPT_DIR"
BUILD_DIR="${SCRIPT_DIR}/public"

echo_blue "🚀 部署脚本"
echo ""



echo_blue "清理并创建目录..."
rm -rf "$BUILD_DIR"
mkdir -p "$BUILD_DIR"
echo_info "完成"
echo ""


# Theme is managed manually; ensure the desired theme exists in themes/ directory

echo_blue "构建 Hugo 站点..."
hugo --minify
echo_info "完成"
echo ""

echo_blue "同步到 GitHub..."
if [ -d ".git" ]; then
  git checkout main 2>/dev/null || git checkout -b main
  git pull origin main --ff-only 2>/dev/null || true

  find . -maxdepth 1 -not -name '.git' -not -name 'public' -not -name 'hugo.toml' -not -name 'deploy.sh' -not -name 'go.mod' -not -name 'go.sum' -not -name '.gitignore' -not -name 'README.md' -not -name 'LICENSE' -type f -exec rm -f {} +
  find . -maxdepth 1 -not -name '.git' -not -name 'public' -not -name '.' -not -name 'content' -not -name 'themes' -not -name 'static' -not -name 'assets' -not -name 'resources' -not -name '.github' -not -name 'layouts' -type d -exec rm -rf {} + 2>/dev/null || true

  cp -r "$BUILD_DIR"/* ./
  touch .nojekyll

  git add -A
  if git diff --cached --quiet; then
      echo_info "没有新内容"
  else
      git commit -m "Deploy: $(date +'%Y-%m-%d %H:%M:%S')"
      git push origin main
  fi
else
  echo_info "未检测到 Git 仓库，已跳过同步步骤"
fi

echo ""
echo_info "完成！"
echo_blue "访问: https://vanvj00001.github.io/hugoblox-blog/"
