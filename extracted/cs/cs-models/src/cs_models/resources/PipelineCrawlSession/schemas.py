from marshmallow import Schema, fields


class PipelineCrawlSessionSchema(Schema):
    id = fields.Int(dump_only=True)
    company_sec_id = fields.Int(allow_none=True)
    company_ous_id = fields.Int(allow_none=True)
    session_uuid = fields.Str(required=True)
    crawl_date = fields.DateTime(required=True)
    crawl_duration_seconds = fields.Float(allow_none=True)
    page_discovery_time_seconds = fields.Float(allow_none=True)
    extraction_time_seconds = fields.Float(allow_none=True)
    status = fields.Str(required=True)
    error_message = fields.Str(allow_none=True)
    total_pages_discovered = fields.Int(allow_none=True)
    total_pages_crawled = fields.Int(allow_none=True)
    total_screenshots_captured = fields.Int(allow_none=True)
    total_drugs_extracted = fields.Int(allow_none=True)
    crawl_method = fields.Str(allow_none=True)
    max_depth = fields.Int(allow_none=True)
    created_at = fields.DateTime(dump_only=True)
    updated_at = fields.DateTime(dump_only=True)
