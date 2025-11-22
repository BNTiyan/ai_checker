// API Configuration
const API_BASE_URL = window.location.hostname === 'localhost' 
    ? 'http://localhost:5000' 
    : '/.netlify/functions';

// State
let currentReport = null;

// Initialize
document.addEventListener('DOMContentLoaded', () => {
    setupTabSwitching();
    setupFileUpload();
    setupTextAnalysis();
    setupDragAndDrop();
});

// Tab Switching
function setupTabSwitching() {
    const tabButtons = document.querySelectorAll('.tab-btn');
    const tabContents = document.querySelectorAll('.tab-content');

    tabButtons.forEach(btn => {
        btn.addEventListener('click', () => {
            const tabName = btn.getAttribute('data-tab');
            
            // Update active states
            tabButtons.forEach(b => b.classList.remove('active'));
            tabContents.forEach(c => c.classList.remove('active'));
            
            btn.classList.add('active');
            document.getElementById(`${tabName}Tab`).classList.add('active');
        });
    });
}

// File Upload
function setupFileUpload() {
    const fileInput = document.getElementById('fileInput');
    const uploadArea = document.getElementById('uploadArea');

    fileInput.addEventListener('change', (e) => {
        const file = e.target.files[0];
        if (file) {
            handleFileUpload(file);
        }
    });

    uploadArea.addEventListener('click', () => {
        fileInput.click();
    });
}

// Drag and Drop
function setupDragAndDrop() {
    const uploadArea = document.getElementById('uploadArea');

    ['dragenter', 'dragover', 'dragleave', 'drop'].forEach(eventName => {
        uploadArea.addEventListener(eventName, preventDefaults, false);
    });

    function preventDefaults(e) {
        e.preventDefault();
        e.stopPropagation();
    }

    ['dragenter', 'dragover'].forEach(eventName => {
        uploadArea.addEventListener(eventName, () => {
            uploadArea.classList.add('drag-over');
        });
    });

    ['dragleave', 'drop'].forEach(eventName => {
        uploadArea.addEventListener(eventName, () => {
            uploadArea.classList.remove('drag-over');
        });
    });

    uploadArea.addEventListener('drop', (e) => {
        const files = e.dataTransfer.files;
        if (files.length > 0) {
            handleFileUpload(files[0]);
        }
    });
}

// Text Analysis
function setupTextAnalysis() {
    const analyzeBtn = document.getElementById('analyzeTextBtn');
    const textInput = document.getElementById('textInput');

    analyzeBtn.addEventListener('click', () => {
        const text = textInput.value.trim();
        
        if (!text) {
            showError('Please enter some text to analyze');
            return;
        }

        if (text.split(' ').length < 50) {
            showError('Text must be at least 50 words');
            return;
        }

        handleTextAnalysis(text);
    });
}

// Handle File Upload
async function handleFileUpload(file) {
    if (!file.name.endsWith('.pdf')) {
        showError('Please upload a PDF file');
        return;
    }

    if (file.size > 10 * 1024 * 1024) {
        showError('File size must be less than 10MB');
        return;
    }

    showLoading();

    const formData = new FormData();
    formData.append('file', file);

    try {
        const response = await fetch(`${API_BASE_URL}/api/analyze`, {
            method: 'POST',
            body: formData
        });

        if (!response.ok) {
            const error = await response.json();
            throw new Error(error.error || 'Analysis failed');
        }

        const report = await response.json();
        currentReport = report;
        displayReport(report);
    } catch (error) {
        hideLoading();
        showError(error.message);
    }
}

// Handle Text Analysis
async function handleTextAnalysis(text) {
    showLoading();

    try {
        const response = await fetch(`${API_BASE_URL}/api/analyze-text`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ text })
        });

        if (!response.ok) {
            const error = await response.json();
            throw new Error(error.error || 'Analysis failed');
        }

        const report = await response.json();
        currentReport = report;
        displayReport(report);
    } catch (error) {
        hideLoading();
        showError(error.message);
    }
}

// Show Loading
function showLoading() {
    document.getElementById('uploadSection').classList.add('hidden');
    document.getElementById('resultsSection').classList.add('hidden');
    document.getElementById('loadingSection').classList.remove('hidden');

    // Simulate loading steps
    setTimeout(() => {
        document.getElementById('step1').classList.add('completed');
        document.getElementById('step2').classList.add('active');
    }, 500);

    setTimeout(() => {
        document.getElementById('step2').classList.add('completed');
        document.getElementById('step2').classList.remove('active');
        document.getElementById('step3').classList.add('active');
    }, 1500);

    setTimeout(() => {
        document.getElementById('step3').classList.add('completed');
        document.getElementById('step3').classList.remove('active');
        document.getElementById('step4').classList.add('active');
    }, 2500);
}

// Hide Loading
function hideLoading() {
    document.getElementById('loadingSection').classList.add('hidden');
    document.getElementById('uploadSection').classList.remove('hidden');
}

