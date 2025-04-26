import datetime
import os
import agilicus
from agilicus import ApiException
from . import get_many_entries


import json
from .input_helpers import get_org_from_input_or_ctx
from .input_helpers import pop_item_if_none
from .output import output_if_console
from .context import get_apiclient_from_ctx
import operator

from .output.table import (
    column,
    spec_column,
    status_column,
    metadata_column,
    format_table,
    subtable,
    format_timestamp,
    format_currency_from_cents,
    format_date_only,
)


def delete_billing_account(ctx, billing_account_id=None, **kwargs):
    client = get_apiclient_from_ctx(ctx)
    return client.billing_api.delete_billing_account(billing_account_id, **kwargs)


def delete_subscription(ctx, billing_subscription_id, **kwargs):
    client = get_apiclient_from_ctx(ctx)
    return client.billing_api.delete_subscription(billing_subscription_id, **kwargs)


def get_billing_account(ctx, billing_account_id=None, **kwargs):
    client = get_apiclient_from_ctx(ctx)

    org_id = get_org_from_input_or_ctx(ctx, **kwargs)
    if org_id:
        kwargs["org_id"] = org_id
    else:
        kwargs.pop("org_id")
    return client.billing_api.get_billing_account(billing_account_id, **kwargs)


def update_subscription(ctx, billing_subscription_id, subscription, **kwargs):
    client = get_apiclient_from_ctx(ctx)
    return client.billing_api.replace_subscription(
        billing_subscription_id, billing_org_subscription=subscription, **kwargs
    )


def get_billing_subscription(ctx, billing_subscription_id, **kwargs):
    client = get_apiclient_from_ctx(ctx)
    return client.billing_api.get_subscription(billing_subscription_id, **kwargs)


def cancel_billing_subscription(
    ctx,
    org_id=None,
    billing_subscription_id=None,
    immediately=None,
    cancel_at_period_end=None,
    cancel_at=None,
    comment=None,
    feedback=None,
    **kwargs,
):
    client = get_apiclient_from_ctx(ctx)

    cancel_detail = agilicus.BillingSubscriptionCancelDetail()

    if immediately is not None:
        cancel_detail.immediately = immediately
    if cancel_at_period_end is not None:
        cancel_detail.cancel_at_period_end = cancel_at_period_end
    if cancel_at is not None:
        cancel_detail.cancel_at = cancel_at
    if comment:
        cancel_detail.comment = comment
    if feedback:
        cancel_detail.feedback = feedback

    if billing_subscription_id:
        subscription = client.billing_api.get_subscription(
            billing_subscription_id, **kwargs
        )
        subscription.spec.cancel_detail = cancel_detail
        return client.billing_api.update_subscription_cancellation(
            billing_subscription_id, billing_org_subscription=subscription
        )
    elif org_id:
        return client.org_api.cancel_subscription(
            org_id, billing_subscription_cancel_detail=cancel_detail
        )


def new_billing_subscription(ctx, billing_subscription_id, **kwargs):
    client = get_apiclient_from_ctx(ctx)
    pop_item_if_none(kwargs)
    new_sub = agilicus.BillingSubscriptionNewSubscription(**kwargs)
    return client.billing_api.new_subscription(
        billing_subscription_id, billing_subscription_new_subscription=new_sub
    )


def list_accounts(ctx, page_size=100, page_at_id=None, **kwargs):
    client = get_apiclient_from_ctx(ctx)

    org_id = get_org_from_input_or_ctx(ctx, **kwargs)
    if org_id:
        kwargs["org_id"] = org_id
    else:
        kwargs.pop("org_id")

    if page_at_id is None:
        page_at_id = ""
    pop_item_if_none(kwargs)
    return get_many_entries(
        client.billing_api.list_billing_accounts,
        "billing_accounts",
        maximum=kwargs.get("limit", None),
        page_size=page_size,
        page_at_id=page_at_id,
        page_callback=client.refresh_token,
        **kwargs,
    )


