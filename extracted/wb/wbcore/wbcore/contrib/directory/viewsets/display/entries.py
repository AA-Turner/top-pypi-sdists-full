from typing import Optional

from django.utils.translation import gettext as _

from wbcore.metadata.configs import display as dp
from wbcore.metadata.configs.display.instance_display import (
    Display,
    Inline,
    Layout,
    Page,
    Section,
    Style,
    create_simple_display,
)
from wbcore.metadata.configs.display.instance_display.operators import default, lte
from wbcore.metadata.configs.display.view_config import DisplayViewConfig


class EntryModelDisplay(DisplayViewConfig):
    def get_instance_display(self) -> Display:
        return create_simple_display([["computed_str"]])


# CONTACT_PAGE = Page(
#     title=_("Contacts"),
#     layouts={
#         default(): Layout(
#             grid_template_areas=[
#                 ["addresses_table", "addresses_table"],
#                 ["telephones_table", "emails_table"],
#                 ["websites_table", "social_media_table"],
#                 ["bankings_table", "bankings_table"],
#                 ["relationships_table", "relationships_table"],
#             ],
#             grid_auto_rows=Style.AUTO,
#             grid_template_rows=[
#                 "200px",
#                 "200px",
#                 "200px",
#                 "200px",
#                 "200px",
#             ],
#             inlines=[
#                 Inline(
#                     key="addresses_table",
#                     endpoint="addresses",
#                     title="Addresses",
#                 ),
#                 Inline(
#                     key="telephones_table",
#                     endpoint="telephones",
#                     title="Telephones",
#                 ),
#                 Inline(
#                     key="emails_table",
#                     endpoint="emails",
#                     title="Emails",
#                 ),
#                 Inline(
#                     key="websites_table",
#                     endpoint="websites",
#                     title="Websites",
#                 ),
#                 Inline(
#                     key="bankings_table",
#                     endpoint="bankings",
#                     title="Banking",
#                 ),
#                 Inline(
#                     key="social_media_table",
#                     endpoint="social_media",
#                     title="Socials",
#                 ),
#                 Inline(
#                     key="relationships_table",
#                     endpoint="relationships",
#                     title="Relationships",
#                 ),
#             ],
#         ),
#     },
# )
contact_section = Section(
    key="contact_section",
    collapsible=False,
    title=_("Contacts"),
    display=Display(
        pages=[
            Page(
                title=_("Telephones"),
                layouts={
                    default(): Layout(
                        grid_template_areas=[["telephone_table"]],
                        inlines=[Inline(key="telephone_table", endpoint="telephones")],
                    )
                },
            ),
            Page(
                title=_("Emails"),
                layouts={
                    default(): Layout(
                        grid_template_areas=[["email_table"]],
                        inlines=[Inline(key="email_table", endpoint="emails")],
                    )
                },
            ),
            Page(
                title=_("Addresses"),
                layouts={
                    default(): Layout(
                        grid_template_areas=[["addresses_table"]],
                        inlines=[Inline(key="addresses_table", endpoint="addresses")],
                    )
                },
            ),
            Page(
                title=_("Websites"),
                layouts={
                    default(): Layout(
                        grid_template_areas=[["website_table"]],
                        inlines=[Inline(key="website_table", endpoint="websites")],
                    )
                },
            ),
            Page(
                title=_("Bankings"),
                layouts={
                    default(): Layout(
                        grid_template_areas=[["banking_table"]],
                        inlines=[Inline(key="banking_table", endpoint="bankings")],
                    )
                },
            ),
            Page(
                title=_("Socials"),
                layouts={
                    default(): Layout(
                        grid_template_areas=[["socials_table"]],
                        inlines=[Inline(key="socials_table", endpoint="social_media")],
                    )
                },
            ),
            Page(
                title=_("Relationships"),
                layouts={
                    default(): Layout(
                        grid_template_areas=[["relationship_table"]],
                        inlines=[Inline(key="relationship_table", endpoint="relationships")],
                    )
                },
            ),
        ]
    ),
)


