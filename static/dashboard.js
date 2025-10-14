let costChart, modelChart;

document.addEventListener('DOMContentLoaded', function() {
    loadDashboardData();
    loadModels();
    setInterval(loadDashboardData, 30000); // Refresh mỗi 30 giây
});

async function loadDashboardData() {
    try {
        const response = await fetch('/api/usage/stats');
        const data = await response.json();
        
        updateSummaryCards(data);
        updateCharts(data);
    } catch (error) {
        console.error('Error loading dashboard data:', error);
    }
}

async function loadModels() {
    try {
        const response = await fetch('/api/models');
        const models = await response.json();
        
        document.getElementById('total-models').textContent = models.length;
        updateModelsTable(models);
    } catch (error) {
        console.error('Error loading models:', error);
    }
}

function updateSummaryCards(data) {
    document.getElementById('total-cost').textContent = '$' + data.total.cost.toFixed(4);
    document.getElementById('total-tokens').textContent = data.total.tokens.toLocaleString();
    document.getElementById('total-requests').textContent = data.total.requests.toLocaleString();
}

function updateCharts(data) {
    updateCostChart(data.daily);
    updateModelChart(data.by_model);
}

function updateCostChart(dailyData) {
    const ctx = document.getElementById('costChart').getContext('2d');
    
    if (costChart) {
        costChart.destroy();
    }
    
    const labels = dailyData.map(item => {
        const date = new Date(item.date);
        return date.toLocaleDateString('vi-VN');
    });
    
    const costs = dailyData.map(item => item.cost);
    
    costChart = new Chart(ctx, {
        type: 'line',
        data: {
            labels: labels,
            datasets: [{
                label: 'Chi phí ($)',
                data: costs,
                borderColor: '#667eea',
                backgroundColor: 'rgba(102, 126, 234, 0.1)',
                borderWidth: 2,
                fill: true,
                tension: 0.4
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: {
                    display: false
                }
            },
            scales: {
                y: {
                    beginAtZero: true,
                    ticks: {
                        callback: function(value) {
                            return '$' + value.toFixed(4);
                        }
                    }
                }
            }
        }
    });
}

function updateModelChart(modelData) {
    const ctx = document.getElementById('modelChart').getContext('2d');
    
    if (modelChart) {
        modelChart.destroy();
    }
    
    const labels = modelData.map(item => item.name);
    const costs = modelData.map(item => item.cost);
    const backgroundColors = [
        '#FF6384', '#36A2EB', '#FFCE56', '#4BC0C0', 
        '#9966FF', '#FF9F40', '#FF6384', '#C9CBCF'
    ];
    
    modelChart = new Chart(ctx, {
        type: 'doughnut',
        data: {
            labels: labels,
            datasets: [{
                data: costs,
                backgroundColor: backgroundColors,
                borderWidth: 2
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: {
                    position: 'bottom'
                }
            }
        }
    });
}

function updateModelsTable(models) {
    const tbody = document.getElementById('models-table');
    tbody.innerHTML = '';
    
    models.forEach(model => {
        const row = document.createElement('tr');
        row.innerHTML = `
            <td>${model.name}</td>
            <td>$${model.cost_per_token.toFixed(6)}</td>
            <td>${model.description || '-'}</td>
            <td>
                <span class="badge ${model.is_active ? 'bg-success' : 'bg-secondary'}">
                    ${model.is_active ? 'Active' : 'Inactive'}
                </span>
            </td>
            <td>${new Date(model.created_at).toLocaleDateString('vi-VN')}</td>
        `;
        tbody.appendChild(row);
    });
}

async function addModel() {
    const form = document.getElementById('addModelForm');
    const formData = new FormData(form);
    
    const modelData = {
        name: formData.get('name'),
        cost_per_token: parseFloat(formData.get('cost_per_token')),
        description: formData.get('description')
    };
    
    try {
        const response = await fetch('/api/models', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(modelData)
        });
        
        const result = await response.json();
        
        if (result.success) {
            // Đóng modal và reset form
            const modal = bootstrap.Modal.getInstance(document.getElementById('addModelModal'));
            modal.hide();
            form.reset();
            
            // Reload data
            loadModels();
            loadDashboardData();
            
            alert('Model đã được thêm thành công!');
        } else {
            alert('Lỗi: ' + result.error);
        }
    } catch (error) {
        console.error('Error adding model:', error);
        alert('Lỗi khi thêm model');
    }
}