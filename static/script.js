// Global variables
let allDataset = [];
let filteredDataset = [];
let currentFilters = {
    income: 'all',
    age: 'all',
    location: 'all'
};

// Initialize the application
document.addEventListener('DOMContentLoaded', () => {
    loadDataset();
    setupEventListeners();
    loadDatasetStatistics();
});

// Setup event listeners
function setupEventListeners() {
    // Form submission
    document.getElementById('predictionForm').addEventListener('submit', (e) => {
        e.preventDefault();
        makePrediction();
    });

    // Quick select
    document.getElementById('loadSampleBtn').addEventListener('click', loadSelectedSample);

    // Filter buttons
    document.querySelectorAll('.filter-btn').forEach(btn => {
        btn.addEventListener('click', (e) => {
            const filterType = e.target.dataset.filter;
            const filterValue = e.target.dataset.value;
            
            // Update active state
            document.querySelectorAll(`[data-filter="${filterType}"]`).forEach(b => {
                b.classList.remove('active');
            });
            e.target.classList.add('active');
            
            // Apply filter
            currentFilters[filterType] = filterValue;
            applyFilters();
        });
    });
}

// Load dataset from server
async function loadDataset() {
    try {
        const response = await fetch('/api/dataset');
        if (!response.ok) throw new Error('Failed to load dataset');
        const data = await response.json();
        
        allDataset = data.samples;
        filteredDataset = [...allDataset];
        
        // Populate sample selector
        populateSampleSelector();
        applyFilters();
    } catch (error) {
        console.error('Error loading dataset:', error);
        showError('Failed to load dataset');
    }
}

// Populate the sample selector dropdown
function populateSampleSelector() {
    const selector = document.getElementById('sampleSelector');
    selector.innerHTML = '<option value="">-- Choose a sample --</option>';
    
    allDataset.slice(0, 50).forEach((sample, index) => {
        const option = document.createElement('option');
        option.value = index;
        const price = (sample.price * 100000).toFixed(0);
        option.textContent = `Sample ${index + 1} - $${price} (Income: ${sample.MedInc.toFixed(2)})`;
        selector.appendChild(option);
    });
}

// Load selected sample into the form
function loadSelectedSample() {
    const selector = document.getElementById('sampleSelector');
    const index = selector.value;
    
    if (index === '') {
        showError('Please select a sample');
        return;
    }
    
    const sample = allDataset[index];
    document.getElementById('medInc').value = sample.MedInc.toFixed(2);
    document.getElementById('houseAge').value = Math.round(sample.HouseAge);
    document.getElementById('aveRooms').value = sample.AveRooms.toFixed(2);
    document.getElementById('aveBdrms').value = sample.AveBedrms.toFixed(2);
    document.getElementById('population').value = Math.round(sample.Population);
    document.getElementById('aveOccup').value = sample.AveOccup.toFixed(2);
    document.getElementById('latitude').value = sample.Latitude.toFixed(2);
    document.getElementById('longitude').value = sample.Longitude.toFixed(2);
}

// Make prediction
async function makePrediction() {
    const features = {
        MedInc: parseFloat(document.getElementById('medInc').value),
        HouseAge: parseFloat(document.getElementById('houseAge').value),
        AveRooms: parseFloat(document.getElementById('aveRooms').value),
        AveBedrms: parseFloat(document.getElementById('aveBdrms').value),
        Population: parseFloat(document.getElementById('population').value),
        AveOccup: parseFloat(document.getElementById('aveOccup').value),
        Latitude: parseFloat(document.getElementById('latitude').value),
        Longitude: parseFloat(document.getElementById('longitude').value)
    };

    // Validate inputs
    if (!validateFeatures(features)) {
        return;
    }

    showLoading();

    try {
        const response = await fetch('/api/predict', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ features: Object.values(features) })
        });

        if (!response.ok) {
            const error = await response.json();
            throw new Error(error.error || 'Prediction failed');
        }

        const result = await response.json();
        displayResults(result, features);
    } catch (error) {
        showError(`Error: ${error.message}`);
    }
}

