import os
import re
import json

# This script is not perfect. It assumes that you will always link to tools in your posts using markdown links.
# It also assumes that the link text will be the name of the tool.
# It will not be able to get a description of the tool automatically.
# You will need to manually add a description to the tools.json file.


def find_md_links(text):
    """Finds all markdown links in a string of text."""
    links = re.findall(r'\[([^\]]+)\]\(([^)]+)\)', text)
    return links

def main():
    """Main function."""
    posts_dir = "content/posts"
    tools_file = "data/tools.json"

    tools = []
    if os.path.exists(tools_file):
        with open(tools_file, "r", encoding="utf-8") as f:
            tools = json.load(f)

    for filename in os.listdir(posts_dir):
        if filename.endswith(".md"):
            with open(os.path.join(posts_dir, filename), "r", encoding="utf-8") as f:
                content = f.read()
                links = find_md_links(content)
                for link in links:
                    tool_name = link[0]
                    tool_url = link[1]
                    if not any(d.get('name') == tool_name for d in tools):
                        tools.append({"name": tool_name, "url": tool_url, "description": ""})

    with open(tools_file, "w", encoding="utf-8") as f:
        json.dump(tools, f, indent=2)

if __name__ == "__main__":
    main()
