from typing import TYPE_CHECKING

from wbcore.metadata.configs import display as dp

if TYPE_CHECKING:
    from wbcore.contrib.permission.viewsets import PivotUserObjectPermissionModelViewSet


class PivotUserObjectPermissionDisplayViewConfig(dp.DisplayViewConfig):
    view: "PivotUserObjectPermissionModelViewSet"

    def get_list_display(self) -> dp.ListDisplay:
        return dp.ListDisplay(
            fields=[
                dp.Field(key="userref", label="User", width=250),
                *[
                    dp.Field(
                        key=permission.codename,
                        label=permission.name,
                        width=150,
                        formatting_rules=[
                            dp.FormattingRule(style={"backgroundColor": "#FF6961"}, condition=("==", False)),
                            dp.FormattingRule(style={"backgroundColor": "#77DD77"}, condition=("==", True)),
                        ],
                    )
                    for permission in self.view.permissions
                ],
            ],
            formatting=[
                dp.Formatting(
                    column="non_editable",
                    formatting_rules=[dp.FormattingRule(style={"color": "gray"}, condition=("==", True))],
                )
            ],
        )

    def get_instance_display(self) -> dp.Display:
        gta = [["userref"]]

        for permission in self.view.permissions:
            gta.append([permission.codename])

        return dp.create_simple_display(grid_template_areas=gta)
