import datetime
import os
import traceback
from calendar import monthrange
from collections import OrderedDict
from email.header import Header
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from io import BytesIO
from pathlib import Path
from pprint import pprint
from typing import Union
from threading import Thread
from email.utils import formataddr
from dateutil.relativedelta import relativedelta

import cv2
import numpy as np
import pandas as pd
from PIL import Image, ImageDraw, ImageFont
import smtplib
from concurrent.futures import ThreadPoolExecutor

from BoschRpaMagicBox.smb_functions import *
from openpyxl.utils import column_index_from_string

from mini_rpa_core import MiniRPACore

card_template_cache = {}


def copy_as_new_file(from_folder_path: str, from_file_name: str, update_folder_path: str, update_file_name: str, from_period: str, user_name: str, user_password: str,
                     server_name: str, share_name: str, port: int):
    """This function is used to copy files from from_folder or sub_folder to update folder

    Args:

        from_folder_path: This is the from_folder_path
        from_file_name: This is the file name that contains common file name fragment
        update_folder_path: This is the target folder path
        update_file_name: This is the file name of update file
        from_period(str): This is the start period
        user_name(str): This is the username
        user_password(str): This is the password
        server_name(str):This is the server name (url), e.g. szh0fs06.apac.bosch.com
        share_name(str): This is the share_name of public folder, e.g. GS_ACC_CN$
        port(int): This is the port number of the server name
    """
    from_file_extension = Path(from_file_name).suffix
    save_update_file_name = f"{update_file_name}{from_period}.{from_file_extension}"

    from_file_path = from_folder_path + os.sep + from_file_name
    update_file_path = update_folder_path + os.sep + save_update_file_name

    is_from_file_exist, from_file_obj = smb_check_file_exist(user_name, user_password, server_name, share_name, from_file_path, port)

    if is_from_file_exist:
        smb_store_remote_file_by_obj(user_name, user_password, server_name, share_name, update_file_path, from_file_obj, port)
        print(f'--------------- copy file for {from_file_path} to {update_file_path}---------------')
    else:
        print('Target file is not found！')


def hrs_calculate_duration(hrs_time_data: Union[pd.DataFrame, None], from_column_name: str, from_period: str, new_column_name: str, ) -> pd.DataFrame:
    """This function is used to calculate time difference between values of from column and today

    Args:
        hrs_time_data(pd.DataFrame): This is the hrs time related data
        from_column_name:This is the column name
        from_period(str): This is the start period
        new_column_name: This is the new column that will record compare result
    """
    hrs_time_data[from_column_name].fillna('', inplace=True)
    hrs_time_data[from_column_name] = hrs_time_data[from_column_name].apply(MiniRPACore.prepare_date_info)
    # hrs_time_data[from_column_name] = hrs_time_data[from_column_name].astype(str)
    # hrs_time_data[from_column_name] = hrs_time_data[from_column_name].str.strip().str.split(' ', expand=True)[0]
    # hrs_time_data[from_column_name] = (pd.to_datetime(hrs_time_data[from_column_name], errors='coerce')).dt.date
    for row_index in hrs_time_data.index:
        row_data = hrs_time_data.loc[row_index]
        previous_date = row_data[from_column_name]
        if not pd.isna(previous_date) and previous_date:
            if from_period:
                # current_date = datetime.datetime.strptime(f'{from_period[:4]}-{from_period[4:6]}-{from_period[6:8]}', '%Y-%m-%d').date()
                current_date = MiniRPACore.prepare_date_info(from_period)
            else:
                current_date = datetime.datetime.now().date()
            day_duration = (current_date - previous_date).days
            year_duration = current_date.year - previous_date.year
            # hrs_time_data.loc[row_index, new_column_name] = f'{day_duration} days'
            hrs_time_data.loc[row_index, new_column_name] = day_duration
            if previous_date.month == current_date.month:
                if previous_date.day == current_date.day and year_duration > 0:
                    hrs_time_data.loc[row_index, 'Annivesary'] = 'Yes'
                    hrs_time_data.loc[row_index, 'Annivesary Years'] = f'{year_duration}'
                elif previous_date.month == 2 and previous_date.day == 29 and monthrange(current_date.year, current_date.month)[1] == 28 and current_date.day == 28:
                    hrs_time_data.loc[row_index, 'Annivesary'] = 'Yes'
                    hrs_time_data.loc[row_index, 'Annivesary Years'] = f'{year_duration}'
                else:
                    hrs_time_data.loc[row_index, 'Annivesary'] = 'No'
            else:
                hrs_time_data.loc[row_index, 'Annivesary'] = 'No'
        else:
            hrs_time_data.loc[row_index, 'Annivesary'] = 'No'
    return hrs_time_data


