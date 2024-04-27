document.addEventListener("DOMContentLoaded", function() {
    const languageBoxes = document.querySelectorAll(".language-box");

    // Event listener for language boxes
    languageBoxes.forEach(function(box) {
        box.addEventListener("click", function() {
            const selectedLanguage = box.dataset.language;
            const selectedGenre = document.querySelector('input[name="genre"]').value;
            window.location.href = `/proverb?genre=${selectedGenre}&language=${selectedLanguage}`;
        });
    });
});
