from navigator.views import BaseView
from navigator.responses import FileResponse
from ...conf import MARKETPLACE_DIR


class PluginHandler(BaseView):
    async def put(self):
        """put.

        Upload a Component into Marketplace, sign-in component and register into Metadata database.
        """

    async def get(self):
        """
        List all Components or getting one component (metadata or download).
        """
        params = self.match_parameters()
        try:
            option = params["option"]
        except KeyError:
            option = "component"
        try:
            component = params["component"]
        except KeyError:
            component = None
        if component:
            ### First Step, try to look out if "component" exists on Plugins.components directory
            component_file = MARKETPLACE_DIR.joinpath(f"{component}.py")
            signature_file = MARKETPLACE_DIR.joinpath(f"{component}.py.sign")
            checksum_file = MARKETPLACE_DIR.joinpath(f"{component}.py.checksum")
            if component_file.exists():
                ### TODO: add validations if able to see this component:
                file_list = [component_file, signature_file, checksum_file]
                return await FileResponse(
                    file=file_list, request=self.request, status=200
                )
            else:
                return self.error(
                    response="Component {component} doesn't exists on Marketplace.",
                    status=404,
                )

        else:
            ### getting a list of components:
            return self.no_content()
