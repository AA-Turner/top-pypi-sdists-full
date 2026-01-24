from typing import Callable
from sqlparse.sql import Token
from sqlparse import tokens as TOKEN

from adam.utils import log_exc
from adam.utils_repl.state_machine import StateMachine, State

__all__ = [
    'SqlStateMachine', 'CqlStateMachine', 'AthenaStateMachine'
]

SQL_SPEC = [
    # <select_statement> ::= SELECT <select_list>
    #                      FROM <table_expression>
    #                      [WHERE <search_condition>]
    #                      [<group_by_clause>]
    #                      [<having_clause>]
    #                      [<order_by_clause>]
    #                      [<limit_clause>]

    # <search_condition> ::= <boolean_term>
    #                      | <search_condition> OR <boolean_term>

    # <boolean_term> ::= <boolean_factor>
    #                  | <boolean_term> AND <boolean_factor>

    # <boolean_factor> ::= [NOT] <predicate>
    #                    | ([NOT] <search_condition>)

    # <predicate> ::= <comparison_predicate>
    #               | <between_predicate>
    #               | <in_predicate>
    #               | <like_predicate>
    #               | <null_predicate>
    #               | <exists_predicate>
    #               | <quantified_predicate>
    #               | <unique_predicate>
    #               | <match_predicate>
    #               | <overlaps_predicate>
    #               | <distinct_predicate>
    #               | <member_predicate>
    #               | <submultiset_predicate>
    #               | <set_predicate>

    # <comparison_predicate> ::= <row_value_expression> <comparison_operator> <row_value_expression>
    # <comparison_operator> ::= '=' | '<>' | '<' | '<=' | '>' | '>='

    # <row_value_expression> ::= <value_expression>
    #                          | (<value_expression> [ { <comma> <value_expression> }... ])

    # <value_expression> ::= <numeric_value_expression>
    #                      | <string_value_expression>
    #                      | <datetime_value_expression>
    #                      | <interval_value_expression>
    #                      | <boolean_value_expression>
    #                      | <user_defined_type_value_expression>
    #                      | <reference_value_expression>
    #                      | <collection_value_expression>
    #                      | <row_value_constructor>
    #                      | <case_expression>
    #                      | <cast_expression>
    #                      | <subquery>
    #                      | NULL
    #                      | DEFAULT
    #                      | <identifier>
    #                      | <literal>
    '                                > select           > select                                  ^ select,insert,update,delete,alter,preview',
    'select_                         > name|*           > select_a                                ^ *',
    'select_a                        > ,                > select_a_comma_',
    'select_a_comma_                 > name|*           > select_a                                ^ *',
    'select_a_                       > from             > select_from                             ^ from',
    'select_from_                    > name|audit       > select_from_x                           ^ (select,tables',
    '-                               > (                > select_from_lp_',
    '-                               < )                > select_from_sq',
    'select_from_lp_                 > select           > select',
    'select_from_x                   > ,                > select_from_x_comma_                    ^ (select,tables',
    '-                               > ;                > ',
    'select_from_sq_                 > as               > select_from_x_as                        ^ as',
    'select_from_x_comma_            > name|audit       > select_from_x                           ^ tables',
    'select_from_x_                                                                               ^ as,where,inner join,left outer join,right outer join,full outer join,group by,order by,limit,&',
    'select_from_x_as_x_             > ,                > select_from_x_comma_                    ^ where,inner join,left outer join,right outer join,full outer join,group by,order by,limit,&',
    '-                               > as               > select_from_x_as',
    '-                               > where            > select_where',
    '-                               > order            > select_order',
    '-                               > order by         > select_order_by',
    '-                               > limit            > select_where_sc_limit',
    '-                               > group            > select_group',
    '-                               > group by         > select_group_by',
    '-                               > inner            > select_from_x_inner',
    '-                               > inner join       > select_join',
    '-                               > left             > select_from_x_left',
    '-                               > left join        > select_join',
    '-                               > left outer join  > select_join',
    '-                               > right            > select_from_x_right',
    '-                               > right join       > select_join',
    '-                               > right outer join > select_join',
    '-                               > full             > select_from_x_full',
    '-                               > full outer join  > select_join',
    '-                               > ;                > ',
    '-                               > &                > select_from_x$',
    'select_from_x_as_               > name             > select_from_x_as_x                      ^ x,y,z',
    'select_from_x_as_x              > ,                > select_from_x_as_x_comma_',
    '-                               > ;                > ',
    'select_from_x_as_x_comma_       > name|audit       > select_from_x                           ^ tables',
    'select_where_                   > name             > select_where_a                          ^ columns',
    'select_where_a                  > name             > select_where_a                          ^ columns,=,<,<=,>,>=,<>',
    '-                               > comparison       > select_where_a_op',
    'select_where_a_                 > comparison       > select_where_a_op                       ^ =,<,<=,>,>=,<>,like,not,in',
    '-                               > not              > select_where_a_not',
    '-                               > in               > select_where_a_in',
    'select_where_a_not_             > comparison       > select_where_a_not_op                   ^ like,in',
    '-                               > in               > select_where_a_in',
    'select_where_a_in               > (                > select_where_a_in_lp_                   ^ (',
    '-                               < )                > select_where_sc',
    'select_where_a_in_lp_           > name|single|num  > select_where_a_in_lp_a                  ^ single,select',
    '-                               > select           > select_where_a_in_lp_select',
    'select_where_a_in_lp_select_    > name             > select_a                                ^ id',
    'select_where_a_in_lp_a          > ,                > select_where_a_in_lp_a_comma_           ^ comma,)',
    'select_where_a_in_lp_a_comma_   > name|single|num  > select_where_a_in_lp_a                  ^ single',
    'select_where_a_not_op           > name|single|num  > select_where_sc                         ^ single',
    'select_where_a_op               > name|single|num  > select_where_sc                         ^ single',
    'select_where_sc                 > ;                > ',
    'select_where_sc_                > and|or           > select_where                            ^ and,or,order by,group by,limit,&',
    '-                               > group            > select_group',
    '-                               > group by         > select_group_by',
    '-                               > order            > select_order',
    '-                               > order by         > select_order_by',
    '-                               > limit            > select_where_sc_limit',
    '-                               > ;                > ',
    '-                               > &                > select_from_x$',
    'select_group_                   > by               > select_group_by                         ^ by',
    'select_group_by_                > name             > select_group_by_a                       ^ columns',
    'select_group_by_a               > ,                > select_group_by_a_comma_                ^ columns',
    '-                               > ;                > ',
    'select_group_by_a_comma_        > name             > select_group_by_a                       ^ columns',
    'select_group_by_a_              > limit            > select_where_sc_limit                   ^ limit,order by,&',
    '-                               > order            > select_order',
    '-                               > order by         > select_order_by',
    '-                               > ;                > ',
    '-                               > &                > select_from_x$',
    'select_order_                   > by               > select_order_by                         ^ by',
    'select_order_by_                > name             > select_order_by_a                       ^ columns',
    'select_order_by_a               > ,                > select_order_by_a_comma_',
    '-                               > ;                > ',
    'select_order_by_a_comma_        > name             > select_order_by_a                       ^ columns',
    'select_order_by_a_              > desc|asc         > select_order_by_a_desc                  ^ desc,asc,limit,&',
    '-                               > limit            > select_where_sc_limit',
    '-                               > ;                > ',
    '-                               > &                > select_from_x$',
    'select_order_by_a_desc          > ,                > select_order_by_a_comma_',
    '-                               > ;                > ',
    'select_order_by_a_desc_         > limit            > select_where_sc_limit                   ^ limit,&',
    '-                               > ;                > ',
    '-                               > &                > select_from_x$',
    'select_where_sc_limit_          > num              > select_where_sc_limit_num               ^ 1',
    'select_where_sc_limit_num       > ;                > ',
    'select_where_sc_limit_num_rp__  > as               > select_from_x_as                        ^ as',
    'select_where_x_inner_           > join             > select_join',
    'select_join_                    > name|audit       > select_x_join_y                         ^ tables',
    'select_from_x_left_             > join             > select_join                             ^ outer join',
    '-                               > outer            > select_from_x_left_outer',
    'select_from_x_left_outer_       > join             > select_join                             ^ join',
    'select_from_x_right_            > join             > select_join                             ^ outer join',
    '-                               > outer            > select_from_x_right_outer',
    'select_from_x_right_outer_      > join             > select_join                             ^ join',
    'select_from_x_full_             > join             > select_join                             ^ outer join',
    '-                               > outer            > select_from_x_full_outer',
    'select_from_x_full_outer_       > join             > select_join                             ^ join',
    'select_x_join_y_                > as               > select_x_join_y_as                      ^ as,on',
    '-                               > on               > select_x_join_y_on                      ^ as,on',
    'select_x_join_y_as_             > name             > select_x_join_y_as_y                    ^ x,y,z',
    'select_x_join_y_as_y_           > on               > select_x_join_y_on                      ^ on',
    'select_x_join_y_on_             > name             > select_x_join_y_on_a                    ^ columns',
    'select_x_join_y_on_a            > name             > select_x_join_y_on_a                    ^ columns,=',
    '-                               > comparison       > select_x_join_y_on_a_op',
    'select_x_join_y_on_a_           > comparison       > select_x_join_y_on_a_op                 ^ =',
    'select_x_join_y_on_a_op         > name             > select_x_join_y_on_a_op_b               ^ columns',
    'select_x_join_y_on_a_op_b       > _                > select_from_x_as_x_',
    '-                               > ;                > ',

    # <insert_statement> ::= INSERT INTO <table_name> [ ( <column_list> ) ]
    #                        VALUES ( <value_list> )
    #                      | INSERT INTO <table_name> [ ( <column_list> ) ]
    #                        <query_expression>

    # <table_name> ::= <identifier>

    # <column_list> ::= <column_name> [ , <column_list> ]

    # <column_name> ::= <identifier>

    # <value_list> ::= <expression> [ , <value_list> ]

    # <query_expression> ::= SELECT <select_list> FROM <table_reference_list> [ WHERE <search_condition> ] [ GROUP BY <grouping_column_list> ] [ HAVING <search_condition> ] [ ORDER BY <sort_specification_list> ]
    '                                > insert           > insert',
    'insert_                         > into             > insert_into                             ^ into',
    'insert_into_                    > name|audit       > insert_into_x                           ^ tables',
    'insert_into_x                   > (                > insert_into_x_lp_',
    'insert_into_x_                  > (                > insert_into_x_lp_                       ^ (,values(',
    '-                               > values           > insert_values',
    'insert_into_x_lp_               > name             > insert_into_x_lp_a                      ^ id',
    'insert_into_x_lp_a              > ,                > insert_into_x_lp_a_comma_',
    '-                               > )                > insert_into_x_lp_a_rp_',
    'insert_into_x_lp_a_comma_       > name             > insert_into_x_lp_a                      ^ id',
    'insert_into_x_lp_a_rp__         > values           > insert_values                           ^ values(,select',
    '-                               > select           > select',
    'insert_values                   > (                > insert_values_lp_',
    'insert_values_lp_               > name|single|num  > insert_values_lp_v                      ^ single',
    'insert_values_lp_v              > ,                > insert_values_lp_v_comma_',
    '-                               > )                > insert_values_lp_v_rp_',
    'insert_values_lp_v_comma_       > name|single|num  > insert_values_lp_v',
    'insert_values_lp_v_rp__         > &                > insert_values_lp_v_rp_$                 ^ &',

    # <update_statement> ::= UPDATE <table_name>
    #                        SET <set_clause_list>
    #                        [WHERE <search_condition>]

    # <set_clause_list> ::= <set_clause> { , <set_clause> }

    # <set_clause> ::= <column_name> = <update_value>

    # <update_value> ::= <expression> | NULL | DEFAULT

    # <search_condition> ::= <boolean_expression>
    '                                > update           > update',
    'update_                         > name|audit       > update_x                                ^ tables',
    'update_x_                       > set              > update_set                              ^ set',
    'update_set_                     > name             > update_set_a                            ^ id',
    'update_set_a                    > comparison       > update_set_a_op',
    'update_set_a_op                 > name|single|num  > update_set_sc                           ^ single',
    'update_set_sc                   > ,                > update_set_sc_comma_',
    'update_set_sc_comma_            > name             > update_set_a                            ^ id',
    'update_set_sc_                  > ,                > update_set_sc_comma_                    ^ where,&',
    '-                               > where            > update_where',
    '-                               > &                > update_set_sc$                          ^ &',
    'update_where_                   > name             > update_where_a                          ^ id',
    'update_where_a                  > comparison       > update_where_a_op',
    'update_where_a_                 > comparison       > update_where_a_op                       ^ =,<,<=,>,>=,<>,like,not,in',
    '-                               > not              > update_where_a_not',
    '-                               > in               > update_where_a_in',
    'update_where_a_not_             > comparison       > update_where_a_not_op                   ^ like,in',
    '-                               > in               > update_where_a_in',
    'update_where_a_in               > (                > update_where_a_in_lp_                   ^ (',
    '-                               < )                > update_where_sc',
    'update_where_a_in_lp_           > name|single|num  > update_where_a_in_lp_a                  ^ single,select',
    '-                               > select           > update_where_a_in_lp_select',
    'update_where_a_in_lp_select_    > name             > select_a                                ^ id',
    'update_where_a_in_lp_a          > ,                > update_where_a_in_lp_a_comma_           ^ comma,)',
    'update_where_a_in_lp_a_comma_   > name|single|num  > update_where_a_in_lp_a                  ^ single',
    'update_where_a_not_op           > name|single|num  > update_where_sc                         ^ single',
    'update_where_a_op               > name|single|num  > update_where_sc                         ^ single',
    'update_where_sc_                > and|or           > update_where                            ^ and,or,&',

    # <delete_statement> ::= DELETE FROM <table_name> [ WHERE <search_condition> ]

    # <table_name> ::= <identifier>

    # <search_condition> ::= <boolean_expression>

    # <boolean_expression> ::= <predicate>
    #                      | <boolean_expression> AND <predicate>
    #                      | <boolean_expression> OR <predicate>
    #                      | NOT <predicate>
    #                      | ( <boolean_expression> )

    # <predicate> ::= <expression> <comparison_operator> <expression>
    #              | <expression> IS NULL
    #              | <expression> IS NOT NULL
    #              | <expression> LIKE <pattern> [ ESCAPE <escape_character> ]
    #              | <expression> IN ( <expression_list> )
    #              | EXISTS ( <select_statement> )
    #              | ... (other predicates)

    # <comparison_operator> ::= = | <> | != | > | < | >= | <=

    # <expression> ::= <literal>
    #               | <column_name>
    #               | <function_call>
    #               | ( <expression> )
    #               | <expression> <arithmetic_operator> <expression>
    #               | ... (other expressions)

    # <literal> ::= <numeric_literal> | <string_literal> | <boolean_literal> | <date_literal> | ...

    # <column_name> ::= <identifier>

    # <identifier> ::= <letter> { <letter> | <digit> | _ }...

    # <pattern> ::= <string_literal>

    # <escape_character> ::= <string_literal> (single character)

    # <expression_list> ::= <expression> { , <expression> }...
    '                                > delete           > delete',
    'delete_                         > from             > delete_from                             ^ from',
    'delete_from_                    > name|audit       > delete_from_x                           ^ tables',
    'delete_from_x_                  > where            > update_where                            ^ where',

    # <alter table action> ::=
    #     ADD <column definition>
    #     | DROP COLUMN <column name>
    #     | MODIFY COLUMN <column name> <column modification>
    #     | RENAME TO <new table name>
    #     | ADD CONSTRAINT <constraint definition>
    #     | DROP CONSTRAINT <constraint name>
    #     | ... (other actions like adding/dropping indexes, partitions, etc.)

    # <column definition> ::= <column name> <data type> [ <column constraint> ... ]

    # <column modification> ::=
    #     SET DATA TYPE <data type>
    #     | SET DEFAULT <expression>
    #     | DROP DEFAULT
    #     | SET NOT NULL
    #     | DROP NOT NULL
    #     | ...

    # <constraint definition> ::=
    #     PRIMARY KEY ( <column name list> )
    #     | UNIQUE ( <column name list> )
    #     | FOREIGN KEY ( <column name list> ) REFERENCES <referenced table> ( <referenced column list> )
    #     | CHECK ( <search condition> )

    '                                > alter              > alter',
    'alter_                          > table              > alter_table                             ^ table',
    'alter_table_                    > name|audit|cluster > alter_table_t                           ^ tables',
    'alter_table_t_                  > add                > alter_table_add                         ^ add,add constraint,drop column,drop constraint,rename to',
    '-                               > drop               > alter_table_drop',

    '                                > preview            > preview',
    'preview_                        > name|audit         > preview_t                               ^ tables',
]