def list_subscriptions(ctx, page_size=100, page_at_id=None, **kwargs):
    client = get_apiclient_from_ctx(ctx)
    pop_item_if_none(kwargs)
    org_id = get_org_from_input_or_ctx(ctx, **kwargs)
    if org_id:
        kwargs["org_id"] = org_id
    else:
        kwargs.pop("org_id", None)

    if page_at_id is None:
        page_at_id = ""
    return get_many_entries(
        client.billing_api.list_subscriptions,
        "billing_subscriptions",
        maximum=kwargs.get("limit", None),
        page_size=page_size,
        page_at_id=page_at_id,
        page_callback=client.refresh_token,
        **kwargs,
    )


def format_accounts(
    ctx, accounts, get_subscription_data=False, get_customer_data=False, **kwargs
):
    orgs_column = [column("id"), column("organisation")]
    subscriptions = [
        metadata_column("id"),
        spec_column("subscription_id", out_name="stripe subscription"),
        subtable(ctx, "orgs", orgs_column, subobject_name="status"),
        status_column("subscription.status", optional=True),
        status_column(
            "subscription.cancel_at_period_end",
            out_name="cancel_at_period_end",
            optional=True,
        ),
    ]
    products_column = [
        column("name", optional=True),
    ]
    columns = [
        metadata_column("id"),
        status_column("product.spec.name", optional=True),
    ]

    def _get_customer_name(record, key):
        status = record.get("status")
        return status.get("customer", {}).get("name")

    if get_customer_data:
        columns.append(
            column(
                "status", newname="customer", getter=_get_customer_name, optional=True
            )
        )
    else:
        columns.append(spec_column("customer_id"))

    if get_subscription_data:
        columns.append(
            subtable(ctx, "products", products_column, subobject_name="status"),
        )

    columns.append(subtable(ctx, "orgs", orgs_column, subobject_name="status"))
    columns.append(
        subtable(ctx, "org_subscriptions", subscriptions, subobject_name="status")
    )
    return format_table(ctx, accounts, columns)


def format_subscriptions(
    ctx, subscriptions, get_usage_metrics=False, get_stripe_status=False, **kwargs
):
    orgs_column = [column("id"), column("organisation")]

    def _convert_amount(record, amount):
        status = record.get("status")
        subscription = status.get("subscription")
        currency = subscription.get("currency")
        return format_currency_from_cents(amount, currency)

    def _get_amount(record, key):
        status = record.get("status")
        balance = status.get("balance")
        amount = balance.get("subscription_balance")
        return _convert_amount(record, amount)

    def _get_invoice_total(record, key):
        status = record.get("status")
        invoice = status.get("balance", {}).get("upcoming_invoice")
        return _convert_amount(record, invoice.get("total"))

    columns = [
        metadata_column("id", optional=True),
        spec_column("subscription_id"),
        spec_column("product_id"),
        subtable(ctx, "orgs", orgs_column, subobject_name="status"),
        column(
            "invoice.total",
            newname="upcoming invoice",
            getter=_get_invoice_total,
            optional=True,
        ),
        column("subscription_balance", optional=True, getter=_get_amount),
        column(
            "status.balance.estimate_balance_end_date",
            newname="end date estimate",
            format_fn=format_date_only,
            optional=True,
        ),
        status_column(
            "subscription.status",
            optional=True,
        ),
        spec_column(
            "cancel_detail",
            optional=True,
        ),
    ]

    if get_usage_metrics:
        metrics_columns = [column("type"), column("active")]
        columns.append(
            subtable(
                ctx, "metrics", metrics_columns, subobject_name="status.usage_metrics"
            )
        )

    if get_stripe_status:
        columns.append(status_column("provider_status"))

    return format_table(ctx, subscriptions, columns)


def add_billing_account(ctx, customer_id=None, dev_mode=None, **kwargs):
    client = get_apiclient_from_ctx(ctx)
    spec = agilicus.BillingAccountSpec(customer_id=customer_id)

    if dev_mode is not None:
        spec.dev_mode = dev_mode

    account = agilicus.BillingAccount(spec=spec)

    return client.billing_api.create_billing_account(account)