def read_image_from_bytesio(card_obj: BytesIO, image_file_path: str):
    """ Read image from BytesIO

    Args:
        card_obj(BytesIO): This is the BytesIO object
        image_file_path(str): This is the file path of image

    """

    byte_array = np.frombuffer(card_obj.getvalue(), np.uint8)

    flag = cv2.IMREAD_COLOR
    img_bgr = cv2.imdecode(byte_array, flag)
    if img_bgr is None:
        raise ValueError(f"Unable to decode image: {image_file_path}")

    has_alpha = img_bgr.shape[2] == 4

    if has_alpha:
        img_rgb = cv2.cvtColor(img_bgr, cv2.COLOR_BGRA2RGBA)
    else:
        img_rgb = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2RGB)

    return Image.fromarray(img_rgb)


def hrs_generate_email_content(service_year, birthday_year, card_type, user_name, seq_id, template_folder_path,
                               smb_user_name, user_password, server_name, share_name, port):
    """ Initialization parameters

    Args:
        service_year(str): This is the server year value
        birthday_year(str): This is the birthday year
        user_name(str): This is the username
        seq_id(int): This is the sequence id
        template_folder_path(str): This is the template folder path
        smb_user_name(str): This is the username
        user_password(str): This is the password
        server_name(str):This is the server name (url), e.g. szh0fs06.apac.bosch.com
        share_name(str): This is the share_name of public folder, e.g. GS_ACC_CN$
        port(int): This is the port number of the server name
        card_type(str): This is the card type
    """
    try:
        global card_template_cache
        new_img_prename = f'add_text_{seq_id}'
        new_img_fullname = os.path.join(template_folder_path, f'add_text_{seq_id}.jpg')

        font_path = "/opt/SourceHanSans.ttc"
        font = ImageFont.truetype(font_path, 80, index=1)

        if card_type == 'Service':
            card_path = template_folder_path + os.sep + 'Card Template' + os.sep + f'{service_year}-Card.jpg'
        else:
            card_path = template_folder_path + os.sep + 'Card Template' + os.sep + f'{birthday_year}-Card.jpg'

        card_obj: Union[BytesIO, None] = card_template_cache.get(card_path, None)

        if not card_obj:
            return {'is_successful': False, 'email_content': 'No card template,please check!'}
        else:
            byte_io = BytesIO()
            img_pil = read_image_from_bytesio(card_obj, card_path)
            draw = ImageDraw.Draw(img_pil)
            draw.text((5150, 800), user_name, font=font, fill=(0, 0, 0), stroke_width=4, stroke_fill=(0, 0, 0))
            bk_img = cv2.cvtColor(np.array(img_pil), cv2.COLOR_RGB2BGR)

            success, encoded_image = cv2.imencode('.jpg', bk_img, [int(cv2.IMWRITE_JPEG_QUALITY), 95])
            if success:
                byte_io.write(encoded_image.tobytes())
                byte_io.seek(0)

            smb_store_remote_file_by_obj(smb_user_name, user_password, server_name, share_name, new_img_fullname, byte_io, port)
            email_content = f'''
                            <body>                                                     
                            <p><img src=cid:{new_img_prename} alt=newimg_prename></p>
                            </body>
                        '''

            return {'is_successful': True, 'email_content': email_content, 'image_bytes': byte_io}
    except:
        return {'is_successful': False, 'email_content': traceback.format_exc()}


