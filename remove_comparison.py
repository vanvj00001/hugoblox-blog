#!/usr/bin/env python3
import re
import os

japan_dir = "/Users/fanweijun/vanvj0001/content/posts/japan"
files = [f for f in os.listdir(japan_dir) if f.endswith(".md") and f != "_index.md"]

for filename in files:
    filepath = os.path.join(japan_dir, filename)
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 删除"与其他神话的比较"整个章节
    # 匹配从"## X、与其他神话的比较"开始到下一个"## "或文件结尾
    pattern = r'\n## [一二三四五六七八九十]+、与其他神话的比较.*?(?=\n## [一二三四五六七八九十]+、|\n## 结语|\Z)'
    new_content = re.sub(pattern, '', content, flags=re.DOTALL)
    
    # 重新编号章节：六→五，七→六，等等
    # 先处理二级标题
    new_content = re.sub(r'\n## 六、', '\n## 五、', new_content)
    new_content = re.sub(r'\n## 七、', '\n## 六、', new_content)
    new_content = re.sub(r'\n## 八、', '\n## 七、', new_content)
    
    # 再处理三级标题
    new_content = re.sub(r'\n### 6\.', '\n### 5.', new_content)
    new_content = re.sub(r'\n### 7\.', '\n### 6.', new_content)
    new_content = re.sub(r'\n### 8\.', '\n### 7.', new_content)
    
    if new_content != content:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(new_content)
        print(f"已处理: {filename}")
    else:
        print(f"未找到比较章节: {filename}")

print("\n完成！所有文章的'与其他神话的比较'章节已去除并重新编号。")
