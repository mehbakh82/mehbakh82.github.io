# Mehran Bakhtiari

Source for the [personal academic portfolio](https://mehbakh82.github.io/).

Open `index.html` directly or serve the repository root with a static web server. The site uses HTML, CSS, local WebP artwork and fonts, and a small JavaScript file for project filters. There is no installation or build step.

- `index.html` holds the homepage and advisor details.
- `research/` contains the four case studies and links to the evidence in their repositories.
- `industry.html` holds the Mohaymen ICT project summaries and CV-reported evaluations.
- `projects.html` holds the project index and its checked-in snapshot. The full list is available with JavaScript disabled. Shared URLs can retain the search text and category.
- `cv.html` holds the public version of the CV. When updating it, print the page to A4 with browser headers and footers disabled and replace `assets/Mehran-Bakhtiari-CV.pdf`.

## Project sync

GitHub Actions builds and deploys the portfolio on pushes to `main` and every six hours. For an immediate refresh, open **Actions → Sync projects and deploy portfolio → Run workflow**. GitHub may disable the schedule after 60 days without activity in this repository. It can be re-enabled from the workflow page.

Every build refreshes the static project index from the account’s public repository metadata. Private, forked, archived, empty, and explicitly excluded repositories stay out of the index. Descriptions come from GitHub, with portfolio fallbacks for entries without a description. Existing titles and categories are curated in `scripts/projects.json` using repository IDs, so they carry over when a repository is renamed. New projects default to **Other projects**. A GitHub topic such as `portfolio-research` or `portfolio-machine-learning` assigns a new repository to that category.

The workflow publishes the refreshed page directly and makes no commits. Featured work on the homepage, the CV, and research case studies can be edited separately. To refresh the checked-in snapshot locally, run the following from the repository root with GitHub CLI available.

```sh
inventory=$(mktemp)
gh api --paginate --slurp 'users/mehbakh82/repos?type=owner&per_page=100&sort=full_name' > "$inventory" &&
  python3 scripts/sync_projects.py "$inventory" projects.html
rm "$inventory"
```

The website’s imagery illustrates computational methods. The published study artifacts are linked from the case studies. Font licenses are in `assets/`.
