// 主题切换器
(function() {
  const THEME_KEY = 'monkvan-theme';
  const THEMES = ['hugo-book', 'PaperMod'];
  const DEFAULT_THEME = 'hugo-book';

  // 获取当前主题
  function getCurrentTheme() {
    return localStorage.getItem(THEME_KEY) || DEFAULT_THEME;
  }

  // 设置主题
  function setTheme(theme) {
    if (!THEMES.includes(theme)) return;
    localStorage.setItem(THEME_KEY, theme);
    updateThemeButton();
  }

  // 获取下一个主题
  function getNextTheme() {
    const current = getCurrentTheme();
    return current === THEMES[0] ? THEMES[1] : THEMES[0];
  }

  // 更新按钮文字
  function updateThemeButton() {
    const button = document.getElementById('theme-switcher-btn');
    if (!button) return;
    
    const current = getCurrentTheme();
    const next = getNextTheme();
    button.textContent = `切换到 ${next}`;
    button.dataset.next = next;
  }

  // 切换主题
  function switchTheme() {
    const next = getNextTheme();
    setTheme(next);
    
    // 通知用户需要重新加载
    const message = `主题将切换到 ${next}，请等待重新生成网站后刷新页面。`;
    alert(message);
    
    // 可选：尝试调用后端 API 重新编译
    fetch('/api/switch-theme', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ theme: next })
    }).catch(() => {
      console.log('后端 API 不可用，请手动运行: ./switch-theme.sh ' + next);
    });
  }

  // 初始化
  function init() {
    const button = document.getElementById('theme-switcher-btn');
    if (button) {
      updateThemeButton();
      button.addEventListener('click', switchTheme);
    }
  }

  // DOM 加载完成时初始化
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
  } else {
    init();
  }

  // 暴露到全局作用域
  window.ThemeSwitcher = {
    getCurrentTheme,
    setTheme,
    switchTheme,
    getNextTheme
  };
})();
