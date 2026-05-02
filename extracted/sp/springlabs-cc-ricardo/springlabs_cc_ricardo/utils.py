import os
import re
import requests
from zipfile import ZipFile
import shutil
import random
import string


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
        return f'El archivo no existe', False
    if find == None:
        try:
            """ if not os.path.exists(path):
                    open(path, "x")
            with open(f'{path}.bak', "w") as f:
                    f.write(open(path).read()) """
            with open(path, "a") as f:
                newContent = f'\n{content}'
                f.write(newContent)
            return f'Se actualizó correctamente el archivo: {path}', True
        except Exception as exc:
            return f'Error al escribir el contenido:{exc}', False
    else:
        if recursive == False:
            return notRecursiveModify(path, content, find, 'append')
        elif recursive == True:
            return recursiveModify(path, content, find, 'append')

        return f'Valor no válido para el parametro recursive', False


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
        return f'El archivo no existe', False

    starts = getRangeStr(path, start)
    ends = getRangeEnds(path, end)
    if ends == None or len(ends) == 0:
        return f'Tu archivo no cuenta con delimitadores de fin: "{end}"', False
    if starts == None or len(starts) == 0:
        return f'Tu archivo no cuenta con delimitadores de inicio: "{start}"', False
    textsReplace = []
    for idx, _ in enumerate(ends):
        if len(starts) <= idx or starts[idx][1] > ends[idx][0]:
            break
        textsReplace.append([starts[idx][1] + 1,  ends[idx][0] - 1])
    file = open(path).read()
    # print(textsReplace)
    # print(file[textsReplace[0][0]:textsReplace[0][1]])
    if len(textsReplace) == 0:
        return f'Tu archivo tiene mal los delimitadores de inicio "{start}" y/o los deliminatores de fin "{end}" , favor de verificar.', False
    if recursive == False:
        return notRecursiveModify(path, content, file[textsReplace[0][0]:textsReplace[0][1]], 'replace')
    elif recursive == True:
        try:
            for text in textsReplace:
                recursiveModify(
                    path, content, file[text[0]:text[1]], 'replace')
            return f'Se actualizó correctamente el archivo: {path}', True
        except Exception as exc:
            return f'Error al escribir el contenido: {exc}', False

    return f'Valor no válido para el parametro recursive', False


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
        return f'El archivo no existe', False
    if recursive == False:
        return notRecursiveModify(path, content, find, 'replace')
    elif recursive == True:
        return recursiveModify(path, content, find, 'replace')

    return f'Valor no válido para el parametro recursive', False


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
        return f'El archivo no existe', False
    if recursive == False:
        return findNReplace(path, '', find)
    elif recursive == True:
        return findNReplace(path, '', find, recursive=True)

    return f'Valor no válido para el parametro recursive', False


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
        return f'El archivo no existe', False
    if recursive == False:
        return replaceContent(path, '', start, end)
    elif recursive == True:
        return replaceContent(path, '', start, end, recursive=True)

    return f'Valor no válido para el parametro recursive', False


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
    diagonal = chr(92)
    find = find.replace("(", '\(')
    find = find.replace(")", '\)')
    find = find.replace("{", '\{')
    find = find.replace("}", '\}')
    find = find.replace("[", '\[')
    find = find.replace("]", '\]')
    find = find.replace("+", '\+')
    find = find.replace("<", '\<')
    find = find.replace("-", '\-')
    find = find.replace("!", '\!')
    find = find.replace("*", '\*')
    find = find.replace("~", '\~')
    find = find.replace("¬", '\¬')
    find = find.replace(",", '\,')
    find = find.replace(":", '\:')
    find = find.replace(".", '\.')

    matches = re.finditer(find, file)
    for m in matches:
        matchFound = True
        break
    if matchFound == False:
        return f'No se encontraron coincidencias de "{find}"', False
    if type == 'append':
        newContent = f'{file[: m.end()]}  \n{content} \n{file[m.end() + 1:]}'
    elif type == 'replace':
        newContent = f'{file[: m.start()]}{content}{file[m.end():]}'
    else:
        return f'Tipo de remplazo no válido', False
    try:
        '''with open(f'{path}.bak', "w") as f:
                f.write(open(path).read())'''
        with open(path, "w") as f:
            f.write(newContent)
        return f'Se actualizó correctamente el archivo: {path}', True
    except Exception as exc:
        return f'Error al escribir el contenido: {exc}', False


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
        return f'Tipo de remplazo no válido', False
    try:
        file = open(path).read()
        '''with open(f'{path}.bak', "w") as f:
			f.write(open(path).read())'''
        with open(path, "w") as f:
            f.write(file.replace(find, newContent))
        return f'Se actualizó correctamente el archivo: {path}', True
    except Exception as exc:
        return f'Error al escribir el contenido: {exc}', False


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
    find = find.replace("(", '\(')
    find = find.replace(")", '\)')
    find = find.replace("{", '\{')
    find = find.replace("}", '\}')
    find = find.replace("[", '\[')
    find = find.replace("]", '\]')
    find = find.replace("+", '\+')
    find = find.replace("<", '\<')
    find = find.replace("-", '\-')
    find = find.replace("!", '\!')
    find = find.replace("*", '\*')
    find = find.replace("~", '\~')
    find = find.replace("¬", '\¬')
    find = find.replace(",", '\,')
    find = find.replace(":", '\:')
    find = find.replace(".", '\.')

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
        for num, line in enumerate(file):
            if find in line:
                return getRangeStr(path, line)