// Validate features
function validateFeatures(features) {
    const ranges = {
        MedInc: { min: 0.5, max: 15.0 },
        HouseAge: { min: 1, max: 52 },
        AveRooms: { min: 1.0, max: 141.0 },
        AveBedrms: { min: 0.33, max: 34.07 },
        Population: { min: 3, max: 35682 },
        AveOccup: { min: 0.69, max: 55.23 },
        Latitude: { min: 32.54, max: 41.95 },
        Longitude: { min: -124.35, max: -114.13 }
    };

    for (const [key, value] of Object.entries(features)) {
        const range = ranges[key];
        if (value < range.min || value > range.max) {
            showError(`${key} must be between ${range.min} and ${range.max}`);
            return false;
        }
    }
    return true;
}

// Display results
function displayResults(result, features) {
    hideLoading();
    
    const prediction = result.prediction;
    const totalPrice = (prediction * 100000).toFixed(2);
    
    document.getElementById('predictedPrice').textContent = prediction.toFixed(3);
    document.getElementById('totalPrice').textContent = totalPrice;
    document.getElementById('confidence').textContent = '75'; // Placeholder confidence
    document.getElementById('r2Score').textContent = '0.58';

    // Find similar samples
    displaySimilarSamples(features);

    // Show result container
    document.getElementById('resultContainer').classList.remove('hidden');
    document.getElementById('emptyState').classList.add('hidden');
}

// Display similar samples
function displaySimilarSamples(features) {
    const similarities = allDataset.map(sample => {
        const distance = Math.sqrt(
            Math.pow(sample.MedInc - features.MedInc, 2) +
            Math.pow(sample.HouseAge - features.HouseAge, 2) +
            Math.pow(sample.AveRooms - features.AveRooms, 2) +
            Math.pow(sample.Latitude - features.Latitude, 2) +
            Math.pow(sample.Longitude - features.Longitude, 2)
        );
        return { ...sample, distance };
    });

    similarities.sort((a, b) => a.distance - b.distance);
    const similar = similarities.slice(0, 5);

    const listContainer = document.getElementById('similarSamplesList');
    listContainer.innerHTML = '';

    similar.forEach(sample => {
        const div = document.createElement('div');
        div.className = 'sample-item';
        div.innerHTML = `
            <p><strong>Income:</strong> $${sample.MedInc.toFixed(2)}K | <strong>Age:</strong> ${Math.round(sample.HouseAge)} yrs</p>
            <p><strong>Price:</strong> $${(sample.price * 100000).toFixed(0)} | <strong>Rooms:</strong> ${sample.AveRooms.toFixed(1)}</p>
            <p><strong>Location:</strong> (${sample.Latitude.toFixed(2)}, ${sample.Longitude.toFixed(2)})</p>
        `;
        listContainer.appendChild(div);
    });

    document.getElementById('similarSamplesContainer').classList.remove('hidden');
}

// Load dataset statistics
async function loadDatasetStatistics() {
    try {
        const response = await fetch('/api/statistics');
        if (!response.ok) throw new Error('Failed to load statistics');
        const stats = await response.json();

        document.getElementById('totalSamples').textContent = stats.total_samples;
        document.getElementById('avgPrice').textContent = `$${(stats.avg_price * 100000).toFixed(0)}`;
        document.getElementById('priceRange').textContent = 
            `$${(stats.min_price * 100000).toFixed(0)} - $${(stats.max_price * 100000).toFixed(0)}`;
    } catch (error) {
        console.error('Error loading statistics:', error);
    }
}

