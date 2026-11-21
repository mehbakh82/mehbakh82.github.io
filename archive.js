const controls = document.querySelector('.filter-form');
const search = document.querySelector('#search');
const category = document.querySelector('#category');
const count = document.querySelector('#count');
const empty = document.querySelector('#empty');
const reset = controls.querySelector('.filter-reset');
const entries = Array.from(document.querySelectorAll('.archive-row'), row => ({
  row,
  text: (row.textContent + ' ' + row.dataset.repo).trim().toLocaleLowerCase(),
  category: row.dataset.category,
}));

function filterProjects({ updateURL = true } = {}) {
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
  reset.disabled = !search.value && !category.value;

  if (updateURL && location.protocol !== 'file:') {
    const url = new URL(location.href);
    url.searchParams.delete('q');
    url.searchParams.delete('category');
    if (search.value.trim()) url.searchParams.set('q', search.value.trim());
    if (category.value) url.searchParams.set('category', category.value);
    if (url.href !== location.href) history.replaceState(null, '', url);
  }
}

function restoreFilters() {
  const params = new URL(location.href).searchParams;
  search.value = params.get('q') || '';
  const requestedCategory = params.get('category') || '';
  category.value = requestedCategory === 'Bioinformatics coursework' ? 'Bioinformatics' : requestedCategory;
  if (category.selectedIndex === -1) category.selectedIndex = 0;
  filterProjects({ updateURL: false });
}

controls.hidden = false;
controls.addEventListener('submit', event => event.preventDefault());
search.addEventListener('input', () => filterProjects());
category.addEventListener('change', () => filterProjects());
controls.addEventListener('reset', () => {
  requestAnimationFrame(() => {
    search.focus();
    filterProjects();
  });
});
window.addEventListener('popstate', restoreFilters);
restoreFilters();
