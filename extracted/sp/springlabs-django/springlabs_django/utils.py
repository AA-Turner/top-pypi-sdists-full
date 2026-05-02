import os
import json

from .primary_functions import (
    appendContent,
    replaceContent,
    findNReplace,
    findNDelete,
    deleteContent,
    notRecursiveModify,
    recursiveModify,
    getRangeStr,
    getRangeEnds,
    generateBackup,
    reverseChanges,
    modifyFilesNewVersion,
    createDirectoriesNewVersion,
    modifyFilesNewAPI,
    modifyFilesNewGraph,
    modifyFilesNewGroup,
    createDirectoriesNewGroup,
    deleteBackup
)
from . import PROJECT_PACKAGE, CONFIG_JSON, logging

global_error="Sorry, an internal error occurred"
def createVersion(version, project_name, old_versions):
    """
        Función encargada de crear nueva version en proyecto django

        Función encargada de crear nueva versión en proyecto django

        Parámetros:
            version         [String]    Nueva versión del proyecto
        Retorno:
            message,result  [Tuple]     Mensaje[String] y result[Boolean]
    """
    message, result = generateBackup(project_name=project_name)
    if result == False:
        message = "An internal error occurred while creating backup"
        logging.error(message)
        return global_error, False
    
    errors = []
    # Modifica archivos para nueva versión
    message, result = modifyFilesNewVersion(version=version,
        project_name=project_name,
        old_versions=old_versions)
    
    # Si falla al escribir archivos se agrega a arreglo
    if result == False:
        logging.error(message)
        errors.append([global_error, True])
    
    # Crea directorios y archivos dentro para nueva versión
    message, result = createDirectoriesNewVersion(version=version,
        project_name=project_name,
        old_versions=old_versions)
    
    # Si falla al modificar directorios se agrega a arreglo
    if result == False:
        logging.error(message)
        errors.append([global_error, True])
    try:
        with open(CONFIG_JSON) as file:
            data = json.load(file)
    except:
        message = f"An internal error occurred while creating backup {CONFIG_JSON}"
        logging.error(message)
        errors.append([global_error, True])
    else:
        objVersionDetail = {
            "version": version,
            "groups": ["users"],
            "graph_list":["ExampleDjangoUsersQueries"],
            "groups_detail": [
                {
                    "group": "users",
                    "apis": [],
                    "graph": [
                        {
                            "graph_name": "ExampleDjangoUsers",
                            "graph_type" : "open"
                        }
                    ]
                }
            ]
        }
        data["versions"].append(version)
        data['versions_detail'].append(objVersionDetail)
        try:
            with open(CONFIG_JSON, "w") as file:
                file.write(json.dumps(data))
        except:
            message = f"An internal error occurred while updating the file {CONFIG_JSON}"
            logging.error(message)
            errors.append([global_error, True])

    for error in errors:
        if error[1] == True:
            message, result = reverseChanges(project_name=project_name)
            os.chdir("..")
            os.remove(project_name + ".zip")
            os.chdir(project_name)
            return error[0], False
    deleteBackup(project_name=project_name)
    return "OK", True

def createAPI(version,group,name,http_verb,type_api,url,availability,project_name):
    """
        Función encargada de crear nueva api en proyecto django

        Función encargada de crear nueva api en proyecto django

        Parámetros:
            version         [String]    Versión donde se creará la API
            group           [String]    Grupo donde se creará la API
            name            [String]    Nombre de la API
            http_verb       [String]    HTTP Verb de la API (POST, PUT, DELETE)
            type_api        [String]    Tipo de la API (MODEL, OPEN)
            url             [String]    URL donde se podrá acceder a la API
            availability    [String]    Disponibilidad de la API (public, private)
            project_name    [String]    Nombre del proyecto
        Retorno:
            message,result  [Tuple]     Mensaje[String] y result[Boolean]
    """
    # Generar respaldo de proyecto
    message, result = generateBackup(project_name=project_name)
    if result == False:
        message = "An internal error occurred while creating backup"
        logging.error(message)
        return global_error, False

    errors = []

    # Modifica archivos para nueva api
    message, result = modifyFilesNewAPI(version=version,
        group=group,
        name=name,
        http_verb=http_verb,
        type_api=type_api,
        url=url,
        availability=availability,
        project_name=project_name)
    
    # Si falla al modificar directorios se agrega a arreglo
    if result == False:
        logging.error(message)
        errors.append([global_error, True])


    try:
        with open(CONFIG_JSON) as file:
            data = json.load(file)
    except:
        message = f"An internal error occurred while updating the file {CONFIG_JSON}"
        logging.error(message)
        errors.append([global_error, True])
    else:
        objApis = {
            "api_name": name,
            "http_verb": http_verb,
            "api_type" : type_api,
            "url": url,
            "availability" : availability
        }
        versions_detail = data['versions_detail']
        # Recorremos todas las versiones
        for index_versions, versions in enumerate(versions_detail):
            # Si la versión del ciclo es en donde vamos a insertar la api
            if versions['version'] == version:
                groups_detail = versions["groups_detail"]
                # Recorremos todos los grupos de esa versión
                for index_groups, group_detail in enumerate(groups_detail):
                    # Si el grupo del ciclo es en donde vamos a insertar la api
                    if group == group_detail['group']:
                        data['versions_detail'][index_versions]['groups_detail'][index_groups]['apis'].append(objApis)
        try:
            with open(CONFIG_JSON, "w") as file:
                file.write(json.dumps(data))
        except:
            message = f"An internal error occurred while updating the file {CONFIG_JSON}"
            logging.error(message)
            errors.append([global_error, True])
    # Si algo sale mal revertir los cambios y eliminar respaldo
    for error in errors:
        if error[1] == True:
            message, result = reverseChanges(project_name=project_name)
            os.chdir("..")
            os.remove(project_name + ".zip")
            os.chdir(project_name)
            return error[0], False
    deleteBackup(project_name=project_name)
    return "OK", True

