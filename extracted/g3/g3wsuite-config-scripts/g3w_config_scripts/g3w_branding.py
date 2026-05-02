#!/usr/bin/env python3
# A script to setup a docker based development environment for the g3w suite

import sys
import os
import shutil
import datetime

import PIL.Image
import json


def main():
    # first check if we are in the right folder, i.e. the folders g3w-admin and g3w-suite-docker are present
    if not os.path.exists("g3w-admin") or not os.path.exists("g3w-suite-docker"):
        print("#### This script must be run from the root folder of the installation folder.")
        sys.exit(1)

    # then check if we are in devel mode or prod mode, checking for start_dev.sh
    doDevel = False
    if os.path.exists("start_dev.sh"):
        doDevel = True


    settingsPath = "./g3w-suite-docker/config/g3w-suite/settings_docker.py"
    envPath = "./g3w-suite-docker/.env"
    locationsPath = "./g3w-suite-docker/config/nginx/locations"
    sharedVolume = None

    # get from the env file the WEBGIS_DOCKER_SHARED_VOLUME variable
    with open(envPath, "r") as f:
        lines = f.readlines()
    for line in lines:
        if line.startswith("WEBGIS_DOCKER_SHARED_VOLUME="):
            sharedVolume = line.split("=")[1].strip()
            break
    if not sharedVolume:
        print("#### The shared volume path could not be found in the .env file. Exiting...")
        sys.exit(1)


    G3WSUITE_CUSTOM_STATIC_PATH = None
    if doDevel:
        relPath = "./g3w-admin/g3w-admin/core/static/custom_static/"
        G3WSUITE_CUSTOM_STATIC_PATH = os.path.abspath(relPath)
    else:
        # if sharedVolume has no end slash, add it
        if sharedVolume[-1] != "/":
            sharedVolume += "/"
        G3WSUITE_CUSTOM_STATIC_PATH = sharedVolume + "custom_static/"
    if not os.path.exists(G3WSUITE_CUSTOM_STATIC_PATH):
        os.makedirs(G3WSUITE_CUSTOM_STATIC_PATH)

    # check that both exist
    if not os.path.exists(settingsPath) or not os.path.exists(G3WSUITE_CUSTOM_STATIC_PATH) or not os.path.exists(locationsPath):
        print("#### The settings file, the static folder or the nginx locations file do not exist. Exiting...")
        sys.exit(1)


        

    ####################
    # settings section
    ####################
    
    G3WSUITE_POWERD_BY = False
    answ = input(f"Set the G3WSUITE_POWERD_BY: [{G3WSUITE_POWERD_BY}] ->   ")
    if answ and answ.lower() == "true":
        G3WSUITE_POWERD_BY = True

    G3WSUITE_CUSTOM_TITLE = None
    answ = input(f"Set the G3WSUITE_CUSTOM_TITLE: ->   ")
    if answ:
        G3WSUITE_CUSTOM_TITLE = answ

    G3W_CLIENT_SEARCH_TITLE = None
    answ = input(f"Set the G3W_CLIENT_SEARCH_TITLE: ->   ")
    if answ:
        G3W_CLIENT_SEARCH_TITLE = answ

    G3W_CLIENT_RIGHT_PANEL = None
    answ = input(f"Set the G3W_CLIENT_RIGHT_PANEL width (0-100): -> ")
    if answ:
        G3W_CLIENT_RIGHT_PANEL = json.dumps({"width": answ}, indent=4)

    G3WSUITE_CUSTOM_STATIC_URL = '/custom_static/'
    if doDevel:
        G3WSUITE_CUSTOM_STATIC_URL = '/static/custom_static/'
    else:
        # add the location to the locationsPath file before the first location
        with open(locationsPath, "r") as f:
            lines = f.readlines()
        hasWritten = False
        with open(locationsPath, "w") as f:
            for line in lines:
                if not hasWritten and line.strip().startswith("location"):
                    f.write(f"\nlocation {G3WSUITE_CUSTOM_STATIC_URL} {{\n   root /shared-volume/;\n}}\n")
                    hasWritten = True
                f.write(line)

    G3WSUITE_CUSTOM_CSS = "G3WSUITE_CUSTOM_CSS = [\n    G3WSUITE_CUSTOM_STATIC_URL + 'css/custom.css'\n]"
    # also create the css folder and custom.css file
    if not os.path.exists(G3WSUITE_CUSTOM_STATIC_PATH + 'css/'):
        os.makedirs(G3WSUITE_CUSTOM_STATIC_PATH + 'css/')
    # create an empty custom.css file
    customCssFilePath = G3WSUITE_CUSTOM_STATIC_PATH + 'css/custom.css'

    

    G3WSUITE_FAVICON = None
    # check if in the current folder there is a favicon.ico file
    proposedPath = ""
    if os.path.exists("favicon.ico"):
        proposedPath = "favicon.ico"
    answ = input(f"Set path to the favicon: -> [{proposedPath}]   ")
    if not answ and proposedPath:
        answ = proposedPath
    if answ:
        # if answ is a path and the file exists
        if os.path.exists(answ):
            G3WSUITE_FAVICON = G3WSUITE_CUSTOM_STATIC_URL + 'favicon.ico'
            # copy the file in the right place using shutil
            shutil.copy(answ, G3WSUITE_CUSTOM_STATIC_PATH + 'favicon.ico')
        else:
            print(f"File {answ} does not exist. Check your path. Exiting...")
            sys.exit(1)
    else:
        print("No favicon set.")

    G3WSUITE_MAIN_LOGO = None
    proposedPath = ""
    if os.path.exists("logo_main.png"):
        proposedPath = "logo_main.png"
    answ = input(f"Set path to the logo_main: -> [{proposedPath}]   ")
    if not answ and proposedPath:
        answ = proposedPath
    size = 60
    if answ:
        if os.path.exists(answ):
            # check that the image has a height of 60px or less. In case scale it using pillow
            # and save a copy in the right place
            im = PIL.Image.open(answ)
            if im.height > size:
                scale = size / im.height
                im = im.resize((int(im.width * scale), size))
            im.save(G3WSUITE_CUSTOM_STATIC_PATH + 'logo_main.png')

            G3WSUITE_MAIN_LOGO = G3WSUITE_CUSTOM_STATIC_URL + 'logo_main.png'
        else:
            print(f"File {answ} does not exist. Check your path. Exiting...")
            sys.exit(1)

    G3WSUITE_RID_LOGO = None
    proposedPath = ""
    if os.path.exists("logo_reduced.png"):
        proposedPath = "logo_reduced.png"
    answ = input(f"Set path to the logo_reduced: -> [{proposedPath}]   ")
    if not answ and proposedPath:
        answ = proposedPath
    if answ:
        if os.path.exists(answ):
            # check that the image is square and of size 60x60. In case scale it to teh shape using pillow
            # and save a copy in the right place
            im = PIL.Image.open(answ)
            if im.height != im.width:
                # make it square
                if im.height > im.width:
                    im = im.crop((0, 0, im.width, im.width))
                else:
                    im = im.crop((0, 0, im.height, im.height))
            if im.height != size:
                im = im.resize((size, size))
            im.save(G3WSUITE_CUSTOM_STATIC_PATH + 'logo_reduced.png')

            G3WSUITE_RID_LOGO = G3WSUITE_CUSTOM_STATIC_URL + 'logo_reduced.png'
        else:
            print(f"File {answ} does not exist. Check your path. Exiting...")
            sys.exit(1)

    G3WSUITE_LOGIN_LOGO = None
    proposedPath = ""
    if os.path.exists("logo_login.png"):
        proposedPath = "logo_login.png"
    answ = input(f"Set path to the logo_login: -> [{proposedPath}]   ")
    if not answ and proposedPath:
        answ = proposedPath
    size = 320
    if answ:
        if os.path.exists(answ):
            # check that the image has a width of 320px or less. In case scale it using pillow
            # and save a copy in the right place
            im = PIL.Image.open(answ)
            if im.width > size:
                scale = size / im.width
                im = im.resize((size, int(im.height * scale)))
            im.save(G3WSUITE_CUSTOM_STATIC_PATH + 'logo_login.png')

            G3WSUITE_LOGIN_LOGO = G3WSUITE_CUSTOM_STATIC_URL + 'logo_login.png'
        else:
            print(f"File {answ} does not exist. Check your path. Exiting...")
            sys.exit(1)

    G3W_CLIENT_LEGEND = None
    answ = input(f"Set a standard (customizable) legend? -> [False]   ")
    if answ and answ.lower() == "true":
        G3W_CLIENT_LEGEND = {
            "layerfontsize": 20, # layer title font size
            "itemfontsize": 16, # legend rules font size
            'color': 'black', # all text font color
            'transparent': False, # if false, makes a white background
            'boxspace': 10,  # insets around legend
            "layerspace": 8, # space between layers
            'layertitlespace': 4, # space between layer title and rules
            'symbolspace': 4, # spacing between rules
            'iconlabelspace': 5, # spacing between icon and rule name
            'symbolwidth': 18, # width of the icon
            'symbolheight': 4,  # height of the icon
            "showfeaturecount": True  # show the number of features in the legend
        }


    

    ##########################
    # css section
    ##########################
    cssString = ""
    answ = input(f"Remove the metadata section? -> [False]   ")
    if answ and answ.lower() == "true":
        cssString += "\n#metadata {\n    display: none !important;\n}\n"
    
    answ = input(f"Remove the bookmarks section? -> [False]   ")
    if answ and answ.lower() == "true":
        cssString += "\n#spatialbookmarks {\n    display: none !important;\n}\n"

    answ = input(f"Remove the search section? -> [False]   ")
    if answ and answ.lower() == "true":
        cssString += "\n#search {\n    display: none !important;\n}\n"

    answ = input(f"Remove the print section? -> [False]   ")
    if answ and answ.lower() == "true":
        cssString += "\n#print {\n    display: none !important;\n}\n"

    answ = input(f"Remove the layers themes section? -> [False]   ")
    if answ and answ.lower() == "true":
        cssString += "\n#g3w-catalog-toc-layers-toolbar {\n    display: none !important;\n}\n"

    answ = input(f"Remove the bottom suite logo in the map? -> [False]   ")
    if answ and answ.lower() == "true":
        cssString += "\n#map_footer_left {\n    display: none !important;\n}\n"

    answ = input(f"Set the primary skin color: -> format is 0,100,48   ")
    if answ:
        hslSplit = answ.split(",")
        if len(hslSplit) != 3:
            print("Wrong format. Exiting...")
            sys.exit(1)
        h = hslSplit[0]
        s = hslSplit[1]
        l = hslSplit[2]
        cssString += f":root {{\n    --skin-h: {h};\n    --skin-s: {s}%;\n    --skin-l: {l}%;\n    --skin-color: hsl(var(--skin-h), var(--skin-s), var(--skin-l));\n}}\n"


    # append the settings to the end of the settings file
    currentDateTimeString = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open(settingsPath, "a") as f:
        f.write(f"\n\n# {currentDateTimeString} Custom settings for the g3w suite\n")
        f.write(f"G3WSUITE_POWERD_BY = {G3WSUITE_POWERD_BY}\n")
        if G3WSUITE_CUSTOM_TITLE:
            f.write(f"G3WSUITE_CUSTOM_TITLE = '{G3WSUITE_CUSTOM_TITLE}'\n")
        if G3W_CLIENT_SEARCH_TITLE:
            f.write(f"G3W_CLIENT_SEARCH_TITLE = '{G3W_CLIENT_SEARCH_TITLE}'\n")
        if G3W_CLIENT_RIGHT_PANEL:
            f.write(f"G3W_CLIENT_RIGHT_PANEL = {G3W_CLIENT_RIGHT_PANEL}\n")

        f.write(f"G3WSUITE_CUSTOM_STATIC_URL = '{G3WSUITE_CUSTOM_STATIC_URL}'\n")
        if G3WSUITE_FAVICON:
            f.write(f"G3WSUITE_FAVICON = '{G3WSUITE_FAVICON}'\n")
        if G3WSUITE_MAIN_LOGO:
            f.write(f"G3WSUITE_MAIN_LOGO = '{G3WSUITE_MAIN_LOGO}'\n")
        if G3WSUITE_RID_LOGO:
            f.write(f"G3WSUITE_RID_LOGO = '{G3WSUITE_RID_LOGO}'\n")
        if G3WSUITE_LOGIN_LOGO:
            f.write(f"G3WSUITE_LOGIN_LOGO = '{G3WSUITE_LOGIN_LOGO}'\n")
        if G3W_CLIENT_LEGEND:
            f.write(f"G3W_CLIENT_LEGEND = {json.dumps(G3W_CLIENT_LEGEND, indent=4).replace("false", "False")}\n")
        
        f.write(f"{G3WSUITE_CUSTOM_CSS}\n")

    # write the css to the custom.css file
    with open(customCssFilePath, "w") as f:
        f.write(cssString)

    print("#### The branding setup is complete.")
        
    



    


if __name__ == "__main__":
    main()