def prepare_email_message(email_message, email_content_template_data, seq_id):
    """ Prepare email message

    Args:
        email_message(MIMEMultipart): This is the email message
        email_content_template_data(dict): This is the email content template data
        seq_id(int): This is the sequence id
    """
    content = MIMEText(email_content_template_data['email_content'], 'html', 'utf-8')
    email_message.attach(content)

    img_prename = f'add_text_{seq_id}'
    msg_image_bytes = email_content_template_data['image_bytes']
    msg_image = MIMEImage(msg_image_bytes.getvalue())

    # set image id as img_prename
    msg_image.add_header('Content-ID', img_prename)
    email_message.attach(msg_image)

    return email_message


def hrs_send_html_content_email(mail_host, mail_user, mail_pass, email_to, email_cc, email_header, email_subject, service_year, birthday_year, card_type, user_name,
                                sender, seq_id, template_folder_path, smb_user_name, user_password, server_name, share_name, port):
    """ Send email with html content

    Args:
        mail_host (str): The SMTP server address for sending emails.
        mail_user (str): The username for authenticating with the SMTP server.
        mail_pass (str): The password or authentication token for the SMTP server.
        email_to (list): The primary recipient(s) of the email.
        email_cc (list): The carbon copy (CC) recipient(s) of the email.
        email_header (str): The header or display name to use for the email.
        email_subject (str): The subject line of the email.
        service_year (str): The service year for which the email is being generated (e.g., employee milestone year).
        birthday_year (str): The birthday year for which the email is being generated.
        user_name (str): The full name of the user (in the local language) being addressed in the email.
        sender (str): The email address of the sender.
        seq_id (int): A unique identifier for the email sequence, used for tracking or logging.
        template_folder_path(str): This is the template folder path
        smb_user_name(str): This is the username
        user_password(str): This is the password
        server_name(str):This is the server name (url), e.g. szh0fs06.apac.bosch.com
        share_name(str): This is the share_name of public folder, e.g. GS_ACC_CN$
        port(int): This is the port number of the server name
        card_type(str): This is the card type

    """
    try:
        smtp_obj = smtplib.SMTP(mail_host, 25)
        # connect to server
        smtp_obj.starttls()
        # login in server
        smtp_obj.login(mail_user, mail_pass)

        to_receivers = ','.join(email_to)
        cc_receivers = ','.join(email_cc)

        # set email content
        message = MIMEMultipart()

        message = MIMEMultipart()
        if email_header.strip():
            message["From"] = Header(email_header, "utf-8")
        else:
            message['From'] = formataddr((str(Header(email_header, 'utf-8')), sender))

        # message['From'] = Header(email_header, 'utf-8')
        message['To'] = to_receivers
        message['Cc'] = cc_receivers
        message['Subject'] = email_subject

        email_content_template_data = hrs_generate_email_content(service_year, birthday_year, card_type, user_name, seq_id, template_folder_path, smb_user_name, user_password,
                                                                 server_name, share_name, port)
        if email_content_template_data['is_successful']:
            try:
                message = prepare_email_message(message, email_content_template_data, seq_id)

                # send
                smtp_obj.sendmail(from_addr=sender, to_addrs=email_to + email_cc, msg=message.as_string())

                # quit
                smtp_obj.quit()
                print(f'-----email is sent successfully to {email_to[0]}!-----')
            except:
                print(f'-----try again to send email to {email_to[0]}!-----')
                message = prepare_email_message(message, email_content_template_data, seq_id)

                # send
                smtp_obj.sendmail(from_addr=sender, to_addrs=email_to + email_cc, msg=message.as_string())

                # quit
                smtp_obj.quit()
        else:
            print(f'Email template was generated failed,please check from the log file!')
            print(f"{user_name}-{service_year}: Failed to generate email template!\n{email_content_template_data['email_content']}")
    except:
        print(f'Failed to send email to {email_to[0]}')
        print(traceback.format_exc())