class PersonModelDisplay(EntryModelDisplay):
    @classmethod
    def _get_person_instance_display(cls) -> Display:
        """Returns a person instance's display

        Returns:
            Display: The display instance
        """

        employers_section = Section(
            key="employers_section",
            collapsible=False,
            title=_("Employers"),
            display=Display(
                pages=[
                    Page(
                        title=_("Employers"),
                        layouts={
                            default(): Layout(
                                grid_template_areas=[["employers_table"]],
                                inlines=[Inline(key="employers_table", endpoint="employers")],
                            )
                        },
                    ),
                ]
            ),
        )

        return Display(
            pages=[
                Page(
                    title=_("Main Information"),
                    layouts={
                        default(): Layout(
                            grid_template_areas=[
                                ["profile_image", "prefix", "specializations", "activity_table"],
                                ["profile_image", "first_name", "last_name", "activity_table"],
                                ["profile_image", "primary_email", "primary_telephone", "activity_table"],
                                ["profile_image", "activity_heat", "activity_heat", "activity_table"],
                                [
                                    "personality_profile_red",
                                    "personality_profile_green",
                                    "personality_profile_blue",
                                    "activity_table",
                                ],
                                ["employers_section", "employers_section", "employers_section", "contact_section"],
                            ],
                            grid_template_columns=[
                                Style.MIN_CONTENT,
                                "minmax(min-content, 1fr)",
                                "minmax(min-content, 1fr)",
                                "50%",
                            ],
                            grid_template_rows=[Style.rem(6), Style.rem(6), Style.rem(6), Style.rem(6)],
                            grid_auto_rows=Style.MIN_CONTENT,
                            sections=[employers_section, contact_section],
                            inlines=[
                                Inline(
                                    key="activity_table",
                                    endpoint="wbcrm_activity",
                                    title="Activities",
                                    hide_controls=True,
                                ),
                            ],
                        ),
                        lte(1100): Layout(
                            grid_template_areas=[
                                ["profile_image", "prefix", "specializations"],
                                ["profile_image", "first_name", "last_name"],
                                ["profile_image", "primary_email", "primary_telephone"],
                                ["activity_heat", "activity_heat", "activity_heat"],
                                ["personality_profile_red", "personality_profile_green", "personality_profile_blue"],
                                ["employers_section", "employers_section", "employers_section"],
                            ],
                            grid_template_columns=[
                                Style.MIN_CONTENT,
                                "minmax(min-content, 1fr)",
                                "minmax(min-content, 1fr)",
                            ],
                            grid_auto_rows=Style.MIN_CONTENT,
                            sections=[employers_section],
                        ),
                        lte(700): Layout(
                            grid_template_areas=[
                                ["first_name"],
                                ["last_name"],
                                ["primary_email"],
                                ["primary_telephone"],
                                ["activity_heat"],
                            ],
                            grid_auto_columns="minmax(min-content, 1fr)",
                            grid_auto_rows=Style.MIN_CONTENT,
                        ),
                    },
                ),
                Page(
                    title=_("Additional Information"),
                    layouts={
                        default(): Layout(
                            grid_template_areas=[
                                ["salutation", "birthday", "formal", "."],
                                ["has_user_account", "last_connection", ".", "."],
                                ["description", "description", "description", "description"],
                            ],
                            grid_template_columns=[
                                "minmax(min-content, 1fr)",
                                "minmax(min-content, 1fr)",
                                "minmax(min-content, 1fr)",
                                "35%",
                            ],
                            grid_auto_rows=Style.MIN_CONTENT,
                            row_gap=Style.rem(5),
                            column_gap=Style.rem(4),
                        ),
                        lte(715): Layout(
                            grid_template_areas=[
                                ["salutation", "formal"],
                                ["birthday", "."],
                                ["has_user_account", "last_connection"],
                            ],
                            grid_template_columns=["minmax(min-content, 4fr)", "minmax(min-content, 1fr)"],
                            grid_auto_rows=Style.MIN_CONTENT,
                        ),
                        lte(550): Layout(
                            grid_template_areas=[
                                ["salutation"],
                                ["birthday"],
                                ["formal"],
                                ["has_user_account"],
                                ["last_connection"],
                            ],
                            grid_auto_columns=Style.MIN_CONTENT,
                            grid_auto_rows=Style.MIN_CONTENT,
                        ),
                    },
                ),
            ],
        )

    @classmethod
    def _get_new_person_instance_display(cls) -> Display:
        """Returns the display for creating a new person

        Returns:
            Display: The display instance
        """

        return Display(
            pages=[
                Page(
                    title=_("Main Information"),
                    layouts={
                        default(): Layout(
                            grid_template_areas=[
                                ["profile_image", "prefix", "specializations", "."],
                                ["profile_image", "first_name", "last_name", "."],
                                ["profile_image", "primary_email", "primary_telephone", "."],
                                ["profile_image", "primary_employer", "position_in_company", "."],
                                [".", "primary_manager", "position_name", "."],
                                [
                                    "personality_profile_red",
                                    "personality_profile_green",
                                    "personality_profile_blue",
                                    ".",
                                ],
                            ],
                            grid_template_columns=[
                                Style.MIN_CONTENT,
                                "minmax(min-content, 1fr)",
                                "minmax(min-content, 1fr)",
                                Style.fr(1),
                            ],
                            column_gap=Style.rem(4),
                            grid_auto_rows=Style.MIN_CONTENT,
                        ),
                        lte(800): Layout(
                            grid_template_areas=[
                                ["profile_image", "prefix"],
                                ["profile_image", "first_name"],
                                ["profile_image", "last_name"],
                                ["profile_image", "specializations"],
                                ["primary_email", "primary_telephone"],
                                ["primary_employer", "position_in_company"],
                                ["primary_manager", "position_name"],
                                ["personality_profile_red", "personality_profile_green"],
                                ["personality_profile_blue", "."],
                            ],
                            grid_template_columns=[Style.MIN_CONTENT, "minmax(min-content, 1fr)"],
                            column_gap=Style.rem(2),
                            grid_auto_rows=Style.MIN_CONTENT,
                        ),
                        lte(450): Layout(
                            grid_template_areas=[
                                ["prefix"],
                                ["first_name"],
                                ["last_name"],
                                ["specializations"],
                                ["primary_email"],
                                ["primary_telephone"],
                                ["primary_employer"],
                                ["position_in_company"],
                                ["position_name"],
                                ["primary_manager"],
                                ["personality_profile_red"],
                                ["personality_profile_green"],
                                ["personality_profile_blue"],
                                ["prefix"],
                                ["first_name"],
                                ["last_name"],
                                ["specializations"],
                                ["primary_email"],
                                ["primary_telephone"],
                                ["primary_manager"],
                                ["personality_profile_red"],
                                ["personality_profile_green"],
                                ["personality_profile_blue"],
                            ],
                            grid_auto_columns="minmax(min-content, 1fr)",
                            grid_auto_rows=Style.MIN_CONTENT,
                        ),
                    },
                ),
                Page(
                    title=_("Additional Information"),
                    layouts={
                        default(): Layout(
                            grid_template_areas=[
                                ["salutation", "birthday", "formal", "."],
                            ],
                            grid_template_columns=[
                                "minmax(min-content, 1fr)",
                                "minmax(min-content, 1fr)",
                                "minmax(min-content, 1fr)",
                                "25%",
                            ],
                            grid_auto_rows=Style.MIN_CONTENT,
                            column_gap=Style.rem(5),
                        ),
                        lte(650): Layout(
                            grid_template_areas=[
                                ["birthday", "birthday"],
                                ["salutation", "formal"],
                            ],
                            grid_auto_columns="minmax(min-content, 1fr)",
                            grid_auto_rows=Style.MIN_CONTENT,
                        ),
                        lte(370): Layout(
                            grid_template_areas=[
                                ["salutation"],
                                ["birthday"],
                                ["formal"],
                            ],
                            grid_auto_columns="minmax(min-content, 1fr)",
                            grid_auto_rows=Style.MIN_CONTENT,
                        ),
                    },
                ),
            ],
        )

    def get_list_display(self) -> Optional[dp.ListDisplay]:
        return dp.ListDisplay(
            fields=[
                dp.Field(key="name", label=_("Name")),
                dp.Field(key="customer_status", label=_("Status")),
                dp.Field(key="position_in_company", label=_("Position")),
                dp.Field(key="cities", label=_("City")),
                dp.Field(key="tier", label=_("Tier")),
                dp.Field(
                    key=None,
                    label=_("Primary Contacts"),
                    children=[
                        dp.Field(key="primary_employer_repr", label=_("Primary Employer")),
                        dp.Field(key="primary_manager_repr", label=_("Relationship Manager")),
                        dp.Field(key="primary_telephone", label=_("Telephone")),
                        dp.Field(key="primary_email", label=_("Email")),
                        dp.Field(key="primary_address", label=_("Address"), show="open"),
                        dp.Field(key="primary_website", label=_("Website"), show="open"),
                        dp.Field(key="primary_social", label=_("Social"), show="open"),
                    ],
                ),
                dp.Field(
                    key=None,
                    label=_("Last Event"),
                    children=[
                        dp.Field(key="last_event", label=_("Name")),
                        dp.Field(key="last_event_period_endswith", label=_("End Date")),
                    ],
                ),
                dp.Field(key="activity_heat", label=_("Activity Heat")),
            ],
        )

    AUM_TABLE: Section = []
    PORTFOLIO_FIELDS: Section = []

    def get_instance_display(self) -> Display:
        return (
            self._get_person_instance_display()
            if "pk" in self.view.kwargs
            else self._get_new_person_instance_display()
        )


