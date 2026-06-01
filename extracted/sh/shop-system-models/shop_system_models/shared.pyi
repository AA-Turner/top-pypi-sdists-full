from pydantic import BaseModel

class PageInfo(BaseModel):
    total_rows: int
    page: int
    page_size: int
    is_first_page: bool
    is_last_page: bool

class ListResponseModel(BaseModel):
    page_info: PageInfo
