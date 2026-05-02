import os
import re
from zipfile import ZipFile
import shutil
import pkgutil
import json
from . import CONFIG_JSON, PROJECT_PACKAGE


def appendContent(path, content, find=None, recursive=False):
    '''
    Agrega contenido al final del archivo especificado, si existe un valor en "find", agregará el contenido despues de la coincidencia.

    Atributos:
            path            [String]            Ruta de archivo a editar
            content         [String]            Nuevo contenido a agregar
            find            [String]            cadena a buscar, si es nulo el contenido se agregara al final
            recursive       [Boolean]           Indica si la operación será recursiva
    Retorno:
            result          [Tupla]             Resultado de operación
    Excepciones:
            OSError                             Error al crear el archivo
            OSError                             Error al escribir el contenido
    '''
    if not os.path.exists(path):
        return f'File {path} does not exist', False
    if find == None:
        try:
            """ if not os.path.exists(path):
                    open(path, "x")
            with open(f'{path}.bak', "w") as f:
                    f.write(open(path).read()) """
            with open(path, "a") as f:
                newContent = f'\n{content}'
                f.write(newContent)
            return f'The file "{path}" has been updated successfully.', True
        except Exception as exc:
            return f'Error writing content:{exc}', False
    else:
        if recursive == False:
            return notRecursiveModify(path, content, find, 'append')
        elif recursive == True:
            return recursiveModify(path, content, find, 'append')

        return f'Invalid value for recursive parameter', False


def replaceContent(path, content, start, end='--end', recursive=False):
    '''
    Remplaza cierto contenido del archivo especificado.

    Atributos:
            path            [String]            Ruta de archivo a editar
            content         [String]            Nuevo contenido a agregar
            start           [String]            Parametro a partir del cual se iniciará el remplazo hasta encontrar el parametro "end"
            recursive       [Boolean]           Indica si la operación será recursiva
    Retorno:
            result          [Tupla]             Resultado de operación
    Excepciones:
            OSError                             Error al escribir el contenido
    '''
    if not os.path.exists(path):
        return f'File {path} does not exists', False

    starts = getRangeStr(path, start)
    ends = getRangeEnds(path, end)
    if ends == None or len(ends) == 0:
        return f'The file does not have end delimiters: "{end}"', False
    if starts == None or len(starts) == 0:
        return f'The file does not have start delimiters: "{start}"', False
    textsReplace = []
    for idx, _ in enumerate(ends):
        if len(starts) <= idx or starts[idx][1] > ends[idx][0]:
            break
        textsReplace.append([starts[idx][1] + 1,  ends[idx][0] - 1])
    file = open(path).read()
    if len(textsReplace) == 0:
        return f'The file has wrong start delimiters "{start}" and/or end delimiters "{end}", please check', False
    if recursive == False:
        return notRecursiveModify(path, content, file[textsReplace[0][0]:textsReplace[0][1]], 'replace')
    elif recursive == True:
        try:
            for text in textsReplace:
                recursiveModify(
                    path, content, file[text[0]:text[1]], 'replace')
            return f'File "{path}" was successfully updated', True
        except Exception as exc:
            return f'Error writing content: {exc}', False

    return f'Invalid value for recursive parameter', False


def findNReplace(path, content, find, recursive=False):
    '''
    Remplaza cierto contenido del archivo especificado.

    Atributos:
            path            [String]            Ruta de archivo a editar
            content         [String]            Nuevo contenido a agregar
            find            [String]            Se hará un "search & replace de la valor dado
            recursive       [Boolean]           Indica si la operación será recursiva
    Retorno:
            result          [Tupla]             Resultado de operación
    Excepciones:
            OSError                             Error al escribir el contenido
    '''
    if not os.path.exists(path):
        return f'File {path} does not exists', False
    if recursive == False:
        return notRecursiveModify(path, content, find, 'replace')
    elif recursive == True:
        return recursiveModify(path, content, find, 'replace')

    return f'Invalid value for recursive parameter', False


def findNDelete(path, find, recursive=False):
    '''
    Elimina cierto contenido del archivo especificado.

    Atributos:
            path            [String]            Ruta de archivo a editar
            find            [String]            Se hará un "search & replace de la valor dado
            recursive       [Boolean]           Indica si la operación será recursiva
    Retorno:
            result          [Tupla]             Resultado de operación
    Excepciones:
            OSError                             Error al escribir el contenido
    '''
    if not os.path.exists(path):
        return f'File {path} does not exists', False
    if recursive == False:
        return findNReplace(path, '', find)
    elif recursive == True:
        return findNReplace(path, '', find, recursive=True)

    return f'Invalid value for recursive parameter', False


def deleteContent(path, start, end='--end', recursive=False):
    '''
    Elimina cierto contenido del archivo especificado.

    Atributos:
            path            [String]            Ruta de archivo a editar
            start           [String]            Parametro a partir del cual se iniciará el remplazo hasta encontrar el parametro "end"
            recursive       [Boolean]           Indica si la operación será recursiva
    Retorno:
            result          [Tupla]             Resultado de operación
    Excepciones:
            OSError                             Error al escribir el contenido
    '''
    if not os.path.exists(path):
        return f'The file does not exists', False
    if recursive == False:
        return replaceContent(path, '', start, end)
    elif recursive == True:
        return replaceContent(path, '', start, end, recursive=True)

    return f'Invalid value for recursive parameter', False