SQL_KEYWORDS = [
    'select', 'from', 'as', 'not', 'in', 'where',
    'and', 'or', 'group', 'by', 'group by', 'order', 'order by', 'limit', 'asc', 'desc',
    'inner join', 'on', 'left', 'right', 'full', 'outer', 'left outer join',
    'left join', 'right outer join', 'right join', 'full join', 'full outer join',
    'insert', 'into', 'values',
    'update', 'where', 'set',
    'delete',
    'audit', 'cluster',
    'alter', 'table', 'tables', 'add', 'drop', 'with',
    'describe', 'preview'
]

EXPANDABLE_NAMES = {'keyspaces', 'tables', 'columns', 'partition-columns', 'table-props', 'table-props-values'}

CQL_SPEC = SQL_SPEC + [
    '                                > select           > select                                  ^ select,insert,update,delete,alter,describe,preview,consistency,export,import,drop,clean',

    # ALTER TABLE [ <keyspace_name> . ] <table_name>
    #     ( ALTER <column_name> TYPE <cql_type>
    #     | ADD ( <column_definition_list> )
    #     | DROP ( <column_list> )
    #     | RENAME <column_name> TO <column_name> [ AND <column_name> TO <column_name> ... ]
    #     | WITH <table_properties> );

    'alter_                          > table            > alter_table                             ^ table,`tables`',
    '-                               > tables           > alter_tables',
    'alter_tables_                   > with             > alter_table_with                        ^ with',
    'alter_table_t_                  > with             > alter_table_with                        ^ with,add,drop',
    'alter_table_with_               > name             > alter_table_with_p                      ^ table-props',
    'alter_table_with_p              > comparison       > alter_table_with_p_op                   ^ =',
    'alter_table_with_p_op           > name|single|num  > alter_table_with_p_op_v                 ^ table-prop-values',
    'alter_table_with_p_op_v_        > --include-reaper > alter_table_with_p_op_v_$               ^ --include-reaper',

    '                                > describe         > describe',
    'describe_                       > table            > desc_table                              ^ table,`tables`,keyspace,`keyspaces`,schema',
    '-                               > tables           > desc_tables',
    '-                               > keyspace         > desc_keyspace',
    '-                               > keyspaces        > desc_keyspaces',
    '-                               > schema           > desc_schema',
    'desc_table_                     > name             > desc_table_t                            ^ tables',
    'desc_table_t_                   > &                > desc_table_t_$                          ^ &',
    'desc_tables_                    > &                > desc_tables_$                           ^ &',
    'desc_keyspace_                  > name             > desc_keyspace_k                         ^ keyspaces',
    'desc_keyspace_k_                > &                > desc_keyspace_k_$                       ^ &',
    'desc_schema_                    > &                > desc_schema_$                           ^ &',

    '                                > export           > export',
    'export_                         > name             > export_table                            ^ *,tables',
    '-                               > *                > export_all',
    'export_all_                     > in               > export_in                               ^ in,with',
    '-                               > with             > export_with',
    'export_table                    > (                > export_table_lp_                        ^ (,comma,with,tables',
    '-                               > ,                > export_table_comma_',
    '-                               > .                > export_table                            ^ tables',
    'export_table_                   > (                > export_table_lp_                        ^ as,(,comma,with consistency,to',
    '-                               > ,                > export_table_comma_',
    '-                               > as               > export_as',
    '-                               > with             > export_with',
    '-                               > to               > export_table_to',
    'export_table_comma_             > name             > export_table                            ^ tables',
    'export_table_lp_                > name             > export_table_lp_a                       ^ columns',
    'export_table_lp_a               > ,                > export_table_lp_a_comma_',
    '-                               > )                > export_table_lp_a_comma_rp_',
    'export_table_lp_a_comma_        > name             > export_table_lp_a                       ^ columns',
    'export_table_lp_a_comma_rp_     > as               > export_as                               ^ as,with consistency',
    '-                               > ,                > export                                  ^ with consistency',
    '-                               > with             > export_with',
    'export_as_                      > name             > export_as_f',
    'export_as_f                     > ,                > export_table_comma_',
    'export_as_f_                    > ,                > export_table_comma_                     ^ with consistency,to',
    '-                               > with             > export_with',
    '-                               > to               > export_table_to',
    'export_in_                      > name             > export_in_k                             ^ keyspaces',
    'export_in_k_                    > with             > export_with                             ^ with consistency',
    'export_with_                    > consistency      > export_with_consistency                 ^ consistency',
    'export_with_consistency_        > quorum|all|serial|one|each_quorum|local_quorum|any|local_one|two|three|local_serial > export_with_quorum ^ quorum,all,serial,one,each_quorum,local_quorum,any,local_one,two,three,local_serial',
    'export_table_to_                > athena|sqlite|csv > export_table_to$                        ^ athena,sqlite,csv',

    '                                > import           > import',
    'import_                         > session          > import_session                          ^ session,files',
    '-                               > files            > import_files',
    'import_session_                 > name             > import_session_s                        ^ export-sessions-incomplete',
    'import_session_s_               > to               > import_session_to                       ^ to',
    'import_files_                   > name             > import_files_f',
    'import_files_f                  > ,                > import_files',
    'import_files_f_                 > as               > import_files_f_as                       ^ as',
    'import_files_f_as_              > name             > import_files_f_as_a',
    'import_files_f_as_a_            > to               > import_session_to                       ^ to',
    'import_session_to_              > athena|sqlite    > import_session_to$                      ^ athena,sqlite',

    '                                > consistency      > consistency',
    'consistency_                    > quorum|all|serial|one|each_quorum|local_quorum|any|local_one|two|three|local_serial > consistency_quorum ^ quorum,all,serial,one,each_quorum,local_quorum,any,local_one,two,three,local_serial',
    'consistency_quorum              > ;                > ',

    '                                > drop             > drop',
    'drop_                           > all              > drop_all                                ^ all export databases,export database',
    '-                               > export           > drop_export',
    'drop_all_                       > export           > drop_all_export                         ^ export databases',
    'drop_all_export_                > databases        > drop_all_dbs                            ^ databases',
    'drop_export_                    > database         > drop_export_db                          ^ database',
    'drop_export_db_                 > name             > drop_export_db$                         ^ export-dbs',

    '                                > clean            > clean',
    'clean_                          > up               > clean_up                                ^ up all export sessions,up export session',
    'clean_up_                       > all              > clean_up_all                            ^ all export sessions,export sessions',
    '-                               > export           > clean_up_export',
    'clean_up_all_                   > export           > clean_up_all_export                     ^ export sessions',
    'clean_up_all_export_            > sessions         > clean_up_all_sessions                   ^ sessions',
    'clean_up_export_                > sessions         > clean_up_export_sessions                ^ sessions',
    'clean_up_export_sessions_       > name             > clean_up_export_sessions$               ^ export-sessions',
]

