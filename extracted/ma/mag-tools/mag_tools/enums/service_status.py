from mag_tools.enums.base_enum import BaseEnum


class ServiceStatus(BaseEnum):
    # --- 1xx Informational ---
    CONTINUE = (100, "Continue", "继续")
    SWITCHING_PROTOCOLS = (101, "Switching Protocols", "交换协议")
    PROCESSING = (102, "Processing", "处理中")
    CHECKPOINT = (103, "Checkpoint", "检测点")
    # --- 2xx Success ---
    OK = (200, "OK", "正常")
    CREATED = (201, "Created", "已创建")
    ACCEPTED = (202, "Accepted", "已接受")
    NON_AUTHORITATIVE_INFORMATION = (203, "Non-Authoritative Information", "非授权信息")
    NO_CONTENT = (204, "No Content", "无内容")
    RESET_CONTENT = (205, "Reset Content", "重置内容")
    PARTIAL_CONTENT = (206, "Partial Content", "部分内容")
    MULTI_STATUS = (207, "Multi-Status", "多重状态")
    ALREADY_REPORTED = (208, "Already Reported", "已经报告")
    IM_USED = (226, "IM Used", "IM已使用")
    # --- 3xx Redirection ---
    MULTIPLE_CHOICES = (300, "Multiple Choices", "多重选择")
    MOVED_PERMANENTLY = (301, "Moved Permanently", "永久移除")
    FOUND = (302, "Found", "已发现")
    SEE_OTHER = (303, "See Other", "参见其它")
    NOT_MODIFIED = (304, "Not Modified", "未修改")
    TEMPORARY_REDIRECT = (307, "Temporary Redirect", "临时重定向")
    PERMANENT_REDIRECT = (308, "Permanent Redirect", "永久重定向")
    # --- 4xx Client Error ---
    BAD_REQUEST = (400, "Bad Request", "错误请求")
    UNAUTHORIZED = (401, "Unauthorized", "未经授权")
    PAYMENT_REQUIRED = (402, "Payment Required", "需要支付")
    FORBIDDEN = (403, "Forbidden", "被禁止")
    NOT_FOUND = (404, "Not Found", "未找到")
    METHOD_NOT_ALLOWED = (405, "Method Not Allowed", "方法不允许")
    NOT_ACCEPTABLE = (406, "Not Acceptable", "不可接受")
    PROXY_AUTHENTICATION_REQUIRED = (407, "Proxy Authentication Required", "需要代理身份验证")
    REQUEST_TIMEOUT = (408, "Request Timeout", "请求超时")
    CONFLICT = (409, "Conflict", "冲突")
    GONE = (410, "Gone", "已离开")
    LENGTH_REQUIRED = (411, "Length Required", "需要长度")
    PRECONDITION_FAILED = (412, "Precondition Failed", "先决条件失败")
    PAYLOAD_TOO_LARGE = (413, "Payload Too Large", "有效载荷太大")
    URI_TOO_LONG = (414, "URI Too Long", "URI太长")
    UNSUPPORTED_MEDIA_TYPE = (415, "Unsupported Media Type", "不支持的媒体类型")
    REQUESTED_RANGE_NOT_SATISFIABLE = (416, "Requested range not satisfiable", "请求范围不符合要求")
    EXPECTATION_FAILED = (417, "Expectation Failed", "预期失败")
    I_AM_A_TEAPOT = (418, "I'm a teapot", "“我是茶壶")
    UNPROCESSABLE_ENTITY = (422, "Unprocessable Entity", "不可处理实体")
    LOCKED = (423, "Locked", "已锁定")
    FAILED_DEPENDENCY = (424, "Failed Dependency", "依赖失败")
    TOO_EARLY = (425, "Too Early", "太早")
    UPGRADE_REQUIRED = (426, "Upgrade Required", "需要升级")
    PRECONDITION_REQUIRED = (428, "Precondition Required", "要求先决条件")
    TOO_MANY_REQUESTS = (429, "Too Many Requests", "请求太多")
    REQUEST_HEADER_FIELDS_TOO_LARGE = (431, "Request Header Fields Too Large", "请求头字段太大")
    UNAVAILABLE_FOR_LEGAL_REASONS = (451, "Unavailable For Legal Reasons", "因法律原因不可用")
    BUS_OPERATION_FAIL = (499, "业务处理失败", "业务处理失败")
    # --- 5xx Server Error ---
    INTERNAL_SERVER_ERROR = (500, "Internal Server Error", "内部服务器错误")
    BAD_GATEWAY = (502, "Bad Gateway", "网关故障")
    SERVICE_UNAVAILABLE = (503, "Service Unavailable", "服务不可用")
    GATEWAY_TIMEOUT = (504, "Gateway Timeout", "网关超时")
    HTTP_VERSION_NOT_SUPPORTED = (505, "HTTP Version not supported", "HTTP版本不支持")
    VARIANT_ALSO_NEGOTIATES = (506, "Variant Also Negotiates", "变体也在协商中")
    INSUFFICIENT_STORAGE = (507, "Insufficient Storage", "存储空间不足")
    LOOP_DETECTED = (508, "Loop Detected", "检测到循环")
    BANDWIDTH_LIMIT_EXCEEDED = (509, "Bandwidth Limit Exceeded", "超出带宽限制")
    NOT_EXTENDED = (510, "Not Extended", "未扩展")
    NETWORK_AUTHENTICATION_REQUIRED = (511, "Network Authentication Required", "需要网络身份验证")
    # --- 6xx DB Error ---
    DB_OPERATION_FAIL = (600, "数据操作失败", "数据操作失败")
    DUPLICATE_ENTRY = (601, "Duplicate entry", "数据重复")
    PARAMETER_MISS_MATCH = (602, "参数个数不匹配", "参数个数不匹配")
    CONNECT_FAIL = (603, "取数据库连接失败", "取数据库连接失败")
    INSERT_FAIL = (604, "插入失败", "插入失败")

    def __init__(self, code, reason, desc):
        super().__init__(code, desc)
        self.reason = reason

    @classmethod
    def of_reason(cls, reason):
        status = None
        if reason:
            for status in cls:
                if reason.startswith(status.reason):
                    break
        return status