// Display Report
function displayReport(report) {
    document.getElementById('loadingSection').classList.add('hidden');
    document.getElementById('resultsSection').classList.remove('hidden');

    // Overall Verdict
    const verdict = report.overall_verdict;
    const riskBadge = document.getElementById('riskBadge');
    const verdictContent = document.getElementById('verdictContent');

    riskBadge.textContent = verdict.risk_level.toUpperCase() + ' RISK';
    riskBadge.className = 'risk-badge ' + verdict.risk_level;

    let verdictText = '';
    if (verdict.ai_generated && verdict.plagiarized) {
        verdictText = '⚠️ This document shows signs of both AI generation and plagiarism.';
    } else if (verdict.ai_generated) {
        verdictText = '🤖 This document appears to be AI-generated.';
    } else if (verdict.plagiarized) {
        verdictText = '📋 This document contains plagiarized content.';
    } else {
        verdictText = '✅ This document appears to be original human-written content.';
    }
    verdictContent.textContent = verdictText;

    // AI Detection Score
    const aiScore = report.ai_detection.probability;
    document.getElementById('aiScore').textContent = Math.round(aiScore);
    updateCircularProgress('aiCircle', aiScore);
    
    const aiVerdict = document.getElementById('aiVerdict');
    aiVerdict.textContent = report.ai_detection.verdict;
    aiVerdict.className = 'score-verdict ' + (aiScore > 60 ? 'high' : aiScore > 40 ? 'medium' : 'low');

    // AI Details
    const aiDetails = document.getElementById('aiDetails');
    const metrics = report.ai_detection.metrics;
    aiDetails.innerHTML = `
        <p><strong>Confidence:</strong> ${report.ai_detection.confidence}</p>
        ${metrics ? `
            <p><strong>Readability:</strong> ${metrics.flesch_reading_ease}</p>
            <p><strong>Grade Level:</strong> ${metrics.flesch_kincaid_grade}</p>
        ` : ''}
    `;

    // Plagiarism Score
    const plagScore = report.plagiarism.score;
    document.getElementById('plagScore').textContent = Math.round(plagScore);
    updateCircularProgress('plagCircle', plagScore);
    
    const plagVerdict = document.getElementById('plagVerdict');
    plagVerdict.textContent = plagScore > 30 ? 'Plagiarism Detected' : 'No Significant Matches';
    plagVerdict.className = 'score-verdict ' + (plagScore > 50 ? 'high' : plagScore > 30 ? 'medium' : 'low');

    // Plagiarism Sources
    const sources = report.plagiarism.sources || [];
    if (sources.length > 0) {
        document.getElementById('sourcesSection').classList.remove('hidden');
        const sourcesList = document.getElementById('sourcesList');
        sourcesList.innerHTML = sources.map(source => `
            <div class="source-item">
                <h4>${source.title}</h4>
                <a href="${source.url}" target="_blank">${source.url}</a>
                <p>"${source.snippet}"</p>
            </div>
        `).join('');
    }

    // Detailed Metrics
    if (metrics) {
        const metricsGrid = document.getElementById('metricsGrid');
        metricsGrid.innerHTML = `
            <div class="metric-item">
                <h4>Reading Ease</h4>
                <p>${metrics.flesch_reading_ease}</p>
            </div>
            <div class="metric-item">
                <h4>Grade Level</h4>
                <p>${metrics.flesch_kincaid_grade}</p>
            </div>
            <div class="metric-item">
                <h4>Avg Sentence Length</h4>
                <p>${metrics.avg_sentence_length} words</p>
            </div>
            <div class="metric-item">
                <h4>Sentence Variance</h4>
                <p>${metrics.sentence_length_variance}</p>
            </div>
            <div class="metric-item">
                <h4>Unique Word Ratio</h4>
                <p>${(metrics.unique_word_ratio * 100).toFixed(1)}%</p>
            </div>
        `;
    }

    // Document Stats
    const stats = report.text_stats;
    const statsGrid = document.getElementById('statsGrid');
    statsGrid.innerHTML = `
        <div class="stat-item">
            <h4>Total Words</h4>
            <p>${stats.total_words.toLocaleString()}</p>
        </div>
        <div class="stat-item">
            <h4>Total Characters</h4>
            <p>${stats.total_characters.toLocaleString()}</p>
        </div>
        <div class="stat-item">
            <h4>Total Sentences</h4>
            <p>${stats.total_sentences.toLocaleString()}</p>
        </div>
        <div class="stat-item">
            <h4>Analysis Date</h4>
            <p>${new Date(report.analyzed_at).toLocaleDateString()}</p>
        </div>
    `;

    // Setup action buttons
    document.getElementById('exportJsonBtn').onclick = () => exportReport('json');
    document.getElementById('newAnalysisBtn').onclick = () => {
        document.getElementById('resultsSection').classList.add('hidden');
        document.getElementById('uploadSection').classList.remove('hidden');
        document.getElementById('fileInput').value = '';
        document.getElementById('textInput').value = '';
    };
}

// Update Circular Progress
function updateCircularProgress(circleId, percentage) {
    const circle = document.getElementById(circleId);
    const circumference = 2 * Math.PI * 45;
    const offset = circumference - (percentage / 100) * circumference;
    
    circle.style.strokeDashoffset = offset;
    
    // Color based on percentage
    if (percentage > 60) {
        circle.style.stroke = '#ef4444'; // danger
    } else if (percentage > 40) {
        circle.style.stroke = '#f59e0b'; // warning
    } else {
        circle.style.stroke = '#10b981'; // success
    }
}

// Export Report
function exportReport(format) {
    if (!currentReport) return;

    if (format === 'json') {
        const dataStr = JSON.stringify(currentReport, null, 2);
        const blob = new Blob([dataStr], { type: 'application/json' });
        const url = URL.createObjectURL(blob);
        const link = document.createElement('a');
        link.href = url;
        link.download = `analysis_report_${Date.now()}.json`;
        link.click();
        URL.revokeObjectURL(url);
    }
}

// Show Error
function showError(message) {
    alert('Error: ' + message);
}

