import click
import os
import json
from . import PROJECT_PACKAGE, CONFIG_JSON, logging

global_error="Sorry, an internal error occurred"
try:
    with open(CONFIG_JSON) as file:
        data = json.load(file)
    versions = data["versions"]
    project_name = data["project_name"]
    versions_detail=data["versions_detail"]
except:
    message = f"The springlabs_django commands must be executed in the main project path ({CONFIG_JSON})"
    #logging.warning(message)
    raise click.BadParameter(message)

groups_api = ["options"]

def validate_manage():
    """
        Función que valida si se ejecuta comando en raiz de proyecto Django

        Función que valida si se ejecuta comando en la raiz del proyecto
        Django basandonos en el archivo manage.py
        Parámetros:
        Retorno:
            message,result      [Tuple] Mensaje de respuesta, Resultado booleano
        Excepciones:
            click.BadParameter  [Raise] Mensaje de parámetro incorrecto
    """
    list_dir = os.listdir()
    if not "manage.py" in list_dir:
        message = "The springlabs_django commands must be executed in the main project path (manage.py)"
        #logging.warning(message)
        return message, False
    return "OK", True


def validate_version_version(ctx, param, value):
    """
        Función que valida versión de subcomando create-version

        Función que valida si versión recibida es de tipo entero
        (ej. 1,2,3,4,...,n) y no existe ya una versión creada con ese
        número

        Parámetros:
            ctx         [Click Object]  Contexto de click
            param       [Click Option]  Parametro recibido
            value       [String]        Valor recibido como parámetro
        Retorno:
            value       [String]        Valor recibido como parámetro
        Excepciones:
            click.BadParameter  [Raise] Mensaje de parámetro incorrecto
    """
    message, result = validate_manage()
    if result == False:
        logging.warning(message)
        raise click.BadParameter(message)

    if not value.isdigit():
        message = f"Incorrect version '{value}'. It must be an integer value"
        logging.warning(message)
        raise click.BadParameter(message)
    if str(value) in versions:
        message = f"Duplicate version '{value}'. It must be a unique value"
        logging.warning(message)
        raise click.BadParameter(message)
    return value

def validate_api_name(ctx, param, value):
    """
        Función que valida que nombre de api este en formato correcto

        Función que valida que el nombre de la api este con formato correcto,
        es decir que solo sea alfanumérico

        Parámetros:
            ctx         [Click Object]  Contexto de click
            param       [Click Option]  Parametro recibido
            value       [String]        Valor recibido como parámetro
        Retorno:
            value       [String]        Valor recibido como parámetro
        Excepciones:
            click.BadParameter  [Raise] Mensaje de parámetro incorrecto
    """
    if value.isalnum():
        if not len(value) > 3 and len(value) < 16: 
            message = "The api name must contain between 4 and 15 characters (only letters and numbers)"
            logging.warning(message)
            raise click.BadParameter(message)
    else:
        message = "The group name must only contain letters and number (between 4 and 15 characters)"
        logging.warning(message)
        raise click.BadParameter(message)
    return value

def validate_api_version(ctx, param, value):
    """
        Función que valida versión de subcomando create-api

        Función que valida los grupos disponibles para generar una nueva
        api y llenar lista de choices en campo group de nueva api

        Parámetros:
            ctx         [Click Object]  Contexto de click
            param       [Click Option]  Parametro recibido
            value       [String]        Valor recibido como parámetro
        Retorno:
            value       [String]        Valor recibido como parámetro
        Excepciones:
            click.BadParameter  [Raise] Mensaje de parámetro incorrecto
    """
    try:
        with open(CONFIG_JSON) as file:
            data = json.load(file)
    except:
        message = f"An internal error occurred while reading file ({CONFIG_JSON})"
        logging.error(message)
        raise click.BadParameter(global_error)
    else:
        versions_detail = data['versions_detail']
        # Recorremos todas las versiones
        for versions in versions_detail:
            # Si la versión del ciclo es en donde vamos a insertar la api
            if versions['version'] == value:
                groups_api.remove("options")
                # Agregamos los grupos disponibles de esta version a la lista de grupos
                groups_api.extend(versions['groups'])
                return value
        message = "There are no groups created in this version"
        logging.warning(message)
        raise click.BadParameter(message)
    