CQL_KEYWORDS = SQL_KEYWORDS + [
    'schema', 'keyspace', 'keyspaces', 'tables', 'export', 'copy', 'consistency',
    'quorum', 'all', 'serial', 'one', 'each_quorum', 'local_quorum', 'any', 'local_one', 'two', 'three', 'local_serial', 'to',
    'database', 'databases', 'session', 'sessions', 'clean', 'up', 'athena', 'sqlite', 'csv', 'import', 'files'
]

CQL_EXPANDABLE_NAMES = EXPANDABLE_NAMES | {
    'export-dbs', 'export-sessions', 'export-sessions-incomplete'
}

ATHENA_SPEC = SQL_SPEC + [
    '                                > select           > select                                  ^ select,insert,update,delete,alter,describe,preview,drop',

    'alter_table_t_                  > add              > alter_table_add                         ^ add partition,drop partition',
    'alter_table_add_                > partition        > alter_partition                         ^ partition',
    'alter_table_drop_               > partition        > alter_partition                         ^ partition',
    'alter_partition                 > (                > alter_partition_lp                      ^ (',
    'alter_partition_lp              > name             > alter_partition_lp_a                    ^ partition-columns',
    'alter_partition_lp_a            > comparison       > alter_partition_lp_a_op                 ^ =',
    'alter_partition_lp_a_op         > single           > alter_partition_lp_a_op_v               ^ single',
    'alter_partition_lp_a_op_v       > ,                > alter_partition_lp_sc                   ^ single',
    'alter_partition_lp_sc           > name|)           > alter_partition_lp_a                    ^ partition-columns',

    '                                > describe         > describe',
    'describe_                       > name             > desc_t                                  ^ tables',
    'desc_t_                         > name             > desc_t_',

    'repair',

    '                                > drop             > drop',
    'drop_                           > all              > drop_all                                ^ all export databases,export database',
    '-                               > export           > drop_export',
    'drop_all_                       > export           > drop_all_export                         ^ export databases',
    'drop_all_export_                > databases        > drop_all_dbs                            ^ databases',
    'drop_export_                    > database         > drop_export_db                          ^ database',
    'drop_export_db_                 > name             > drop_export_db$                         ^ export-dbs',
]