class CompanyModelDisplay(EntryModelDisplay):
    @classmethod
    def _get_company_instance_display(cls, aum_table: Section, portfolio_fields: Section) -> Display:
        """Returns a company instance's display

        Args:
            aum_table: A section with an AUM by product inline table that will be imported when wbportfolio is installed. Can be empty.
            portfolio fields: A section containing a few portfolio fields that will be imported when wbportfolio is installed. Can be empty.

        Returns:
            Display: The display instance
        """

        employees_section = Section(
            key="employees_section",
            collapsible=False,
            title=_("Employees"),
            display=Display(
                pages=[
                    Page(
                        title=_("Employees"),
                        layouts={
                            default(): Layout(
                                grid_template_areas=[["employees_table"]],
                                inlines=[Inline(key="employees_table", endpoint="employees")],
                            )
                        },
                    ),
                ]
            ),
        )

        grid_template_areas = [
            ["profile_image", "name", "customer_status", "activity_table"],
            ["profile_image", "primary_telephone", "primary_telephone", "activity_table"],
            ["profile_image", "type", "tier", "activity_table"],
            ["profile_image", "activity_heat", "activity_heat", "activity_table"],
            ["employees_section", "employees_section", "employees_section", "contact_section"],
        ]
        sections = [employees_section, contact_section]
        if portfolio_fields:
            grid_template_areas.insert(
                4,
                [
                    portfolio_fields.key,
                    portfolio_fields.key,
                    portfolio_fields.key,
                    "activity_table",
                ],
            )
            sections.append(portfolio_fields)
        if aum_table:
            grid_template_areas.append([aum_table.key, aum_table.key, aum_table.key, aum_table.key])
            sections.append(aum_table)

        return Display(
            pages=[
                Page(
                    title=_("Main Information"),
                    layouts={
                        default(): Layout(
                            grid_template_areas=grid_template_areas,
                            grid_template_columns=[
                                Style.MIN_CONTENT,
                                "minmax(min-content, 1fr)",
                                "minmax(min-content, 1fr)",
                                "50%",
                            ],
                            grid_template_rows=[Style.rem(6), Style.rem(6), Style.rem(6)],
                            grid_auto_rows=Style.MIN_CONTENT,
                            sections=sections,
                            inlines=[
                                Inline(
                                    key="activity_table",
                                    endpoint="wbcrm_activity",
                                    title="Activities",
                                    hide_controls=True,
                                ),
                            ],
                        ),
                    },
                ),
                Page(
                    title=_("Additional Information"),
                    layouts={
                        default(): Layout(
                            grid_template_areas=[["salutation", "."], ["description", "description"]],
                            grid_template_columns=["minmax(min-content, 1fr)", "minmax(min-content, 2fr)"],
                            grid_auto_rows=Style.MIN_CONTENT,
                        )
                    },
                ),
            ]
        )

    @classmethod
    def _get_new_company_instance_display(cls) -> Display:
        """Returns the display for creating a new company

        Returns:
            Display: The display instance
        """

        return Display(
            pages=[
                Page(
                    title=_("Main Information"),
                    layouts={
                        default(): Layout(
                            grid_template_areas=[
                                ["profile_image", "name", "customer_status", "."],
                                ["profile_image", "primary_email", "primary_telephone", "."],
                                ["profile_image", "primary_manager", "type", "."],
                            ],
                            grid_template_columns=[
                                Style.MIN_CONTENT,
                                "minmax(min-content, 1fr)",
                                "minmax(min-content, 1fr)",
                                Style.fr(1),
                            ],
                            grid_auto_rows=Style.MIN_CONTENT,
                            gap=Style.rem(5),
                        ),
                    },
                ),
                Page(
                    title=_("Additional Information"),
                    layouts={
                        default(): Layout(
                            grid_template_areas=[["salutation", "."], ["description", "description"]],
                            grid_template_columns=["minmax(min-content, 1fr)", "minmax(min-content, 2fr)"],
                            grid_auto_rows=Style.MIN_CONTENT,
                            gap=Style.rem(5),
                        )
                    },
                ),
            ],
        )

    def get_list_display(self) -> Optional[dp.ListDisplay]:
        return dp.ListDisplay(
            fields=[
                dp.Field(key="name", label=_("Name")),
                dp.Field(key="cities", label=_("City")),
                dp.Field(key="type", label=_("Type")),
                dp.Field(key="tier", label=_("Tier")),
                dp.Field(key="customer_status", label=_("Status")),
                dp.Field(
                    key=None,
                    label=_("Primary Contacts"),
                    children=[
                        dp.Field(key="primary_manager_repr", label=_("Relationship Manager")),
                        dp.Field(key="primary_telephone", label=_("Telephone")),
                        dp.Field(key="primary_email", label=_("Email")),
                        dp.Field(key="primary_address", label=_("Address"), show="open"),
                        dp.Field(key="primary_website", label=_("Website"), show="open"),
                        dp.Field(key="primary_social", label=_("Social"), show="open"),
                    ],
                ),
                dp.Field(
                    key=None,
                    label=_("Last Event"),
                    children=[
                        dp.Field(key="last_event", label=_("Name")),
                        dp.Field(key="last_event_period_endswith", label=_("Date")),
                    ],
                ),
                dp.Field(key="activity_heat", label=_("Activity Heat")),
            ]
        )

    AUM_TABLE: Section = []
    PORTFOLIO_FIELDS: Section = []

    def get_instance_display(self) -> Display:
        return (
            self._get_company_instance_display(self.AUM_TABLE, self.PORTFOLIO_FIELDS)
            if "pk" in self.view.kwargs
            else self._get_new_company_instance_display()
        )


class BankModelDisplay(CompanyModelDisplay):
    def get_list_display(self) -> Optional[dp.ListDisplay]:
        return dp.ListDisplay(
            fields=[
                dp.Field(key="primary_manager_repr", label=_("Primary Relationship Manager")),
                dp.Field(key="name", label=_("Name")),
                dp.Field(key="primary_telephone", label=_("Telephone")),
                dp.Field(key="primary_email", label=_("Email")),
                dp.Field(key="primary_address", label=_("Address")),
            ]
        )


class UserIsManagerDisplayConfig(DisplayViewConfig):
    def get_list_display(self) -> Optional[dp.ListDisplay]:
        return dp.ListDisplay(
            fields=[
                dp.Field(key="computed_str", label=_("Name")),
                dp.Field(key="primary_telephone", label=_("Primary Telephone")),
                dp.Field(key="primary_email", label=_("Primary Email")),
                dp.Field(key="primary_address", label=_("Primary Address")),
            ]
        )
