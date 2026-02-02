from marshmallow import Schema, fields


class PipelineCrawledPageSchema(Schema):
    id = fields.Int(dump_only=True)
    session_id = fields.Int(required=True)
    url = fields.Str(required=True)
    url_hash = fields.Str(required=True)
    page_title = fields.Str(allow_none=True)
    html_content_s3_key = fields.Str(allow_none=True)
    html_content_hash = fields.Str(allow_none=True)
    html_content_length = fields.Int(allow_none=True)
    screenshot_s3_key = fields.Str(allow_none=True)
    screenshot_hash = fields.Str(allow_none=True)
    screenshot_width = fields.Int(allow_none=True)
    screenshot_height = fields.Int(allow_none=True)
    screenshot_file_size = fields.Int(allow_none=True)
    page_type = fields.Str(allow_none=True)
    relevance_score = fields.Float(allow_none=True)
    has_drug_data = fields.Bool(allow_none=True)
    extraction_method = fields.Str(allow_none=True)
    crawl_depth = fields.Int(allow_none=True)
    parent_page_id = fields.Int(allow_none=True)
    discovered_from_url = fields.Str(allow_none=True)
    http_status_code = fields.Int(allow_none=True)
    content_type = fields.Str(allow_none=True)
    response_time_ms = fields.Int(allow_none=True)
    crawled_at = fields.DateTime(required=True)
    created_at = fields.DateTime(dump_only=True)
    updated_at = fields.DateTime(dump_only=True)


class PipelineCrawledPageResourceSchema(PipelineCrawledPageSchema):
    pass