def notRecursiveModify(path, content, find, type):
    '''
    Modifica un archivo dado, en la coincidencia "find" con el contenido de "content" (solo primera coincidencia).

    Atributos:
            path            [String]            Ruta de archivo a editar
            content         [String]            Nuevo contenido a agregar
            find            [String]            Se hará un "search & replace de la valor dado
            type	        [String]            Indica el tipo de operación
    Retorno:
            result          [Tupla]             Resultado de operación
    Excepciones:
            OSError                             Error al escribir el contenido
    '''
    file = open(path).read()
    matchFound = False
    find = find.replace("(", r'\(')
    find = find.replace(")", r'\)')
    find = find.replace("{", r'\{')
    find = find.replace("}", r'\}')
    find = find.replace("[", r'\[')
    find = find.replace("]", r'\]')
    find = find.replace("+", r'\+')
    find = find.replace("<", r'\<')
    find = find.replace("-", r'\-')
    find = find.replace("!", r'\!')
    find = find.replace("*", r'\*')
    find = find.replace("~", r'\~')
    find = find.replace("¬", r'\¬')
    find = find.replace(",", r'\,')
    find = find.replace(":", r'\:')
    find = find.replace(".", r'\.')

    matches = re.finditer(find, file)
    for m in matches:
        matchFound = True
        break
    if matchFound == False:
        return f'No matches found with "{find}"', False
    if type == 'append':
        newContent = f'{file[: m.end()]}  \n{content} \n{file[m.end() + 1:]}'
    elif type == 'replace':
        newContent = f'{file[: m.start()]}{content}{file[m.end():]}'
    else:
        return f'Invalid replacement type', False
    try:
        '''with open(f'{path}.bak', "w") as f:
                f.write(open(path).read())'''
        with open(path, "w") as f:
            f.write(newContent)
        return f'File "{path}" was successfully updated', True
    except Exception as exc:
        return f'Error writing content: {exc}', False


def recursiveModify(path, content, find, type):
    '''
    Modifica un archivo dado, en la coincidencia "find" con el contenido de "content" de manera recursiva.

    Atributos:
            path            [String]            Ruta de archivo a editar
            content         [String]            Nuevo contenido a agregar
            find            [String]            Se hará un "search & replace de la valor dado
            type	        [String]            Indica el tipo de operación
    Retorno:
            result          [Tupla]             Resultado de operación
    Excepciones:
            OSError                             Error al escribir el contenido
    '''
    if type == 'append':
        newContent = f'{find} \n{content}\n'
    elif type == 'replace':
        newContent = content
    else:
        return f'Invalid replacement type', False
    try:
        file = open(path).read()
        '''with open(f'{path}.bak', "w") as f:
			f.write(open(path).read())'''
        with open(path, "w") as f:
            f.write(file.replace(find, newContent))
        return f'File "{path}" was successfully updated', True
    except Exception as exc:
        return f'Error writing content: {exc}', False


def getRangeStr(path, find):
    '''
    Obtiene los indices del primer y ultimo caracter del valor de "find".

    Atributos:
            path            [String]            Ruta de archivo a editar
            find            [String]            Se hará un search de la valor dado
    Retorno:
            arr          	[Lista]            Indices
    Excepciones:
            OSError                             Error al escribir el contenido
    '''
    arr = []
    file = open(path).read()
    find = find.replace("(", r'\(')
    find = find.replace(")", r'\)')
    find = find.replace("{", r'\{')
    find = find.replace("}", r'\}')
    find = find.replace("[", r'\[')
    find = find.replace("]", r'\]')
    find = find.replace("+", r'\+')
    find = find.replace("<", r'\<')
    find = find.replace("-", r'\-')
    find = find.replace("!", r'\!')
    find = find.replace("*", r'\*')
    find = find.replace("~", r'\~')
    find = find.replace("¬", r'\¬')
    find = find.replace(",", r'\,')
    find = find.replace(":", r'\:')
    find = find.replace(".", r'\.')

    matches = re.finditer(find, file)
    for m in matches:
        arr.append([m.start(), m.end()])
    return arr


def getRangeEnds(path, find):
    '''
    Obtiene los indices del primer y ultimo caracter de la linea donde se encuentre el valor de "find".

    Atributos:
            path            [String]            Ruta de archivo a editar
            find            [String]            Se hará un "search & replace de la valor dado
    Retorno:
            arr          	[Lista]            Indices
    Excepciones:
            OSError                             Error al escribir el contenido
    '''
    with open(path) as file:
        for line in file:
            if find in line:
                return getRangeStr(path, line)


def generateBackup(project_name, path=os.getcwd()):
    """
        Función que genera un respaldo del proyecto 

        Función encargada de generar un respaldo del proyecto antes de realizar alguna
        acción, se genera un zip con el nombre del proyecto por si algo llega a fallar
        revertir los cambios 
        
        Parametros:
            project_name (String): Nombre del proyecto a generar respaldo
            path (String): Ruta donde se encuentra el proyecto a respaldar 
        Retorno:
            message,result (Tuple): Mensaje[String] y result[Boolean]

    """
    oldPath = path
    os.chdir("..")
    shutil.make_archive(project_name, 'zip', base_dir=project_name)
    os.chdir(oldPath)
    return "OK", True
    

def reverseChanges(project_name, path=os.getcwd()):
    """
        Función que revierte los cambios de una acción 

        Función encargada de revertir los cambios de una acción, hace que se haga un unzip
        del respaldo realizado antes de la acción y poder eliminar el contenido con errores 
        
        Parametros:
            project_name (String): Nombre del proyecto a revertir cambios
            path (String): Ruta donde se encuentra el proyecto a revertir 
        Retorno:
            message,result (Tuple): Mensaje[String] y result[Boolean]

    """
    try:
        oldPath = path
        os.chdir("..")
        shutil.rmtree(project_name)
        botZip = f'{project_name}.zip'
        with ZipFile(botZip, 'r') as zip_ref:
            zip_ref.extractall(os.getcwd())
        os.chdir(oldPath)
        return "OK", True
    except Exception as e:
        return str(e), False


