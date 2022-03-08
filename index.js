function deleteNote(noteId){
    fetch("/delete-note", { /* to send a request in JS we use fetch */
        method: "POST",
        body: JSON.stringify({ noteId: noteId }),
    }).then((_res) => {
        window.location.href = "/";
    }); /*send request to delete-noteId, and after getting a response from it it will reload the window (by window.location...)*/
}