def createGraph(version,group,name,type_graph,project_name):
    """
        Función encargada de crear nuevo graph en proyecto django

        Función encargada de crear nuevo graph en proyecto django

        Parámetros:
            version         [String]    Versión donde se creará el Graph
            group           [String]    Grupo donde se creará el Graph
            name            [String]    Nombre del Graph
            type_graph      [String]    Tipo del Graph (MODEL, OPEN)
            project_name    [String]    Nombre del proyecto
        Retorno:
            message,result  [Tuple]     Mensaje[String] y result[Boolean]
    """
    
    # Generar respaldo de proyecto
    message, result = generateBackup(project_name=project_name)
    if result == False:
        message = "An internal error occurred while creating backup"
        logging.error(message)
        return global_error, False

    errors = []

    # Modifica archivos para nuevo graph
    message, result = modifyFilesNewGraph(version=version,
        group=group,
        name=name,
        type_graph=type_graph,
        project_name=project_name)
    
    # Si falla al modificar directorios se agrega a arreglo
    if result == False:
        logging.error(message)
        errors.append([global_error, True])


    try:
        with open(CONFIG_JSON) as file:
            data = json.load(file)
    except:
        message = f"An internal error occurred while updating the file {CONFIG_JSON}"
        logging.error(message)
        errors.append([global_error, True])
    else:
        objGraph = {
            "graph_name": name,
            "graph_type": type_graph
        }
        versions_detail = data['versions_detail']
        # Recorremos todas las versiones
        for index_versions, versions in enumerate(versions_detail):
            # Si la versión del ciclo es en donde vamos a insertar el graph
            if versions['version'] == version:
                groups_detail = versions["groups_detail"]
                # Recorremos todos los grupos de esa versión
                for index_groups, group_detail in enumerate(groups_detail):
                    # Si el grupo del ciclo es en donde vamos a insertar el graph
                    if group == group_detail['group']:
                        data['versions_detail'][index_versions]['groups_detail'][index_groups]['graph'].append(objGraph)
        try:
            with open(CONFIG_JSON, "w") as file:
                file.write(json.dumps(data))
        except:
            message = f"An internal error occurred while updating the file {CONFIG_JSON}"
            logging.error(message)
            errors.append([global_error, True])
    # Si algo sale mal revertir los cambios y eliminar respaldo
    for error in errors:
        if error[1] == True:
            message, result = reverseChanges(project_name=project_name)
            os.chdir("..")
            os.remove(project_name + ".zip")
            os.chdir(project_name)
            return error[0], False
    deleteBackup(project_name=project_name)
    return "OK", True

def getVersions():
    """
        Función que obtiene las versiones existentes del proyecto.

        Esta función abre el archivo springlabs_json y obtiene las versiones
        que existen en el proyecto

        Retorno:
            version     [Array]       Lista de versiones existentes
        Exceptions:
            OSError                   Error al abrir el archivo json
    """
    try:
        with open(CONFIG_JSON, "r") as file:
            data = json.load(file)
        versions = data["versions"]
    except:
        message="An error occurred while opening file 'springlabs_django.json'"
        logging.error(message)
        versions=["1"]
    return versions

def createGroup(version, group, project_name):
    """
        Función encargada de crear nuevo grupo en proyecto django

        Parámetros:
            version         [String]    Versión donde se creará el grupo
            group           [String]    Grupo donde se creará el grupo
            project_name    [String]    Nombre del proyecto
        Retorno:
            message,result  [Tuple]     Mensaje[String] y result[Boolean]
        Excepciones:
            OSError                     Error al abrir archivos

    """

    # Generar respaldo de proyecto
    message, result = generateBackup(project_name=project_name)
    if result == False:
        message = "An internal error occurred while creating backup"
        logging.error(message)
        return global_error, False
    
    errors=[]
    message,result=modifyFilesNewGroup(version, group,project_name)
    if result == False:
        logging.error(message)
        errors.append([global_error, True])

    # Crea directorios y archivos dentro para un nuevo grupo
    message, result = createDirectoriesNewGroup(version, group, project_name)
    
    # Si falla al modificar directorios se agrega a arreglo
    if result == False:
        logging.error(message)
        errors.append([global_error, True])


    try:
        with open(CONFIG_JSON) as file:
            data = json.load(file)
    except Exception as e:
        message = f"An internal error occurred while updating the file {CONFIG_JSON}"
        logging.error(message)
        errors.append([global_error, True])
    else:
        groupcap=group.capitalize()
        changename=f"ExampleDjango{groupcap}"

        objGroupDetail = {
                    "group": group,
                    "apis": [],
                    "graph": [{"graph_name": changename,
                    "graph_type": "open"}]
                }

        for obj in data["versions_detail"]:
            if obj["version"]==version:
                obj["groups"].append(group)
                if not "groups_detail" in obj:
                    obj["groups_detail"]=[]
                obj["groups_detail"].append(objGroupDetail)
                if not "graph_list" in obj:
                    obj["graph_list"]=[]
                obj["graph_list"].append(f"{changename}Queries")
        try:
            with open(CONFIG_JSON, "w") as file:
                file.write(json.dumps(data))
        except:
            message = f"An internal error occurred while updating the file {CONFIG_JSON}"
            logging.error(message)
            errors.append([global_error, True])
    for error in errors:
        if error[1] == True:
            message, result = reverseChanges(project_name=project_name)
            os.chdir("..")
            os.remove(project_name + ".zip")
            os.chdir(project_name)
            return error[0], False
    deleteBackup(project_name=project_name)
    return "OK", True
