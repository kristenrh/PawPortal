/* * JavaScript for handling drag-and-drop functionality on the kennel page.*/
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
/* Allow dropping by preventing the default behavior. */

function allowDrop(ev) {
    ev.preventDefault();
}

function drag(ev) {
    ev.dataTransfer.setData("animalID", ev.target.id);
}

async function drop(ev) {
    ev.preventDefault();
    const animalElementID = ev.dataTransfer.getData("animalID");
    const animalElement = document.getElementById(animalElementID);
    const dropTarget = ev.target.closest('.kennel-slot, .animal-dock');
    
    if (dropTarget) {
        dropTarget.appendChild(animalElement);
        const animalDbId = animalElementID.split('-')[1];
        const kennelDbId = dropTarget.getAttribute('data-kennel-id');

        try {
            await updateAnimalLocation(animalDbId, kennelDbId);
            console.log(`Animal ${animalDbId} moved to kennel ${kennelDbId}`);
        } catch (err) {
            console.error("Error updating animal location:", err);
        }
    }
}

async function updateAnimalLocation(animalId, kennelId) {
    const response = await fetch('/location_update/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': getCookie('csrftoken')
        },
        body: JSON.stringify({ animal_id: animalId, kennel_id: kennelId })
    });
    if (!response.ok) {
        throw new Error('Animal location update has failed');
    }
    return await response.json();
}