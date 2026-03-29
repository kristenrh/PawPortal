function openPanel() {
    document.getElementById("animalPanel").style.display = "block";
}
function closePanel() {
    document.getElementById("animalPanel").style.display = "none";
}

//form handling logic
document.getElementById("animalForm").addEventListener("submit", function(e) {
    e.preventDefault();
    const formData = new FormData(this);
    fetch("/add_animal/", {
        method: "POST",
        body: formData,
        headers: {
            "X-CSRFToken": getCookie("csrftoken")
        }
    })
    .then(response => response.json())
    .then(data => {
        alert("Animal added successfully!");
        closePanel();
    });
});

function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}