def validate_api_name_verb(ctx, param, value):
    """
        Función que valida nombre de subcomando create-api

        Función que valida que nombre de la api no se encuentre ya registrado
        en la misma versión y mismo HTTP VERB de la aplicación.

        Parámetros:
            ctx         [Click Object]  Contexto de click
            param       [Click Option]  Parametro recibido
            value       [String]        Valor recibido como parámetro
        Retorno:
            value       [String]        Valor recibido como parámetro
        Excepciones:
            click.BadParameter  [Raise] Mensaje de parámetro incorrecto
    """
    if "version" in ctx.params and "name" in ctx.params and "group" in ctx.params:
        api_version = ctx.params['version']
        name_api = ctx.params['name']
        group_api = ctx.params['group']
    else:
        message = "Parameters are in the wrong order"
        logging.warning(message)
        raise click.BadParameter(message)
    try:
        with open(CONFIG_JSON) as file:
            data = json.load(file)
    except:
        message = f"An internal error occurred while reading file ({CONFIG_JSON})"
        logging.error(message)
        raise click.BadParameter(global_error)
    else:
        versions_detail = data['versions_detail']
        names_no_valid = []
        # Recorremos todas las versiones
        for versions in versions_detail:
            # Si la versión del ciclo es en donde vamos a insertar la api
            if versions['version'] == api_version:
                groups_detail = versions["groups_detail"]
                # Recorremos todos los grupos de esa versión
                for group_detail in groups_detail:
                    # Si el grupo del ciclo es en donde vamos a insertar la api
                    if group_api == group_detail['group']:
                        apis = group_detail['apis']
                        # Recorremos todas las apis de ese grupo
                        for api in apis:
                            verb = api["http_verb"]
                            name = api["api_name"]
                            name_verb = name.lower() + verb.upper()
                            # Agregamos a lista de names_no_valid los nombres de api no validos
                            names_no_valid.append(name_verb)
        find = name_api.lower() + value.upper()
        # Si el nombre de nuestra api ya se encuentra en el proyecto
        if find in names_no_valid:
            message = f"The api with name '{name_api}' and with HTTP '{value}' is already registered in the application"
            logging.warning(message)
            raise click.BadParameter(message)
        return value

def validate_api_url(ctx, param, value):
    """
        Función que valida url de subcomando create-api

        Función que valida que url de la api no se encuentre ya registrado
        en la misma versión.

        Parámetros:
            ctx         [Click Object]  Contexto de click
            param       [Click Option]  Parametro recibido
            value       [String]        Valor recibido como parámetro
        Retorno:
            value       [String]        Valor recibido como parámetro
        Excepciones:
            click.BadParameter  [Raise] Mensaje de parámetro incorrecto
    """
    if "version" in ctx.params:
        api_version = ctx.params['version']
    else:
        message = "Parameters are in the wrong order"
        logging.warning(message)
        raise click.BadParameter(message)
    # Validar que url no empiece en /
    if value.startswith("/") or value.endswith("/"):
        message = "The url cannot start or end with the character '/'"
        logging.warning(message)
        raise click.BadParameter(message)

    # Validar que parametros de url sean correctos
    urls = value.split("/")
    for url in urls:
        
        # Si empieza con parentesis se refiere a un argumento de la url
        if "(" in url:
            # Si NO empieza con (?P< y termina con ) es parámetro incorrecto
            if not url.startswith("(?P<") and url.endswith(")"):
                message = "Invalid url parameter"
                logging.warning(message)
                raise click.BadParameter(message)
            # Si la cantidad de parentesis de apertura '(' es diferente a los de cierre ')' es parámetro incorrecto
            if not url.count("(") == url.count(")"):
                message = "Invalid url parameter"
                logging.warning(message)
                raise click.BadParameter(message)
            # Si la cantidad de diplés de apertura '<' es diferente a los de cierre '>' es parámetro incorrecto
            if not url.count("<") == url.count(">"):
                message = "Invalid url parameter"
                logging.warning(message)
                raise click.BadParameter(message)
    try:
        with open(CONFIG_JSON) as file:
            data = json.load(file)
    except:
        message = f"An internal error occurred while reading file ({CONFIG_JSON})"
        logging.error(message)
        raise click.BadParameter(global_error)
    else:
        versions_detail = data['versions_detail']
        names_no_valid = []
        for versions in versions_detail:
            if versions['version'] == api_version:
                groups_detail = versions["groups_detail"]
                for group_detail in groups_detail:
                    apis = group_detail['apis']
                    for api in apis:
                        url = api["url"]
                        names_no_valid.append(url)
        if value in names_no_valid:
            message = f"The URL '{value}' is already registered in the project"
            logging.warning(message)
            raise click.BadParameter(message)
        return value