def add_subscription_balance_transaction(
    ctx, billing_subscription_id, amount=None, adjustment_type="credit", **kwargs
):
    client = get_apiclient_from_ctx(ctx)
    transaction = agilicus.BillingBalanceTransaction(**kwargs)
    if amount is not None:
        # convert to cents
        transaction.amount = int(amount * 100)
    if adjustment_type == "credit":
        # debits are 'negative', are removed.
        transaction.amount = -transaction.amount

    return client.billing_api.add_subscription_balance_transaction(
        billing_subscription_id, billing_balance_transaction=transaction
    )


def list_subscription_balance_transactions(ctx, billing_subscription_id, **kwargs):
    client = get_apiclient_from_ctx(ctx)
    pop_item_if_none(kwargs)
    return client.billing_api.get_subscription_balance_transactions(
        billing_subscription_id, **kwargs
    )


def list_customer_balance_transactions(ctx, billing_id, **kwargs):
    client = get_apiclient_from_ctx(ctx)
    pop_item_if_none(kwargs)
    return client.billing_api.get_customer_balance_transactions(billing_id, **kwargs)


def format_balance_transactions(ctx, results):
    def get_amount(record, key):
        amount = record.get("amount")
        currency = record.get("currency")
        return format_currency_from_cents(amount, currency)

    columns = [
        column("id"),
        column("created", format_fn=format_timestamp),
        column("description"),
        column("amount", getter=get_amount),
        column("currency"),
        column("type"),
        # column("invoice"),
    ]
    return format_table(ctx, results, columns)


def add_subscription(
    ctx, billing_account_id, subscription_id=None, dev_mode=None, **kwargs
):
    client = get_apiclient_from_ctx(ctx)
    spec = agilicus.BillingOrgSubscriptionSpec(billing_account_id=billing_account_id)

    if dev_mode is not None:
        spec.dev_mode = dev_mode

    if subscription_id is not None:
        spec.subscription_id = subscription_id

    subscription = agilicus.BillingOrgSubscription(spec=spec)

    return client.billing_api.create_subscription(subscription)


def add_org(ctx, billing_account_id=None, org_id=None, **kwargs):
    client = get_apiclient_from_ctx(ctx)
    billing_org = agilicus.BillingOrg._from_openapi_data(org_id=org_id)
    return client.billing_api.add_org_to_billing_account(
        billing_account_id, billing_org=billing_org
    )


def remove_org(ctx, billing_account_id=None, org_id=None, **kwargs):
    client = get_apiclient_from_ctx(ctx)
    return client.billing_api.remove_org_from_billing_account(billing_account_id, org_id)


def add_org_to_subscription(ctx, billing_subscription_id, org_id, **kwargs):
    client = get_apiclient_from_ctx(ctx)
    billing_org = agilicus.BillingOrg._from_openapi_data(org_id=org_id)
    return client.billing_api.add_org_to_billing_subscription(
        billing_subscription_id, billing_org=billing_org
    )


def remove_org_from_subscription(ctx, billing_subscription_id, org_id, **kwargs):
    client = get_apiclient_from_ctx(ctx)
    return client.billing_api.remove_org_from_billing_subscription(
        org_id, billing_subscription_id
    )


def replace_billing_account(
    ctx,
    billing_account_id=None,
    customer_id=None,
    dev_mode=None,
    product_id=None,
    **kwargs,
):
    client = get_apiclient_from_ctx(ctx)

    existing = client.billing_api.get_billing_account(billing_account_id)
    if customer_id is not None:
        existing.spec.customer_id = customer_id
    if dev_mode is not None:
        existing.spec.dev_mode = dev_mode
    if product_id is not None:
        existing.spec.product_id = product_id
    return client.billing_api.replace_billing_account(
        billing_account_id, billing_account=existing
    )


def format_usage_records(ctx, records):
    columns = [
        column("id"),
        column("period"),
        column("total_usage"),
    ]
    return format_table(ctx, records, columns, getter=operator.itemgetter)


def get_usage_records(ctx, billing_account_id=None, **kwargs):
    client = get_apiclient_from_ctx(ctx)
    return client.billing_api.get_usage_records(billing_account_id)