def hrs_send_anniversary_email(card_type, anniversary_year_column, email_to_column, user_name_column, email_cc, email_subject, email_header, email_account, email_password,
                               email_address, anniversary_file_path, template_folder_path, birthday_year, smb_user_name, user_password, server_name, share_name, port):
    """ Send anniversary email

    Args:
        anniversary_year_column(str): This is the anniversary year column name
        email_to_column(str): This is the email to column name
        user_name_column(str): This is the username column name
        email_cc(list): This is the email cc list
        email_subject(str): This is the email subject
        email_header(str): This is the email header
        email_account(str): This is the email account
        email_password(str): This is the email password
        email_address(str): This is the email address
        anniversary_file_path(str): This is the file path
        smb_user_name(str): This is the username
        user_password(str): This is the password
        server_name(str):This is the server name (url), e.g. szh0fs06.apac.bosch.com
        share_name(str): This is the share_name of public folder, e.g. GS_ACC_CN$
        port(int): This is the port number of the server name
        template_folder_path(str): This is the template folder path
        birthday_year(str): This is the birthday year
        card_type(str): This is the card type
    """
    # mail_host = 'rb-smtp-int.bosch.com'
    mail_host = 'rb-smtp-auth.rbesz01.com'
    mail_user = email_account
    mail_pass = email_password
    sender = email_address

    file_obj = smb_load_file_obj(smb_user_name, user_password, server_name, share_name, anniversary_file_path, port)

    anniversary_data = pd.read_excel(file_obj, dtype={email_to_column: str, user_name_column: str, anniversary_year_column: str})
    anniversary_data.fillna('', inplace=True)
    for column in [email_to_column, user_name_column, anniversary_year_column]:
        anniversary_data[column] = anniversary_data[column].str.strip()

    if anniversary_data.empty:
        print('No data found in the anniversary file!')
    else:
        global card_template_cache

        card_folder_path = template_folder_path + os.sep + 'Card Template'

        traverse_result_list = smb_traverse_remote_folder(smb_user_name, user_password, server_name, share_name, card_folder_path)
        for traverse_result_dict in traverse_result_list:
            is_file = traverse_result_dict['is_file']
            if is_file:
                file_name = traverse_result_dict['name']
                card_file_path = card_folder_path + os.sep + file_name
                _, card_obj = smb_check_file_exist(smb_user_name, user_password, server_name, share_name, card_file_path, port)
                card_template_cache[card_file_path] = card_obj

        # for row_index in anniversary_data.index:
        #     row_data = anniversary_data.loc[row_index]
        #
        #     email_to = [row_data[email_to_column]]
        #
        #     if email_to:
        #         # Log in and send the email. Handle both Chinese and English names.
        #         service_year, user_name, seq_id = row_data[anniversary_year_column], row_data[user_name_column].split('/')[0], row_index
        #
        #         thr = Thread(target=hrs_send_html_content_email,
        #                      args=[mail_host, mail_user, mail_pass, email_to, email_cc, email_header, email_subject, service_year, birthday_year, card_type, user_name, sender,
        #                            seq_id, template_folder_path, smb_user_name, user_password, server_name, share_name, port])
        #         thr.start()

        with ThreadPoolExecutor(max_workers=10) as executor:
            for row_index in anniversary_data.index:
                row_data = anniversary_data.loc[row_index]
                email_to = [row_data[email_to_column]]

                if email_to:
                    service_year = row_data[anniversary_year_column]
                    user_name = row_data[user_name_column].split('/')[0]
                    seq_id = row_index

                    executor.submit(
                        hrs_send_html_content_email,
                        mail_host, mail_user, mail_pass,
                        email_to, email_cc, email_header, email_subject,
                        service_year, birthday_year, card_type, user_name,
                        sender, seq_id, template_folder_path,
                        smb_user_name, user_password, server_name, share_name, port
                    )


