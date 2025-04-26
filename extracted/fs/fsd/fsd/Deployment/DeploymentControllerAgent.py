import os
import sys
import random
import string
from .DeploymentCheckAgent import DeploymentCheckAgent

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from fsd.log.logger_config import get_logger

logger = get_logger(__name__)

class DeploymentControllerAgent:
    def __init__(self, repo):
        self.repo = repo
        self.deploymentCheckAgent = DeploymentCheckAgent(repo)

    async def get_started_deploy_pipeline(self):
        logger.info(" #### `SnowX` is checking if the current project is eligible for deployment")
        check_result = await self.deploymentCheckAgent.get_deployment_check_plans()
        logger.debug(check_result)
        result = check_result.get('result')
        
        if result in ["0", 0]:
            logger.info(" #### `SnowX` has determined that this project is not supported for deployment at this time!")
        elif result in ["1", 1]:
            path = check_result.get('full_project_path')
            if path != "null":
                project_type = check_result.get('project_type')
                logger.info(" #### This project is eligible for deployment. `SnowX` is proceeding with deployment now.")
                # Generate a valid subdomain name
                valid_chars = string.ascii_lowercase + string.digits + '-'
                name_subdomain = ''.join(random.choices(valid_chars, k=random.randint(5, 15)))
                
                # Ensure the subdomain doesn't start or end with a hyphen
                name_subdomain = name_subdomain.strip('-')
                
                # Ensure the subdomain is at least 2 characters long
                while len(name_subdomain) < 2:
                    name_subdomain += random.choice(string.ascii_lowercase)
                
                # Ensure the subdomain is no longer than 63 characters (DNS limitation)
                name_subdomain = name_subdomain[:63]
                self.repo.deploy_to_server(path, "zinley.site", name_subdomain, project_type)
                logger.info(f"#### Your project is now live! Click [HERE](https://{name_subdomain}.zinley.site) to visit.")
                logger.info("#### Deployment successful!")
            else:
                logger.info(" #### Unable to deploy. Please try again!")