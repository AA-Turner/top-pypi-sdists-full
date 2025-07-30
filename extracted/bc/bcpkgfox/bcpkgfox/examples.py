
# FIX: Driver
# region Driver
"""
Example of how easy is start the driver.

It automatically configure the driver with stealth settings to pass over the captchas.
It also automatically prevents a various bugs like versions incompatibles and others.
"""
import neri_library as nr

# To choose the browser just change the name
driver = nr.Instancedriver(
    Browser="chrome"
    # Browser="Firefox"
    # Browser="edge"
    # Browser="internet explorer"
).initialize_driver()

driver.get("https://www.google.com")



# FIX: Driver Options
# region Driver Options
"""
You can also use arguments to configure the driver manually
"""

import neri_library as nr

instance = nr.Instancedriver(Browser="chrome")
instance.initialize_options() # Iniciate the options mode

# Here you can add as many as you want
instance.arguments.add_new_argument("--headless")  # Example
instance.arguments.add_experimental_option("useAutomationExtension", False)  # Example
instance.arguments.add_experimental_options("excludeSwitches", ["enable-automation"])  # Example

# You can add a extension with one line too (already have 'resourse path')
instance.add_extension("path/to/extension.crx")

driver = instance.initialize_driver()
driver.get("https://www.google.com")



# FIX: Selenoid
# region Selenoid
"""
Functions of selenoid (docker)

The driver comes already configured to run in selenoid, but you can also configure it manually.
"""

import neri_library as nr

instance = nr.Instancedriver(Browser="chrome", Selenoid=True)

# Example if you wanna to customize
instance.Selenoid.add_capabilities("enableVNC", True)  # Example
instance.Selenoid.add_capabilities("versiion", "122.0")  # Example

driver = instance.initialize_driver()
driver.get("https://www.google.com")



# FIX: Elements
#region Elements
"""
Some features of selenium that i improve to prevents bugs and work correctly.

(you only need import the neri_library)
"""
import neri_library as nr
from neri_library import By  # Optional to imitating selenium, you can use 'xpath' in place of By.XPATH for example

instance = nr.Instancedriver()
driver = instance.initialize_driver()
finder = instance.elements

# Selenium searchers
example =      finder.find_element_with_wait(By.XPATH, '/your/xpath/here')  # Have too XPATH, CSS, NAME, ID...
example_list = finder.find_elements_with_wait(By.XPATH, '/this/brings/a/list') # work same as the fn above (this have a 's' in the name)

# Selenium interactions works normally too
finder.find_element_with_wait(By.XPATH, '/elmt/xpath').send_keys('')
finder.find_element_with_wait(By.NAME, 'elmt_name').clear()
finder.find_element_with_wait(By.ID, 'elmt_id').click()



# FIX: Elemets created
#region Creations
"""
Below some functions that i created for web scraping
"""
import neri_library as nr
from neri_library import By

instance = nr.Instancedriver()
driver = instance.initialize_driver()
finder = instance.elements

# Just a example to uso on the functions below
example_element = finder.find_element_with_wait(By.XPATH, '/example')

'''
This function moves the mouse to an element imitating human behavior, to avoid captchas.
With some deviations and inaccuracies on the way to the destination (like a human).
( It use a external UI methods, so the browser can't detect )
'''
finder.move_mouse_smoothly(
    element = example_element,
    pure = True,  # Pure is to you pass the cordinates instead the element
    click = False,
    x_adittional = 100,  # Here you can add a number on cordinates (if the elements is bugged)
    y_adittional = 100
)

# Find a image in the screen (you can pass a screenshot of a element)
finder.move_to_image(
    'img_path.png',  # You can send a list to search for more than one
    click_on_final = True,
    trail = True,  # Move your mouse using 'move_mouse_smoothly' above (if False will teleport you mouse)
    verify = True, # Just verify if the image is on the screen (Deactivates the 'trail' and 'click')
    tolerancia = 0.8, # Deviation tolerance of the found image (0.8 = 80%)
    timeout = 10,  # The time that function will search the image(s)
    repeat = True  # It deactivates the 'timeout'
    )

# It will respect the timeout ignoring the "ClickInterrupted" errors
finder.wait_for_element_be_clickable(By.CLASS_NAME, 'elmt_class', timeout=10)

# It is a 'driver.execute_script' of the selenium, but with a timeout
finder.script_console_with_wait('Returns element.value', timeout = 10)

'''
You can use this function below to wait for a image, window, element or text.
'''
finder.wait_for_appear(
    object = '',  # title_window / img_path / text / element
    type = '',  # window / image / text / element (here you really write the type)
    timeout = 10
)

finder.wait_for_appear(       #  finder.wait_for_appear(         #  finder.wait_for_appear(    #  finder.wait_for_appear(
    object = 'Window title',  #      object = 'C://image_path',  #      object = 'Site Text',  #      object = '/xpath/',
    type = 'window',          #      type = 'image',             #      type = 'text',         #      type = 'element',
    timeout = 10              #      timeout = 10                #      timeout = 10           #      timeout = 10
)                             #  )                               #  )                          #  )
finder.wait_for_disappear()  # Same thing
