// Global variables for subject options
const subjectsForTenth = ['Maths', 'Science', 'Social Science'];
const subjectsForHigher = ['Biology', 'Physics', 'Chemistry', 'Maths'];

// Update subject options based on selected standard
document.getElementById('standard').addEventListener('change', function() {
    const standardValue = parseInt(this.value);
    const subjectSelect = document.getElementById('subject');
    
    // Clear existing options
    subjectSelect.innerHTML = '<option value="">Select Subject</option>';
    
    // Add new options based on standard
    const subjects = standardValue === 10 ? subjectsForTenth : subjectsForHigher;
    subjects.forEach(subject => {
        const option = document.createElement('option');
        option.value = subject;
        option.textContent = subject;
        subjectSelect.appendChild(option);
    });
});

// Function to get chapters from the API
async function getChapters() {
    const language = document.getElementById('language').value;
    const standard = parseInt(document.getElementById('standard').value);
    const subject = document.getElementById('subject').value;

    // Validate all fields are selected
    if (!language || !standard || !subject) {
        alert('Please select all fields');
        return;
    }

    try {
        const response = await fetch('http://127.0.0.1:5000/get-subjects', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                language_id: language,
                standard_id: standard,
                subject_id: subject
            })
        });

        const data = await response.json();
        
        // Check if there's an error in the response
        if (data.error) {
            alert(data.error);
            return;
        }
        
        displayChapters(data);
    } catch (error) {
        console.error('Error:', error);
        alert('An error occurred while fetching chapters');
    }
}

// Function to display chapters
function displayChapters(chapters) {
    const chaptersContainer = document.getElementById('chapters-container');
    const chaptersList = document.getElementById('chapters-list');
    
    // Clear previous chapters
    chaptersList.innerHTML = '';
    
    // Add each chapter to the list
    chapters.forEach(chapter => {
        const chapterElement = document.createElement('div');
        chapterElement.className = 'chapter-item';
        chapterElement.textContent = chapter;
        chaptersList.appendChild(chapterElement);
    });
    
    // Show the chapters container
    chaptersContainer.classList.remove('hidden');
}