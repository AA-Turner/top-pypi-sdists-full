from django.db import connection, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cornerstone', '0024_auto_20221031_1855'),
    ]

    db_engine = connection.settings_dict['ENGINE']

    if 'sqlite3' in db_engine:
        operations = [
            migrations.AlterIndexTogether(
                name='cornerstonelearnerdatatransmissionaudit',
                index_together={('enterprise_customer_uuid', 'plugin_configuration_id')},
            ),
        ]
    else:
        if 'postgresql' in db_engine:
            operations = [
                migrations.SeparateDatabaseAndState(
                    state_operations=[
                        migrations.AlterIndexTogether(
                            name='cornerstonelearnerdatatransmissionaudit',
                            index_together={('enterprise_customer_uuid', 'plugin_configuration_id')},
                        ),
                    ],
                    database_operations=[
                        migrations.RunSQL(sql="""
                            CREATE INDEX cornerstone_cldta_85936b55_idx
                            ON cornerstone_cornerstonelearnerdatatransmissionaudit (enterprise_customer_uuid, plugin_configuration_id)
                        """, reverse_sql="""
                            DROP INDEX cornerstone_cldta_85936b55_idx
                        """),
                    ]
                ),
            ]
        else:
            # For MySQL or other non-sqlite and non-postgresql backends
            operations = [
                migrations.SeparateDatabaseAndState(
                    state_operations=[
                        migrations.AlterIndexTogether(
                            name='cornerstonelearnerdatatransmissionaudit',
                            index_together={('enterprise_customer_uuid', 'plugin_configuration_id')},
                        ),
                    ],
                    database_operations=[
                        migrations.RunSQL(sql="""
                            CREATE INDEX cornerstone_cldta_85936b55_idx
                            ON cornerstone_cornerstonelearnerdatatransmissionaudit (enterprise_customer_uuid, plugin_configuration_id)
                            ALGORITHM=INPLACE LOCK=NONE
                        """, reverse_sql="""
                            DROP INDEX cornerstone_cldta_85936b55_idx
                            ON cornerstone_cornerstonelearnerdatatransmissionaudit
                        """),
                    ],
                ),
            ]
