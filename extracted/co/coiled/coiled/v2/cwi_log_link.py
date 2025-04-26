# modified version of https://stackoverflow.com/a/69816735
def cloudwatch_url(slug, cluster_name, region):
    def escape(s):
        for c in s:
            if c.isalpha() or c.isdigit() or c in ["-", "."]:
                continue
            c_hex = "*{0:02x}".format(ord(c))
            s = s.replace(c, c_hex)
        return s

    def gen_log_insights_url(params):
        S1 = "$257E"
        S2 = "$2528"
        S3 = "$2527"
        S4 = "$2529"

        res = f"{S1}{S2}"
        for k in params:
            value = params[k]
            if isinstance(value, str):
                value = escape(value)
            elif isinstance(value, list):
                for i in range(len(value)):
                    value[i] = escape(value[i])
            prefix = S1 if list(params.items())[0][0] != k else ""
            suffix = f"{S1}{S3}"
            if isinstance(value, list):
                value = "".join([f"{S1}{S3}{n}" for n in value])
                suffix = f"{S1}{S2}"
            elif isinstance(value, int) or isinstance(value, bool):
                value = str(value).lower()
                suffix = S1

            res += f"{prefix}{k}{suffix}{value}"
        res += f"{S4}{S4}"
        QUERY = f"logsV2:logs-insights$3Ftab$3Dlogs$26queryDetail$3D{res}"
        return f"https://{region}.console.aws.amazon.com/cloudwatch/home?region={region}#{QUERY}"

    editorString = (
        f"fields @timestamp, @message\n| sort @timestamp desc\n| filter @logStream like /^{cluster_name}/\n| limit 200"
    )

    params = {
        "end": 0,
        "start": -60 * 60 * 24,  # 1 day ago
        "unit": "seconds",
        "timeType": "RELATIVE",  # "ABSOLUTE",  # OR RELATIVE and end = 0 and start is negative  seconds
        "tz": "Local",  # OR "UTC"
        "editorString": editorString,
        "source": [slug],
    }
    return gen_log_insights_url(params)
