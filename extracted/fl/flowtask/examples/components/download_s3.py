import asyncio
from flowtask.components.DownloadFromS3 import DownloadFromS3

async def test_placer():
    try:
        ds3 = DownloadFromS3(
            credentials={
                "use_credentials": True,
                "region_name": "AWS_REGION_NAME",
                "bucket": "AWS_PLACER_BUCKET",
                "aws_key": "AWS_ACCESS_KEY_ID",
                "aws_secret": "AWS_SECRET_ACCESS_KEY"
            },
            source={
                "file": "metrics_2024-12-09_0003.csv.gz",
                "directory": "placer-analytics/bulk-export/monthly-weekly/2024-12-09/metrics/"
            },
            destination={
                "directory": "/home/ubuntu/symbits/placerai/metrics"
            }
        )
    except Exception as e:
        print(f'Error creating component: {e}')
        return
    async with ds3 as comp: # noqa
        print(' :: Starting Component ::')
        try:
            result = await comp.run()
            print(len(result), type(result))
            print('RESULT >> ')
            print(result)
        except Exception as e:
            print(f'Error: {e}')

async def test_component():
    try:
        ds3 = DownloadFromS3(
            credentials={
                "use_credentials": True,
            },
            config="placer",
            region_name="us-east-2",
            bucket="placer-navigator-data",
            source={
                "file": "metrics_2024-12-09_0002.csv.gz",
                "directory": "placer-analytics/bulk-export/monthly-weekly/2024-12-09/metrics/"
            },
            destination={
                "directory": "/home/ubuntu/symbits/placerai/metrics"
            }
        )
    except Exception as e:
        print(f'Error creating component: {e}')
        return
    async with ds3 as comp: # noqa
        print(' :: Starting Component ::')
        try:
            result = await comp.run()
            print(len(result), type(result))
            print('RESULT >> ')
            print(result)
        except Exception as e:
            print(f'Error: {e}')


if __name__ == '__main__':
    asyncio.run(test_placer())
