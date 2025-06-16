from __future__ import annotations


def count_objects_in_bucket(bucket_name, prefix):
    if not isinstance(bucket_name, str):
        raise TypeError("bucket_name must be string")

    s3 = boto3.resource("s3")
    bucket = s3.Bucket(bucket_name)

    # use loop and count increment
    count_obj = len(bucket.objects.filter(Prefix=prefix))

    return print(f"prefix: {prefix} -> count_obj: {count_obj}")


# Taken + adapted from https://stackoverflow.com/questions/33842944/check-if-a-key-exists-in-a-bucket-in-s3-using-boto3/34562141
def s3_key_exists(BUCKET, KEY):
    s3 = boto3.resource("s3")

    try:
        s3.Object(BUCKET, KEY).load()
    except botocore.exceptions.ClientError as e:
        if e.response["Error"]["Code"] == "404":
            return False
        else:
            # Something else has gone wrong.
            raise
    else:
        return True


def run_delta_crawler(crawler_name, table_names, delta_bucket, delta_key):
    glue_crawler_client = boto3.client("glue", region_name="eu-central-1")
    s3_locations = [f"s3://{delta_bucket}/{delta_key}/{t}/" for t in table_names]
    try:
        c = glue_crawler_client.get_crawler(Name=crawler_name)
    except glue_crawler_client.exceptions.EntityNotFoundException:
        lp("Crawler not found. Creating new crawler ...")
        glue_crawler_client.create_crawler(
            Name=crawler_name,
            Role=f"AWSGlueServiceRole-{environment}",
            DatabaseName=f"vy-da-{environment}-glue-catalog",
            Targets={"DeltaTargets": [{"DeltaTables": s3_locations, "WriteManifest": True}]},
        )
    delta_targets = c["Crawler"]["Targets"]["DeltaTargets"][0]["DeltaTables"]
    if s3_locations != delta_targets:
        lp("Delta targets not equal. Updating crawler ...")
        glue_crawler_client.update_crawler(
            Name=crawler_name,
            Targets={"DeltaTargets": [{"DeltaTables": s3_locations, "WriteManifest": True}]},
        )
    lp(f"Running {crawler_name} ...")
    try:
        glue_crawler_client.start_crawler(Name=crawler_name)
    except glue_crawler_client.exceptions.CrawlerRunningException:
        lp("Crawler already running. Skipping new run.")