def deleteBackup(project_name, path=os.getcwd()):
    """
        Función que elimina el respaldo de un proyecto 

        Función encargada de eliminar el respaldo de un proyecto al terminar una acción 
        
        Parametros:
            project_name (String): Nombre del proyecto que se desea eliminar respaldo
            path (String): Ruta donde se encuentra el proyecto que se desea eliminar respaldo
        Retorno:
            message,result (Tuple): Mensaje[String] y result[Boolean]

    """
    try:
        oldPath = os.getcwd()
        os.chdir("..")
        os.remove(project_name + ".zip")
        os.chdir(oldPath)
        return "OK", True
    except Exception as e:
        return str(e), False

def modifyFilesNewVersion(version, project_name, old_versions):
    """
        Función que modifica archivos para agregar nueva versión

        Función que modifica los archivos de Django en los que se tiene
        que agregar la nueva versión (No contempla nuevas carpetas)

    Args:
        version (String): Nueva versión del proyecto
        project_name (String): Nombre del proyecto
        old_versions (List): Lista de versiones existentes en proyecto
    Returns:
        message,result (Tuple): Mensaje[String] y result[Boolean]
    Exceptions:
        exception ([type]): [description]
    """

    errors = []
    # Crear version en project_name/urls.py
    # Importar public versions de nueva versión
    path = f"{project_name}/urls.py"
    find = "# PUBLIC VERSIONS URLS (Managed by SPRINGLABS_DJANGO)"
    content = f"from api.v{version}.public_urls import public_urls as public_urls_v{version}"
    message, result = appendContent(path=path,
        content=content,
        find=find)
    if result == False:
        errors.append([message, True])

    # Agregar nueva version a urls_versions
    find = "urls_versions ="
    for index, old_version in enumerate(old_versions):
        if index == 0:
            public_urls = f" public_urls_v{old_version}"
        else:
            public_urls = f" + public_urls_v{old_version}"
        find = find + public_urls
    content = find + f" + public_urls_v{version}"

    message, result = findNReplace(path=path,
        content=content,
        find=find)
    if result == False:
        errors.append([message, True])
    
    # Crear version en api/urls.py
    # Agregar nueva version a url_patterns
    path = "api/urls.py"
    find = "# VERSIONS URLS (Managed by SPRINGLABS_DJANGO)"
    content = f"""
    url(r'^v{version}/', include('api.v{version}.urls', namespace='v{version}')),"""
    message, result = appendContent(path=path,
        content=content,
        find=find)
    if result == False:
        errors.append([message, True])
    
    # Crear version en core/documentation.py
    # Crear variables urls de version
    path = "core/documentation.py"
    find = "# DOC STRING VERSIONS (Managed by SPRINGLABS_DJANGO)"
    content = f"""
# VERSION {version}.0
# PUBLIC
title_v{version}_0 = "{project_name} v{version}.0"
description_v{version}_0 = "Descripción del proyecto (v{version})"
namespace_v{version}_0 = "api-docs-v{version}-0"
urls_v{version}_0 = "api.v{version}.urls"
# PRIVATE
title_v{version}_0_private = "{project_name} (Private) v{version}.0"
description_v{version}_0_private = "Descripción del proyecto (Private) (v{version})"
namespace_v{version}_0_private = "api-docs-v{version}-0-private"
urls_v{version}_0_private = "api.v{version}.urls"
# END VERSION {version}.0"""
    message, result = appendContent(path=path,
        content=content,
        find=find)
    
    if result == False:
        errors.append([message, True])
    
    # Crear version en graphql_api/urls.py
    # Agregar nueva version a url_patterns
    path = "graphql_api/urls.py"
    find = "# VERSIONS URLS (Managed by SPRINGLABS_DJANGO)"
    content = f"""
    url(r'^v{version}/', include('graphql_api.v{version}.urls', namespace='v{version}')),"""
    message, result = appendContent(path=path,
        content=content,
        find=find)
    if result == False:
        errors.append([message, True])
    

    for error in errors:
        if error[1] == True:
            return error[0], False
    
    return "OK", True

