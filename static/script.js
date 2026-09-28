let allComplaints = [];

// Google Form Links Mapping
const formLinks = {
    'Hostel': { url: 'https://docs.google.com/forms/u/0/', label: 'Hostel & Mess Google Form' },
    'Academics': { url: 'https://docs.google.com/forms/u/0/', label: 'Academic Grievance Form' },
    'Infrastructure': { url: 'https://docs.google.com/forms/u/0/', label: 'Campus Infrastructure Form' },
    'Other': { url: 'https://forms.google.com', label: 'General Google Form' }
};

function handleCategoryChange() {
    const cat = document.getElementById('category').value;
    const btn = document.getElementById('gformBtn');
    const desc = document.getElementById('gformDesc');
    
    const info = formLinks[cat] || formLinks['Other'];
    btn.href = info.url;
    desc.innerText = `Prefer filing via official ${info.label}?`;
}

async function loadComplaints() {
    try {
        const res = await fetch('/get_complaints');
        allComplaints = await res.json();
        updateStats(allComplaints);
        renderFeed(allComplaints);
    } catch (err) {
        console.error("Error loading complaints:", err);
    }
}

function updateStats(data) {
    document.getElementById('totalCount').innerText = data.length;
    const pending = data.filter(c => (c.status || 'Pending') === 'Pending' || c.status === 'In Progress').length;
    const resolved = data.filter(c => c.status === 'Resolved').length;
    
    document.getElementById('pendingCount').innerText = pending;
    document.getElementById('resolvedCount').innerText = resolved;
}

function renderFeed(data) {
    const list = document.getElementById('complaintsList');
    list.innerHTML = '';

    if (data.length === 0) {
        list.innerHTML = '<div class="empty-feed">📭 No grievances reported yet.</div>';
        return;
    }

    // Display newest first
    [...data].reverse().forEach(item => {
        const status = item.status || 'Pending';
        const statusClass = status.toLowerCase().replace(' ', '-');
        const imgHtml = item.image ? `<div class="img-wrapper"><img src="/static/uploads/${item.image}" alt="Attachment" onclick="window.open(this.src)"></div>` : '';

        const div = document.createElement('div');
        div.className = 'feed-item';
        div.innerHTML = `
            <div class="item-top">
                <h4 class="item-title">${item.title}</h4>
                <span class="cat-pill">${item.category}</span>
            </div>
            <p class="item-desc">${item.description}</p>
            ${imgHtml}
            <div class="item-bottom">
                <span class="status-badge ${statusClass}">● ${status}</span>
                <div class="admin-actions">
                    <select onchange="changeStatus(${item.id}, this.value)" class="status-select">
                        <option value="" disabled selected>Update Status</option>
                        <option value="Pending">Set Pending</option>
                        <option value="In Progress">Set In Progress</option>
                        <option value="Resolved">Set Resolved</option>
                    </select>
                </div>
            </div>
        `;
        list.appendChild(div);
    });
}

function filterFeed() {
    const query = document.getElementById('searchInput').value.toLowerCase();
    const filtered = allComplaints.filter(c => 
        c.title.toLowerCase().includes(query) || 
        c.description.toLowerCase().includes(query) ||
        c.category.toLowerCase().includes(query)
    );
    renderFeed(filtered);
}

async function changeStatus(index, newStatus) {
    const formData = new FormData();
    formData.append('index', index);
    formData.append('status', newStatus);

    const res = await fetch('/update_status', { method: 'POST', body: formData });
    const result = await res.json();
    if (result.status === 'success') {
        loadComplaints();
    } else {
        alert('Failed to update status');
    }
}

document.getElementById('grievanceForm').addEventListener('submit', async (e) => {
    e.preventDefault();
    const formData = new FormData(e.target);

    const res = await fetch('/submit', { method: 'POST', body: formData });
    const result = await res.json();

    if (result.status === 'success') {
        alert('Grievance Submitted Successfully!');
        document.getElementById('grievanceForm').reset();
        handleCategoryChange();
        loadComplaints();
    } else {
        alert('Error: ' + result.message);
    }
});

// Initial Load
document.addEventListener('DOMContentLoaded', () => {
    handleCategoryChange();
    loadComplaints();