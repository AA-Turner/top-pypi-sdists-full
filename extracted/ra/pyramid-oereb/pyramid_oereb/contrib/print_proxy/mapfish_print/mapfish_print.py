# -*- coding: utf-8 -*-
from datetime import datetime
import io
import json
import logging
import requests
from shapely.geometry import mapping
from urllib import parse as urlparse

from pyramid.httpexceptions import HTTPBadRequest
from pyramid_oereb import Config
from pyramid_oereb.core.renderer.extract.json_ import Renderer as JsonRenderer
from pyramid_oereb.core.url import parse_url
from pyramid.httpexceptions import HTTPInternalServerError
from pypdf import PdfReader
from pypdf.errors import PdfReadError
from pyramid_oereb.contrib.print_proxy.mapfish_print.toc_pages import TocPages


log = logging.getLogger(__name__)

LEGEND_ELEMENT_SORT_ORDER = [
    'AreaShare',
    'LengthShare',
    'NrOfPoints'
]


class Renderer(JsonRenderer):

    def __init__(self, info):
        super(Renderer, self).__init__(info)
        self.global_datetime = None
        self.global_datetime_format = '%Y-%m-%dT%H:%M:%S'

    def __call__(self, value, system):
        """
        Implements a subclass of pyramid_oereb.core.renderer.extract.json_.Renderer to create a print result
        out of a json. The json extract is reformatted to fit the structure of mapfish print.

        Args:
            value (tuple): A tuple containing the generated extract record and the params
                dictionary.
            system (dict): The available system properties.

        Returns:
            pyramid.response.Response.content: The pdf content as received from mapfish print.

        Raises:
            HTTPBadRequest: when the print was called with illegal parameters.
            HTTPInternalServerError: when the pdf content could not be produced successfully.
        """
        log.debug("Parameter webservice is {}".format(value[1]))

        if value[1].images:
            raise HTTPBadRequest('With image is not allowed in the print')

        self._request = self.get_request(system)

        # Create a lower case GET dict to be able to accept all cases of upper and lower case writing
        self._lowercase_GET_dict = dict((k.lower(), v.lower()) for k, v in self._request.GET.items())

        # If a language is specified in the request, use it. Otherwise, use the language from base class
        self._fallback_language = Config.get('default_language')
        if 'lang' in self._lowercase_GET_dict:
            self._language = self._lowercase_GET_dict.get('lang')

        self._static_error_message = Config.get('static_error_message').get(self._language) or \
            Config.get('static_error_message').get(self._fallback_language)

        # Based on extract record and webservice parameter, render the extract data as JSON
        extract_record = value[0]
        extract_as_dict = self._render(extract_record, value[1])
        feature_geometry = mapping(extract_record.real_estate.limit)

        print_config = Config.get('print', {})

        # set the global_datetime variable so that it can be used later for the archive
        self.set_global_datetime(extract_as_dict['CreationDate'])
        self.convert_to_printable_extract(extract_as_dict, feature_geometry)

        extract_as_dict['Display_RealEstate_SubunitOfLandRegister'] = print_config.get(
            'display_real_estate_subunit_of_land_register', True
        )

        extract_as_dict['Display_Certification'] = print_config.get(
            'display_certification', False
        )

        extract_as_dict['Display_QRCode'] = print_config.get(
            'display_qrcode', False
        )

        if print_config.get('compute_toc_pages', False):
            extract_as_dict['nbTocPages'] = TocPages(extract_as_dict).getNbPages()
        else:
            if print_config.get('expected_toc_length') and int(print_config.get('expected_toc_length')) > 0:
                extract_as_dict['nbTocPages'] = print_config.get('expected_toc_length')
            else:
                extract_as_dict['nbTocPages'] = 1

        spec = {
            'layout': print_config['template_name'],
            'outputFormat': 'pdf',
            'lang': self._language,
            'attributes': extract_as_dict,
        }

        response = self.get_response(system)

        if self._request.GET.get('getspec', 'no') != 'no':
            response.headers['Content-Type'] = 'application/json; charset=UTF-8'
            return json.dumps(spec, sort_keys=True, indent=4)
        pdf_url = urlparse.urljoin(print_config['base_url'] + '/', 'buildreport.pdf')
        pdf_headers = print_config['headers']
        print_result = requests.post(
            pdf_url,
            headers=pdf_headers,
            data=json.dumps(spec)
        )
        try:
            log.debug('Validation of the TOC length with compute_toc_pages set to {} and expected_toc_length set to {}'.format(print_config.get('compute_toc_pages'), print_config.get('expected_toc_length'))) # noqa
            with io.BytesIO() as pdf:
                pdf.write(print_result.content)
                pdf_reader = PdfReader(pdf)
                x = []
                for i in range(len(pdf_reader.outline)):
                    if isinstance(pdf_reader.outline[i], list):
                        x.append(pdf_reader.outline[i][0]['/Page']['/StructParents'])
                    else:
                        x.append(pdf_reader.outline[i]['/Page']['/StructParents'])
                try:
                    true_nb_of_toc = min(x)-1
                except ValueError:
                    true_nb_of_toc = 1

                log.debug('True number of TOC pages is {}, expected number was {}'.format(true_nb_of_toc, extract_as_dict['nbTocPages'])) # noqa
                if true_nb_of_toc != extract_as_dict['nbTocPages']:
                    log.warning('nbTocPages in result pdf: {} are not equal to the one predicted : {}, request new pdf'.format(true_nb_of_toc,extract_as_dict['nbTocPages'])) # noqa
                    log.debug('Secondary PDF extract call STARTED')
                    extract_as_dict['nbTocPages'] = true_nb_of_toc
                    print_result = requests.post(
                        pdf_url,
                        headers=pdf_headers,
                        data=json.dumps(spec)
                    )
                    log.debug('Secondary PDF extract call to fix TOC pages number DONE')

        except PdfReadError as e:
            err_msg = 'a problem occurred while generating the pdf file'
            log.error(err_msg + ': ' + str(e))
            raise HTTPInternalServerError(self._static_error_message)

        try:
            content = print_result.content
        except PdfReadError as e:
            err_msg = 'No contents from print result available!'
            log.error(err_msg + ': ' + str(e))
            raise HTTPInternalServerError(self._static_error_message)

        # Save printed file to the specified path.
        pdf_archive_path = print_config.get('pdf_archive_path', None)
        if pdf_archive_path is not None:
            self.archive_pdf_file(pdf_archive_path, content, extract_as_dict)

        response.status_code = print_result.status_code
        response.headers = print_result.headers
        if 'Transfer-Encoding' in response.headers:
            del response.headers['Transfer-Encoding']
        if 'Connection' in response.headers:
            del response.headers['Connection']
        return content

    def archive_pdf_file(self, pdf_archive_path, binary_content, extract_as_dict):
        """
        Writes the static extract (pdf) into a dedicated file; this functionality can thus be used
        for archiving.

        Args:
            pdf_archive_path (str): directory path where the file shall be stored.
            binary_content (): the contents of the pdf.
            extract_as_dict (): the extract contents, used to retrieve metadata in order to produce
                the filename.

        Returns:
            str: the name of the file that was written, including the path.
        """
        pdf_archive_path = pdf_archive_path if pdf_archive_path[-1:] == '/' else pdf_archive_path + '/'
        log.debug('Start to archive pdf file at path: ' + pdf_archive_path)
        time_info = self.global_datetime.strftime('%Y%m%d%H%M%S')
        egrid = extract_as_dict.get('RealEstate_EGRID', 'no_egrid')

        if egrid == 'no_egrid' or egrid is None:
            identdn = extract_as_dict.get('RealEstate_IdentDN', 'no_identdn')
            number = extract_as_dict.get('RealEstate_Number', 'no_number')
            path_and_filename = pdf_archive_path + time_info + '_' + identdn + '_' + number + '.pdf'
        else:
            path_and_filename = pdf_archive_path + time_info + '_' + egrid + '.pdf'

        archive = open(path_and_filename, 'ab')
        archive.write(binary_content)
        log.debug('Pdf file archived at: ' + path_and_filename)
        return path_and_filename

    @staticmethod
    def get_wms_url_params():
        """
        Returns the list of additionally configured wms_url_params.

        Returns:
            (dict): The configured wms_url_params.
        """
        result = {}
        wms_url_params = Config.get('print', {}).get('wms_url_params', False)
        if wms_url_params:
            log.debug("get_wms_url_params() read configuration {}".format(wms_url_params))
            if isinstance(wms_url_params, dict):
                result = wms_url_params
            else:
                log.warning("get_wms_url_params() ignoring unaccepted configuration value {}"
                            .format(wms_url_params))
        else:
            log.info("no wms_url_params configuration detected; using default value")
            result = {'TRANSPARENT': 'true'}
        return result

    def lpra_flatten(self, items):
        """
        Flattens a list of PLRs.

        Args:
            items (tuple): a list of PLR documents.
        """
        for item in items:
            self._flatten_object(item, 'Lawstatus')
            self._multilingual_text(item, 'Lawstatus_Text')
            self._multilingual_text(item, 'OfficialNumber')
            self._flatten_object(item, 'ResponsibleOffice')
            self._multilingual_text(item, 'ResponsibleOffice_Name')
            self._multilingual_text(item, 'ResponsibleOffice_OfficeAtWeb')
            self._multilingual_text_at_web(item)
            self._multilingual_text(item, 'Text')
            self._multilingual_text(item, 'Title')
            self._multilingual_text(item, 'Abbreviation')

    def convert_to_printable_extract(self, extract_dict, feature_geometry):
        """
        Converts an oereb extract into a form suitable for printing by mapfish print.

        Args:
            extract_dict: the oereb extract, will get converted by this function into a form
                            convenient for mapfish-print
            feature_geometry: the geometry for this extract, will get added to the extract information
        """
        log.debug("Starting transformation, extract_dict is {}".format(extract_dict))
        log.debug("Parameter feature_geometry is {}".format(feature_geometry))
        if self.global_datetime is None:
            # make sure this is set i.e when running tests
            self.set_global_datetime(extract_dict['CreationDate'])
        extract_dict['Footer'] = '   '.join([
            self.global_datetime.strftime('%d.%m.%Y'),
            self.global_datetime.strftime('%H:%M:%S'),
            extract_dict['ExtractIdentifier']
        ])
        extract_dict['CreationDate'] = self.global_datetime.strftime('%d.%m.%Y')

        for attr_name in ['ConcernedTheme', 'NotConcernedTheme', 'ThemeWithoutData']:
            for theme in extract_dict[attr_name]:
                self._multilingual_text(theme, 'Text')

        # extract theme titles for later use before resetting "ConcernedTheme"
        themeTitles = {theme["Code"]: theme["Text"]
                       for theme in (extract_dict.get("ConcernedTheme", [])
                                     + extract_dict.get("NotConcernedTheme", []))}
        extract_dict['ConcernedTheme'] = []
        self._flatten_object(extract_dict, 'PLRCadastreAuthority')
        self._multilingual_text(extract_dict, 'PLRCadastreAuthority_OfficeAtWeb')
        self._flatten_object(extract_dict, 'RealEstate')

        self._multilingual_text(extract_dict['RealEstate_Type'], 'Text')
        self._flatten_object(extract_dict, 'RealEstate_Type')
        if 'Image' in extract_dict.get('RealEstate_Highlight', {}):
            del extract_dict['RealEstate_Highlight']['Image']

        self._multilingual_text(extract_dict['RealEstate_PlanForLandRegisterMainPage'], 'ReferenceWMS')
        self._multilingual_text(extract_dict['RealEstate_PlanForLandRegister'], 'ReferenceWMS')

        main_page_url, main_page_params = \
            parse_url(extract_dict['RealEstate_PlanForLandRegisterMainPage']['ReferenceWMS'])
        base_url = urlparse.urlunsplit((main_page_url.scheme,
                                        main_page_url.netloc,
                                        main_page_url.path,
                                        None,
                                        None))
        wms_url_params = self.get_wms_url_params()

        main_page_basemap = {
            'type': 'wms',
            'styles': 'default',
            'opacity': extract_dict['RealEstate_PlanForLandRegisterMainPage'].get('layerOpacity', 0.6),
            'baseURL': base_url,
            'layers': main_page_params['LAYERS'][0].split(','),
            'imageFormat': 'image/png',
            'customParams': wms_url_params,
        }
        extract_dict['baseLayers'] = {'layers': [main_page_basemap]}
        url, params = parse_url(extract_dict['RealEstate_PlanForLandRegister']['ReferenceWMS'])
        basemap = {
            'type': 'wms',
            'styles': 'default',
            'opacity': extract_dict['RealEstate_PlanForLandRegister'].get('layerOpacity', 0.6),
            'baseURL': urlparse.urlunsplit((url.scheme, url.netloc, url.path, None, None)),
            'layers': params['LAYERS'][0].split(','),
            'imageFormat': 'image/png',
            'customParams': wms_url_params,
        }
        del extract_dict['RealEstate_PlanForLandRegister']  # /definitions/Map

        flattened_general_info = []
        for item in extract_dict.get('GeneralInformation', []):
            lang_obj = dict([(e['Language'], e['Text']) for e in item])
            if self._language in lang_obj.keys():
                flattened_general_info.append({'Info': lang_obj[self._language]})
            else:
                flattened_general_info.append({'Info': lang_obj[self._fallback_language]})
        extract_dict['GeneralInformation'] = flattened_general_info
        update_date_cs = datetime.strptime(extract_dict['UpdateDateCS'], '%Y-%m-%dT%H:%M:%S')
        extract_dict['UpdateDateCS'] = update_date_cs.strftime('%d.%m.%Y')
        self._multilingual_text(extract_dict, 'Certification')
        self._multilingual_text(extract_dict, 'CertificationAtWeb')

        for item in extract_dict.get('Glossary', []):
            self._multilingual_text(item, 'Title')
            self._multilingual_text(item, 'Content')
        self._multilingual_text(extract_dict, 'PLRCadastreAuthority_Name')

        for restriction_on_landownership in extract_dict.get('RealEstate_RestrictionOnLandownership', []):
            self._flatten_object(restriction_on_landownership, 'Lawstatus')
            self._flatten_object(restriction_on_landownership, 'Theme')
            self._flatten_object(restriction_on_landownership, 'SubTheme')
            self._flatten_array_object(restriction_on_landownership, 'Geometry', 'ResponsibleOffice')
            self._multilingual_text(restriction_on_landownership, 'Theme_Text')
            self._multilingual_text(restriction_on_landownership, 'SubTheme_Text')
            self._multilingual_text(restriction_on_landownership, 'Lawstatus_Text')
            self._multilingual_text(restriction_on_landownership, 'LegendText')

            self._multilingual_text(restriction_on_landownership['ResponsibleOffice'], 'Name')
            self._multilingual_text(restriction_on_landownership['ResponsibleOffice'], 'OfficeAtWeb')
            restriction_on_landownership['ResponsibleOffice'] = \
                [restriction_on_landownership['ResponsibleOffice']]

            self._multilingual_text(restriction_on_landownership['Map'], 'ReferenceWMS')
            url, params = parse_url(restriction_on_landownership['Map']['ReferenceWMS'])

            restriction_on_landownership['baseLayers'] = {
                'layers': [{
                    'type': params.pop('SERVICE', ['wms'])[0].lower(),
                    'opacity': restriction_on_landownership['Map'].get('layerOpacity', 0.6),
                    'styles': params.pop('STYLES', ['default'])[0],
                    'baseURL': urlparse.urlunsplit((url.scheme, url.netloc, url.path, None, None)),
                    'layers': params.pop('LAYERS', '')[0].split(','),
                    'imageFormat': params.pop('FORMAT', ['image/png'])[0],
                    'customParams': self.get_custom_wms_params(params),
                }, basemap]
            }

            # Legend of other visible restriction objects in the topic map
            restriction_on_landownership['OtherLegend'] = restriction_on_landownership['Map'].get(
                'OtherLegend', [])
            for legend_item in restriction_on_landownership['OtherLegend']:
                self._multilingual_text(legend_item, 'LegendText')

            for legend_entry in restriction_on_landownership['OtherLegend']:
                for element in list(legend_entry.keys()):
                    if element not in ['LegendText', 'SymbolRef', 'TypeCode']:
                        del legend_entry[element]

            del restriction_on_landownership['Map']  # /definitions/Map

            for item in restriction_on_landownership.get('Geometry', []):
                self._multilingual_text(item, 'ResponsibleOffice_Name')

            legal_provisions = {}
            laws = {}
            hints = {}

            if 'LegalProvisions' in restriction_on_landownership:
                finish = False
                while not finish:
                    finish = True
                    for legal_provision in restriction_on_landownership['LegalProvisions']:
                        if 'Base64TextAtWeb' in legal_provision:
                            del legal_provision['Base64TextAtWeb']
                        if 'Reference' in legal_provision:
                            for reference in legal_provision['Reference']:
                                self._categorize_documents(reference, legal_provisions, laws, hints)
                            del legal_provision['Reference']
                            finish = False
                        if 'Article' in legal_provision:
                            for article in legal_provision['Article']:
                                self._categorize_documents(article, legal_provisions, laws, hints)
                            del legal_provision['Article']
                            finish = False

                        self._categorize_documents(legal_provision, legal_provisions, laws, hints)

                del restriction_on_landownership['LegalProvisions']

            restriction_on_landownership['LegalProvisions'] = legal_provisions
            restriction_on_landownership['Laws'] = laws
            restriction_on_landownership['Hints'] = hints

        # One restriction entry per theme
        theme_restriction = {}
        text_element = [
            'LegendText', 'Lawstatus_Code', 'Lawstatus_Text', 'SymbolRef', 'TypeCode'
        ]
        legend_element = [
            'TypeCode', 'TypeCodelist', 'AreaShare', 'PartInPercent', 'LengthShare', 'NrOfPoints',
            'SymbolRef', 'LegendText'
        ]
        for restriction_on_landownership in extract_dict.get('RealEstate_RestrictionOnLandownership', []):

            theme_text = restriction_on_landownership['Theme_Text']
            if 'Theme_SubCode' in restriction_on_landownership:
                main_theme_text = themeTitles.get(restriction_on_landownership['Theme_Code'])
                if main_theme_text is not None:
                    theme_text = f"{main_theme_text}: {theme_text}"

            restriction_on_landownership['Theme_Text'] = theme_text

            sub_theme_code = restriction_on_landownership.get('Theme_SubCode', '')
            theme = restriction_on_landownership['Theme_Code'] + \
                sub_theme_code+restriction_on_landownership['Lawstatus_Code']

            extract_dict['ConcernedTheme'].append(
                {
                    'Code': theme,
                    'Text': restriction_on_landownership['Theme_Text']
                }
            )

            geom_type = \
                'AreaShare' if 'AreaShare' in restriction_on_landownership else \
                'LengthShare' if 'LengthShare' in restriction_on_landownership else 'NrOfPoints'

            if theme not in theme_restriction:
                current = dict(restriction_on_landownership)
                current['Geom_Type'] = geom_type
                theme_restriction[theme] = current

                # Legend
                legend = {}
                for element in legend_element:
                    if element in current:
                        legend[element] = current[element]
                        del current[element]
                    legend['Geom_Type'] = geom_type
                current['Legend'] = [legend]

                # Text
                for element in text_element:
                    if element in current:
                        current[element] = set([current[element]])
                    else:
                        current[element] = set()
                continue

            # ELSE - theme is already in theme_restriction
            current = theme_restriction[theme]

            if 'Geom_Type' in current and current['Geom_Type'] != geom_type:
                del current['Geom_Type']

            # Legend
            legend = {}
            for element in legend_element:
                if element in restriction_on_landownership:
                    legend[element] = restriction_on_landownership[element]
                    del restriction_on_landownership[element]
                    legend['Geom_Type'] = geom_type
            current['Legend'].append(legend)

            # Remove in OtherLegend elements that are already in the legend
            current['OtherLegend'] = [other_legend_element
                                      for other_legend_element in current['OtherLegend']
                                      if other_legend_element['SymbolRef'] != legend['SymbolRef']]

            # Number or array
            for element in ['Laws', 'LegalProvisions', 'Hints']:
                if current.get(element) is not None and restriction_on_landownership.get(element) is not None:
                    current[element].update(restriction_on_landownership[element])
                elif restriction_on_landownership.get(element) is not None:
                    current[element] = restriction_on_landownership[element]

            # add additional ResponsibleOffice to theme if it not already exists there
            new_responsible_office = restriction_on_landownership['ResponsibleOffice'][0]
            existing_office_names = list(map(lambda o: o['Name'], current['ResponsibleOffice']))
            if new_responsible_office['Name'] not in existing_office_names:
                current['ResponsibleOffice'].append(new_responsible_office)

            # add additionally map layer to the theme if not already there
            new_layer = restriction_on_landownership['baseLayers']['layers'][0]['layers'][0]
            new_base_url = restriction_on_landownership['baseLayers']['layers'][0]['baseURL']
            existing_layer = [
                layer for layers in current['baseLayers']['layers'] for layer in layers['layers']
                ]
            if new_layer not in existing_layer:
                # add it in the element with the same baseURL.
                # The rest of the parameters should be the same as given by the theme
                layer_added = False
                for element in current['baseLayers']['layers']:
                    if new_base_url == element['baseURL']:
                        element['layers'].append(new_layer)
                        layer_added = True
                        break
                if not layer_added:
                    current['baseLayers']['layers'].append(
                        restriction_on_landownership['baseLayers']['layers'][0]
                    )

            # Text
            for element in text_element:
                if element in restriction_on_landownership:
                    current[element].add(restriction_on_landownership[element])

        for restriction_on_landownership in theme_restriction.values():
            for element in text_element:
                restriction_on_landownership[element] = '\n'.join(restriction_on_landownership[element])
            for element in ['Laws', 'LegalProvisions', 'Hints']:
                values = list(restriction_on_landownership[element].values())
                self.lpra_flatten(values)
                restriction_on_landownership[element] = values

                # Group legal provisions and hints which have the same title.
                if (
                       (Config.get('print', {}).get('group_legal_provisions', False)) and
                       (element == 'LegalProvisions' or element == 'Hints')
                   ):
                    restriction_on_landownership[element] = \
                        self.group_legal_provisions(restriction_on_landownership[element])

            self.sort_restriction_on_landownership_documents(restriction_on_landownership)

        restrictions = list(theme_restriction.values())
        for restriction in restrictions:
            legends = {}
            for legend in restriction['Legend']:
                type_ = f"{legend['SymbolRef']}"
                if type_ in legends:
                    for item in ['AreaShare', 'LengthShare', 'PartInPercent', 'NrOfPoints']:
                        if item in legend:
                            if item in legends[type_]:
                                legends[type_][item] += legend[item]
                            else:
                                legends[type_][item] = legend[item]
                else:
                    legends[type_] = legend
            # After transformation, get the new legend entries, sorted by TypeCode
            transformed_legend = \
                list([transformed_entry for (key, transformed_entry) in legends.items()])
            restriction['Legend'] = self.sort_dict_list(transformed_legend, self.sort_legend_elem)

        extract_dict['RealEstate_RestrictionOnLandownership'] = restrictions
        # End one restriction entry per theme

        # Flatten the disclaimer dictionary
        for item in extract_dict.get('Disclaimer', []):
            self._multilingual_text(item, 'Title')
            self._multilingual_text(item, 'Content')

        # Separate the first item, so it can be placed in a different column in the template
        disclaimer = extract_dict.get('Disclaimer', [])
        if len(disclaimer) > 0:
            extract_dict['DisclaimerLandRegister'] = disclaimer.pop(0)

        self._flatten_object(extract_dict, 'DisclaimerLandRegister')

        extract_dict['features'] = {
            'features': {
                'type': 'FeatureCollection',
                'features': [{
                    'type': 'Feature',
                    'geometry': feature_geometry,
                    'properties': {}
                }]
            }
        }

        # Reformat land registry area
        extract_dict['RealEstate_LandRegistryArea'] = u'{0} m²'.format(
            extract_dict['RealEstate_LandRegistryArea']
        )

        # Reformat AreaShare, LengthShare, NrOfPoints and part in percent values
        for restriction in extract_dict['RealEstate_RestrictionOnLandownership']:
            for legend in restriction['Legend']:
                if 'LengthShare' in legend:
                    legend['LengthShare'] = '{0} m'.format(legend['LengthShare'])
                if 'AreaShare' in legend:
                    legend['AreaShare'] = u'{0} m²'.format(legend['AreaShare'])
                if 'PartInPercent' in legend:
                    legend['PartInPercent'] = '{0}%'.format(round(legend['PartInPercent'], 2))
                if 'NrOfPoints' in legend:
                    legend['NrOfPoints'] = '{0}'.format(legend['NrOfPoints'])

        extract_dict['PrintCantonLogo'] = Config.get('print', {}).get('print_canton_logo', True)
        extract_dict['PrintMunicipalityName'] = Config.get('print', {}).get('print_municipality_name', True)

        log.debug("After transformation, extract_dict is {}".format(json.dumps(extract_dict, indent=4)))
        return extract_dict

    @staticmethod
    def group_legal_provisions(legal_provisions):
        """
        Group PLR documents which have the same title together.

        Args:
            legal_provisions (list): the list of legal provision documents for a PLR

        Returns:
            list: the list of grouped legal provision documents
        """
        merged_provision = []
        for element in legal_provisions:
            # get element with same title if existing
            existing_element = \
                next((item for item in merged_provision if item['Title'] == element['Title']), None)
            if not existing_element:
                merged_provision.append(element)
                continue

            # join the the existing list with the new one
            existing_element['TextAtWeb'].extend(element['TextAtWeb'])
        return merged_provision if len(merged_provision) > 0 else legal_provisions

    def _flatten_array_object(self, parent, array_name, object_name):
        """
        Replace an array's hierarchy by flattened entries, more suitable for print templates

        Args:
            parent (dict): extract data
            array_name (str): the name of the element in the extract data
            object_name (str): the name of an entry whose hierarchy shall be flattened
        """
        if array_name in parent:
            for item in parent[array_name]:
                self._flatten_object(item, object_name)

    @staticmethod
    def _flatten_object(parent, name):
        """
        Replace a hierarchy by flattened entries, more suitable for print templates

        Args:
            parent (dict): a dictionary of entries
            name (str): the name of an entry whose hierarchy shall be flattened
        """
        if name in parent:
            for key, value in parent[name].items():
                parent['{}_{}'.format(name, key)] = value
            del parent[name]

    @staticmethod
    def _categorize_documents(document, legal_provisions, laws, hints):
        """
        Categorize document by their documentType (LegalProvision, Law or Hint)

        Args:
            document (dict): The document type as dictionary.
            legal_provisions (dict): The legal_provisions dictionary to fill.
            laws (dict): The laws dictionary to fill.
            hints (dict): The Hints dictionary to fill.
        """
        uid = Renderer._get_element_of_legal_provision_maybe_uid(document)
        documentType = document.get('Type').get('Code')
        if documentType is None:
            error_msg = "mandatory attribute document_type is missing in document " \
                        ": {}".format(document)
            log.error(error_msg)
            raise AttributeError(error_msg)
        # TODO: We should check if this has potential relation to the configurable translations.
        if documentType == 'LegalProvision':
            legal_provisions[uid] = document
        elif documentType == 'Law':
            laws[uid] = document
        elif documentType == 'Hint':
            hints[uid] = document
        else:
            log.warning(f"Wrong document type {documentType}")
            log.warning("(expected 'LegalProvision', 'Law' or 'Hint')")

    @staticmethod
    def _get_element_of_legal_provision_maybe_uid(element):
        """
        Make a unique key string out of title and TextAtWeb. This is necessary to satisfy the KBS's theme.
        There it can happen, that we get different titles with the same URL. This way we keep even them.

        Args:
            element (dict): The document type as dictionary.

        Returns:
            str: The constructed unique key made of Title and TextAtWeb
        """
        unique_key = []
        if element['TextAtWeb'] is not None:
            # If TextAtWeb exists, we want it for uniqueness too.
            unique_key.append(element['TextAtWeb'][0]['Text'])
        unique_key.append(element['Title'][0]['Text'])
        return '_'.join(unique_key)

    def _multilingual_text_at_web(self, parent):
        """
        Translate the value of a TextAtWeb entry to the appropriate language

        Args:
            parent: the structure containing values to be translated
        """
        name = 'TextAtWeb'
        if name in parent:
            lang_obj = dict([(e['Language'], e['Text']) for e in parent[name]])
            if self._language in lang_obj.keys():
                parent[name] = [{'URL': lang_obj[self._language]}]
            else:
                parent[name] = [{'URL': lang_obj[self._fallback_language]}]

    def _multilingual_text(self, parent, name):
        """
        Translate a value to the appropriate language

        Args:
            parent: the structure containing values to be translated
            name: the entry name to be translated
        """
        if name in parent:
            lang_obj = dict([(e['Language'], e['Text']) for e in parent[name]])
            if self._language in lang_obj.keys():
                parent[name] = lang_obj[self._language]
            else:
                parent[name] = lang_obj[self._fallback_language]

    @staticmethod
    def sort_restriction_on_landownership_documents(restriction_on_landownership):
        """
        sort legal provisioning, hints and laws on restriction_on_landownership

        Args:
            restriction_on_landownership (list(dict)): restrictions on landownership
        """
        for element in ['LegalProvisions', 'Laws', 'Hints']:
            restriction_on_landownership[element] = Renderer.sort_dict_list(
                restriction_on_landownership[element],
                Renderer.sort_by_index
            )

    @staticmethod
    def sort_dict_list(legend_list, sort_keys):
        """
        Sorts list of dictionaries by one or more sort keys.
        This function makes it possible to run test on the sorted list and assure the
        correctness of the sorting.

        Args:
            legend_list (list(dict)): list of legend dictionaries
            sort_keys (tuple/any): tuple of keys according to which the list of dictionaries will be
            sorted (at least one is needed)
        Returns:
            sorted list of legend dictionaries
        """
        return sorted(legend_list, key=sort_keys)

    @staticmethod
    def sort_legal_provision(elem):
        """
        Provides the sort key for the supplied legal provision element as a tuple consisting of:
         * title
         * Official number

        Args:
            elem (dict): one element of the legal provision list
        Returns:
            sort key (tuple)
        """

        sort_title = elem['Title'] if 'Title' in elem else ''
        sort_number = elem['OfficialNumber'] if 'OfficialNumber' in elem else None
        return sort_title, sort_number

    @staticmethod
    def sort_by_index(elem):
        """
        Provides the sort key for the supplied hint / law / legal provision
        element as a tuple consisting of:
        * index


        Notes:
            - index is defined by Interlis model OeREBKRM_V2_0 as range -1000..1000
            - "Index = None" if geolink_formatter processes entry from OEREBLEX that has no index
        Args:
            elem (dict): one element of the hints / laws / legal provisions list
        Returns:
            sort key (tuple)
        """
        index = elem.get('Index', 1000)
        if index is None:
            index = 1000
        return index

    @staticmethod
    def sort_legend_elem(elem):
        """
        Provides the sort key for the supplied legend element as a tuple consisting of:
         * rank of the geometry type as defined in LEGEND_ELEMENT_SORT_ORDER
         * value of the geometry if available (AreaShare and LengthShare)

        Args:
            elem (dict): legend entry

        Returns:
            sort key (tuple)
        """
        geom_type = elem['Geom_Type']

        if geom_type in LEGEND_ELEMENT_SORT_ORDER:
            # Get predefined order
            category = LEGEND_ELEMENT_SORT_ORDER.index(geom_type)
        else:
            # Put elements not found predefined order last
            category = len(LEGEND_ELEMENT_SORT_ORDER)

        # Use value as secondary criteria if available (defaults to 0 if not available).
        # Negative value for ascending sort order.
        value = -elem.get(geom_type, 0)

        return category, value

    def get_custom_wms_params(self, params):
        """
        From a given dictionary filter out all the parameters that are specified in the config
        and return these.
        Only values which exist in the given params are added.
        If there is nothing configured or the config is not a list
        the configured wms_url_params are used as fallback.

        Args:
            params (dict): Parameters available in the URL

        Returns:
            custom_params (dict): dictionary of filtered params
        """
        wms_url_params = Config.get('print', {}).get('wms_url_keep_params', False)
        if not isinstance(wms_url_params, list):
            # If no config exists or config is not as expected fall back to use standard wms_url_params
            return self.get_wms_url_params()

        custom_params = {
            wms_keys: self.string_check(wms_values)
            for wms_keys, wms_values in params.items()
            if wms_keys in wms_url_params
        }
        return custom_params

    @staticmethod
    def string_check(value):
        """
        Check if the value given is a string.
        If it is not, assume it is a list and join the values using comma separator.

        Args:
            value (str or list): value to be treated.

        Returns:
            (str): converted value
        """
        return value if isinstance(value, str) else ','.join(value)

    def set_global_datetime(self, date_time):
        """
        Set/initialize the class variable global_datetime with a given date-time
        Args:
            value (str): date value of the format Y-m-dTH:M:S'
        """
        try:
            self.global_datetime = datetime.strptime(date_time, self.global_datetime_format)
        except PdfReadError as e:
            err_msg = f'Not able to set the datetime. Expected date-time format is: \
                {self.global_datetime_format}. Given date-time value is: {date_time}'
            log.error(err_msg + ': ' + str(e))
            raise HTTPInternalServerError(self._static_error_message)