def createDirectoriesNewVersion(version, project_name, old_versions):
    """
        Función que modifica directorios para agregar nueva versión

        Función que modifica los directorios de Django y sus archivos dentro 
        en los que se tiene que agregar la nueva versión

    Args:
        version (String): Nueva versión del proyecto
        project_name (String): Nombre del proyecto
        old_versions (List): Lista de versiones existentes en proyecto
    Returns:
        message,result (Tuple): Mensaje[String] y result[Boolean]
    Exceptions:
        exception ([type]): [description]
    """

    errors = []
    
    # Crear carpeta API nueva versión con archivos
    os.chdir("api")
    new_version = f"v{version}"
    os.mkdir(new_version)
    base_urls_py = "/core/new_version/api/baseUrls.py"
    base_public_urls_py = "/core/new_version/api/basePublicUrls.py"
    base_private_urls_py = "/core/new_version/api/basePrivateUrls.py"
    base_serializers_py = "/core/new_version/api/baseSerializers.py"
    base_views_py = "/core/new_version/api/baseViews.py"

    # Obtiene contenido de core/new_version/api/baseUrls.py
    try:
        template_urls_py = pkgutil.get_data(PROJECT_PACKAGE, base_urls_py).decode('utf-8')
        template_urls_py = template_urls_py.replace("name_version", new_version)
    except:
        message = f"An internal error occurred in core/{new_version}/api/baseUrls.py"
        errors.append([message, True])

    # Obtiene contenido de core/new_version/api/basePublicUrls.py
    try:
        template_public_urls_py = pkgutil.get_data(PROJECT_PACKAGE, base_public_urls_py).decode('utf-8')
        template_public_urls_py = template_public_urls_py.replace("name_version", new_version)
    except:
        message = f"An internal error occurred in core/{new_version}/api/basePublicUrls.py"
        errors.append([message, True])

    # Obtiene contenido de core/new_version/api/basePrivateUrls.py
    try:
        template_private_urls_py = pkgutil.get_data(PROJECT_PACKAGE, base_private_urls_py).decode('utf-8')
        template_private_urls_py = template_private_urls_py.replace("name_version", new_version)
    except:
        message = f"An internal error occurred in core/{new_version}/api/basePrivateUrls.py"
        errors.append([message, True])

    # Obtiene contenido de core/new_version/api/baseSerializers.py
    try:
        template_serializers_py = pkgutil.get_data(PROJECT_PACKAGE, base_serializers_py).decode('utf-8')
    except:
        message = f"An internal error occurred in core/{new_version}/api/baseSerializers.py"
        errors.append([message, True])

    # Obtiene contenido de core/new_version/api/baseViews.py
    try:
        template_views_py = pkgutil.get_data(PROJECT_PACKAGE, base_views_py).decode('utf-8')
    except:
        message = f"An internal error occurred in core/{new_version}/api/baseViews.py"
        errors.append([message, True])

    # Escribe contenido base en archivo api/new_version/urls.py
    with open(f"{new_version}/urls.py", "w") as file:
        file. write(template_urls_py)
    
    # Escribe contenido base en archivo api/new_version/public_urls.py
    with open(f"{new_version}/public_urls.py", "w") as file:
        file. write(template_public_urls_py)
    
    # Escribe contenido base en archivo api/new_version/private_urls.py
    with open(f"{new_version}/private_urls.py", "w") as file:
        file. write(template_private_urls_py)
    os.mkdir(f"{new_version}/users")
    
    # Escribe contenido base en archivo api/new_version/users/serializers.py
    with open(f"{new_version}/users/serializers.py", "w") as file:
        file. write(template_serializers_py)
    
    # Escribe contenido base en archivo api/new_version/users/views.py
    with open(f"{new_version}/users/views.py", "w") as file:
        file. write(template_views_py)
    os.chdir("..")
    
    # Crear carpeta GRAPHQL_API nueva versión con archivos
    os.chdir("graphql_api")
    new_version = f"v{version}"
    os.mkdir(new_version)
    base_urls_py = "/core/new_version/graphql_api/baseUrls.py"
    base_api_py = "/core/new_version/graphql_api/baseApi.py"
    base_schema_py = "/core/new_version/graphql_api/baseSchema.py"
    base_types_py = "/core/new_version/graphql_api/baseTypes.py"

    # Obtiene contenido de core/new_version/graphql_api/baseUrls.py
    try:
        template_urls_py = pkgutil.get_data(PROJECT_PACKAGE, base_urls_py).decode('utf-8')
        template_urls_py = template_urls_py.replace("name_version", new_version)
    except:
        message = f"An internal error occurred in core/{new_version}/graphql_api/baseUrls.py"
        errors.append([message, True])

    # Obtiene contenido de core/new_version/graphql_api/baseApi.py
    try:
        template_api_py = pkgutil.get_data(PROJECT_PACKAGE, base_api_py).decode('utf-8')
    except:
        message = f"An internal error occurred in core/{new_version}/graphql_api/baseApi.py"
        errors.append([message, True])


    # Obtiene contenido de core/new_version/graphql_api/baseSchema.py
    try:
        template_schema_py = pkgutil.get_data(PROJECT_PACKAGE, base_schema_py).decode('utf-8')
    except:
        message = f"An internal error occurred in core/{new_version}/graphql_api/baseSchema.py"
        errors.append([message, True])

    # Obtiene contenido de core/new_version/graphql_api/baseTypes.py
    try:
        template_types_py = pkgutil.get_data(PROJECT_PACKAGE, base_types_py).decode('utf-8')
    except:
        message = f"An internal error occurred in core/{new_version}/graphql_api/baseTypes.py"
        errors.append([message, True])

    # Escribe contenido base en archivo graphql_api/new_version/urls.py
    with open(f"{new_version}/urls.py", "w") as file:
        file. write(template_urls_py)
    
    # Escribe contenido base en archivo graphql_api/new_version/api.py
    with open(f"{new_version}/api.py", "w") as file:
        file. write(template_api_py)
    os.mkdir(f"{new_version}/users")
    
    # Escribe contenido base en archivo graphql_api/new_version/users/schema.py
    with open(f"{new_version}/users/schema.py", "w") as file:
        file. write(template_schema_py)
    
    # Escribe contenido base en archivo graphql_api/new_version/users/types.py
    with open(f"{new_version}/users/types.py", "w") as file:
        file. write(template_types_py)
    os.chdir("..")

    # Crear carpeta TESTS nueva versión con archivos
    os.chdir("tests")
    new_version = f"v{version}"
    os.mkdir(new_version)
    os.mkdir(f"{new_version}/integration_tests")
    os.mkdir(f"{new_version}/integration_tests/utils")
    os.mkdir(f"{new_version}/unit_tests")


    base_test_apis_py = "/core/new_version/tests/baseTestApis.py"
    base_test_functions1_py = "/core/new_version/tests/baseTestFunctions1.py"
    base_test_serializers_py = "/core/new_version/tests/baseTestSerializers.py"
    base_test_functions_py = "/core/new_version/tests/baseTestFunctions.py"

    # Obtiene contenido de core/new_version/tests/baseTestApis.py
    try:
        template_test_apis_py = pkgutil.get_data(PROJECT_PACKAGE, base_test_apis_py).decode('utf-8')
    except:
        message = f"An internal error occurred in core/{new_version}/tests/baseTestApis.py"
        errors.append([message, True])
    
    # Obtiene contenido de core/new_version/tests/baseTestFunctions1.py
    try:
        template_test_functions1_py = pkgutil.get_data(PROJECT_PACKAGE, base_test_functions1_py).decode('utf-8')
    except:
        message = f"An internal error occurred in core/{new_version}/tests/baseTestFunctions1.py"
        errors.append([message, True])
    
    # Obtiene contenido de core/new_version/tests/baseTestSerializers.py
    try:
        template_test_serializers_py = pkgutil.get_data(PROJECT_PACKAGE, base_test_serializers_py).decode('utf-8')
    except:
        message = f"An internal error occurred in core/{new_version}/tests/baseTestSerializers.py"
        errors.append([message, True])
    
    # Obtiene contenido de core/new_version/tests/baseTestFunctions.py
    try:
        template_test_functions_py = pkgutil.get_data(PROJECT_PACKAGE, base_test_functions_py).decode('utf-8')
    except:
        message = f"An internal error occurred in core/{new_version}/tests/baseTestFunctions.py"
        errors.append([message, True])
    

    # Escribe contenido base en archivo tests/new_version/integration_tests/test_apis.py
    with open(f"{new_version}/integration_tests/test_apis.py", "w") as file:
        file. write(template_test_apis_py)
    
    # Escribe contenido base en archivo tests/new_version/integration_tests/test_functions1.py
    with open(f"{new_version}/integration_tests/test_functions1.py", "w") as file:
        file. write(template_test_functions1_py)
    
    # Escribe contenido base en archivo tests/new_version/integration_tests/test_serializers.py
    with open(f"{new_version}/integration_tests/test_serializers.py", "w") as file:
        file. write(template_test_serializers_py)
    
    # Escribe contenido base en archivo tests/new_version/unit_tests/test_functions.py
    with open(f"{new_version}/unit_tests/test_functions.py", "w") as file:
        file. write(template_test_functions_py)
    os.chdir("..")
    
    for error in errors:
        if error[1] == True:
            return error[0], False
    
    return "OK", True

