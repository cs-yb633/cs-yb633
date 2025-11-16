import os
import markdown
from pygments.formatters import HtmlFormatter
from bs4 import BeautifulSoup

CSS_STYLE = HtmlFormatter().get_style_defs('.codehilite')

PAGE_TEMPLATE = """
<!DOCTYPE html>
<html lang="zh">
<head>
<meta charset="UTF-8">
<title>{title}</title>
<meta name="viewport" content="width=device-width, initial-scale=1">

<style>
{css}

/* ======= CSDIY 深蓝黑主题 ======= */
:root {{
    --bg: #0d1117;
    --bg2: #161b22;
    --text: #e6e6e6;
    --border: #30363d;
    --code-bg: #1c2128;

    --accent: #2387ff;  /* 高级亮蓝 */
}}

.dark {{
    --bg: #ffffff;
    --bg2: #f7f7f7;
    --text: #000000;
    --border: #d0d0d0;
    --code-bg: #f0f0f0;
}}

body {{
    margin: 0;
    display: flex;
    background: var(--bg);
    color: var(--text);
    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
}}

/* ======= 顶部导航栏 ======= */
.navbar {{
    position: fixed;
    top: 0;
    width: 100%;
    height: 52px;
    background: var(--bg2);
    color: var(--text);
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 0 20px;
    border-bottom: 1px solid var(--border);
    z-index: 10;
}}

.nav-left {{
    font-size: 20px;
    font-weight: bold;
}}

.nav-right {{
    display: flex;
    align-items: center;
    gap: 15px;
}}

.nav-right input {{
    padding: 6px 10px;
    width: 180px;
    border-radius: 6px;
    border: 1px solid var(--border);
    background: var(--bg);
    color: var(--text);
}}

/* ======= 侧边栏 ======= */
.sidebar {{
    margin-top: 52px;
    width: 260px;
    background: var(--bg2);
    border-right: 1px solid var(--border);
    height: calc(100vh - 52px);
    overflow-y: auto;
    padding: 10px;
    position: fixed;
}}

.toc-item {{
    margin: 6px 0;
    padding: 4px 6px;
    border-radius: 5px;
    cursor: pointer;
    user-select: none;
}}

.toc-item:hover {{
    background: #2387ff33;
}}

.toc-link {{
    color: var(--text);
    text-decoration: none;
}}

.toc-h2 {{
    margin-left: 15px;
    display: none;
}}

.toc-h3 {{
    margin-left: 30px;
    display: none;
}}

/* ======= 内容区 ======= */
.content {{
    margin-left: 280px;
    padding: 20px;
    margin-top: 52px;
    width: calc(100% - 280px);
    color: var(--text);
}}

a {{
    color: var(--accent);
}}

/* ======= 代码块 ======= */
pre {{
    background: var(--code-bg);
    padding: 12px;
    border-radius: 6px;
    overflow-x: auto;
}}
</style>

<script>
// 切换主题
function toggleDarkMode() {{
    document.body.classList.toggle("dark");
    localStorage.setItem("dark", document.body.classList.contains("dark"));
}}

window.onload = function() {{
    if (localStorage.getItem("dark") === "true") {{
        document.body.classList.add("dark");
    }}
}};

// 搜索并跳转
function searchContent() {{
    const q = document.getElementById("search").value.toLowerCase();
    const blocks = document.querySelectorAll(".content *");
    let firstMatch = null;

    blocks.forEach(b => {{
        if (b.innerText && b.innerText.toLowerCase().includes(q)) {{
            b.style.background = "#2387ff44";
            if (!firstMatch) {{
                firstMatch = b;
            }}
        }} else {{
            b.style.background = "transparent";
        }}
    }});

    // 如果找到匹配项，跳转到第一个匹配项
    if (firstMatch) {{
        window.location.hash = firstMatch.id;
    }}
}}

// 折叠目录
function toggle(id) {{
    let group = document.querySelectorAll("." + id);
    group.forEach(el => {{
        el.style.display = el.style.display === "none" ? "block" : "none";
    }});
}}
</script>
</head>

<body>

<div class="navbar">
    <div class="nav-left">My CS61A Notes</div>

    <div class="nav-right">
        <input id="search" onkeyup="searchContent()" placeholder="Search...">

        <a href="https://github.com/MYB0503/CS61A" target="_blank">
            <img src="https://cdn-icons-png.flaticon.com/512/25/25231.png" width="22">
        </a>

        <button onclick="toggleDarkMode()">🌙/☀️</button>
    </div>
</div>

<div class="sidebar">
    <h3>📘 目录</h3>
    {toc}
</div>

<div class="content">
{content}
</div>

</body>
</html>
"""

def generate_toc(html):
    soup = BeautifulSoup(html, "html.parser")
    headers = soup.find_all(["h1", "h2", "h3"])

    toc_html = ""
    h1_index = 0
    h2_index = 0

    for h in headers:
        text = h.text
        hid = text.replace(" ", "-")
        h["id"] = hid   # 正文跳转 anchor

        if h.name == "h1":
            h1_index += 1
            h2_index = 0
            toc_html += f'''
            <div class="toc-item" onclick="toggle('h1-{h1_index}')">
                <a class="toc-link" href="#{hid}">📁 {text}</a>
            </div>
            '''

        elif h.name == "h2":
            h2_index += 1
            toc_html += f'''
            <div class="toc-item toc-h2 h1-{h1_index}" onclick="toggle('h1-{h1_index}-h2-{h2_index}')">
                <a class="toc-link" href="#{hid}">📄 {text}</a>
            </div>
            '''

        elif h.name == "h3":
            toc_html += f'''
            <div class="toc-item toc-h3 h1-{h1_index}-h2-{h2_index}">
                <a class="toc-link" href="#{hid}">- {text}</a>
            </div>
            '''

    return str(soup), toc_html


def convert_md_to_html(md_file, out_dir):
    with open(md_file, "r", encoding="utf-8") as f:
        text = f.read()

    html = markdown.markdown(text, extensions=["fenced_code", "codehilite"])
    html, toc = generate_toc(html)

    title = os.path.basename(md_file).replace(".md", "")

    full_html = PAGE_TEMPLATE.format(
        title=title,
        content=html,
        toc=toc,
        css=CSS_STYLE
    )

    out_path = os.path.join(out_dir, title + ".html")
    with open(out_path, "w", encoding="utf-8") as f:
        f.write(full_html)

    print(f"✔ {title}.html 已生成")


def main():
    out_dir = "html_out"
    os.makedirs(out_dir, exist_ok=True)

    md_files = [f for f in os.listdir(".") if f.endswith(".md")]

    for md in md_files:
        convert_md_to_html(md, out_dir)

    if md_files:
        first = md_files[0].replace(".md", ".html")
        with open(os.path.join(out_dir, "index.html"), "w", encoding="utf-8") as f:
            f.write(f'<meta http-equiv="refresh" content="0; URL={first}">')

    print("\n🎉 全部网页已生成 → html_out 文件夹\n")


if __name__ == "__main__":
    main()