def hrs_merge_weekly_rehiring_data(username, password, server_name, share_name, rehiring_folder_path, rehiring_sheet_name, save_folder_path, port=445, text_column_names=''):
    """ This function merges weekly rehiring data from a specified SMB share into a single output file.

    Args:
        username(str): The username for SMB authentication.
        password(str): The password for SMB authentication.
        server_name(str): The name of the SMB server.
        share_name(str): The name of the SMB share.
        rehiring_folder_path(str): The path to the rehiring folder on the SMB share.
        rehiring_sheet_name(str): The name of the sheet in the rehiring Excel files to be merged.
        save_folder_path(str): The path to the save folder on the SMB share.
        port(int): The port number for the SMB connection.
        text_column_names(list, optional): A list of column names that should be treated as text in the merged DataFrame. Defaults to None.
    """
    current_date = datetime.datetime.now().date()
    str_date_list = [str((current_date - relativedelta(days=i)).strftime('%Y%m%d')) for i in range(7)]
    rehiring_name_list = [f'Rehiring_{str_date}' for str_date in str_date_list]
    rehiring_file_list = smb_traverse_remote_folder(username, password, server_name, share_name, rehiring_folder_path, port)
    rehiring_data_list = []

    text_column_name_list = text_column_names.replace('，', ',').split(',')
    text_column_name_list = [column_name.strip() for column_name in text_column_name_list if column_name.strip()]
    text_column_name_dict = {column_name: str for column_name in text_column_name_list}
    for file_dict in rehiring_file_list:
        if file_dict['is_file']:
            file_name = file_dict['name']
            if str(file_name).startswith(tuple(rehiring_name_list)):
                file_path = rehiring_folder_path + os.sep + file_name
                file_obj = smb_load_file_obj(username, password, server_name, share_name, file_path, port)
                if text_column_name_dict:
                    rehiring_data = pd.read_excel(file_obj, header=3, sheet_name=rehiring_sheet_name, dtype=text_column_name_dict)
                else:
                    rehiring_data = pd.read_excel(file_obj, header=3, sheet_name=rehiring_sheet_name)

                rehiring_data['Rehiring File Name'] = file_name
                if not rehiring_data.empty:
                    rehiring_data_list.append(rehiring_data)

    if rehiring_data_list:
        merged_rehiring_data = pd.concat(rehiring_data_list, ignore_index=True)
        output_file_name = f'Rehiring_{current_date.strftime("%Y%m%d")}.xlsx'
        output_file_path = os.path.join(save_folder_path, output_file_name)

        file_obj = BytesIO()
        with pd.ExcelWriter(file_obj, engine='xlsxwriter') as writer:
            merged_rehiring_data.to_excel(writer, index=False, float_format='%.2f', sheet_name='Sheet1')
        file_obj.seek(0)

        smb_store_remote_file_by_obj(username, password, server_name, share_name, output_file_path, file_obj, port)
        print(f'Merged rehiring data saved to {output_file_path}.')
    else:
        print('No rehiring data found for the specified dates.')


