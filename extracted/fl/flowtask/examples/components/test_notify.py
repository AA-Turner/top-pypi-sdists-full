import asyncio
from flowtask.components.SendNotify import SendNotify


async def main():
    notify = SendNotify(
        via='email',
        account={
            'hostname': 'NAVIGATOR_ALERT_EMAIL_HOSTNAME',
            'port': "NAVIGATOR_ALERT_EMAIL_PORT",
            'password': 'NAVIGATOR_ALERT_EMAIL_PASSWORD',
            'username': 'NAVIGATOR_ALERT_EMAIL_USERNAME'
        },
        masks={
            "{human-today}": [
                'today',
                {
                    'mask': "%m/%d/%Y",
                    'tz': 'America/New_York'
                }
            ]
        },
        recipients=[
            {
                'name': 'Jesus Lara',
                'account': {
                    'address': 'jlara@trocglobal.com'
                }
            }
        ],
        message={
            'subject': "Link to the EPSON slides in SharePoint ({human-today})",
            'template': 'email_upload_sharepoint.html',
            'clientName': 'EPSON',
            'dateGenerated': "{human-today}"
        }
    )
    async with notify as cp:
        # Working with the Component:
        try:
            result = await cp.run()
            print(len(result), type(result))
            # print('RESULT >> ')
            # print(result)
        except Exception as e:
            print(f'Error: {e}')

if __name__ == '__main__':
    asyncio.run(main())
