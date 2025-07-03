/**
 * Dashboard JavaScript functionality
 * Handles Chart.js initialization and interactive elements
 */

document.addEventListener('DOMContentLoaded', function() {
    // Initialize spending chart if data is available
    if (typeof chartData !== 'undefined' && chartData.labels && chartData.data) {
        initializeSpendingChart();
    }

    // Add smooth animations to category bars
    animateCategoryBars();

    // Add click handlers for interactive elements
    setupInteractiveElements();
});

function initializeSpendingChart() {
    const ctx = document.getElementById('spendingChart');
    if (!ctx) return;

    // Generate colors for each category
    const colors = generateCategoryColors(chartData.labels.length);

    // Chart configuration
    const config = {
        type: 'doughnut',
        data: {
            labels: chartData.labels,
            datasets: [{
                label: 'Spending Amount',
                data: chartData.data,
                backgroundColor: colors.background,
                borderColor: colors.border,
                borderWidth: 2,
                hoverOffset: 10
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: {
                    position: 'bottom',
                    labels: {
                        color: '#b0b0b0',
                        font: {
                            family: 'Inter',
                            size: 12
                        },
                        padding: 20,
                        usePointStyle: true,
                        pointStyle: 'circle'
                    }
                },
                tooltip: {
                    backgroundColor: 'rgba(26, 26, 26, 0.9)',
                    titleColor: '#ffffff',
                    bodyColor: '#b0b0b0',
                    borderColor: '#404040',
                    borderWidth: 1,
                    cornerRadius: 8,
                    displayColors: true,
                    callbacks: {
                        label: function(context) {
                            const label = context.label || '';
                            const value = context.parsed;
                            const total = context.dataset.data.reduce((a, b) => a + b, 0);
                            const percentage = ((value / total) * 100).toFixed(1);
                            return `${label}: $${value.toFixed(2)} (${percentage}%)`;
                        }
                    }
                }
            },
            animation: {
                animateRotate: true,
                animateScale: true,
                duration: 2000,
                easing: 'easeOutQuart'
            },
            cutout: '50%',
            radius: '90%'
        }
    };

    // Create the chart
    new Chart(ctx, config);
}

function generateCategoryColors(count) {
    // Predefined color palette matching the category colors in CSS
    const colorPalette = [
        { bg: 'rgba(251, 191, 36, 0.8)', border: '#fbbf24' },   // Food
        { bg: 'rgba(239, 68, 68, 0.8)', border: '#ef4444' },   // Rent
        { bg: 'rgba(59, 130, 246, 0.8)', border: '#3b82f6' },  // Utilities
        { bg: 'rgba(168, 85, 247, 0.8)', border: '#a855f7' },  // Shopping
        { bg: 'rgba(34, 197, 94, 0.8)', border: '#22c55e' },   // Transport
        { bg: 'rgba(236, 72, 153, 0.8)', border: '#ec4899' },  // Entertainment
        { bg: 'rgba(249, 115, 22, 0.8)', border: '#f97316' },  // Subscriptions
        { bg: 'rgba(107, 114, 128, 0.8)', border: '#6b7280' }  // Other
    ];

    const background = [];
    const border = [];

    for (let i = 0; i < count; i++) {
        const color = colorPalette[i % colorPalette.length];
        background.push(color.bg);
        border.push(color.border);
    }

    return { background, border };
}

function animateCategoryBars() {
    const categoryFills = document.querySelectorAll('.category-fill');
    
    // Use Intersection Observer to trigger animations when visible
    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.style.width = entry.target.dataset.width || entry.target.style.width;
                observer.unobserve(entry.target);
            }
        });
    }, {
        threshold: 0.1
    });

    categoryFills.forEach(fill => {
        const originalWidth = fill.style.width;
        fill.style.width = '0%';
        fill.dataset.width = originalWidth;
        observer.observe(fill);
    });
}