ATHENA_KEYWORDS = SQL_KEYWORDS + [
    'partition',
    'database', 'databases', 'session', 'sessions', 'clean', 'up', 'all', 'export'
]

ATHENA_EXPANDABLE_NAMES = EXPANDABLE_NAMES | {
    'export-dbs'
}

class SqlStateMachine(StateMachine[Token]):
    def __init__(self, indent=0, push_level = 0, debug = False):
        super().__init__(indent, push_level, debug)

    def traverse_tokens(self, tokens: list[Token], state: State = State('')):
        def handle_push():
            if f'{state.state} > {it}' in self.states:
                state_test = self.states[f'{state.state} > {it}']
                if state_test.comeback_token:
                    self.comebacks[self.push_level] = state_test.comeback_state

        def handle_pop():
            if self.push_level in self.comebacks:
                try:
                    return State(self.comebacks[self.push_level])
                finally:
                    del self.comebacks[self.push_level]

            return None

        for token in tokens:
            if self.debug:
                if token.ttype == TOKEN.Whitespace:
                    print('_ ', end='')
                elif token.ttype in [TOKEN.DML, TOKEN.Wildcard, TOKEN.Punctuation, TOKEN.CTE]:
                    print(f'{token.value} ', end='')
                elif token.ttype:
                    tks = str(token.ttype).split('.')
                    typ = tks[len(tks) - 1]
                    if ' ' in token.value:
                        print(f'"{token.value}:{typ}" ', end='')
                    else:
                        print(f'{token.value}:{typ} ', end='')
            # print("  " * self.indent + f"Token: {token.value}, Type: {token.ttype}@{token.ttype.__class__}")

            last_name = None
            if token.is_group:
                state = self.traverse_tokens(token.tokens, state)
            else:
                comeback_state = None

                it = ''
                if (t := token.value.lower()) in self.keywords():
                    it = t
                elif token.ttype == TOKEN.Text.Whitespace:
                    it = '_'
                elif token.ttype == TOKEN.Name:
                    it = 'name'
                    last_name = token.value
                elif token.ttype == TOKEN.Literal.String.Single:
                    it = 'single'
                elif token.ttype in [TOKEN.Literal.Number.Integer, TOKEN.Literal.Number.Float]:
                    it = 'num'
                elif token.ttype == TOKEN.Wildcard:
                    it = '*'
                elif token.ttype == TOKEN.Punctuation:
                    it = token.value

                    if it == '(':
                        handle_push()
                        self.push_level += 1
                    elif it == ')':
                        self.push_level -= 1
                        comeback_state = handle_pop()
                    elif it == '.' and 'last_name' in state.context and (ln := state.context['last_name']):
                        state.context['last_namespace'] = ln

                elif token.ttype == TOKEN.Operator.Comparison:
                    it = 'comparison'

                with log_exc(False):
                    # print(f'\n{state.to_s} > {it} > ', end='')
                    if comeback_state:
                        state = comeback_state
                    else:
                        context = state.context
                        state = self.states[f'{state.state} > {it}']
                        state.context = context

                    if last_name:
                        state.context['last_name'] = last_name

        return state

    def spec(self):
        return SQL_SPEC

    def keywords(self):
        return SQL_KEYWORDS

    def expandable_names(self):
        return EXPANDABLE_NAMES

    def witespace_transition_condition(self, from_s: str, to_s: str):
        return from_s.endswith('_') and not from_s.endswith('_comma_') and not from_s.endswith('_lp_') and not from_s.endswith('_rp_')

    def incomplete_name_transition_condition(self, from_s: str, token: str, to_s: str, suggestions: str):
        if not suggestions:
            return None

        tokens = [token]
        if '|' in token:
            tokens = token.split('|')

        if 'name' not in tokens:
            return None

        if not self.expandable_names().intersection(set(suggestions.split(','))):
            return None

        return tokens

class CqlStateMachine(SqlStateMachine):
    def __init__(self, indent=0, push_level = 0, debug = False):
        super().__init__(indent, push_level, debug)

    def spec(self):
        return CQL_SPEC

    def keywords(self):
        return CQL_KEYWORDS

    def expandable_names(self):
        return CQL_EXPANDABLE_NAMES

class AthenaStateMachine(SqlStateMachine):
    def __init__(self, indent=0, push_level = 0, debug = False):
        super().__init__(indent, push_level, debug)

    def spec(self):
        return ATHENA_SPEC

    def keywords(self):
        return ATHENA_KEYWORDS

    def expandable_names(self):
        return ATHENA_EXPANDABLE_NAMES