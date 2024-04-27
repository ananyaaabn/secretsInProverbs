document.addEventListener('DOMContentLoaded', function() {
    const genreList = document.getElementById('genreList');
    genreList.addEventListener('click', function(event) {
        if (event.target.classList.contains('genre-box')) {
            const selectedGenre = event.target.dataset.genre;
            document.getElementById('selectedGenre').value = selectedGenre;
            document.getElementById('languageForm').style.display = 'block';
        }
    });
});
