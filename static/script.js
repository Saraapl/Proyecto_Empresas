function agregarDB(nombre, localizacion, telefono, correo){
    let localizacion = prompt("Escriba la ubicacion de la empresa: ")
    let correo = prompt("Escriba la el nombre de la empresa: ")
    let telefono = prompt("Escriba el telefono de la empresa: ")
    let nombre = prompt("Escriba el nombre de la empresa: ")
    return devolverBaseDedatos(nombre, localizacion, telefono, correo)
}

function consultarUnaNacional(nombre){
    nombre = prompt("Escriba el nombre de la empresa que desea consultar: ")
    buscarEmpresaNacional = Empresas_nacionales.find_one({"Nombre": nombreBuscar})
    return buscarEmpresaNacional
    }

function consultarUnaInternacional(nombre){
    nombre = prompt("Escriba el nombre de la empresa que desea consultar: ")
    buscarEmpresaExtranjera = Empresas_extranjeras.find_one({"Nombre": nombreBuscar})
    return buscarEmpresaExtranjera
    }
    