def _dump_billing_failure(ctx, exception_description, account):
    account_info = {}
    try:
        account_info = account.to_dict()
    except Exception as exc:
        output_if_console(
            ctx,
            f"Failed to dump account info when handling billing failure: {str(exc)}",
        )
    error_message = {
        "time": datetime.datetime.now(datetime.timezone.utc),
        "msg": "error",
        "reason": str(exception_description),
        "account": account_info,
    }
    try:
        print(json.dumps(error_message, default=str))
    except Exception as exc:
        output_if_console(ctx, f"Failed to json.dumps failure info: {str(exc)}")


def run_billing_um_all_accounts(
    ctx,
    client,
    dry_run=False,
    push_to_prometheus_on_success=True,
    orgs_enabled_since_days=None,
    **kwargs,
):
    kwargs = {}
    if orgs_enabled_since_days:
        kwargs["active_orgs_since"] = datetime.datetime.utcnow() - datetime.timedelta(
            days=orgs_enabled_since_days
        )
    accounts = client.billing_api.list_billing_accounts(**kwargs)
    record = agilicus.CreateBillingUsageRecords(dry_run=dry_run)
    numSuccess = 0
    numSkipped = 0
    numFail = 0

    for account in accounts.billing_accounts:

        if not account.spec.customer_id:
            numSkipped += 1
            continue
        try:

            if len(account.status.orgs) == 0:
                numSkipped += 1
                print(
                    json.dumps(
                        {
                            "skip": True,
                            "billing_account": account.metadata.id,
                            "customer_id": account.spec.customer_id,
                        }
                    )
                )
                continue

            # get the client again, which checks if a refresh of the token is required
            client = get_apiclient_from_ctx(ctx)
            base_result = client.billing_api.add_billing_usage_record(
                account.metadata.id, create_billing_usage_records=record
            )
            success = False
            if base_result:
                result = base_result.to_dict()
                success = True
            else:
                result = {}

            result["billing_account"] = account.metadata.id
            result["customer_id"] = account.spec.customer_id
            result["orgs"] = [
                {"id": org.id, "organisation": org.organisation}
                for org in account.status.orgs
            ]
            if success:
                numSuccess += 1
                result["published"] = True
            else:
                numSkipped += 1
                result["published"] = False
            print(json.dumps(result))
        except ApiException as exc:
            numFail += 1
            _dump_billing_failure(ctx, exc.body, account)
        except Exception as exc:
            numFail += 1
            _dump_billing_failure(ctx, exc, account)

    if push_to_prometheus_on_success:
        try:
            from prometheus_client import (
                CollectorRegistry,
                Gauge,
                push_to_gateway,
            )
        except ModuleNotFoundError:
            output_if_console(ctx, "Not posting success to prometheus_client.")
            output_if_console(
                ctx, "Add the 'billing' option to the install to gain access"
            )
            return

        registry = CollectorRegistry()
        gSuccess = Gauge(
            "billing_usage_records_created_count",
            "number of billing accounts that have created a usage record",
            registry=registry,
        )

        gFail = Gauge(
            "billing_usage_records_failed_count",
            "number of billing accounts that failed to create a usage record",
            registry=registry,
        )
        gSkipped = Gauge(
            "billing_usage_records_skipped_count",
            "number of billing accounts that were skipped",
            registry=registry,
        )

        push_gateway = os.environ.get(
            "PROMETHEUS_PUSH_GATEWAY",
            "push-prometheus-pushgateway.prometheus-pushgateway:9091",
        )
        job_name = os.environ.get("JOB_NAME", "billing_usage_job")
        gSuccess.set(numSuccess)
        gFail.set(numFail)
        gSkipped.set(numSkipped)
        push_to_gateway(push_gateway, job=job_name, registry=registry)


def create_usage_record(
    ctx, billing_account_id=None, all_accounts=None, dry_run=False, **kwargs
):
    client = get_apiclient_from_ctx(ctx)
    record = agilicus.BillingUsageRecord(dry_run=dry_run)
    if billing_account_id is not None:
        records = agilicus.CreateBillingUsageRecords(usage_records=[record])
        result = client.billing_api.add_billing_usage_record(
            billing_account_id, create_billing_usage_records=records
        )
        print(json.dumps(result.to_dict()))
    elif all_accounts is not None:
        run_billing_um_all_accounts(ctx, client, dry_run=dry_run, **kwargs)
    else:
        raise Exception("Need to choose --billing-account-or or --all-accounts")