function setupInteractiveElements() {
    // Add click handlers for transaction rows
    const transactionRows = document.querySelectorAll('.transactions-table tbody tr');
    transactionRows.forEach(row => {
        row.addEventListener('click', function() {
            // Remove previous selections
            transactionRows.forEach(r => r.classList.remove('selected'));
            // Add selection to clicked row
            this.classList.add('selected');
        });
    });

    // Add hover effects to summary cards
    const summaryCards = document.querySelectorAll('.summary-card');
    summaryCards.forEach(card => {
        card.addEventListener('mouseenter', function() {
            this.style.transform = 'translateY(-5px) scale(1.02)';
        });
        
        card.addEventListener('mouseleave', function() {
            this.style.transform = 'translateY(-3px) scale(1)';
        });
    });

    // Add smooth scrolling for any anchor links
    const anchorLinks = document.querySelectorAll('a[href^="#"]');
    anchorLinks.forEach(link => {
        link.addEventListener('click', function(e) {
            e.preventDefault();
            const target = document.querySelector(this.getAttribute('href'));
            if (target) {
                target.scrollIntoView({
                    behavior: 'smooth',
                    block: 'start'
                });
            }
        });
    });

    // Add copy functionality to advice text
    const adviceText = document.querySelector('.advice-text');
    if (adviceText) {
        adviceText.addEventListener('click', function() {
            copyToClipboard(this.textContent);
            showToast('Advice copied to clipboard!');
        });
        
        // Add a subtle indicator that the text is clickable
        adviceText.style.cursor = 'pointer';
        adviceText.title = 'Click to copy advice to clipboard';
    }
}

function copyToClipboard(text) {
    if (navigator.clipboard && window.isSecureContext) {
        navigator.clipboard.writeText(text);
    } else {
        // Fallback for older browsers
        const textArea = document.createElement('textarea');
        textArea.value = text;
        textArea.style.position = 'fixed';
        textArea.style.left = '-999999px';
        textArea.style.top = '-999999px';
        document.body.appendChild(textArea);
        textArea.focus();
        textArea.select();
        
        try {
            document.execCommand('copy');
        } catch (err) {
            console.error('Failed to copy text: ', err);
        }
        
        document.body.removeChild(textArea);
    }
}

function showToast(message, type = 'success') {
    const toast = document.createElement('div');
    toast.className = `toast toast-${type}`;
    toast.textContent = message;
    toast.style.cssText = `
        position: fixed;
        bottom: 2rem;
        right: 2rem;
        background: ${type === 'success' ? '#4ade80' : '#ef4444'};
        color: white;
        padding: 1rem 1.5rem;
        border-radius: 8px;
        box-shadow: 0 10px 30px rgba(0, 0, 0, 0.3);
        z-index: 1002;
        transform: translateY(100px);
        opacity: 0;
        transition: all 0.3s ease;
        font-family: Inter, sans-serif;
        font-weight: 500;
    `;
    
    document.body.appendChild(toast);
    
    // Trigger animation
    setTimeout(() => {
        toast.style.transform = 'translateY(0)';
        toast.style.opacity = '1';
    }, 100);
    
    // Remove after 3 seconds
    setTimeout(() => {
        toast.style.transform = 'translateY(100px)';
        toast.style.opacity = '0';
        setTimeout(() => {
            if (toast.parentElement) {
                toast.remove();
            }
        }, 300);
    }, 3000);
}

// Add CSS for selected transaction row
const style = document.createElement('style');
style.textContent = `
    .transactions-table tbody tr.selected {
        background: rgba(54, 162, 235, 0.1) !important;
        border-left: 3px solid #36A2EB;
    }
    
    .transactions-table tbody tr {
        cursor: pointer;
        transition: all 0.2s ease;
    }
    
    .advice-text:hover {
        background: rgba(255, 255, 255, 0.02);
        border-radius: 4px;
    }
`;
document.head.appendChild(style);
