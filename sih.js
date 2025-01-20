function navigateToSection(ageGroup) {
    document.getElementById('age-selection').style.display = 'none';
    document.getElementById('section-content').style.display = 'block';
    document.getElementById('age-title').innerText = ageGroup.charAt(0).toUpperCase() + ageGroup.slice(1);

    // Change background based on the selected age group
    if (ageGroup === 'kids') {
        document.body.style.backgroundImage = "url('kids playing.jpeg')";
        showContentForAgeGroup('kids');
    } else if (ageGroup === 'teens') {
        document.body.style.backgroundImage = "url('teens bg.jpeg')";
        showContentForAgeGroup('teens');
    } else if (ageGroup === 'adults') {
        document.body.style.backgroundImage = "url('adults bg.jpeg')";
        showContentForAgeGroup('adults');
    }
}

function showContentForAgeGroup(ageGroup) {
    // Hide all age-specific sections initially
    document.querySelectorAll('.age-specific-content').forEach(function(content) {
        content.style.display = 'none';
    });

    // Show specific content for the selected age group
    document.querySelectorAll(`.${ageGroup}-content`).forEach(function(content) {
        content.style.display = 'block';
    });
}

function navigateTo(section) {
    alert(`Navigating to the ${section} section!`);
    // You can implement logic here to show content for learning, games, chatbot, etc.
}

function backToHome() {
    document.getElementById('age-selection').style.display = 'block';
    document.getElementById('section-content').style.display = 'none';
    document.body.style.backgroundImage = "url('default-bg.jpg')"; // Default homepage background
}