def hrs_compare_excel_data(username, password, server_name, share_name, from_data, from_key_column, update_data, update_key_column, config_folder_path, config_file_name,
                           config_sheet_name, port=445):
    """ This function compares rehiring data from the last two weeks and returns the differences.

    Args:
        username(str): The username for SMB authentication.
        password(str): The password for SMB authentication.
        server_name(str): The name of the SMB server.
        share_name(str): The name of the SMB share.
        from_data(pd.DataFrame): The DataFrame containing the original data to compare from.
        from_key_column(str): The name of the key column in the original data for comparison.
        update_data(pd.DataFrame): The DataFrame containing the updated data to compare against.
        update_key_column(str): The name of the key column in the updated data for comparison.
        config_folder_path(str): The path to the folder containing the configuration file for column mappings.
        config_file_name(str): The name of the configuration file containing the column mappings.
        config_sheet_name(str): The name of the sheet in the configuration file.
        port(int): The port number for the SMB connection.
    """
    config_file_path = os.path.join(config_folder_path, config_file_name)
    config_file_obj = smb_load_file_obj(username, password, server_name, share_name, config_file_path, port)
    config_data = pd.read_excel(config_file_obj, sheet_name=config_sheet_name, dtype=str)
    config_data.fillna('', inplace=True)
    for column_name in config_data.columns:
        config_data[column_name] = config_data[column_name].str.strip()
        if column_name in ['Source Column Index', 'Target Column Index', 'Comparison Result Display']:
            config_data[column_name] = config_data[column_name].str.upper()

    source_display_column_dict = OrderedDict()
    target_display_column_dict = OrderedDict()
    display_data = config_data[config_data['Comparison Result Display'] == 'Y']
    if not display_data.empty:
        for index, row in display_data.iterrows():
            source_column_index = row['Source Column Index']
            source_column_name = row['Source Column Name']
            target_column_index = row['Target Column Index']
            source_display_column_dict[source_column_index] = source_column_name
            target_display_column_dict[target_column_index] = source_column_name

    config_data = config_data[config_data['Comparison Result Display'] != 'Y']
    config_data.set_index('Source Column Index', inplace=True)
    all_config_dict = config_data.to_dict(orient='index')

    if not all_config_dict:
        raise ValueError("Configuration data is empty. Please check the configuration file.")
    if from_data.empty or update_data.empty:
        raise ValueError("Input data is empty. Please provide valid DataFrames for comparison.")

    from_data = from_data.fillna('')
    update_data = update_data.fillna('')
    from_data_columns_dict = {index: column_name for index, column_name in enumerate(from_data.columns.tolist())}
    update_data_columns_dict = {index: column_name for index, column_name in enumerate(update_data.columns.tolist())}
    # pprint(from_data_columns_dict)
    # pprint(update_data_columns_dict)

    from_column_by_data = set(from_data[from_key_column].tolist())
    update_column_by_data = set(update_data[update_key_column].tolist())

    check_result_list = []

    common_column_by_data = from_column_by_data.intersection(update_column_by_data)
    from_diff_to_update = from_column_by_data.difference(update_column_by_data)
    update_diff_to_from = update_column_by_data.difference(from_column_by_data)

    for column_by_type, column_by_data in {'common': common_column_by_data, 'from': from_diff_to_update, 'update': update_diff_to_from}.items():
        for column_by_value in column_by_data:
            if column_by_type == 'common':
                from_row_data = from_data[from_data[from_key_column] == column_by_value].to_dict('records')
                update_row_data = update_data[update_data[update_key_column] == column_by_value].to_dict('records')
            elif column_by_type == 'from':
                from_row_data = from_data[from_data[from_key_column] == column_by_value].to_dict('records')
                update_row_data = [{}]
            else:
                from_row_data = [{}]
                update_row_data = update_data[update_data[update_key_column] == column_by_value].to_dict('records')

            for from_row_dict in from_row_data:
                for update_row_dict in update_row_data:
                    for source_column_index, config_item_dict in all_config_dict.items():
                        source_column_name = config_item_dict['Source Column Name']
                        target_column_index = config_item_dict['Target Column Index']
                        target_column_name = config_item_dict['Target Column Name']

                        from_pd_column_index = column_index_from_string(source_column_index) - 1
                        update_pd_column_index = column_index_from_string(target_column_index) - 1

                        from_column_name = from_data_columns_dict[from_pd_column_index]
                        update_column_name = update_data_columns_dict[update_pd_column_index]

                        from_value = from_row_dict.get(from_column_name, '')
                        update_value = update_row_dict.get(update_column_name, '')

                        if from_value != update_value:
                            check_result = OrderedDict()
                            display_column_dict = source_display_column_dict if column_by_type in ['common', 'from'] else target_display_column_dict
                            for display_column_index, display_column_name in display_column_dict.items():
                                if column_by_type in ['common', 'from']:
                                    check_result[display_column_name] = from_row_dict[from_data_columns_dict[column_index_from_string(display_column_index) - 1]]
                                else:
                                    check_result[display_column_name] = update_row_dict[update_data_columns_dict[column_index_from_string(display_column_index) - 1]]

                            check_result.update({
                                '源数据报错信息栏位': source_column_name,
                                '源数据': from_value,
                                '对比数据报错信息栏位': target_column_name,
                                '对比数据': update_value,
                            })
                            check_result_list.append(check_result)

    check_result_df = pd.DataFrame(check_result_list)
    for column_name in check_result_df.columns:
        if column_name not in ['源数据报错信息栏位', '对比数据报错信息栏位', '源数据', '对比数据']:
            check_result_df[column_name] = check_result_df[column_name].astype(str).str.strip()

    return check_result_df
