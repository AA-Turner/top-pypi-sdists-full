from setuptools import setup

name = "types-stripe"
description = "Typing stubs for stripe"
long_description = '''
## Typing stubs for stripe

This is a [PEP 561](https://peps.python.org/pep-0561/)
type stub package for the [`stripe`](https://github.com/stripe/stripe-python) package.
It can be used by type-checking tools like
[mypy](https://github.com/python/mypy/),
[pyright](https://github.com/microsoft/pyright),
[pytype](https://github.com/google/pytype/),
PyCharm, etc. to check code that uses
`stripe`.

This version of `types-stripe` aims to provide accurate annotations
for `stripe==3.5.*`.
The source for this package can be found at
https://github.com/python/typeshed/tree/main/stubs/stripe. All fixes for
types and metadata should be contributed there.

*Note:* The `stripe` package includes type annotations or type stubs
since version 7.1.0. Please uninstall the `types-stripe`
package if you use this or a newer version.


This stub package is marked as [partial](https://peps.python.org/pep-0561/#partial-stub-packages).
If you find that annotations are missing, feel free to contribute and help complete them.


See https://github.com/python/typeshed/blob/main/README.md for more details.
This package was generated from typeshed commit `1de5830a2703936a96a126248227d5c7db883674` and was tested
with mypy 1.8.0, pyright 1.1.342, and
pytype 2023.12.18.
'''.lstrip()

setup(name=name,
      version="3.5.2.20240106",
      description=description,
      long_description=long_description,
      long_description_content_type="text/markdown",
      url="https://github.com/python/typeshed",
      project_urls={
          "GitHub": "https://github.com/python/typeshed",
          "Changes": "https://github.com/typeshed-internal/stub_uploader/blob/main/data/changelogs/stripe.md",
          "Issue tracker": "https://github.com/python/typeshed/issues",
          "Chat": "https://gitter.im/python/typing",
      },
      install_requires=[],
      packages=['stripe-stubs'],
      package_data={'stripe-stubs': ['__init__.pyi', 'api_requestor.pyi', 'api_resources/__init__.pyi', 'api_resources/abstract/__init__.pyi', 'api_resources/abstract/api_resource.pyi', 'api_resources/abstract/createable_api_resource.pyi', 'api_resources/abstract/custom_method.pyi', 'api_resources/abstract/deletable_api_resource.pyi', 'api_resources/abstract/listable_api_resource.pyi', 'api_resources/abstract/nested_resource_class_methods.pyi', 'api_resources/abstract/searchable_api_resource.pyi', 'api_resources/abstract/singleton_api_resource.pyi', 'api_resources/abstract/updateable_api_resource.pyi', 'api_resources/abstract/verify_mixin.pyi', 'api_resources/account.pyi', 'api_resources/account_link.pyi', 'api_resources/alipay_account.pyi', 'api_resources/apple_pay_domain.pyi', 'api_resources/application_fee.pyi', 'api_resources/application_fee_refund.pyi', 'api_resources/balance.pyi', 'api_resources/balance_transaction.pyi', 'api_resources/bank_account.pyi', 'api_resources/billing_portal/__init__.pyi', 'api_resources/billing_portal/configuration.pyi', 'api_resources/billing_portal/session.pyi', 'api_resources/bitcoin_receiver.pyi', 'api_resources/bitcoin_transaction.pyi', 'api_resources/capability.pyi', 'api_resources/card.pyi', 'api_resources/charge.pyi', 'api_resources/checkout/__init__.pyi', 'api_resources/checkout/session.pyi', 'api_resources/country_spec.pyi', 'api_resources/coupon.pyi', 'api_resources/credit_note.pyi', 'api_resources/credit_note_line_item.pyi', 'api_resources/customer.pyi', 'api_resources/customer_balance_transaction.pyi', 'api_resources/dispute.pyi', 'api_resources/ephemeral_key.pyi', 'api_resources/error_object.pyi', 'api_resources/event.pyi', 'api_resources/exchange_rate.pyi', 'api_resources/file.pyi', 'api_resources/file_link.pyi', 'api_resources/identity/__init__.pyi', 'api_resources/identity/verification_report.pyi', 'api_resources/identity/verification_session.pyi', 'api_resources/invoice.pyi', 'api_resources/invoice_item.pyi', 'api_resources/invoice_line_item.pyi', 'api_resources/issuer_fraud_record.pyi', 'api_resources/issuing/__init__.pyi', 'api_resources/issuing/authorization.pyi', 'api_resources/issuing/card.pyi', 'api_resources/issuing/card_details.pyi', 'api_resources/issuing/cardholder.pyi', 'api_resources/issuing/dispute.pyi', 'api_resources/issuing/transaction.pyi', 'api_resources/line_item.pyi', 'api_resources/list_object.pyi', 'api_resources/login_link.pyi', 'api_resources/mandate.pyi', 'api_resources/order.pyi', 'api_resources/payment_intent.pyi', 'api_resources/payment_link.pyi', 'api_resources/payment_method.pyi', 'api_resources/payout.pyi', 'api_resources/person.pyi', 'api_resources/plan.pyi', 'api_resources/price.pyi', 'api_resources/product.pyi', 'api_resources/promotion_code.pyi', 'api_resources/quote.pyi', 'api_resources/radar/__init__.pyi', 'api_resources/radar/early_fraud_warning.pyi', 'api_resources/radar/value_list.pyi', 'api_resources/radar/value_list_item.pyi', 'api_resources/recipient.pyi', 'api_resources/recipient_transfer.pyi', 'api_resources/refund.pyi', 'api_resources/reporting/__init__.pyi', 'api_resources/reporting/report_run.pyi', 'api_resources/reporting/report_type.pyi', 'api_resources/reversal.pyi', 'api_resources/review.pyi', 'api_resources/search_result_object.pyi', 'api_resources/setup_attempt.pyi', 'api_resources/setup_intent.pyi', 'api_resources/shipping_rate.pyi', 'api_resources/sigma/__init__.pyi', 'api_resources/sigma/scheduled_query_run.pyi', 'api_resources/sku.pyi', 'api_resources/source.pyi', 'api_resources/source_transaction.pyi', 'api_resources/subscription.pyi', 'api_resources/subscription_item.pyi', 'api_resources/subscription_schedule.pyi', 'api_resources/tax_code.pyi', 'api_resources/tax_id.pyi', 'api_resources/tax_rate.pyi', 'api_resources/terminal/__init__.pyi', 'api_resources/terminal/connection_token.pyi', 'api_resources/terminal/location.pyi', 'api_resources/terminal/reader.pyi', 'api_resources/test_helpers/__init__.pyi', 'api_resources/test_helpers/test_clock.pyi', 'api_resources/three_d_secure.pyi', 'api_resources/token.pyi', 'api_resources/topup.pyi', 'api_resources/transfer.pyi', 'api_resources/usage_record.pyi', 'api_resources/usage_record_summary.pyi', 'api_resources/webhook_endpoint.pyi', 'error.pyi', 'http_client.pyi', 'multipart_data_generator.pyi', 'oauth.pyi', 'oauth_error.pyi', 'object_classes.pyi', 'request_metrics.pyi', 'stripe_object.pyi', 'stripe_response.pyi', 'util.pyi', 'version.pyi', 'webhook.pyi', 'METADATA.toml', 'py.typed']},
      license="Apache-2.0 license",
      python_requires=">=3.8",
      classifiers=[
          "License :: OSI Approved :: Apache Software License",
          "Programming Language :: Python :: 3",
          "Typing :: Stubs Only",
      ]
)
