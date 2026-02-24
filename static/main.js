// Drag & Drop Upload Effect
document.addEventListener("DOMContentLoaded", function () {

    const uploadBox = document.querySelector(".upload-box");

    if (uploadBox) {

        uploadBox.addEventListener("dragover", function (e) {
            e.preventDefault();
            uploadBox.classList.add("dragover");
        });

        uploadBox.addEventListener("dragleave", function () {
            uploadBox.classList.remove("dragover");
        });

        uploadBox.addEventListener("drop", function (e) {
            e.preventDefault();
            uploadBox.classList.remove("dragover");
        });
    }

});