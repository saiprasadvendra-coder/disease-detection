// Disease Detection Application JavaScript
// Enhanced with text input, tab navigation, and interactive features

document.addEventListener('DOMContentLoaded', function() {
    // ============ Tab Navigation ============
    setupTabs();
    
    // ============ Checkbox-based Input ============
    setupCheckboxMode();
    
    // ============ Text-based Input ============
    setupTextMode();
});

// ============================================
// TAB NAVIGATION
// ============================================
function setupTabs() {
    const tabBtns = document.querySelectorAll('.tab-btn');
    const tabContents = document.querySelectorAll('.tab-content');
    
    tabBtns.forEach(btn => {
        btn.addEventListener('click', function() {
            const tabName = this.getAttribute('data-tab');
            
            // Remove active class from all buttons and contents
            tabBtns.forEach(b => b.classList.remove('active'));
            tabContents.forEach(tc => tc.classList.remove('active'));
            
            // Add active class to clicked button and corresponding content
            this.classList.add('active');
            const tabContent = document.getElementById(tabName + '-tab');
            if (tabContent) {
                tabContent.classList.add('active');
            }
        });
    });
}

// ============================================
// CHECKBOX MODE
// ============================================
function setupCheckboxMode() {
    const searchInput = document.getElementById('symptom-search');
    const symptomGrid = document.getElementById('symptom-grid');
    const form = document.querySelector('.symptom-form');
    
    if (searchInput && symptomGrid) {
        // Real-time symptom search/filter
        searchInput.addEventListener('input', function(e) {
            const searchTerm = e.target.value.toLowerCase();
            const symptomChips = symptomGrid.querySelectorAll('.symptom-chip');
            let visibleCount = 0;
            
            symptomChips.forEach(chip => {
                const label = chip.getAttribute('data-label');
                if (!searchTerm || label.includes(searchTerm)) {
                    chip.style.display = '';
                    visibleCount++;
                } else {
                    chip.style.display = 'none';
                }
            });
        });
        
        // Update symptom counter
        if (symptomGrid) {
            symptomGrid.addEventListener('change', function() {
                const checked = document.querySelectorAll('#symptom-grid input[type="checkbox"]:checked').length;
                const counter = document.getElementById('selected-count');
                if (counter) {
                    counter.textContent = checked;
                }
            });
        }
    }
    
    // Form validation
    if (form) {
        form.addEventListener('submit', function(e) {
            const checkboxes = form.querySelectorAll('input[type="checkbox"]:checked');
            
            if (checkboxes.length === 0) {
                e.preventDefault();
                showAlert('Please select at least one symptom before analyzing.');
                return false;
            }
        });
    }
}

// ============================================
// TEXT MODE
// ============================================
function setupTextMode() {
    const analyzeTextBtn = document.getElementById('analyze-text-btn');
    const predictTextBtn = document.getElementById('predict-text-btn');
    const symptomTextarea = document.getElementById('symptom-text');
    const parseResult = document.getElementById('parse-result');
    const textLoading = document.getElementById('text-loading');
    
    if (analyzeTextBtn) {
        analyzeTextBtn.addEventListener('click', analyzeTextInput);
    }
    
    if (predictTextBtn) {
        predictTextBtn.addEventListener('click', predictFromText);
    }
    
    // Allow Enter key to submit in textarea (Ctrl+Enter)
    if (symptomTextarea) {
        symptomTextarea.addEventListener('keydown', function(e) {
            if ((e.ctrlKey || e.metaKey) && e.key === 'Enter') {
                analyzeTextInput();
            }
        });
    }
}

// ============================================
// TEXT INPUT - ANALYZE
// ============================================
async function analyzeTextInput() {
    const textInput = document.getElementById('symptom-text');
    const includeCommon = document.getElementById('include-common');
    const parseResult = document.getElementById('parse-result');
    const textLoading = document.getElementById('text-loading');
    const extractedSymptoms = document.getElementById('extracted-symptoms');
    const commonWarning = document.getElementById('common-symptoms-warning');
    
    const text = textInput.value.trim();
    
    if (!text || text.length < 2) {
        showAlert('Please describe your symptoms (at least 2 characters).');
        return;
    }
    
    // Show loading state
    textLoading.classList.remove('hidden');
    parseResult.classList.add('hidden');
    
    try {
        const response = await fetch('/parse-symptoms', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                text: text,
                include_common: includeCommon.checked,
            }),
        });
        
        const data = await response.json();
        textLoading.classList.add('hidden');
        
        if (data.success) {
            // Display extracted symptoms
            extractedSymptoms.innerHTML = '';
            if (data.symptoms.length > 0) {
                data.symptom_labels.forEach(label => {
                    const tag = document.createElement('div');
                    tag.className = 'symptom-tag';
                    tag.textContent = label;
                    extractedSymptoms.appendChild(tag);
                });
                parseResult.classList.remove('hidden');
            }
            
            // Display common symptoms warning if any
            if (data.common_symptoms && data.common_symptoms.length > 0) {
                const labels = data.common_symptoms.map(s => 
                    s.replace(/_/g, ' ').charAt(0).toUpperCase() + s.replace(/_/g, ' ').slice(1)
                );
                commonWarning.innerHTML = `
                    <h4>Common symptoms found:</h4>
                    <ul>
                        ${labels.map(l => `<li>${l}</li>`).join('')}
                    </ul>
                    <p>These are common across many conditions. Your selection is already adjusted.</p>
                `;
                commonWarning.classList.remove('hidden');
            } else {
                commonWarning.classList.add('hidden');
            }
            
            parseResult.classList.remove('hidden');
        } else {
            showAlert(data.message || 'No symptoms could be extracted from your input.');
        }
    } catch (error) {
        textLoading.classList.add('hidden');
        console.error('Error:', error);
        showAlert('Error analyzing symptoms. Please try again.');
    }
}

