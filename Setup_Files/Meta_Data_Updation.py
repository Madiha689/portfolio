"""
***********************************************************************************************
* File Name   : Meta_Data_Updation.py
* Author      : Madhurima Rawat
* Date        : July 12, 2025
* Description : A utility to update `index.html` in the parent directory by:
*               1. Replacing the permalink with an empty front matter.
*               2. Updating meta tags based on user input or JSON data.
*               3. Modifying title, Open Graph tags, and social preview.
*               4. Optionally auto-generates og:url using GitHub username.
*               5. Dynamically cleans image paths under site-previews by removing intermediate
                   folders.
***********************************************************************************************
"""

import os
import json
import re
from pyfiglet import figlet_format
from colorama import Fore, Style, init

# ✅ Initialize colorama
init(autoreset=True)

# ✅ Paths
INDEX_PATH = os.path.abspath(os.path.join("..", "index.html"))
USER_JSON = r"..\assets\user_data\user.json"
SOCIAL_JSON = r"..\assets\user_data\social_links.json"


# ✅ Print styled banner
def print_banner(text):
    print(Fore.YELLOW + figlet_format(text, font="slant"))


# ✅ Read index.html
def read_index_html():
    with open(INDEX_PATH, "r", encoding="utf-8") as f:
        return f.read()


# ✅ Write updated index.html
def write_index_html(content):
    with open(INDEX_PATH, "w", encoding="utf-8") as f:
        f.write(content)


# ✅ Replace permalink block
def update_permalink(content):
    return content.replace(
        "---\npermalink: /Minimalist_Professional_Golden_Fern\n---", "---\n---"
    )


# ✅ Ask user to enter or auto-generate og:url
def get_og_url(default_username):
    print(Fore.CYAN + "Enter og:url or leave blank to auto-generate:")
    custom_url = input("og:url: ").strip()
    if custom_url:
        return custom_url
    return f"https://{default_username}.github.io/Portfolio-Templates"


# ✅ Collect metadata
def get_metadata():
    print(Fore.CYAN + "Choose metadata source:")
    print("1. From JSON")
    print("2. Enter manually")
    choice = input("Enter 1 or 2: ").strip()

    if choice == "1":
        with open(USER_JSON, "r", encoding="utf-8") as f:
            data = json.load(f)
        with open(SOCIAL_JSON, "r", encoding="utf-8") as f:
            social = json.load(f)

        github_url = social.get("github", "https://github.com/janedoe")
        github_username = github_url.strip().split("/")[-1]
        name = data.get("name", "Madhurima Rawat")
        title = f"Professional Portfolio by {name}"
        description = (
            f"Professional portfolio template by {name} showcasing projects, "
            "skills, social links, education, and more."
        )
        keywords = (
            f"portfolio, minimalist, web developer, projects, skills, education, {name}"
        )
        og_url = get_og_url(github_username)

        return {
            "author": name,
            "title": title,
            "description": description,
            "keywords": keywords,
            "og_url": og_url,
        }

    else:
        # ✅ Manual entry
        name = input("Author name: ").strip()
        title = input("Portfolio title: ").strip()
        description = input("Meta description: ").strip()
        keywords = input("Meta keywords (comma separated): ").strip()
        og_url = input("og:url (leave blank to skip): ").strip()
        return {
            "author": name,
            "title": title,
            "description": description,
            "keywords": keywords,
            "og_url": og_url if og_url else "",
        }


# ✅ Update meta tags
def update_meta_tags(content, metadata):
    def replace_meta_tag(tag, value):
        return f'<meta name="{tag}" content="{value}" />'

    def replace_og_tag(tag, value):
        return f'<meta property="og:{tag}" content="{value}" />'

    def replace_twitter_tag(tag, value):
        return f'<meta name="twitter:{tag}" content="{value}" />'

    # ✅ Core meta
    content = re.sub(
        r'<meta name="description".*?>',
        replace_meta_tag("description", metadata["description"]),
        content,
    )
    content = re.sub(
        r'<meta name="keywords".*?>',
        replace_meta_tag("keywords", metadata["keywords"]),
        content,
    )
    content = re.sub(
        r'<meta name="author".*?>',
        replace_meta_tag("author", metadata["author"]),
        content,
    )

    # ✅ Open Graph tags
    content = re.sub(
        r'<meta property="og:title".*?>',
        replace_og_tag("title", metadata["title"]),
        content,
    )
    content = re.sub(
        r'<meta property="og:description".*?>',
        replace_og_tag("description", metadata["description"]),
        content,
    )
    if metadata["og_url"]:
        content = re.sub(
            r'<meta property="og:url".*?>',
            replace_og_tag("url", metadata["og_url"]),
            content,
        )

    # ✅ Twitter tags
    content = re.sub(
        r'<meta name="twitter:title".*?>',
        replace_twitter_tag("title", metadata["title"]),
        content,
    )
    content = re.sub(
        r'<meta name="twitter:description".*?>',
        replace_twitter_tag("description", metadata["description"]),
        content,
    )

    # ✅ HTML <title>
    content = re.sub(
        r"<title>.*?</title>", f'<title>{metadata["title"]}</title>', content
    )

    # ✅ Dynamically fix content lines containing site-previews
    cleaned_lines = []
    for line in content.splitlines():
        if (
            'content="{{ site.url }}{{ site.baseurl }}' in line
            and "site-previews" in line
        ):
            start = line.find("{{ site.url }}{{ site.baseurl }}")
            end = line.find("site-previews")
            if start != -1 and end != -1:
                before = line[:start]
                after = line[end:]
                line = before + "{{ site.url }}{{ site.baseurl }}/" + after
                print("✅ Fixed line:", line.strip())
        cleaned_lines.append(line)

    content = "\n".join(cleaned_lines)

    return content


# ✅ Extract <title> from HTML
def extract_title_from_html(html):
    match = re.search(r"<title>(.*?)</title>", html)
    return match.group(1) if match else "Portfolio"


# ✅ Main
if __name__ == "__main__":
    try:
        html = read_index_html()
        current_title = extract_title_from_html(html)
        print_banner(f"{current_title} Editor 🌿")

        html = update_permalink(html)
        meta = get_metadata()
        html = update_meta_tags(html, meta)
        write_index_html(html)

        print(
            Fore.GREEN
            + "\n✅ index.html updated successfully with new metadata and permalink."
        )
    except Exception as e:
        print(Fore.RED + f"\n❌ Error: {e}")