def downloadNUnzip(url):
    """
        Función que dada una url descarga un zip y lo descomprime

        Función que descarga un zip de una url, lo guarda en la carpeta actual
        y lo descomprime

        Parámetros:
            url             [String]    URL de zip descargable
        Retorno:
            message,result  [Tuple]     Mensaje[String] y result[Boolean]
    """
    target_path = 'name.zip'
    response = requests.get(url, stream=True)
    handle = open(target_path, "wb")
    for chunk in response.iter_content(chunk_size=512):
        if chunk:  # filter out keep-alive new chunks
            handle.write(chunk)
    handle.close()
    # Create a ZipFile Object and load sample.zip in it
    with ZipFile(target_path, 'r') as zipObj:
        # Extract all the contents of zip file in current directory
        zipObj.extractall()
    os.remove(target_path)
    return "OK", True


def cloneTemplate(url, name):
    """
        Función encargada de clonar proyecto template

        Función que clona proyecto template de gitlab, con credenciales de
        usuario ProgramacionSpringlabs y elimina registro de repositorio
        template.

        Parámetros:
            url             [String]    URL de repositorio git
            name            [String]    Nombre del proyecto en repositorio y clone
        Retorno:
            message,result  [Tuple]     Mensaje[String] y result[Boolean]
    """
    username = "ProgramacionSpringlabs"
    token = "rysMXSPyMbmTtG3W3Afq"
    url = url.replace("//", f"//{username}:{token}@")
    clone = f"git clone --quiet {url}"
    os.system(clone)
    shutil.rmtree(os.getcwd() + f"/{name}/.git")
    try:
        os.remove(os.getcwd() + f"/{name}/.gitignore")
    except:
        pass
    return "OK", True


def createDjango(name, database, url, name_git, path=os.getcwd()):
    """
        Función encargada de crear projecto django

        Función que descarga proyecto template de django-logic o django-physic
        y realiza las modificaciones necesarias para nuevo proyecto

        Parámetros:
            name            [String]    Nombre del proyecto nuevo
            database        [String]    Motor de base de datos a utilizar
            path            [String]    Directorio del proyecto
            url             [String]    Url de repositorio gitlab
            name_git        [String]    Nombre de proyecto en repositorio git
        Retorno:
            message,result  [Tuple]     Mensaje[String] y result[Boolean]
    """
    message, result = cloneTemplate(url=url, name=name_git)
    if result == True:
        errors = []
        error_flag = False
        # Cambiar nombre de la carpeta principal name_git to name
        try:
            os.rename(f"{path}/{name_git}", name)
            os.chdir(path + "/" + name)
            project_path = os.getcwd()
        except:
            message = "Error en cambiar nombre de carpeta original por nombre"
            errors.append([message, True])

        # Nombre de la carpeta settings --project_name-- to name
        try:
            os.rename(f"{project_path}/--project_name--", name)
        except:
            message = "Error en cambiar nombre de carpeta de proyecto por nombre"
            errors.append([message, True])
        # Modify SETTINGS.PY
        # Modify SECRET_KEY PROJECT
        chars = ''.join([string.ascii_letters, string.digits, string.punctuation]).replace(
            '\'', '').replace('"', '').replace('\\', '')
        hash = ''.join([random.SystemRandom().choice(chars)
                        for i in range(50)])
        message, result = findNReplace(path=f"{project_path}/{name}/settings.py",
                                       content=hash,
                                       find="SECRET_KEY_PROJECT",
                                       recursive=False)
        if result == False:
            errors.append([message, True])
        # Modify name in /name/settings.py
        message, result = findNReplace(path=f"{project_path}/{name}/settings.py",
                                       content=name,
                                       find="--project_name--",
                                       recursive=True)
        if result == False:
            errors.append([message, True])

        # Modify database in /name/settings.py
        if database == "postgres":
            database_engine = "django.db.backends.postgresql_psycopg2"
        elif database == "mysql":
            database_engine = "django.db.backends.mysql"
        message, result = findNReplace(path=f"{project_path}/{name}/settings.py",
                                       content=database_engine,
                                       find="DATABASE_ENGINE",
                                       recursive=False)
        if result == False:
            errors.append([message, True])

        # Modify name in /name/wsgi.py
        message, result = findNReplace(path=f"{project_path}/{name}/wsgi.py",
                                       content=name,
                                       find="--project_name--",
                                       recursive=True)
        if result == False:
            errors.append([message, True])
        # Modify name in /core/documentation.py
        message, result = findNReplace(path=f"{project_path}/core/documentation.py",
                                       content=name,
                                       find="--project_name--",
                                       recursive=True)
        if result == False:
            errors.append([message, True])

        # Modify name in manage.py
        message, result = findNReplace(path=f"{project_path}/manage.py",
                                       content=name,
                                       find="--project_name--",
                                       recursive=True)
        if result == False:
            errors.append([message, True])

        # Revisa si hay errores en la modificación de archivos y saca el mensaje correcto
        for error in errors:
            if error[1] == True:
                os.chdir("..")
                os.chdir("..")
                shutil.rmtree(os.getcwd() + "/" + name)
                return error[0], False

        return "OK", True
    else:
        return message, False