def validate_graph_name(ctx, param, value):
    """
        Función que valida que nombre de graph este en formato correcto

        Función que valida que el nombre de graph este con formato correcto,
        es decir que solo sea alfanumérico

        Parámetros:
            ctx         [Click Object]  Contexto de click
            param       [Click Option]  Parametro recibido
            value       [String]        Valor recibido como parámetro
        Retorno:
            value       [String]        Valor recibido como parámetro
        Excepciones:
            click.BadParameter  [Raise] Mensaje de parámetro incorrecto
    """
    if value.isalnum():
        if not len(value) > 3 and len(value) < 16: 
            message = "The graph name must contain between 4 and 15 characters (only letters and numbers)"
            logging.warning(message)
            raise click.BadParameter(message)
    else:
        message = "The graph name must only contain letters and number (between 4 and 15 characters)"
        logging.warning(message)
        raise click.BadParameter(message)
    if "version" in ctx.params and "group" in ctx.params:
        graph_version = ctx.params['version']
        group_graph = ctx.params['group']
    else:
        message = "Parameters are in the wrong order"
        logging.warning(message)
        raise click.BadParameter(message)
    name_graph = value
    try:
        with open(CONFIG_JSON) as file:
            data = json.load(file)
    except:
        message = f"An internal error occurred while reading file ({CONFIG_JSON})"
        logging.error(message)
        raise click.BadParameter(global_error)
    else:
        versions_detail = data['versions_detail']
        names_no_valid = []
        # Recorremos todas las versiones
        for versions in versions_detail:
            # Si la versión del ciclo es en donde vamos a insertar el graph
            if versions['version'] == graph_version:
                groups_detail = versions["groups_detail"]
                names_no_valid_version = versions["graph_list"]
                # Recorremos todos los grupos de esa versión
                for group_detail in groups_detail:
                    # Si el grupo del ciclo es en donde vamos a insertar el graph
                    if group_graph == group_detail['group']:
                        graphs = group_detail['graph']
                        # Recorremos todas las apis de ese grupo
                        for graph in graphs:
                            name = graph["graph_name"]
                            name_no_valid = name.lower()
                            # Agregamos a lista de names_no_valid los nombres de los graphs no validos
                            names_no_valid.append(name_no_valid)
        find = f"{name_graph.capitalize()}Queries"
        # Si el nombre de nuestro graph ya se encuentra en el proyecto
        if find in names_no_valid_version:
            message = f"A graph with name '{name_graph}' already exists in the project"
            logging.warning(message)
            raise click.BadParameter(message)
        return value
    return value

def validate_group_group(ctx, param, value):
    """
        Función que valida que nombre insertado para un nuevo grupo

        Función que valida que el nombre de graph este con formato correcto,
        es decir que solo sea alfanumérico

        Parámetros:
            ctx         [Click Object]  Contexto de click
            param       [Click Option]  Parametro recibido
            value       [String]        Valor recibido como parámetro
        Retorno:
            value       [String]        Valor recibido como parámetro
        Excepciones:
            click.BadParameter  [Raise] Mensaje de parámetro incorrecto
    """
    message, result = validate_manage()
    if result == False:
        #logging.warning(message)
        raise click.BadParameter(message)

    if value.isalnum():
        if not len(value) > 3 and len(value) < 16: 
            message = "The group name must contain between 4 and 15 characters (only letters and numbers)"
            logging.warning(message)
            raise click.BadParameter(message)
    else:
        message = "The group name must only contain letters and number (between 4 and 15 characters)"
        logging.warning(message)
        raise click.BadParameter(message)

    if "version" in ctx.params:
        insertversion=ctx.params["version"]
    else:
        message = "Parameters are in the wrong order"
        logging.warning(message)
        raise click.BadParameter(message)

    for detail in versions_detail:
        if detail["version"]==insertversion:
            if value.upper() in (gr.upper() for gr in detail["groups"]):
                message = f"group '{value}' already exists in version '{insertversion}'"
                logging.warning(message)
                raise click.BadParameter(message)
    return value