// Este script jquery nos permite añadir enlaces a las columnas
jQuery(document).ready(function ($) {
    $(".clic-columna").click(function () {
        window.location = $(this).data("href");
    });
});

// Función que nos permite previsualizar la imagen al seleccionarla
function cambiarImagen(event) {
    let ficheroSeleccionado = event.target.files[0];
    let leer = new FileReader();

    let etiquetaImagen = document.getElementById("imagen_auto");
    etiquetaImagen.title = ficheroSeleccionado.name;

    leer.onload = function (event) {
        etiquetaImagen.src = event.target.result;
    };

    leer.readAsDataURL(ficheroSeleccionado);
}