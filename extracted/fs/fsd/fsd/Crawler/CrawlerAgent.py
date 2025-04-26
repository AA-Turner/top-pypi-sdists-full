import time
import logging
from firecrawl import FirecrawlApp


logger = logging.getLogger(__name__)

class CrawlerAgent:
    def __init__(self):
        self.api_keys = [
            "fc-b2462dec87ac47a4a25945ad44da8a07",
            "fc-b0fe3bcb36b64a2f9a144eb2373af19b",
            "fc-ce5f3e7178184ee387e17e9de608781f",
            "fc-f844ba081d1b4c3787936998d58143ca",
            "fc-883a10252439454784529feb36b0e0ed",
            "fc-e43993f41fc940e6b3eeae053e6c75fb",
            "fc-7855953536c14556a1d904a6df6bc919",
            "fc-917fdc49eb53445bb4333d329a337991",
            "fc-8c4ab10abd5445339150ca32d0fc898c",
            "fc-21bba5a0e54a408fbe8c95d99de9bdcf",
            "fc-82b0007f304b42478772d8fae5378990",
            "fc-56a943ef0adc409a81d3407ba7cf0168",
            "fc-d1db63d5e9574d92816e956719e35377",
            "fc-4a00097486e447f796186f0b3fade9f3",
            "fc-b1bda3fc979a44f28b5d954a32a01333",
            "fc-b856cbf292c6494798f4140f78c91f79",
            "fc-7009195a7bdc4d5fa0ec728d19c0247a",
            "fc-82f8f915efe14ba6bb17cccb2c10aaf5",
            "fc-3a3650077e59418b88e130e977f1a33b",
            "fc-bb3b9499589343c2bdac37bf13019012",
            "fc-40b2c1ecbc7349309c3634f77a475948",
            "fc-f41f3536cb8446c8827385ed2169eabd",
            "fc-af0a86f9060b4554b185865683d1b229",
            "fc-b1784bb32e9c46529e0e8019b72019f4",
            "fc-2893ba6ba4bb4d77ae15707bba2be421",
            "fc-e69b7b15327c42aab2c6fecdccc7dc5f",
            "fc-aba319d27a374e3098f4754016733b99",
            "fc-6d1beba51ebb472f8d589af84792c1af",
            "fc-56556023851e4dacbeb4964591d4fc4d",
            "fc-496c6b50e0f14f7eb92b96c432e87fc0",
            "fc-31b200ba51544f87ba90f1ccdcaf02d0",
            "fc-2ec05d42440748f68f0afe60826debb8",
            "fc-5e5fc884eb294d85858782f5f22c1db0",
            "fc-9e40a48ce7194ff18307fb152ea4c83b",
            "fc-33168ba324b2484d8076d6a4bf86b0c1",
            "fc-f1e90ca4afb2417a9fac85af6e9b9868",
            "fc-909935d67d964416a4afbb83101052c9",
            "fc-0416dc8cd4bb47dabfd540d14808a46f",
            "fc-163d0e83de0949eb8fd61fc8b495e540",
            "fc-6efca70ac9a845b781591403ac8fe81d",
            "fc-9c48dd9aa2ed4c34833b1133aad64837",
            "fc-6ead5d04f7b548188fc464b0deca4ec5",
            "fc-e8b1a40ccc3a4441bef80cfd03e45adf",
            "fc-df392c7626794854874ec12ec0278cc2",
            "fc-806e0a884ec04557b1edd98faa9098da",
            "fc-469179deab9646c4b660d114a4419565",
            "fc-2d58ee0a31e54c2db0efc74be482c7dc",
            "fc-dcd6df40eaf3472f98851aacf3501f73",
            "fc-1144ab2473914ba2991c37b4ad314509",
            "fc-f0911b8cf50242848e317200d07f9eef",
            "fc-f3c1836e2ebc4624906e7a24f18248ff",
            "fc-60afd8a733bf40489ed9f628d2ae1b8f",
            "fc-4be9ca8c6fd14735922bc7ca8a95b0f6",
            "fc-4c5dfc793d2745f1a0906d598601375c",
            "fc-5e0d5100cdf344e3acc8fa015aeae619",
            "fc-619b321fc23e43399adbde0f53547ca1",
            "fc-61236a5b57aa42c291dd8ad123e8e0c8",
            "fc-523b2fb935f243c0840f278019138139",
            "fc-e9faba8f42a044e5b090db65c2023869",
            "fc-b17966b5acf14d069ced7e530173dadc",
            "fc-0e1f57fbe25444899ade7d9877ac28c6",
            "fc-bc0e498456054dcbaefc59907614be60",
            "fc-ac111322c3424d55b08fe7e4cf53b53d",
            "fc-0235d54b991a45ff97ba2a83c2e65c8a",
            "fc-e600c07f7850462ab1010dabc2e05d15",
            "fc-aa728a5d300e4f28895949e29fe70353",
            "fc-105812982a054756bab76acda0d64e20",
            "fc-72e7cf9d8929402e94c6a5f32eca73af",
            "fc-d09d0d94c4d24b4088406dfce1c9a06b",
            "fc-abf20db54e474d48bc8558a707f87eee",
            "fc-2db9ba8712c241ea80c9d3b7ae5fbf27",
            "fc-87e7d81261d94d29b7427afac98d638b",
            "fc-f81764974e20468dbebaf2a9d9e80055",
            "fc-6f51ccf7a3d14005885d0a202728ad0c",
            "fc-98ab41f405704b529e201bcaeefc3a7c",
            "fc-3178aabe8c104d4387ecf9ac4d4a86e1",
            "fc-0c0cbb74485940289e356cd45cad8cb5",
            "fc-880fea932575433a8c661fcc102cf57d",
            "fc-8d0ea065e1f84c179b1db5938f803cbf",
            "fc-1a3be8cf7a064893907033a4d5952522",
            "fc-538f998d869f45988e347f25f74f4308",
            "fc-2dd3a1d9bc924aad9b8757e1c0ff82c3",
            "fc-2660a493cdb0404abe14439e7a73702a",
            "fc-251b6d1d91ac4de38d144981d3ce6cbe",
            "fc-91c234953e9b481c89adb6206e468a7f",
            "fc-dfdc2833ead545fcafe5876c806a3ee2",
            "fc-294f8f5dd84d4e4987128478e4a955ae",
            "fc-f5ecef6d528244758f23f654c9c44be9",
            "fc-8145075322eb45c1a2790c8bde03f6b6",
            "fc-865371f88e644020af5643c69b2e968b",
            "fc-8c2e8892bfce40ceac2bda27e7fda04b",
            "fc-b328d84e2c8e45fbb750e22dba0db1c1",
            "fc-b0ffae5535004c158ffde8d9dbf3f224",
            "fc-e6a9d71147f6411984d8780d5c3bd642",
            "fc-f354a7241d7b4a8db940b0ac24a6d13c",
            "fc-bde49f14638c46e6a172a2f01bcf49ab",
            "fc-1d8d950f775341e7817fbc3df626eeb8",
            "fc-4f839453a6e3462791bc7adebd2a8626",
            "fc-781f904acb78448180b6e091ceb59e9c",
            "fc-e9d7a79a580648979117f73248ba2a57"
        ]
        self.current_key_index = 0
        self.app = self.create_app()

    def create_app(self):
        return FirecrawlApp(api_key=self.api_keys[self.current_key_index])

    def get_next_key(self):
        self.current_key_index = (self.current_key_index + 1) % len(self.api_keys)
        return self.api_keys[self.current_key_index]

    def crawl_website(self, website_url, format='markdown'):
        params = {
            'limit': 1,
            'scrapeOptions': {
                'formats': [format.lower()]
            },
        }

        for _ in range(len(self.api_keys)):
            try:
                crawl_status = self.app.async_crawl_url(website_url, params=params)
                crawl_id = crawl_status.get('id')
                if not crawl_id:
                    logger.debug("\n #### `SnowX` failed to initiate the crawl: No crawl ID was returned.")
                    raise Exception("Failed to initiate crawl")
                logger.info(" #### `SnowX` has commenced the reading process!")

                while True:
                    status = self.app.check_crawl_status(crawl_id)
                    logger.info(f" #### `SnowX` reports current reading status: `{status.get('status')}`")
                    if status.get('status') == 'completed':
                        break
                    elif status.get('status') == 'failed':
                        raise Exception("Crawl failed")
                    time.sleep(2.5)

                final_status = self.app.check_crawl_status(crawl_id)
                results = final_status.get('data')
                if results:
                    return results
                else:
                    raise Exception("No results retrieved")

            except Exception as e:
                logger.debug(f" #### `SnowX` encountered an error during the reading process: `{e}`")
                new_key = self.get_next_key()
                logger.info(f" #### Switching to new API key: {new_key}")
                self.app = self.create_app()

        logger.error(f"  All API keys exhausted. Crawl failed.")
        return None

    def process(self, website_url):
        results = self.crawl_website(website_url, 'markdown')
        if results is None:
            logger.debug("\n #### `SnowX` reports that the crawling process has failed.")
            return None

        return results