def modifyFilesNewAPI(version,group,name,http_verb,type_api,url,availability,project_name):
    """
        Función encargada de modificar archivos para nueva api en django

        Función encargada de modificar los archivos necesarios para crear una nueva api
        en el proyecto django.

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
    errors = []
    
    # Obtener variables dependientes del HTTP_VERB
    if http_verb == "POST":
        base_views = "post_views_"
        base_serializers = "post_serializers_"
    elif http_verb == "PUT":
        base_views = "put_views_"
        base_serializers = "put_serializers_"
    elif http_verb == "DELETE":
        base_views = "delete_views_"
        base_serializers = "delete_serializers_"
    
    # Obtener variables dependientes del TYPE_API
    if type_api=="open":
        base_views = base_views+"open.py"
        base_serializers = base_serializers+"open.py"
    elif type_api=="model":
        base_views = base_views+"model.py"
        base_serializers = base_serializers+"model.py"
    
    # Obtener variables dependientes del AVAILABILITY
    if availability=="public":
        general_urls = "public_urls.py"
    elif availability=="private":
        general_urls = "private_urls.py"
    
    base_views_py = f"/core/new_api/api/{base_views}"
    base_serializers_py = f"/core/new_api/api/{base_serializers}"
    # Obtiene contenido de /core/new_api/api/{base_views}
    try:
        template_views_py = pkgutil.get_data(PROJECT_PACKAGE, base_views_py).decode('utf-8')
        template_views_py = template_views_py.replace("API_NAME", name.capitalize())
    except:
        message = f"An internal error occurred in /core/new_api/api/{base_views}"
        errors.append([message, True])
    
    # Obtiene contenido de /core/new_api/api/{base_serializers}
    try:
        template_serializers_py = pkgutil.get_data(PROJECT_PACKAGE, base_serializers_py).decode('utf-8')
        template_serializers_py = template_serializers_py.replace("API_NAME", name.capitalize())
    except:
        message = f"An internal error occurred in /core/new_api/api/{base_serializers}"
        errors.append([message, True])
    
    # Escribe en archivo views.py
    path = f"api/v{version}/{group}/views.py"
    message, result = appendContent(path=path,
        content=template_views_py)
    if result == False:
        errors.append([message, True])

    # Escribe en archivo serializers.py
    path = f"api/v{version}/{group}/serializers.py"
    message, result = appendContent(path=path,
        content=template_serializers_py)
    if result == False:
        errors.append([message, True])

    # Escribe en urls public/private
    views_name = f"{name.capitalize()}{http_verb.capitalize()}"
    path = f"api/v{version}/{general_urls}"
    find = f"# {group.upper()} URLS (Managed by SPRINGLABS_DJANGO)"
    content = f"    url(r'^{url}/$', {group.lower()}_views.{views_name}),"
    message, result = appendContent(path=path,
        content=content,
        find=find)
    if result == False:
        errors.append([message, True])

    for error in errors:
        if error[1] == True:
            return error[0], False

    return "OK", True

def modifyFilesNewGraph(version,group,name,type_graph,project_name):
    """
        Función encargada de modificar archivos para nuevo graph en django

        Función encargada de modificar los archivos necesarios para crear un nuev graph
        en el proyecto django.

        Parámetros:
            version         [String]    Versión donde se creará el Graph
            group           [String]    Grupo donde se creará el Graph
            name            [String]    Nombre del Graph
            type_graph      [String]    Tipo del Graph (MODEL, OPEN)
            project_name    [String]    Nombre del proyecto
        Retorno:
            message,result  [Tuple]     Mensaje[String] y result[Boolean]
    """
    errors = []
    

    graph_version = version
    group_graph = group
    try:
        with open(CONFIG_JSON) as file:
            data = json.load(file)
    except:
        message = f"An internal error occurred while reading file ({CONFIG_JSON})"
        return message, False
    else:
        versions_detail = data['versions_detail']
        old_graphs = []
        old_graphs_version = []
        index_version_modify = 0
        # Recorremos todas las versiones
        for index, versions in enumerate(versions_detail):
            # Si la versión del ciclo es en donde vamos a insertar el graph
            if versions['version'] == graph_version:
                groups_detail = versions["groups_detail"]
                index_version_modify = index
                old_graphs_version = list(versions['graph_list'])
                # Recorremos todos los grupos de esa versión
                for group_detail in groups_detail:
                    # Si el grupo del ciclo es en donde vamos a insertar el graph
                    if group_graph == group_detail['group']:
                        graphs = group_detail['graph']
                        # Recorremos todas las apis de ese grupo
                        for graph in graphs:
                            old_name = graph["graph_name"]
                            # Agregamos a lista de old_graphs los nombres de los graphs existentes
                            old_graphs.append(old_name)
    
    example_django_name = f"ExampleDjango{group.capitalize()}"
    # Si se encuentra ExampleDjango en los graphs existentes
    if example_django_name in old_graphs:
        delete_example = True 
    else:
        delete_example = False
    # Obtener variables dependientes del TYPE_GRAPH
    base_schema = "schema.py"
    if type_graph=="open":
        base_types = "types_open.py"
    elif type_graph=="model":
        base_types = "types_model.py"
    
    base_schema_py = f"/core/new_graph/graph/{base_schema}"
    base_types_py = f"/core/new_graph/graph/{base_types}"

    # Obtiene contenido de /core/new_graph/graph/{base_schema}
    try:
        template_schema_py = pkgutil.get_data(PROJECT_PACKAGE, base_schema_py).decode('utf-8')
        template_schema_py = template_schema_py.replace("GRAPH_NAME", name.capitalize())
    except:
        message = f"An internal error occurred in /core/new_graph/graph/{base_schema}"
        errors.append([message, True])
    
    # Obtiene contenido de /core/new_graph/graph/{base_types}
    try:
        template_types_py = pkgutil.get_data(PROJECT_PACKAGE, base_types_py).decode('utf-8')
        template_types_py = template_types_py.replace("GRAPH_NAME", name.capitalize())
    except:
        message = f"An internal error occurred in /core/new_graph/graph/{base_types}"
        errors.append([message, True])
    
    # Obtiene texto a buscar de import en schema.py y api.py
    find_import_schema = "from .types import"
    find_import_api = f"from .{group}.schema import"
    find_query_api = f"class Query("
    # Arma FIND de class Query api.py
    for index, old_graph in enumerate(old_graphs_version):
        old_graph_name = old_graph
        if index == 0:
            find_query_api = find_query_api+f"{old_graph_name}"
        else:
            find_query_api = find_query_api+f", {old_graph_name}"
    base_new_query_api = str(find_query_api)
    find_query_api = find_query_api + ", graphene.ObjectType):"
    # Arma find de import schema.py e import api.py 
    for index, old_graph in enumerate(old_graphs):
        if old_graph != example_django_name:
            old_graph_name = old_graph.capitalize()
        else:
            old_graph_name = old_graph
        if index == 0:
            
            find_import_schema = find_import_schema+f" {old_graph_name}Type"
            find_import_api = find_import_api+f" {old_graph_name}Queries"
        else:
            find_import_schema = find_import_schema+f", {old_graph_name}Type"
            find_import_api = find_import_api+f", {old_graph_name}Queries"
    
    # Elimina ExampleDjango de archivo schema.py y types.py
    if delete_example==True:
        # Elimina ExampleDjango de archivo schema.py
        path = f"graphql_api/v{version}/{group}/schema.py"
        message, result = deleteContent(path=path,
            start="# EXAMPLE QUERY GRAPHENE (Managed by SPRINGLABS_DJANGO)",
            end="# END EXAMPLE QUERY GRAPHENE (Managed by SPRINGLABS_DJANGO)")
        if result == False:
            errors.append([message, True])
        
        message, result = findNDelete(path=path,
            find="# EXAMPLE QUERY GRAPHENE (Managed by SPRINGLABS_DJANGO)")
        if result == False:
            errors.append([message, True])
        
        message, result = findNDelete(path=path,
            find="# END EXAMPLE QUERY GRAPHENE (Managed by SPRINGLABS_DJANGO)")
        if result == False:
            errors.append([message, True])
        
        # Elimina ExampleDjango de archivo types.py
        path = f"graphql_api/v{version}/{group}/types.py"
        message, result = deleteContent(path=path,
            start="# EXAMPLE GRAPHENE ObjectType (Managed by SPRINGLABS_DJANGO)",
            end="# END EXAMPLE GRAPHENE ObjectType (Managed by SPRINGLABS_DJANGO)")
        if result == False:
            errors.append([message, True])
        # Eliminar bandera START de ExampleDjango
        message, result = findNDelete(path=path,
            find="# EXAMPLE GRAPHENE ObjectType (Managed by SPRINGLABS_DJANGO)")
        if result == False:
            errors.append([message, True])
        # Eliminar bandera END de ExampleDjango
        message, result = findNDelete(path=path,
            find="# END EXAMPLE GRAPHENE ObjectType (Managed by SPRINGLABS_DJANGO)")
        if result == False:
            errors.append([message, True])
        
        new_import_schema = f"from .types import {name.capitalize()}Type"
        new_import_api = f"from .{group}.schema import {name.capitalize()}Queries"
        new_query_api = "class Query("

        counter = 0
        index_replace_example = 0
        for index, old_graph in enumerate(old_graphs_version):
            if old_graph != f"{example_django_name}Queries":
                if index == 0:
                    new_query_api = new_query_api+f"{old_graph}"
                else:
                    new_query_api = new_query_api+f", {old_graph}"
            elif old_graph == f"{example_django_name}Queries" and counter != 0:
                if index == 0:
                    new_query_api = new_query_api+f"{old_graph}"
                else:
                    new_query_api = new_query_api+f", {old_graph}"
            else:
                if index == 0:
                    new_query_api = new_query_api+f"{name.capitalize()}Queries"
                else:
                    new_query_api = new_query_api+f", {name.capitalize()}Queries"
                index_replace_example = index
                counter = counter+1
        for index, old_graph in enumerate(old_graphs):
            if old_graph != example_django_name:
                if index == 0:
                    new_import_schema = new_import_schema+f" {old_graph.capitalize()}Type"
                    new_import_api = new_import_api+f" {old_graph.capitalize()}Queries"
                else:
                    new_import_schema = new_import_schema+f", {old_graph}Type"
                    new_import_api = new_import_api+f", {old_graph.capitalize()}Queries"
        index_graph_example_django = False
        try:
            with open(CONFIG_JSON) as file:
                data = json.load(file)
        except:
            message = f"An internal error occurred while updating file {CONFIG_JSON}"
            errors.append([message, True])
        else:
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
                            graphs_json = group_detail['graph']
                            # Recorremos los graphs en la aplicación y grupo especificados
                            for index_graph, graph_json in enumerate(graphs_json):
                                if graph_json['graph_name'] == example_django_name:
                                    index_graph_example_django = [index_versions,index_groups,index_graph]
            # Si existió graphQL en la lista de graphs de la versión y grupo
            if index_graph_example_django != False:
                # Elimina el graph de Example Django
                index_version = index_graph_example_django[0]
                index_groups = index_graph_example_django[1]
                index_graph = index_graph_example_django[2]
                data['versions_detail'][index_version]['graph_list'][index_replace_example] = f"{name.capitalize()}Queries"
                data['versions_detail'][index_version]['groups_detail'][index_groups]['graph'].pop(index_graph)
            try:
                with open(CONFIG_JSON, "w") as file:
                    file.write(json.dumps(data))
            except:
                message = f"An internal error occurred while updating file {CONFIG_JSON}"
                errors.append([message, True])
    else:
        new_import_schema = find_import_schema + f", {name.capitalize()}Type"
        new_import_api = find_import_api + f", {name.capitalize()}Queries"
        new_query_api = base_new_query_api + f", {name.capitalize()}Queries"
        # Modifica graph_list
        try:
            with open(CONFIG_JSON) as file:
                data = json.load(file)
        except:
            message = f"An internal error occurred while updating file {CONFIG_JSON}"
            errors.append([message, True])
        else:
            data['versions_detail'][index_version_modify]['graph_list'].append(f"{name.capitalize()}Queries")
            try:
                with open(CONFIG_JSON, "w") as file:
                    file.write(json.dumps(data))
            except:
                message = f"An internal error occurred while updating file {CONFIG_JSON}"
                errors.append([message, True])
        
        
    new_query_api = new_query_api + ", graphene.ObjectType):"
    # Escribe nuevo graph en archivo schema.py
    path = f"graphql_api/v{version}/{group}/schema.py"
    message, result = appendContent(path=path,
        content=template_schema_py)
    if result == False:
        errors.append([message, True])
    
    # Modifica imports en schema.py
    message, result = findNReplace(path=path,
        content=new_import_schema,
        find=find_import_schema)
    if result == False:
        errors.append([message, True])

    # Escribe en archivo types.py
    path = f"graphql_api/v{version}/{group}/types.py"
    message, result = appendContent(path=path,
        content=template_types_py)
    if result == False:
        errors.append([message, True])

    # Escribe en archivo api.py
    path = f"graphql_api/v{version}/api.py"
    message, result = findNReplace(path=path,
        content=new_import_api,
        find=find_import_api)
    if result == False:
        errors.append([message, True])
    
    message, result = findNReplace(path=path,
        content=new_query_api,
        find=find_query_api)
    if result == False:
        errors.append([message, True])

    for error in errors:
        if error[1] == True:
            return error[0], False
    return "OK", True

def modifyFilesNewGroup(version, group,project_name):
    """
        Función encargada de modificar archivos para un nuevo grupo en django

        Función encargada de modificar los archivos necesarios para crear un nuevo grupo
        en el proyecto django.

        Parámetros:
            version         [String]    Versión donde se creará el grupo
            group           [String]    Nombre del grupo
            
        Retorno:
            message,result  [Tuple]     Mensaje[String] y result[Boolean]
        Exceptions:
            OSError                     Error al abrir o escribir archivos

    """
    errors = []
    # Crear version en project_name/urls.py
    # Importar public versions de nueva versión
    groupcap=group.capitalize()
    publicpath = f"api/v{version}/public_urls.py"
    privatepath = f"api/v{version}/private_urls.py"
    find = f"# v{version} PATTERNS (Managed by SPRINGLABS_DJANGO)"
    uppergroup=group.upper()
    content = f"""