// ============================================
// TEXT INPUT - PREDICT
// ============================================
async function predictFromText() {
    const textInput = document.getElementById('symptom-text');
    const includeCommon = document.getElementById('include-common');
    const text = textInput.value.trim();
    
    if (!text) {
        showAlert('Please describe your symptoms.');
        return;
    }
    
    // Show loading state
    const textLoading = document.getElementById('text-loading');
    textLoading.classList.remove('hidden');
    
    try {
        const response = await fetch('/predict-from-text', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                text: text,
                include_common: includeCommon.checked,
            }),
        });
        
        const data = await response.json();
        
        if (data.success) {
            // Redirect to results page or display results
            displayPredictionResults(data);
        } else {
            showAlert(data.message || 'Could not generate prediction.');
        }
    } catch (error) {
        console.error('Error:', error);
        showAlert('Error generating prediction. Please try again.');
    } finally {
        textLoading.classList.add('hidden');
    }
}

// ============================================
// DISPLAY PREDICTION RESULTS
// ============================================
function displayPredictionResults(data) {
    // Create HTML for results page
    const resultsHTML = `
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Disease Detection Results</title>
            <link rel="stylesheet" href="/static/css/style.css">
        </head>
        <body class="results-page">
            <div class="container results-container">
                <header class="app-header">
                    <h1>Analysis Result</h1>
                </header>
                
                <section class="result-hero">
                    <p class="result-label">Possible Condition</p>
                    <h2 class="disease-name">${data.disease}</h2>
                    ${data.confidence !== null && data.confidence !== undefined ? `<p class="confidence">Model confidence: <strong>${data.confidence}%</strong> <span class="confidence-note">(a statistical estimate, not medical certainty)</span></p>` : ''}
                    ${data.uncertainty ? '<p class="alert alert-warning">The available symptoms do not identify one condition reliably. The alternatives below are possibilities, not a diagnosis.</p>' : ''}
                    ${data.selected_symptoms ? `<p class="selected-symptoms"><strong>Symptoms you entered:</strong> ${data.selected_symptoms.join(', ')}</p>` : ''}
                </section>
                
                ${data.alternatives && data.alternatives.length ? `
                    <section class="result-section alternatives-section">
                        <h3>Other possible matches</h3>
                        <ul>${data.alternatives.map(item => `<li>${item.disease} (${item.probability}%)</li>`).join('')}</ul>
                    </section>
                ` : ''}

                <section class="result-section">
                    <h3>About this condition</h3>
                    <p>${data.info.description || 'No description available'}</p>
                </section>
                        
                        ${data.info.common_symptoms ? `
                            <section class="result-section">
                                <h3>Common symptoms</h3>
                                <ul>
                                    ${data.info.common_symptoms.map(s => `<li>${s}</li>`).join('')}
                                </ul>
                            </section>
                        ` : ''}
                        
                        ${data.info.precautions ? `
                            <section class="result-section">
                                <h3>General precautions</h3>
                                <ul>
                                    ${data.info.precautions.map(p => `<li>${p}</li>`).join('')}
                                </ul>
                                ${data.info.self_care ? `<p><strong>Self-care:</strong> ${data.info.self_care}</p>` : ''}
                            </section>
                        ` : ''}

                <div class="disclaimer">
                    <strong>Disclaimer:</strong> ${data.disclaimer || 'This application is for educational purposes only.'}
                </div>
                
                <a href="/" class="btn-secondary">Check Different Symptoms</a>
            </div>
        </body>
        </html>
    `;
    
    // Write results to page
    document.open();
    document.write(resultsHTML);
    document.close();
}

// ============================================
// UTILITY FUNCTIONS
// ============================================

function showAlert(message) {
    alert(message);
}

function closeParse() {
    document.getElementById('parse-result').classList.add('hidden');
}

function clearAllSymptoms() {
    const checkboxes = document.querySelectorAll('#symptom-grid input[type="checkbox"]');
    checkboxes.forEach(cb => cb.checked = false);
    
    const counter = document.getElementById('selected-count');
    if (counter) {
        counter.textContent = '0';
    }
}

function printResults() {
    window.print();
}

function exportResults() {
    const resultsText = document.body.innerText;
    const element = document.createElement('a');
    element.setAttribute('href', 'data:text/plain;charset=utf-8,' + encodeURIComponent(resultsText));
    element.setAttribute('download', 'disease_detection_results.txt');
    element.style.display = 'none';
    document.body.appendChild(element);
    element.click();
    document.body.removeChild(element);
}
