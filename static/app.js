const pageSize = 25;
let currentPage = 0;
let currentSource = '';
let currentQuery = '';
let currentStart = '';
let currentEnd = '';
let autoRefreshMs = 30000;
let autoRefreshTimer = null;

async function fetchStats(){
  const r = await fetch('/api/stats');
  const data = await r.json();
  document.getElementById('totalIOCs').innerText = data.total;
  const sc = document.getElementById('sourceCounts');
  sc.innerHTML = data.per_source.map(s => `${s.source}: ${s.count}`).join('<br>');

  const sel = document.getElementById('sourceFilter');
  const existing = Array.from(sel.options).map(o => o.value);
  data.per_source.forEach(s => {
    if(!existing.includes(s.source)){
      const opt = document.createElement('option');
      opt.value = s.source;
      opt.text = s.source;
      sel.appendChild(opt);
    }
  });
}

async function fetchResults(){
  const offset = currentPage * pageSize;
  const params = new URLSearchParams({ limit: pageSize, offset, source: currentSource, q: currentQuery, start: currentStart, end: currentEnd });
  const r = await fetch('/api/search?' + params.toString());
  const rows = await r.json();
  const body = document.getElementById('resultsBody');
  body.innerHTML = '';
  if(rows.length === 0){
    body.innerHTML = '<tr><td colspan="4">No results</td></tr>';
  } else {
    rows.forEach((row, i) => {
      const tr = document.createElement('tr');
      tr.innerHTML = `<td>${offset + i + 1}</td><td><code>${escapeHtml(row.url)}</code></td><td>${row.source}</td><td>${row.date_added}</td>`;
      body.appendChild(tr);
    });
  }
  renderPagination(rows.length);
  document.getElementById('lastRef').innerText = new Date().toLocaleTimeString();
}

function renderPagination(count){
  const pag = document.getElementById('pagination');
  pag.innerHTML = '';
  const prev = document.createElement('li');
  prev.className = 'page-item';
  prev.innerHTML = `<a class='page-link' href='#'>Prev</a>`;
  prev.onclick = (e)=>{ e.preventDefault(); if(currentPage>0){ currentPage--; fetchResults(); } };
  pag.appendChild(prev);

  const next = document.createElement('li');
  next.className = 'page-item';
  next.innerHTML = `<a class='page-link' href='#'>Next</a>`;
  next.onclick = (e)=>{ e.preventDefault(); currentPage++; fetchResults(); };
  pag.appendChild(next);
}

function escapeHtml(text){
  const map = { '&': '&amp;', '<': '&lt;', '>': '&gt;', '\"': '&quot;', "'": '&#039;' };
  return text.replace(/[&<>\"']/g, function(m){ return map[m]; });
}

function scheduleAutoRefresh(){
  if(autoRefreshTimer) clearInterval(autoRefreshTimer);
  autoRefreshTimer = setInterval(()=>{ fetchStats(); fetchResults(); }, autoRefreshMs);
}

document.getElementById('searchBtn').onclick = ()=>{
  currentQuery = document.getElementById('searchInput').value.trim();
  currentSource = document.getElementById('sourceFilter').value;
  currentStart = document.getElementById('startDate').value;
  currentEnd = document.getElementById('endDate').value;
  currentPage = 0;
  fetchResults();
};

document.getElementById('refreshBtn').onclick = ()=>{ fetchStats(); fetchResults(); };

(async function(){
  await fetchStats();
  await fetchResults();
  scheduleAutoRefresh();
})();

// Theme toggle
document.getElementById("themeToggle")?.addEventListener("click", () => {
  const body = document.getElementById("body");
  body.classList.toggle("bg-dark");
  body.classList.toggle("text-white");
  localStorage.setItem("theme", body.classList.contains("bg-dark") ? "dark" : "light");
});

// Restore theme
window.addEventListener("load", () => {
  const theme = localStorage.getItem("theme");
  const body = document.getElementById("body");
  if (theme === "dark") body.classList.add("bg-dark", "text-white");
});

// Chart example (dummy counts)
if (document.getElementById("iocChart")) {
  const ctx = document.getElementById("iocChart");
  new Chart(ctx, {
    type: "bar",
    data: {
      labels: ["URLHaus", "PhishTank", "MalwareBazaar"],
      datasets: [{ label: "IOC Count", data: [120, 80, 45], borderWidth: 1 }]
    },
    options: { scales: { y: { beginAtZero: true } } }
  });
}
