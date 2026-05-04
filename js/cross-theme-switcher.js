// 跨主题切换导航脚本
// 允许在 hugo-book 和 papermod 两个版本间无缝切换

(function() {
  const THEME_PREF_KEY = 'monkvan-theme-preference';
  const CURRENT_PATH = window.location.pathname;
  
  // 检测当前主题
  function getCurrentTheme() {
    const parts = CURRENT_PATH.split('/').filter(Boolean);
    const themeIndex = parts.findIndex(part => part === 'hugo-book' || part === 'papermod');
    if (themeIndex >= 0) {
      return parts[themeIndex];
    }
    return null;
  }

  // 获取另一个主题
  function getOtherTheme() {
    const current = getCurrentTheme();
    return current === 'hugo-book' ? 'papermod' : 'hugo-book';
  }

  // 获取基础路径（支持子目录仓库部署）
  function getBasePath() {
    const parts = CURRENT_PATH.split('/').filter(Boolean);
    const themeIndex = parts.findIndex(part => part === 'hugo-book' || part === 'papermod');
    if (themeIndex > 0) {
      return `/${parts.slice(0, themeIndex).join('/')}/`;
    }
    return '/';
  }

  // 转换 URL 到另一个主题
  function getOtherThemeUrl() {
    const current = getCurrentTheme();
    if (!current) return getBasePath();

    const parts = CURRENT_PATH.split('/').filter(Boolean);
    const themeIndex = parts.findIndex(part => part === current);
    const basePath = getBasePath();
    const relativeParts = parts.slice(themeIndex + 1);
    const relativePath = relativeParts.length ? relativeParts.join('/') + '/' : '';
    const otherTheme = getOtherTheme();

    return `${basePath}${otherTheme}/${relativePath}`;
  }

  // 切换主题
  function switchTheme() {
    const targetTheme = getOtherTheme();
    localStorage.setItem(THEME_PREF_KEY, targetTheme);
    
    // 导航到另一个主题
    const otherUrl = getOtherThemeUrl();
    window.location.href = otherUrl;
  }

  // 保存用户选择
  function saveThemePreference() {
    const current = getCurrentTheme();
    if (current) {
      localStorage.setItem(THEME_PREF_KEY, current);
    }
  }

  // 初始化
  function init() {
    if (getCurrentTheme()) {
      saveThemePreference();
    }
  }

  // 暴露到全局作用域
  window.ThemeSwitcher = {
    getCurrentTheme,
    getOtherTheme,
    switchTheme,
    getOtherThemeUrl
  };

  init();
})();