def createFlask(name, database, url, name_git, path=os.getcwd()):
    """
        Función encargada de crear projecto flask

        Función que descarga proyecto template de flask-logic o flask-physic
        y realiza las modificaciones necesarias para nuevo proyecto

        Parámetros:
            name            [String]    Nombre del proyecto nuevo
            database        [String]    Motor de base de datos a utilizar
            path            [String]    Directorio del proyecto
            url             [String]    Url de repositorio gitlab
            name_git        [String]    Nombre de proyecto en repositorio git
        Retorno:
            message,result  [Tuple]     Mensaje[String] y result[Boolean]
    """
    message, result = cloneTemplate(url=url, name=name_git)
    if result == True:
        errors = []
        error_flag = False
        # Cambiar nombre de la carpeta principal name_git to name
        try:
            os.rename(f"{path}/{name_git}", name)
            os.chdir(path + "/" + name)
            project_path = os.getcwd()
        except:
            message = "Error en cambiar nombre de carpeta original por nombre"
            errors.append([message, True])

        # Modify APPLICATION.PY
        # Modify SECRET_KEY PROJECT
        chars = ''.join([string.ascii_letters, string.digits, string.punctuation]).replace(
            '\'', '').replace('"', '').replace('\\', '')
        hash = ''.join([random.SystemRandom().choice(chars)
                        for i in range(50)])
        message, result = findNReplace(path=f"{project_path}/application.py",
                                       content=hash,
                                       find="SECRET_KEY_PROJECT",
                                       recursive=False)
        if result == False:
            errors.append([message, True])

        # Modify name in /apis/__init__.py
        message, result = findNReplace(path=f"{project_path}/apis/__init__.py",
                                       content=name,
                                       find="--project_name--",
                                       recursive=True)
        if result == False:
            errors.append([message, True])

        # Revisa si hay errores en la modificación de archivos y saca el mensaje correcto
        for error in errors:
            if error[1] == True:
                os.chdir("..")
                os.chdir("..")
                shutil.rmtree(os.getcwd() + "/" + name)
                return error[0], False

        return "OK", True
    else:
        return message, False


def createDjangoProject(name, database, design):
    """
        Función encargada de crear projecto django

        Función que descarga proyecto template de [design=[logico|fisico]]
        y realiza las modificaciones necesarias para nuevo proyecto

        Parámetros:
            name            [String]    Nombre del proyecto nuevo
            database        [String]    Motor de base de datos a utilizar
            design          [String]    Diseño de base de datos a utilizar
            path            [String]    Directorio del proyecto
        Retorno:
            message,result  [Tuple]     Mensaje[String] y result[Boolean]
    """
    try:
        os.mkdir(name)
    except:
        return f"Ya existe una carpeta con el nombre '{name}' en el directorio actual", False
    else:
        os.chdir(os.getcwd() + "/" + name)
        if design == "logico":
            url = "https://gitlab.com/AlejandroBarcenas/template-django-logic.git"
            name_git = "template-django-logic"
        elif design == "fisico":
            url = "https://gitlab.com/AlejandroBarcenas/template-django-physic.git"
            name_git = "template-django-physic"
        message, result = createDjango(name=name,
                                       database=database,
                                       path=os.getcwd(),
                                       url=url,
                                       name_git=name_git)

        return message, result


def createFlaskProject(name, database, design):
    """
        Función encargada de crear projecto flask

        Función que descarga proyecto template de [design=[logico|fisico]]
        y realiza las modificaciones necesarias para nuevo proyecto

        Parámetros:
            name            [String]    Nombre del proyecto nuevo
            database        [String]    Motor de base de datos a utilizar
            design          [String]    Diseño de base de datos a utilizar
            path            [String]    Directorio del proyecto
        Retorno:
            message,result  [Tuple]     Mensaje[String] y result[Boolean]
    """
    try:
        os.mkdir(name)
    except:
        return f"Ya existe una carpeta con el nombre '{name}' en el directorio actual", False
    else:
        os.chdir(os.getcwd() + "/" + name)
        if design == "logico":
            url = "https://gitlab.com/AlejandroBarcenas/template-flask-logic.git"
            name_git = "template-flask-logic"
        message, result = createFlask(name=name,
                                      database=database,
                                      path=os.getcwd(),
                                      url=url,
                                      name_git=name_git)
        return message, result
