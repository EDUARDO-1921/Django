/**
 * Función que verifica si el usuario
 * quiere eliminar una película de acuerdo con
 * su id.
 * @param {*} id 
 */
function eliminarPelicula(id) {
    Swal.fire({
        title: "¿Está seguro de eliminar la Película?",
        showDenyButton: true,
        confirmButtonText: "SI",
        denyButtonText: "NO"
    }).then((result) => {
        if (result.isConfirmed) {
            location.href = "/eliminarPelicula/" + id;
        }
    });
}