# START {uppergroup} URLS v{version} (Managed by SPRINGLABS_DJANGO)
{group}_patterns = [
    # {uppergroup} URLS (Managed by SPRINGLABS_DJANGO)
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
# END {uppergroup} URLS v{version} (Managed by SPRINGLABS_DJANGO)

"""
    message, result = appendContent(path=publicpath,
        content=content,
        find=find)
    if result == False:
        errors.append([message, True])

    message, result = appendContent(path=privatepath,
        content=content,
        find=find)
    if result == False:
        errors.append([message, True])

    find="# PATTERNS URLS (Managed by SPRINGLABS_DJANGO)"
    content=f"    url(r'^', include({group}_patterns)),"
    message, result = appendContent(path=privatepath,
        content=content,
        find=find)
    if result == False:
        errors.append([message, True])

    message, result = appendContent(path=publicpath,
        content=content,
        find=find)
    if result == False:
        errors.append([message, True])

    
    find="# Our custom libraries (Managed by SPRINGLABS_DJANGO)"
    content=f"from .{group} import views as {group}_views"
    message, result = appendContent(path=privatepath,
        content=content,
        find=find)
    if result == False:
        errors.append([message, True])

    message, result = appendContent(path=publicpath,
        content=content,
        find=find)
    if result == False:
        errors.append([message, True])

    content=f"from .{group}.schema import ExampleDjango{groupcap}Queries"
    path=f"graphql_api/v{version}/api.py"
    message, result = appendContent(path=path,
        content=content,
        find=find)
    if result == False:
        errors.append([message, True])

    try:
        with open(CONFIG_JSON) as file:
            data = json.load(file)
    except:
        message = F"An internal error occurred while reading file ({CONFIG_JSON})"
        return message, False

    versions_detail=data["versions_detail"]
    version_data=None
    for obj in versions_detail:
        if obj["version"]==version:
            if "graph_list" in obj:
                version_data=obj["graph_list"]
            else:
                version_data=[]

    if version_data!=None:
        content="class Query("
        for obj in version_data:
            content=content+obj+", "
        find=content+"graphene.ObjectType):"

        content=content+f"ExampleDjango{groupcap}Queries, graphene.ObjectType):"
        message, result=findNReplace(path, content, find)
        if result == False:
            errors.append([message, True])

    else:
        message = F"An internal error occurred while reading file ({CONFIG_JSON})"
        return message, False

    for error in errors:
        if error[1] == True:
            return error[0], False
    
    return "OK", True

def createDirectoriesNewGroup(version, group, project_name):
    """
        Función que modifica directorios para agregar nuevo grupo

        Función que modifica los directorios de Django y sus archivos dentro 
        en los que se tiene que agregar el nuevo grupo

        Parámetros:
                version         [String]    Versión donde se creará el grupo
                group           [String]    Nombre del grupo
                project_name    [String]    Nombre del proyecto
                
        Retorno:
                message,result  [Tuple]     Mensaje[String] y result[Boolean]
        Exceptions:
                OSError                     Error al abrir o escribir archivos
    """
    errors = []
    os.chdir(f"api/v{version}")
    os.mkdir(group)

    base_serializers_py = "/core/new_version/api/baseSerializers.py"
    base_views_py = "/core/new_version/api/baseViews.py"
    
    # Obtiene contenido de core/new_version/api/baseSerializers.py
    try:
        template_serializers_py = pkgutil.get_data(PROJECT_PACKAGE, base_serializers_py).decode('utf-8')
    except:
        message = f"An internal error occurred in core/new_version/api/baseSerializers.py"
        errors.append([message, True])

    # Obtiene contenido de core/new_version/api/baseViews.py
    try:
        template_views_py = pkgutil.get_data(PROJECT_PACKAGE, base_views_py).decode('utf-8')
    except:
        message = f"An internal error occurred in core/new_version/api/baseViews.py"
        errors.append([message, True])

    # Escribe contenido base en archivo api/new_version/users/serializers.py
    with open(f"{group}/serializers.py", "w") as file:
        file. write(template_serializers_py)
    
    # Escribe contenido base en archivo api/new_version/users/views.py
    with open(f"{group}/views.py", "w") as file:
        file. write(template_views_py)
    os.chdir("../..")

    os.chdir(f"graphql_api/v{version}")
    os.mkdir(group)
    base_schema_py = "/core/new_group/graph/initial_schema.py"
    base_types_py = "/core/new_group/graph/initial_type.py"
    groupcap=group.capitalize()
    changename=f"ExampleDjango{groupcap}"

    # Obtiene contenido de core/new_version/graphql_api/baseSchema.py
    try:
        template_schema_py = pkgutil.get_data(PROJECT_PACKAGE, base_schema_py).decode('utf-8')
        template_schema_py = template_schema_py.replace("GRAPH_NAME", changename)
    except:
        message = f"An internal error occurred in core/new_version/graphql_api/baseSchema.py"
        errors.append([message, True])

    # Obtiene contenido de core/new_version/graphql_api/baseTypes.py
    try:
        template_types_py = pkgutil.get_data(PROJECT_PACKAGE, base_types_py).decode('utf-8')
        template_types_py = template_types_py.replace("GRAPH_NAME", changename)
    except:
        message = f"An internal error occurred in core/new_version/graphql_api/baseTypes.py"
        errors.append([message, True])

     # Escribe contenido base en archivo graphql_api/new_version/users/schema.py
    with open(f"{group}/schema.py", "w") as file:
        file. write(template_schema_py)
    
    # Escribe contenido base en archivo graphql_api/new_version/users/types.py
    with open(f"{group}/types.py", "w") as file:
        file. write(template_types_py)
    os.chdir("../..")
    for error in errors:
        if error[1] == True:
            return error[0], False

    return "OK", True