def _get_subscription(org_subscriptions, subscription_id):
    for org_subscription in org_subscriptions:
        if org_subscription.spec.subscription_id == subscription_id:
            return org_subscription


def _has_org(orgs, org_id):
    for org in orgs:
        if org.id == org_id:
            return True
    return False


def migrate_billing_subscriptions(ctx, billing_account_id=None, commit=False, **kwargs):
    kwargs = {}
    kwargs["get_customer_data"] = True
    kwargs["get_subscription_data"] = True
    kwargs["org_id"] = ""
    if billing_account_id is not None:
        accounts = [get_billing_account(ctx, billing_account_id, **kwargs)]
    else:
        accounts = list_accounts(ctx, **kwargs).billing_accounts
    for account in accounts:
        customer = account.status.customer
        if not customer:
            print(f"billing account {account.metadata.id} has no customer")
            continue
        if customer.get("deleted"):
            continue
        for sub in account.status.subscriptions:
            # check if there is an org sub for this first.
            org_subscription = _get_subscription(
                account.status.org_subscriptions, sub["id"]
            )
            if not org_subscription:
                print(
                    f"  billing account:{account.metadata.id} "
                    "{customer['name']}:{sub['id']} "
                    "needs BillingSubscription"
                )
                if not commit:
                    for org in account.status.orgs:
                        print(f"    {org.organisation} needs to be attached")
                    continue
                sub = add_subscription(
                    ctx,
                    account.metadata.id,
                    subscription_id=sub["id"],
                    dev_mode=account.spec.dev_mode,
                )
                print(f"    created billing subscription {sub.metadata.id}")
                for org in account.status.orgs:
                    print(f"    adding org {org.organisation} to billing subscription")
                    val = add_org_to_subscription(ctx, sub.metadata.id, org.id)
                    print(f"    added org {val.id} to billing subscription")
            else:
                # verify that the orgs are added to subscription
                for org in account.status.orgs:
                    if not _has_org(org_subscription.status.orgs, org.id):
                        if org.admin_state != "active":
                            # not interested in orgs that are not active
                            continue
                        print(
                            f"    NOTICE: org {org.organisation} is missing billing "
                            f"in subscription {org_subscription.metadata.id}",
                        )
                        if not commit:
                            continue
                        val = add_org_to_subscription(
                            ctx, org_subscription.metadata.id, org.id
                        )
                        print(f"    added org {val.id} to billing subscription")


