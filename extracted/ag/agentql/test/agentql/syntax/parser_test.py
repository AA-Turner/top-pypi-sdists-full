import pytest

from agentql import QueryParser, QuerySyntaxError

PARSE_TEST_DATA = [
    (
        # Id Node without description
        """
        {
            sign_in_btn
        }
        """
    ),
    (
        # Id Node with description
        """
        {
            sign_in_btn(good button)
        }
        """
    ),
    (
        # IdList Node without description
        """
        {
            sign_in_btn[]
        }
        """
    ),
    (
        # IdList Node with description
        """
        {
            sign_in_btn(good button)[]
        }
        """
    ),
    (
        # Container Node without description
        """
        {
            sign_in_btn {
                good_child
            }
        }
        """
    ),
    (
        # Container Node with description
        """
        {
            sign_in_btn(good button) {
                good_child(bad button)
            }
        }
        """
    ),
    (
        # ContainerList Node without description
        """
        {
            sign_in_btn[] {
                pasha
            }
        }
        """
    ),
    (
        # ContainerList Node with description
        """
        {
            sign_in_btn(good button)[] {
                thanks_for_review_pasha
            }
        }
        """
    ),
    (
        # Same children name, different parent
        """
        {
            sign_in_btn(good button)[] {
                thanks_for_review_pasha
            }
            log_in_btn(good button)[] {
                thanks_for_review_pasha
            }
        }
        """
    ),
    (
        # Same children name across different nested levels
        """
        {
            jinyang {
                pasha {
                    pasha {
                        pasha
                    }
                }
            }
            pasha
        }
        """
    ),
    (
        # Empty lines
        """
        {


            sign_in_btn(good button)[] {
                thanks_for_review_pasha
            }
        }
        """
    ),
    (
        # Messy indentations
        """
        {

sign_in_btn(good button)[] {
                          thanks_for_review_pasha
                   }}
        """
    ),
    (
        # Complex
        """
        {
            sign_in_btn
            container {
                child1(a good child) {
                    child(bad button)
                }
            }
            andrew[] {
                mingyang
                zifan[] {
                    jinyang {
                        jinyang
                    }
                }
                jason
            }
            urvish[]
        }
        """
    ),
    (
        # Complex with weird quotes and apostrophes
        """
        {
            sign_in_btn
            container {
                child1(a good child) {
                    child(bad button)
                }
            }
            andrew()[] {
                mingyang
                zifan('yes')[] {
                    jinyang {
                        jinyang
                    }
                }
                jason("no')
            }
            urvish[]
        }
        """
    ),
    (
        # Comma after the last child
        """
        {
            search_btn,
        }
        """
    ),
    (
        # Comma after the last child with description
        """
        {
            search_btn (description),
        }
        """
    ),
    (
        # Comma after last containerList
        """
        {
            products[],
        }
        """
    ),
    (
        # Comma after last containerNode
        """
        {
            header {
                about
            },
        }
        """
    ),
    (
        # Comma between items
        """
        {
            header,
            about
        }
        """
    ),
    (
        # Comma between items with no new line character
        """
        {
            header (top of the page),about
        }
        """
    ),
    (
        # Comma between containerList and IdNode
        """
        {
            products[],
            footer
        }
        """
    ),
    (
        # Comma between containerList and IdNode with description
        """
        {
            products(description)[]   ,
            footer
        }
        """
    ),
    (
        # Comma between containerList and IdNode with description
        """
        {
            products[] {
                name,price
            },
            footer
        }
        """
    ),
    (
        # Comma within identifier
        """
        {
            sear,ch_btn
        }
        """
    ),
    (
        # Multiple descriptions in parentheses
        """
        {
            search_btn (description, description2)
        }
        """
    ),
    (
        # Multiple descriptions in parentheses
        """
        {
            search_box, search_btn (description)
        }
        """
    ),
]

PARSE_INVALID_TEST_DATA = [
    (
        """
        {
            header {
                sign_in_btn
            }
            about
        """
    ),
    (
        """
        {
            header {
                sign_in_btn
            about
        }
        """
    ),
    (
        """
            header {
                sign_in_btn
            about
        }
        """
    ),
    (
        """
        {
            header
                sign_in_btn
            }
            about
        }
        """
    ),
    (
        """
        {
            header {
                list]
            }
            about
        }
        """
    ),
    (
        """
        {
            header {
                list[
            }
            about
        }
        """
    ),
    (
        """
        {
            header {
                []
            }
            about
        }
        """
    ),
    (
        """
        {
            header
            {
                []list
            }
            about
        }
        """
    ),
    (
        """
        {
            header {
                []list
                news
                sign_in_btn
            }
            about
        }
        """
    ),
    (
        """
        {
            header
            {
                news
                []list
                sign_in_btn
            }
            about
        }
        """
    ),
    (
        """
        {
            header {
                news
                sign_in_btn
                []list
            }
            about
        }
        """
    ),
    (
        """
        {
            news
            sign_in_btn

            []list

        }
        """
    ),
    (
        """
        {
            header {
                [list]
            }
            about
        }
        """
    ),
    (
        """
        {

        }
        """
    ),
    (
        """
        {
            1_sign_in_btn
        }
        """
    ),
    (
        """
        {
            sign_in_btn
            sign_in_btn
        }
        """
    ),
    (
        """
        {
            header {
                sign_in_btn
                sign_in_btn
            }
        }
        """
    ),
    (
        """
        {
            header {
                sign_in_btn
            }
            about
            header {
                sign_in_btn
            }
        }
        """
    ),
    (
        """
        {
            header {
                sign_in_btn(babu
                tton)
            }
        }
        """
    ),
    (
        """
        {
            sign_in_btn,,sign_out_btn
        }
        """
    ),
    (
        """
        ,{
            sign_in_btn
        }
        """
    ),
    (
        """
        {
            sign_in_btn
        },
        """
    ),
    (
        """
        {
            ,sign_in_btn
        }
        """
    ),
    (
        """
        {
            sign_in_btn,(description)
        }
        """
    ),
    (
        """
        {
            ,sign_in_btn(description)
        }
        """
    ),
    (
        """
        {
            sign_in_btn,[]
        }
        """
    ),
]


@pytest.mark.parametrize("query", PARSE_TEST_DATA)
def test_parse(query):
    parser = QueryParser(query)
    parser.parse()


@pytest.mark.parametrize("query", PARSE_INVALID_TEST_DATA)
def test_parse_invalid(query):
    parser = QueryParser(query)
    with pytest.raises(QuerySyntaxError):
        parser.parse()
