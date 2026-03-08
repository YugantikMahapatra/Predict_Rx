// Loading Spinner
function showLoading() {
    const symptomsInput = document.getElementById('symptoms');
    const symptoms = symptomsInput.value;
    if (symptoms && symptoms !== "Symptoms") {
        document.getElementById('loading-overlay').style.display = 'flex';
    }
}

// Autocomplete Functionality
function setupAutocomplete(symptomsArray) {
    const symptomsInput = document.getElementById('symptoms');
    const symptomsListDiv = document.getElementById('symptoms-list');

    if (!symptomsInput || !symptomsListDiv) return;

    symptomsInput.addEventListener('input', function() {
        const val = this.value;
        closeAllLists();
        if (!val) { return false; }

        // Get the last symptom being typed (after the last comma)
        const terms = val.split(',');
        const currentTerm = terms[terms.length - 1].trim().toLowerCase();

        if (currentTerm.length === 0) return;

        let matchCount = 0;

        symptomsArray.forEach(function(symptom) {
            if (symptom.toLowerCase().includes(currentTerm) && matchCount < 10) { // Limit to 10 suggestions
                const itemDiv = document.createElement("div");
                // Highlight the matching part
                const regex = new RegExp(currentTerm, "gi");
                itemDiv.innerHTML = symptom.replace(regex, (match) => `<strong>${match}</strong>`);

                itemDiv.addEventListener("click", function() {
                    // Replace the current term with the selected symptom
                    terms[terms.length - 1] = symptom;
                    symptomsInput.value = terms.join(', ') + ', ';
                    closeAllLists();
                    symptomsInput.focus();
                });
                symptomsListDiv.appendChild(itemDiv);
                matchCount++;
            }
        });

        if (matchCount > 0) {
            symptomsListDiv.style.display = "block";
        }
    });

    // Close the list if clicked outside
    document.addEventListener("click", function (e) {
        if (e.target !== symptomsInput) {
            closeAllLists();
        }
    });

    function closeAllLists() {
        symptomsListDiv.innerHTML = "";
        symptomsListDiv.style.display = "none";
    }
}

// Speech Recognition
function setupSpeechRecognition() {
    const startSpeechRecognitionButton = document.getElementById('startSpeechRecognition');
    const transcriptionDiv = document.getElementById('transcription');
    const symptomsInput = document.getElementById('symptoms');

    if (startSpeechRecognitionButton) {
        startSpeechRecognitionButton.addEventListener('click', startSpeechRecognition);
    }

    function startSpeechRecognition() {
        if (!('webkitSpeechRecognition' in window)) {
            alert("Speech recognition is not supported in this browser. Please use Chrome.");
            return;
        }

        const recognition = new webkitSpeechRecognition(); // Use webkitSpeechRecognition for compatibility

        recognition.lang = 'en-US'; // Set the language for recognition

        recognition.onresult = function (event) {
            const result = event.results[0][0].transcript;
            transcriptionDiv.textContent = result;
            if (symptomsInput) {
                // Append the speech result to the existing input
                const currentVal = symptomsInput.value;
                if (currentVal) {
                    symptomsInput.value = currentVal + ', ' + result;
                } else {
                    symptomsInput.value = result;
                }
            }
        };

        recognition.onend = function () {
            console.log('Speech recognition ended.');
        };

        recognition.start();
    }
}

// Section Toggling
function showSection(sectionId) {
    // Hide all sections
    const sections = document.querySelectorAll('.content-section');
    sections.forEach(section => {
        section.classList.remove('active');
    });

    // Show the selected section
    const selectedSection = document.getElementById(sectionId);
    if (selectedSection) {
        selectedSection.classList.add('active');
        // Smooth scroll to the section
        selectedSection.scrollIntoView({ behavior: 'smooth', block: 'center' });
    }
}

// Initialize everything when DOM is ready
document.addEventListener('DOMContentLoaded', function() {
    setupSpeechRecognition();

    // Note: setupAutocomplete needs to be called from the HTML template
    // because it requires the symptoms_list data from Jinja2
});