from .base import ScrapperBase
import re


class CostcoScrapper(ScrapperBase):
    domain: str = 'costco.com'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.expected_columns = [
            'region',
            'store_name',
            'start_date',
            'end_date',
            'event',
            'brand_event',
            'state'
        ]
        # self.url: str = 'https://www.costco.com/special-events.html'
        self.url: str = None
        self.use_proxy = True
        self.us_proxy = True
        self._free_proxy = False
        # self.use_edge = True
        # self.use_firefox = True
        self.headless = False
        self.use_wire = False
        # self._browser_binary = '/opt/google/chrome/chrome'
        # self._driver_binary = '/home/jesuslara/.cache/selenium/geckodriver/linux64/0.33.0/geckodriver'

    async def connect(self):
        """Creates the Driver and Connects to the Site.
        """
        self._driver = await self.get_driver()
        await self.start()

    async def disconnect(self):
        """Disconnects the Driver and closes the Connection.
        """
        if self._driver:
            self.close_driver()

    async def get_events(self, response: object, idx: int, row: dict) -> tuple:
        """
        Get the special events from Costco page.
        This method extracts events information from the HTML response.
        """
        try:
            document = self.get_bs(response)
            events = []
            
            # Extraer la región del título dinámicamente
            region = "Unknown Region"
            title = document.find('title')
            if title:
                title_text = title.get_text(strip=True)
                # Buscar patrones como "Special Events in [Region] Region"
                region_match = re.search(r'Special Events in (.*?) Region', title_text)
                if region_match:
                    region = region_match.group(1).strip()
            
            # Extraer el estado dinámicamente
            current_state = "Unknown State"
            
            # Buscar todos los warehouses (tiendas)
            warehouses = document.find_all('div', class_='sp-event-warehouse')

            for warehouse in warehouses:
                # Verificar si hay un cambio de estado antes de este warehouse
                prev_state_header = warehouse.find_previous('h2', class_='state-name')
                if prev_state_header:
                    state_text = prev_state_header.get_text(strip=True)
                    current_state = state_text.replace("Warehouses", "").strip()

                # Extraer el nombre de la tienda
                store_name_elem = warehouse.find('h3', class_='warehouse-name')
                if not store_name_elem:
                    continue

                store_name = store_name_elem.get_text(strip=True)

                # Obtener el ID del warehouse desde aria-controls del panel-heading
                panel_heading = warehouse.find('div', class_='panel-heading')
                if not panel_heading:
                    continue
                warehouse_id = panel_heading.get('aria-controls')
                if not warehouse_id:
                    continue

                table_container = document.find('div', id=warehouse_id)
                if not table_container:
                    continue
                    
                table = table_container.find('table')
                if not table:
                    continue
                    
                # Procesar las filas de la tabla
                table_rows = table.find_all('tr')
                
                # Saltamos la primera fila (encabezado)
                for table_row in table_rows[1:]:
                    cells = table_row.find_all('td')
                    
                    if len(cells) >= 2:  # Necesitamos al menos fecha y evento
                        event_data = {}
                        
                        # Datos comunes para todos los eventos de esta tienda
                        event_data["region"] = region
                        event_data["store_name"] = store_name
                        event_data["state"] = current_state
                        
                        # Extraer fecha
                        date_cell = cells[0]
                        # Extract full dates from <time> elements with datetime attributes
                        time_elements = date_cell.find_all('time')
                        if time_elements and len(time_elements) >= 2:
                            # Extract start and end dates
                            start_datetime = time_elements[0].get('datetime')
                            end_datetime = time_elements[1].get('datetime')
                            event_data["start_date"] = start_datetime if start_datetime else ""
                            event_data["end_date"] = end_datetime if end_datetime else ""
                        elif time_elements and len(time_elements) == 1:
                            # Only one date found, use it as both start and end
                            datetime_attr = time_elements[0].get('datetime')
                            event_data["start_date"] = datetime_attr if datetime_attr else ""
                            event_data["end_date"] = datetime_attr if datetime_attr else ""
                        else:
                            # Fallback to original text if no time elements found
                            date_text = date_cell.get_text(strip=True)
                            event_data["start_date"] = date_text
                            event_data["end_date"] = ""
                        
                        # Extraer evento y enlace
                        event_cell = cells[1]
                        event_data["event"] = event_cell.get_text(strip=True)
                        
                        # Para el enlace del evento
                        link = event_cell.find('a')
                        if link and link.get('href'):
                            event_data["brand_event"] = link.get('href')
                        else:
                            event_data["brand_event"] = ""
                        
                        events.append(event_data)
            
            # Si encontramos eventos, actualizar la fila con el primer evento
            # y crear nuevas filas para los eventos adicionales
            if events:
                # Actualizar la fila original con el primer evento
                for key, value in events[0].items():
                    row[key] = value
                
                # Retornar la fila actualizada
                return idx, row
            else:
                # Si no encontramos eventos, retornar la fila original
                return idx, row
                
        except Exception as err:
            self._logger.error(f'Error getting events from Costco: {err}')
            return idx, row

    async def special_events(self, response: object, idx: int, row: dict) -> tuple:
        """
        Get the special events from Costco.
        """
        try:
            document = self.get_bs(response)
            category_header = document.find('div', {'id': 'category-name-header'})
            print('category_header > ', category_header)
            return idx, row
        except Exception as err:
            self._logger.error(f'Error getting special events from Costco: {err}')
            return None

    async def product_information(self, response: object, idx: int, row: dict) -> tuple:
        """
        Get the product information from Costco.
        """
        try:
            document = self.get_bs(response)
            search_results_div = document.find('div', {'id': 'search-results'})
            if search_results_div:
                # 1. Get the brand name: find the <div> with class "search-results-tile", then the first <h1>
                search_results_tile = search_results_div.find('div', class_="search-results-tile")
                brand_name = None
                if search_results_tile:
                    h1_tag = search_results_tile.find('h1')
                    if h1_tag:
                        brand_name = h1_tag.get_text(strip=True)
                        row['brand_name'] = brand_name
                # 2. Get the brand image: find the <div> with class "dual-row", then find the <img> with class "img-responsive"
                dual_row_div = search_results_div.find('div', class_="dual-row")
                brand_image = None
                if dual_row_div:
                    img_tag = dual_row_div.find('img', class_="img-responsive")
                    if img_tag and img_tag.has_attr('src'):
                        brand_image = img_tag['src']
                        row['brand_image'] = brand_image
                # 3. Get the brand description: find the <div> with class "sp-event-product-copy" then its first <p>
                copy_div = search_results_div.find('div', class_="sp-event-product-copy")
                brand_description = None
                if copy_div:
                    p_tag = copy_div.find('p')
                    if p_tag:
                        brand_description = p_tag.get_text(strip=True)
                        row['brand_description'] = brand_description
                # 4. Get the short name: find the <div> with class "search-results-tile",
                _div = search_results_div.find('div', class_="sp-event-product-title")
                short_name = None
                if _div:
                    short_name = _div.get_text(strip=True)
                    row['short_name'] = short_name
            return idx, row
        except Exception as err:
            self._logger.error(f'Error getting product information from Costco: {err}')
            return None
