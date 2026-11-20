const controls = document.querySelector('.filter-form');
const search = document.querySelector('#search');
const category = document.querySelector('#category');
const count = document.querySelector('#count');
const empty = document.querySelector('#empty');
const entries = Array.from(document.querySelectorAll('.archive-row'), row => ({
  row,
  text: (row.textContent + ' ' + row.dataset.repo).trim().toLocaleLowerCase(),
  category: row.dataset.category,
}));

function filterProjects() {
  const terms = search.value.trim().toLocaleLowerCase().split(/\s+/).filter(Boolean);
  let visible = 0;
  for (const entry of entries) {
    const matchesCategory = !category.value || entry.category === category.value;
    const matchesText = terms.every(term => entry.text.includes(term));
    entry.row.hidden = !(matchesCategory && matchesText);
    if (!entry.row.hidden) visible += 1;
  }
  count.textContent = `${visible} of ${entries.length} repositories`;
  empty.hidden = visible !== 0;
}

controls.hidden = false;
controls.addEventListener('submit', event => event.preventDefault());
search.addEventListener('input', filterProjects);
category.addEventListener('change', filterProjects);
filterProjects();
