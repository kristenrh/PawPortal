function openAddPanel() {
    document.getElementById("animalAddPanel").style.display = "block";
}
function closeAddPanel() {
    document.getElementById("animalAddPanel").style.display = "none";
}

function openRemovePanel() {
    document.getElementById("animalRemovePanel").style.display = "block";
}
function closeRemovePanel() {
    document.getElementById("animalRemovePanel").style.display = "none";
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
        if(data.status === "success") {
            alert("Animal added successfully!");
            closeAddPanel();
            location.reload(); // Refresh to show new animal
        } else {
            alert("Failed to add animal. Please try again."+data.message);
        }
    })
    .catch(err => {
        console.error("Error adding animal:", err);
        alert("Failed to add animal. Please try again.");
    });
});

document.getElementById("removeForm").addEventListener("submit", function(e) {
    e.preventDefault();
    const animalId = document.getElementById("removeAnimalSelect").value;

    fetch("/remove_animal/", {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
            "X-CSRFToken": getCookie("csrftoken")
        },
        body: JSON.stringify({ id: animalId })
    })
    .then(response => response.json())
    .then(data => {
        if(data.status === "success") {
            alert("Animal removed successfully!");
            closeRemovePanel();
            location.reload();
        } else {
            alert("Failed to remove animal. Please try again.");
        }
    })
    .catch(err => {
        console.error("Error removing animal:", err);
        alert("Failed to remove animal. Please try again.");
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