def reconcile_billing_subscriptions(  # noqa
    ctx,
    billing_account_id=None,
    commit=False,
    push_to_prometheus=False,
    orgs_enabled_since_days=None,
    **kwargs,
):
    """
    find cancelled stripe subscriptions with an active organsanistion(s).
    """
    kwargs = {}
    kwargs["get_customer_data"] = True
    kwargs["get_subscription_data"] = True
    kwargs["org_id"] = ""
    page_size = 10
    subscriptionsGood = 0
    subscriptionsNotActive = 0
    subscriptionOrgNotActive = 0
    if billing_account_id is not None:
        accounts = [get_billing_account(ctx, billing_account_id, **kwargs)]
    else:
        if orgs_enabled_since_days:
            kwargs[
                "active_orgs_since"
            ] = datetime.datetime.utcnow() - datetime.timedelta(
                days=orgs_enabled_since_days
            )
        accounts = list_accounts(ctx, page_size=page_size, page_at_id="", **kwargs)
    results = []
    for account in accounts:
        customer = account.status.customer
        if not customer:
            print(f"billing account {account.metadata.id} has no customer")
            continue
        for sub in account.status.subscriptions:
            counts = {}
            subscriptionGood = True
            for org in account.status.orgs:
                admin_state = org.admin_state.value
                orgs_admin_state = counts.setdefault(admin_state, [])
                orgs_admin_state.append(org)
                if admin_state == "active" and sub["status"] == "canceled":
                    print(
                        "  NOTICE: Subscription cancelled, "
                        f"but org {org.id} ({org.organisation}) still active "
                    )
                    results.append(
                        {
                            "billing_account_id": account.metadata.id,
                            "org": org,
                            "sub": sub,
                        }
                    )
                    subscriptionsNotActive += 1
                    subscriptionGood = False
            if len(counts.get("active", [])) == 0 and (
                not sub.get("cancel_at_period_end")
                and (["status"] == "active" or sub["status"] == "trialing")
            ):
                print(
                    "  NOTICE: All orgs deleted in billing account "
                    f"{account.metadata.id}, subscription still active "
                    f"{sub['status']}"
                )
                results.append(
                    {
                        "billing_account_id": account.metadata.id,
                        "sub": sub,
                        "orgs_by_state": counts,
                    }
                )
                subscriptionGood = False
                subscriptionOrgNotActive += 1
            if subscriptionGood:
                subscriptionsGood += 1

    def org_getter(record, key):
        return record["org"]["organisation"]

    def org_id_getter(record, key):
        return record["org"]["id"]

    def state_getter(record, key):
        return record["org"]["admin_state"]

    def sub_getter(record, key):
        return record["sub"]["status"]

    def get_customer_id(record, key):
        return record["sub"]["customer"]["id"]

    def get_billing_account_id(record, key):
        return record["billing_account_id"]

    def get_orgs_by_state(record, key):
        return record["orgs_by_state"]

    columns = [
        column("billing_account_id", getter=get_billing_account_id),
        column("customer_id", getter=get_customer_id),
        column("orgs_by_state", getter=get_orgs_by_state, optional=True),
        column("organisation", getter=org_getter, optional=True),
        column("id", getter=org_id_getter, optional=True),
        column("admin_state", getter=state_getter, optional=True),
        column("stripe subscription status", getter=sub_getter),
    ]
    print(format_table(ctx, results, columns))

    if push_to_prometheus:
        try:
            from prometheus_client import (
                CollectorRegistry,
                Gauge,
                push_to_gateway,
            )
        except ModuleNotFoundError:
            output_if_console(ctx, "Not posting success to prometheus_client.")
            output_if_console(
                ctx, "Add the 'billing' option to the install to gain access"
            )
            return

        registry = CollectorRegistry()
        gSubscriptionsGood = Gauge(
            "billing_subscriptions_good",
            "billing accounts that have an active org and active subscription",
            registry=registry,
        )
        gSubscriptionsNotActive = Gauge(
            "billing_subscriptions_not_active",
            "billing accounts that have an active org but inactive subscription",
            registry=registry,
        )
        gOrgNotActive = Gauge(
            "billing_subscriptions_organisation_not_active",
            "billing accounts that have disable org but active subscription",
            registry=registry,
        )
        gSubscriptionsGood.set(subscriptionsGood)
        gSubscriptionsNotActive.set(subscriptionsNotActive)
        gOrgNotActive.set(subscriptionOrgNotActive)

        push_gateway = os.environ.get(
            "PROMETHEUS_PUSH_GATEWAY",
            "push-prometheus-pushgateway.prometheus-pushgateway:9091",
        )
        job_name = os.environ.get("JOB_NAME", "billing_reconcile_job")
        push_to_gateway(push_gateway, job=job_name, registry=registry)


def list_subscription_features(ctx, billing_subscription_id, **kwargs):
    client = get_apiclient_from_ctx(ctx)
    return client.billing_api.list_subscription_features(
        billing_subscription_id, **kwargs
    ).features


def create_billing_checkout_session(
    ctx, ui_mode=None, return_url=None, success_url=None, custom_text=None, **kwargs
):
    client = get_apiclient_from_ctx(ctx)
    org_id = get_org_from_input_or_ctx(ctx, **kwargs)
    createSession = agilicus.CreateBillingCheckoutSession()
    if ui_mode:
        createSession.ui_mode = ui_mode

    if return_url:
        createSession.return_url = return_url

    if success_url:
        createSession.success_url = success_url

    if custom_text:
        createSession.custom_text = custom_text
    return client.org_api.create_checkout_session(
        org_id, create_billing_checkout_session=createSession
    )


def list_billing_checkout_sessions(ctx, billing_account_id, **kwargs):
    client = get_apiclient_from_ctx(ctx)
    pop_item_if_none(kwargs)
    return client.billing_api.list_checkout_sessions(billing_account_id, **kwargs)
