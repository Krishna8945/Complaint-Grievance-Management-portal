document.getElementById('complaintForm').addEventListener('submit', async function(e) {
    e.preventDefault();

    const formData = new FormData(this);

    const response = await fetch('/submit', {
        method: 'POST',
        body: formData
    });

    const result = await response.json();
    alert(result.message);

    if (result.status === 'success') {
        this.reset();
        loadComplaints();
    }
});

async function loadComplaints() {
    const response = await fetch('/get_complaints');
    const complaints = await response.json();

    const listDiv = document.getElementById('complaintList');
    listDiv.innerHTML = '';

    complaints.forEach(item => {
        const card = document.createElement('div');
        card.className = 'complaint-card';
        card.innerHTML = `
            <div class="complaint-header">
                <span class="complaint-title">${item.title}</span>
                <span class="category-badge">${item.category}</span>
            </div>
            <p class="complaint-desc">${item.description}</p>
        `;
        listDiv.appendChild(card);
    });
}

loadComplaints();