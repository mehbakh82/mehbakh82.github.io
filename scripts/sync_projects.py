"""Render the static project index from paginated GitHub repository metadata."""
import argparse
import json
import re
from html import escape
from pathlib import Path
from urllib.parse import quote

CONFIG = Path(__file__).with_name("projects.json")


def replace_section(page, name, value):
    pattern = rf"(<!-- {name}:start -->).*?(<!-- {name}:end -->)"
    page, count = re.subn(pattern, lambda match: match[1] + value + match[2],
                         page, flags=re.DOTALL)
    if count != 1:
        raise ValueError(f"Expected one marked {name} section, found {count}")
    return page


def render(page, inventory, config):
    owner = config["owner"]
    categories = config["categories"]
    excluded = {name.casefold() for name in config["excluded_repositories"]}
    category_topics = {
        "portfolio-" + category.lower().replace(" ", "-"): category
        for category in categories
    }
    seen = set()
    projects = []

    if not isinstance(inventory, list) or not inventory:
        raise ValueError("Missing GitHub API inventory pages")
    for batch in inventory:
        if not isinstance(batch, list):
            raise ValueError("Expected an array of repositories on every GitHub API page")
        for repo in batch:
            if repo["owner"]["login"].casefold() != owner.casefold():
                raise ValueError("GitHub returned a repository from an unexpected owner")
            name = repo["name"]
            if (repo["private"] or repo["fork"] or repo["archived"] or not repo["size"]
                    or name.casefold() in excluded):
                continue
            if repo["id"] in seen:
                raise ValueError("Duplicate repository in paginated GitHub response")
            seen.add(repo["id"])

            override = config["overrides"].get(str(repo["id"]), {})
            topics = set(repo.get("topics", []))
            category = override.get("category") or next(
                (category for topic, category in category_topics.items() if topic in topics),
                "Other projects",
            )
            title = override.get("title") or name.replace("-", " ").replace("_", " ")
            description = (repo["description"] or "").strip() or override.get(
                "description", "View the repository on GitHub for details."
            )
            url = f"https://github.com/{quote(owner, safe='')}/{quote(name, safe='')}"
            projects.append((categories.index(category), title, name, description, url))

    if not projects:
        raise ValueError("No projects returned. Refusing to replace the project index.")
    projects.sort(key=lambda item: (item[0], item[1].casefold(), item[2].casefold()))

    used_categories = {item[0] for item in projects}
    options = "".join(f"<option>{escape(category)}</option>"
                      for i, category in enumerate(categories) if i in used_categories)
    rows = []
    for group, title, name, description, url in projects:
        category = escape(categories[group])
        rows.append(
            f'    <article class="archive-row" data-category="{category}" data-repo="{escape(name)}">\n'
            f'      <div><h2><a href="{escape(url)}">{escape(title)}</a></h2>'
            f'<p class="meta">{category}</p></div>\n'
            f'      <p>{escape(description)}</p>\n'
            f'    </article>'
        )
    page = replace_section(page, "project-categories", options)
    page = replace_section(page, "project-count", f"{len(projects)} repositories")
    page = replace_section(page, "project-rows", "\n" + "\n".join(rows) + "\n  ")
    return page, len(projects)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("inventory", type=Path, help="JSON from gh api --paginate --slurp")
    parser.add_argument("page", type=Path, help="projects.html to refresh")
    args = parser.parse_args()
    page, count = render(args.page.read_text(encoding="utf-8"),
                         json.loads(args.inventory.read_text(encoding="utf-8")),
                         json.loads(CONFIG.read_text(encoding="utf-8")))
    args.page.write_text(page, encoding="utf-8")
    print(f"Rendered {count} public projects.")


if __name__ == "__main__":
    main()
