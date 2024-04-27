document.addEventListener("DOMContentLoaded", function () {
    const urlParams = new URLSearchParams(window.location.search);
    const language = urlParams.get('language');
    let genre = urlParams.get('genre');

    const proverbContainer = document.getElementById("proverb-container");

    // Fetch proverbs based on genre and language
    fetch(`/proverb?genre=${genre}&language=${language}`)
        .then(response => response.json())
        .then(data => {
            // Assuming proverbs are returned as an array in the response
            const proverbs = data.proverbs;
            const proverbList = proverbs.map(proverb => `<li>${proverb}</li>`).join('');
            proverbContainer.innerHTML = `<ul>${proverbList}</ul>`;
        })
        .catch(error => {
            console.error('Error fetching proverbs:', error);
            proverbContainer.innerHTML = '<p>Error fetching proverbs</p>';
        });
});