// Apply filters to dataset
function applyFilters() {
    filteredDataset = allDataset.filter(sample => {
        let match = true;

        // Income filter
        if (currentFilters.income !== 'all') {
            if (currentFilters.income === 'low' && sample.MedInc >= 3) match = false;
            if (currentFilters.income === 'medium' && (sample.MedInc < 3 || sample.MedInc > 8)) match = false;
            if (currentFilters.income === 'high' && sample.MedInc <= 8) match = false;
        }

        // Age filter
        if (currentFilters.age !== 'all') {
            if (currentFilters.age === 'new' && sample.HouseAge >= 10) match = false;
            if (currentFilters.age === 'medium' && (sample.HouseAge < 10 || sample.HouseAge > 40)) match = false;
            if (currentFilters.age === 'old' && sample.HouseAge <= 40) match = false;
        }

        // Location filter
        if (currentFilters.location !== 'all') {
            if (currentFilters.location === 'north' && sample.Latitude <= 38) match = false;
            if (currentFilters.location === 'central' && (sample.Latitude < 37 || sample.Latitude > 38)) match = false;
            if (currentFilters.location === 'south' && sample.Latitude >= 37) match = false;
        }

        return match;
    });

    displayFilteredSamples();
}

// Display filtered samples
function displayFilteredSamples() {
    const container = document.getElementById('filteredSamplesContainer');
    container.innerHTML = '';

    const samplesToShow = filteredDataset.slice(0, 12);

    if (samplesToShow.length === 0) {
        container.innerHTML = '<p style="grid-column: 1/-1; text-align: center; padding: 40px;">No samples match the selected filters</p>';
        return;
    }

    samplesToShow.forEach((sample, index) => {
        const card = document.createElement('div');
        card.className = 'sample-card';
        card.innerHTML = `
            <h5>Sample ${index + 1}</h5>
            <p><strong>Income:</strong> $${sample.MedInc.toFixed(2)}K</p>
            <p><strong>House Age:</strong> ${Math.round(sample.HouseAge)} years</p>
            <p><strong>Rooms:</strong> ${sample.AveRooms.toFixed(1)}</p>
            <p><strong>Location:</strong> (${sample.Latitude.toFixed(2)}, ${sample.Longitude.toFixed(2)})</p>
            <div class="sample-price">$${(sample.price * 100000).toFixed(0)}</div>
        `;
        card.addEventListener('click', () => loadSampleData(sample));
        container.appendChild(card);
    });

    // Add count info
    const countInfo = document.createElement('p');
    countInfo.style.gridColumn = '1/-1';
    countInfo.style.textAlign = 'center';
    countInfo.style.marginTop = '20px';
    countInfo.style.color = '#7f8c8d';
    countInfo.innerHTML = `Showing ${samplesToShow.length} of ${filteredDataset.length} filtered samples`;
    container.appendChild(countInfo);
}

// Load sample data into the form
function loadSampleData(sample) {
    document.getElementById('medInc').value = sample.MedInc.toFixed(2);
    document.getElementById('houseAge').value = Math.round(sample.HouseAge);
    document.getElementById('aveRooms').value = sample.AveRooms.toFixed(2);
    document.getElementById('aveBdrms').value = sample.AveBedrms.toFixed(2);
    document.getElementById('population').value = Math.round(sample.Population);
    document.getElementById('aveOccup').value = sample.AveOccup.toFixed(2);
    document.getElementById('latitude').value = sample.Latitude.toFixed(2);
    document.getElementById('longitude').value = sample.Longitude.toFixed(2);

    // Scroll to form
    document.querySelector('.prediction-panel').scrollIntoView({ behavior: 'smooth' });
}

// UI Helper Functions
function showLoading() {
    document.getElementById('loadingState').classList.remove('hidden');
    document.getElementById('resultContainer').classList.add('hidden');
    document.getElementById('emptyState').classList.add('hidden');
    document.getElementById('errorState').classList.add('hidden');
}

function hideLoading() {
    document.getElementById('loadingState').classList.add('hidden');
}

function showError(message) {
    document.getElementById('errorMessage').textContent = message;
    document.getElementById('errorState').classList.remove('hidden');
    document.getElementById('resultContainer').classList.add('hidden');
    document.getElementById('emptyState').classList.add('hidden');
    document.getElementById('loadingState').classList.add('hidden');
}
