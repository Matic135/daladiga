function deleteNote(id) {
    fetch('/delete/' + id, { method: 'POST' })
        .then(response => {
            if (response.ok) {
                document.getElementById('note-' + id).remove();
            } else {
                alert("Napaka pri brisanju zapiska!");
            }
        });
}