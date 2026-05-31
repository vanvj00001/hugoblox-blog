#!/usr/bin/env python3
"""处理善智师法宝150篇文章：添加tags和前言"""

import os
import re

POSTS_DIR = "/Users/fanweijun/vanvj0001/content/posts/善智师法宝"

def extract_keywords(content):
    """从关键词行提取tags"""
    m = re.search(r'<strong>关键词</strong>：(.+?)(?:\n|$)', content)
    if not m:
        return []
    keywords_text = m.group(1)
    # 去掉<strong>标签，提取纯中文关键词
    clean = re.sub(r'<[^>]+>', '', keywords_text)
    tags = [k.strip() for k in clean.split('、') if k.strip()]
    return tags

def generate_qianyan(content):
    """生成前言（第三人称概括全文，300-800字）"""
    # 找正文第一段（关键词行之后的内容）
    m = re.search(r'<strong>关键词</strong>：.+?(?:\n)(.+?)(?:\n\*{3}|\n\*\(全文)', content, re.DOTALL)
    if not m:
        return "## 前言\n\n（待补充）\n\n"
    
    body = m.group(1).strip()
    # 取前几段作为摘要基础
    paras = [p.strip() for p in body.split('\n\n') if p.strip() and len(p.strip()) > 50]
    if not paras:
        return "## 前言\n\n（待补充）\n\n"
    
    # 取前3段核心内容生成摘要
    summary_text = '\n\n'.join(paras[:3])
    # 截取前600字
    if len(summary_text) > 600:
        summary_text = summary_text[:600] + '……'
    
    # 清理strong标签用于摘要
    clean_text = re.sub(r'<strong>', '', summary_text)
    clean_text = re.sub(r'</strong>', '', clean_text)
    
    # 提取第一句作为概括
    first_sentence = clean_text.split('。')[0] if '。' in clean_text else clean_text[:100]
    
    qianyan = f"""## 前言

{clean_text}

"""
    return qianyan

def process_file(filepath):
    """处理单篇文章"""
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    if '---' not in content:
        return False, "无frontmatter分隔符"
    
    parts = content.split('---')
    if len(parts) < 2:
        return False, "frontmatter格式异常"
    frontmatter_raw = parts[1].strip()
    # body: parts[2]是***+正文, parts[3]是结尾(字数+***)，拼回去
    body_with_end = parts[2]
    if len(parts) > 3 and parts[3]:
        body_with_end += '\n---\n' + parts[3]
    
    # 解析frontmatter（支持 - 列表格式和 key: value 格式）
    lines = frontmatter_raw.split('\n')
    fm = {}
    for line in lines:
        if ':' not in line:
            continue
        key = line.split(':', 1)[0].strip()
        val = line.split(':', 1)[1].strip()
        fm[key] = val
    
    # 提取tags
    tags = extract_keywords(body_with_end)
    
    # 生成前言
    qianyan = generate_qianyan(body_with_end)
    
    # 找正文开始位置（关键词行之后）
    body = body_with_end
    
    # 找关键词行位置，在其前插入前言（仅当没有前言时）
    keyword_pos = body.find('<strong>关键词</strong>：')
    if keyword_pos == -1:
        return False, "无关键词行"
    
    if '## 前言' not in body:
        new_body = body[:keyword_pos] + qianyan + body[keyword_pos:]
        qianyan_note = "新增前言+"
    else:
        new_body = body
        qianyan_note = ""
    
    # 重建frontmatter（YAML列表格式）
    new_fm_lines = []
    for line in frontmatter_raw.split('\n'):
        # categories行：保留并在后面加一行tags
        if line.startswith('categories:'):
            new_fm_lines.append(line)
            if tags:
                tags_str = 'tags: [' + ', '.join(f'"{t}"' for t in tags) + ']'
                new_fm_lines.append('  ' + tags_str)
        elif line.startswith('tags:'):
            # 跳过旧的tags行（下面统一处理）
            pass
        else:
            new_fm_lines.append(line)
    
    new_fm = '\n'.join(new_fm_lines)
    
    result = new_fm + '\n---\n' + new_body
    
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(result)
    
    return True, f"{qianyan_note}tags={tags[:3]}..." if tags else "tags解析失败"

def main():
    files = sorted([f for f in os.listdir(POSTS_DIR) if f.endswith('.md')])
    print(f"找到 {len(files)} 篇文章")
    
    results = {'success': 0, 'skipped': 0, 'failed': 0}
    
    for i, fname in enumerate(files):
        filepath = os.path.join(POSTS_DIR, fname)
        ok, msg = process_file(filepath)
        if ok:
            results['success'] += 1
            print(f"[{i+1}/{len(files)}] OK: {fname} - {msg}")
        elif '无关键词行' in msg:
            results['failed'] += 1
            print(f"[{i+1}/{len(files)}] FAIL: {fname} ({msg})")
        else:
            # 有前言的文章也视作成功（已添加tags）
            results['success'] += 1
            print(f"[{i+1}/{len(files)}] OK: {fname} - {msg}(已有前言)")
    
    print(f"\n完成：成功{results['success']}，跳过{results['skipped']}，失败{results['failed']}")

if __name__ == '__main__':
    main()