/* generated */
#ifndef _PROTON_PROTOCOL_H
#define _PROTON_PROTOCOL_H 1

#include "proton/type_compat.h"

/* Field constants */
#define AMQP_FIELD_OPEN_CONTAINER_ID (0)
#define AMQP_FIELD_OPEN_HOSTNAME (1)
#define AMQP_FIELD_OPEN_MAX_FRAME_SIZE (2)
#define AMQP_OPEN_MAX_FRAME_SIZE_DEFAULT (4294967295) /* uint */
#define AMQP_FIELD_OPEN_CHANNEL_MAX (3)
#define AMQP_OPEN_CHANNEL_MAX_DEFAULT (65535) /* ushort */
#define AMQP_FIELD_OPEN_IDLE_TIME_OUT (4)
#define AMQP_FIELD_OPEN_OUTGOING_LOCALES (5)
#define AMQP_FIELD_OPEN_INCOMING_LOCALES (6)
#define AMQP_FIELD_OPEN_OFFERED_CAPABILITIES (7)
#define AMQP_FIELD_OPEN_DESIRED_CAPABILITIES (8)
#define AMQP_FIELD_OPEN_PROPERTIES (9)
#define AMQP_FIELD_BEGIN_REMOTE_CHANNEL (0)
#define AMQP_FIELD_BEGIN_NEXT_OUTGOING_ID (1)
#define AMQP_FIELD_BEGIN_INCOMING_WINDOW (2)
#define AMQP_FIELD_BEGIN_OUTGOING_WINDOW (3)
#define AMQP_FIELD_BEGIN_HANDLE_MAX (4)
#define AMQP_BEGIN_HANDLE_MAX_DEFAULT (4294967295) /* uint */
#define AMQP_FIELD_BEGIN_OFFERED_CAPABILITIES (5)
#define AMQP_FIELD_BEGIN_DESIRED_CAPABILITIES (6)
#define AMQP_FIELD_BEGIN_PROPERTIES (7)
#define AMQP_FIELD_ATTACH_NAME (0)
#define AMQP_FIELD_ATTACH_HANDLE (1)
#define AMQP_FIELD_ATTACH_ROLE (2)
#define AMQP_FIELD_ATTACH_SND_SETTLE_MODE (3)
#define AMQP_FIELD_ATTACH_RCV_SETTLE_MODE (4)
#define AMQP_FIELD_ATTACH_SOURCE (5)
#define AMQP_FIELD_ATTACH_TARGET (6)
#define AMQP_FIELD_ATTACH_UNSETTLED (7)
#define AMQP_FIELD_ATTACH_INCOMPLETE_UNSETTLED (8)
#define AMQP_FIELD_ATTACH_INITIAL_DELIVERY_COUNT (9)
#define AMQP_FIELD_ATTACH_MAX_MESSAGE_SIZE (10)
#define AMQP_FIELD_ATTACH_OFFERED_CAPABILITIES (11)
#define AMQP_FIELD_ATTACH_DESIRED_CAPABILITIES (12)
#define AMQP_FIELD_ATTACH_PROPERTIES (13)
#define AMQP_FIELD_FLOW_NEXT_INCOMING_ID (0)
#define AMQP_FIELD_FLOW_INCOMING_WINDOW (1)
#define AMQP_FIELD_FLOW_NEXT_OUTGOING_ID (2)
#define AMQP_FIELD_FLOW_OUTGOING_WINDOW (3)
#define AMQP_FIELD_FLOW_HANDLE (4)
#define AMQP_FIELD_FLOW_DELIVERY_COUNT (5)
#define AMQP_FIELD_FLOW_LINK_CREDIT (6)
#define AMQP_FIELD_FLOW_AVAILABLE (7)
#define AMQP_FIELD_FLOW_DRAIN (8)
#define AMQP_FIELD_FLOW_ECHO (9)
#define AMQP_FIELD_FLOW_PROPERTIES (10)
#define AMQP_FIELD_TRANSFER_HANDLE (0)
#define AMQP_FIELD_TRANSFER_DELIVERY_ID (1)
#define AMQP_FIELD_TRANSFER_DELIVERY_TAG (2)
#define AMQP_FIELD_TRANSFER_MESSAGE_FORMAT (3)
#define AMQP_FIELD_TRANSFER_SETTLED (4)
#define AMQP_FIELD_TRANSFER_MORE (5)
#define AMQP_FIELD_TRANSFER_RCV_SETTLE_MODE (6)
#define AMQP_FIELD_TRANSFER_STATE (7)
#define AMQP_FIELD_TRANSFER_RESUME (8)
#define AMQP_FIELD_TRANSFER_ABORTED (9)
#define AMQP_FIELD_TRANSFER_BATCHABLE (10)
#define AMQP_FIELD_DISPOSITION_ROLE (0)
#define AMQP_FIELD_DISPOSITION_FIRST (1)
#define AMQP_FIELD_DISPOSITION_LAST (2)
#define AMQP_FIELD_DISPOSITION_SETTLED (3)
#define AMQP_FIELD_DISPOSITION_STATE (4)
#define AMQP_FIELD_DISPOSITION_BATCHABLE (5)
#define AMQP_FIELD_DETACH_HANDLE (0)
#define AMQP_FIELD_DETACH_CLOSED (1)
#define AMQP_FIELD_DETACH_ERROR (2)
#define AMQP_FIELD_END_ERROR (0)
#define AMQP_FIELD_CLOSE_ERROR (0)
#define AMQP_FIELD_ERROR_CONDITION (0)
#define AMQP_FIELD_ERROR_DESCRIPTION (1)
#define AMQP_FIELD_ERROR_INFO (2)
#define AMQP_FIELD_HEADER_DURABLE (0)
#define AMQP_FIELD_HEADER_PRIORITY (1)
#define AMQP_HEADER_PRIORITY_DEFAULT (4) /* ubyte */
#define AMQP_FIELD_HEADER_TTL (2)
#define AMQP_FIELD_HEADER_FIRST_ACQUIRER (3)
#define AMQP_FIELD_HEADER_DELIVERY_COUNT (4)
#define AMQP_HEADER_DELIVERY_COUNT_DEFAULT (0) /* uint */
#define AMQP_FIELD_PROPERTIES_MESSAGE_ID (0)
#define AMQP_FIELD_PROPERTIES_USER_ID (1)
#define AMQP_FIELD_PROPERTIES_TO (2)
#define AMQP_FIELD_PROPERTIES_SUBJECT (3)
#define AMQP_FIELD_PROPERTIES_REPLY_TO (4)
#define AMQP_FIELD_PROPERTIES_CORRELATION_ID (5)
#define AMQP_FIELD_PROPERTIES_CONTENT_TYPE (6)
#define AMQP_FIELD_PROPERTIES_CONTENT_ENCODING (7)
#define AMQP_FIELD_PROPERTIES_ABSOLUTE_EXPIRY_TIME (8)
#define AMQP_FIELD_PROPERTIES_CREATION_TIME (9)
#define AMQP_FIELD_PROPERTIES_GROUP_ID (10)
#define AMQP_FIELD_PROPERTIES_GROUP_SEQUENCE (11)
#define AMQP_FIELD_PROPERTIES_REPLY_TO_GROUP_ID (12)
#define AMQP_FIELD_RECEIVED_SECTION_NUMBER (0)
#define AMQP_FIELD_RECEIVED_SECTION_OFFSET (1)
#define AMQP_FIELD_REJECTED_ERROR (0)
#define AMQP_FIELD_MODIFIED_DELIVERY_FAILED (0)
#define AMQP_FIELD_MODIFIED_UNDELIVERABLE_HERE (1)
#define AMQP_FIELD_MODIFIED_MESSAGE_ANNOTATIONS (2)
#define AMQP_FIELD_SOURCE_ADDRESS (0)
#define AMQP_FIELD_SOURCE_DURABLE (1)
#define AMQP_FIELD_SOURCE_EXPIRY_POLICY (2)
#define AMQP_SOURCE_EXPIRY_POLICY_DEFAULT ("session-end") /* symbol */
#define AMQP_FIELD_SOURCE_TIMEOUT (3)
#define AMQP_SOURCE_TIMEOUT_DEFAULT (0) /* uint */
#define AMQP_FIELD_SOURCE_DYNAMIC (4)
#define AMQP_FIELD_SOURCE_DYNAMIC_NODE_PROPERTIES (5)
#define AMQP_FIELD_SOURCE_DISTRIBUTION_MODE (6)
#define AMQP_FIELD_SOURCE_FILTER (7)
#define AMQP_FIELD_SOURCE_DEFAULT_OUTCOME (8)
#define AMQP_FIELD_SOURCE_OUTCOMES (9)
#define AMQP_FIELD_SOURCE_CAPABILITIES (10)
#define AMQP_FIELD_TARGET_ADDRESS (0)
#define AMQP_FIELD_TARGET_DURABLE (1)
#define AMQP_FIELD_TARGET_EXPIRY_POLICY (2)
#define AMQP_TARGET_EXPIRY_POLICY_DEFAULT ("session-end") /* symbol */
#define AMQP_FIELD_TARGET_TIMEOUT (3)
#define AMQP_TARGET_TIMEOUT_DEFAULT (0) /* uint */
#define AMQP_FIELD_TARGET_DYNAMIC (4)
#define AMQP_FIELD_TARGET_DYNAMIC_NODE_PROPERTIES (5)
#define AMQP_FIELD_TARGET_CAPABILITIES (6)
#define AMQP_FIELD_COORDINATOR_CAPABILITIES (0)
#define AMQP_FIELD_DECLARE_GLOBAL_ID (0)
#define AMQP_FIELD_DISCHARGE_TXN_ID (0)
#define AMQP_FIELD_DISCHARGE_FAIL (1)
#define AMQP_FIELD_DECLARED_TXN_ID (0)
#define AMQP_FIELD_TRANSACTIONAL_STATE_TXN_ID (0)
#define AMQP_FIELD_TRANSACTIONAL_STATE_OUTCOME (1)
#define AMQP_FIELD_SASL_MECHANISMS_SASL_SERVER_MECHANISMS (0)
#define AMQP_FIELD_SASL_INIT_MECHANISM (0)
#define AMQP_FIELD_SASL_INIT_INITIAL_RESPONSE (1)
#define AMQP_FIELD_SASL_INIT_HOSTNAME (2)
#define AMQP_FIELD_SASL_CHALLENGE_CHALLENGE (0)
#define AMQP_FIELD_SASL_RESPONSE_RESPONSE (0)
#define AMQP_FIELD_SASL_OUTCOME_CODE (0)
#define AMQP_FIELD_SASL_OUTCOME_ADDITIONAL_DATA (1)

/* Descriptors */
#define AMQP_DESC_OPEN_SYM ("amqp:open:list")
#define AMQP_DESC_OPEN ((uint64_t) 16)
#define AMQP_DESC_BEGIN_SYM ("amqp:begin:list")
#define AMQP_DESC_BEGIN ((uint64_t) 17)
#define AMQP_DESC_ATTACH_SYM ("amqp:attach:list")
#define AMQP_DESC_ATTACH ((uint64_t) 18)
#define AMQP_DESC_FLOW_SYM ("amqp:flow:list")
#define AMQP_DESC_FLOW ((uint64_t) 19)
#define AMQP_DESC_TRANSFER_SYM ("amqp:transfer:list")
#define AMQP_DESC_TRANSFER ((uint64_t) 20)
#define AMQP_DESC_DISPOSITION_SYM ("amqp:disposition:list")
#define AMQP_DESC_DISPOSITION ((uint64_t) 21)
#define AMQP_DESC_DETACH_SYM ("amqp:detach:list")
#define AMQP_DESC_DETACH ((uint64_t) 22)
#define AMQP_DESC_END_SYM ("amqp:end:list")
#define AMQP_DESC_END ((uint64_t) 23)
#define AMQP_DESC_CLOSE_SYM ("amqp:close:list")
#define AMQP_DESC_CLOSE ((uint64_t) 24)
#define AMQP_DESC_ERROR_SYM ("amqp:error:list")
#define AMQP_DESC_ERROR ((uint64_t) 29)
#define AMQP_DESC_HEADER_SYM ("amqp:header:list")
#define AMQP_DESC_HEADER ((uint64_t) 112)
#define AMQP_DESC_PROPERTIES_SYM ("amqp:properties:list")
#define AMQP_DESC_PROPERTIES ((uint64_t) 115)
#define AMQP_DESC_RECEIVED_SYM ("amqp:received:list")
#define AMQP_DESC_RECEIVED ((uint64_t) 35)
#define AMQP_DESC_ACCEPTED_SYM ("amqp:accepted:list")
#define AMQP_DESC_ACCEPTED ((uint64_t) 36)
#define AMQP_DESC_REJECTED_SYM ("amqp:rejected:list")
#define AMQP_DESC_REJECTED ((uint64_t) 37)
#define AMQP_DESC_RELEASED_SYM ("amqp:released:list")
#define AMQP_DESC_RELEASED ((uint64_t) 38)
#define AMQP_DESC_MODIFIED_SYM ("amqp:modified:list")
#define AMQP_DESC_MODIFIED ((uint64_t) 39)
#define AMQP_DESC_SOURCE_SYM ("amqp:source:list")
#define AMQP_DESC_SOURCE ((uint64_t) 40)
#define AMQP_DESC_TARGET_SYM ("amqp:target:list")
#define AMQP_DESC_TARGET ((uint64_t) 41)
#define AMQP_DESC_DELETE_ON_CLOSE_SYM ("amqp:delete-on-close:list")
#define AMQP_DESC_DELETE_ON_CLOSE ((uint64_t) 43)
#define AMQP_DESC_DELETE_ON_NO_LINKS_SYM ("amqp:delete-on-no-links:list")
#define AMQP_DESC_DELETE_ON_NO_LINKS ((uint64_t) 44)
#define AMQP_DESC_DELETE_ON_NO_MESSAGES_SYM ("amqp:delete-on-no-messages:list")
#define AMQP_DESC_DELETE_ON_NO_MESSAGES ((uint64_t) 45)
#define AMQP_DESC_DELETE_ON_NO_LINKS_OR_MESSAGES_SYM ("amqp:delete-on-no-links-or-messages:list")
#define AMQP_DESC_DELETE_ON_NO_LINKS_OR_MESSAGES ((uint64_t) 46)
#define AMQP_DESC_COORDINATOR_SYM ("amqp:coordinator:list")
#define AMQP_DESC_COORDINATOR ((uint64_t) 48)
#define AMQP_DESC_DECLARE_SYM ("amqp:declare:list")
#define AMQP_DESC_DECLARE ((uint64_t) 49)
#define AMQP_DESC_DISCHARGE_SYM ("amqp:discharge:list")
#define AMQP_DESC_DISCHARGE ((uint64_t) 50)
#define AMQP_DESC_DECLARED_SYM ("amqp:declared:list")
#define AMQP_DESC_DECLARED ((uint64_t) 51)
#define AMQP_DESC_TRANSACTIONAL_STATE_SYM ("amqp:transactional-state:list")
#define AMQP_DESC_TRANSACTIONAL_STATE ((uint64_t) 52)
#define AMQP_DESC_SASL_MECHANISMS_SYM ("amqp:sasl-mechanisms:list")
#define AMQP_DESC_SASL_MECHANISMS ((uint64_t) 64)
#define AMQP_DESC_SASL_INIT_SYM ("amqp:sasl-init:list")
#define AMQP_DESC_SASL_INIT ((uint64_t) 65)
#define AMQP_DESC_SASL_CHALLENGE_SYM ("amqp:sasl-challenge:list")
#define AMQP_DESC_SASL_CHALLENGE ((uint64_t) 66)
#define AMQP_DESC_SASL_RESPONSE_SYM ("amqp:sasl-response:list")
#define AMQP_DESC_SASL_RESPONSE ((uint64_t) 67)
#define AMQP_DESC_SASL_OUTCOME_SYM ("amqp:sasl-outcome:list")
#define AMQP_DESC_SASL_OUTCOME ((uint64_t) 68)
#define AMQP_DESC_DELIVERY_ANNOTATIONS_SYM ("amqp:delivery-annotations:map")
#define AMQP_DESC_DELIVERY_ANNOTATIONS ((uint64_t) 113)
#define AMQP_DESC_MESSAGE_ANNOTATIONS_SYM ("amqp:message-annotations:map")
#define AMQP_DESC_MESSAGE_ANNOTATIONS ((uint64_t) 114)
#define AMQP_DESC_APPLICATION_PROPERTIES_SYM ("amqp:application-properties:map")
#define AMQP_DESC_APPLICATION_PROPERTIES ((uint64_t) 116)
#define AMQP_DESC_DATA_SYM ("amqp:data:binary")
#define AMQP_DESC_DATA ((uint64_t) 117)
#define AMQP_DESC_AMQP_SEQUENCE_SYM ("amqp:amqp-sequence:list")
#define AMQP_DESC_AMQP_SEQUENCE ((uint64_t) 118)
#define AMQP_DESC_AMQP_VALUE_SYM ("amqp:amqp-value:*")
#define AMQP_DESC_AMQP_VALUE ((uint64_t) 119)
#define AMQP_DESC_FOOTER_SYM ("amqp:footer:map")
#define AMQP_DESC_FOOTER ((uint64_t) 120)

/* Described type field descriptions */
#include <stddef.h>

typedef struct {
  const unsigned char name_index;
  const unsigned char first_field_index;
  const unsigned char field_count;
} pn_fields_t;

extern const pn_fields_t FIELDS[];
extern const uint16_t FIELD_NAME[];
extern const uint16_t FIELD_FIELDS[];

struct FIELD_STRINGS {
  const char STRING0[sizeof("")];
  const char FIELD_STRINGS_application_properties[sizeof("application-properties")];
  const char FIELD_STRINGS_handle_max[sizeof("handle-max")];
  const char FIELD_STRINGS_header[sizeof("header")];
  const char FIELD_STRINGS_discharge[sizeof("discharge")];
  const char FIELD_STRINGS_received[sizeof("received")];
  const char FIELD_STRINGS_disposition[sizeof("disposition")];
  const char FIELD_STRINGS_distribution_mode[sizeof("distribution-mode")];
  const char FIELD_STRINGS_initial_delivery_count[sizeof("initial-delivery-count")];
  const char FIELD_STRINGS_settled[sizeof("settled")];
  const char FIELD_STRINGS_sasl_outcome[sizeof("sasl-outcome")];
  const char FIELD_STRINGS_drain[sizeof("drain")];
  const char FIELD_STRINGS_delivery_tag[sizeof("delivery-tag")];
  const char FIELD_STRINGS_address[sizeof("address")];
  const char FIELD_STRINGS_state[sizeof("state")];
  const char FIELD_STRINGS_ttl[sizeof("ttl")];
  const char FIELD_STRINGS_sasl_server_mechanisms[sizeof("sasl-server-mechanisms")];
  const char FIELD_STRINGS_expiry_policy[sizeof("expiry-policy")];
  const char FIELD_STRINGS_flow[sizeof("flow")];
  const char FIELD_STRINGS_first[sizeof("first")];
  const char FIELD_STRINGS_absolute_expiry_time[sizeof("absolute-expiry-time")];
  const char FIELD_STRINGS_outcome[sizeof("outcome")];
  const char FIELD_STRINGS_closed[sizeof("closed")];
  const char FIELD_STRINGS_response[sizeof("response")];
  const char FIELD_STRINGS_durable[sizeof("durable")];
  const char FIELD_STRINGS_modified[sizeof("modified")];
  const char FIELD_STRINGS_delivery_failed[sizeof("delivery-failed")];
  const char FIELD_STRINGS_detach[sizeof("detach")];
  const char FIELD_STRINGS_outgoing_window[sizeof("outgoing-window")];
  const char FIELD_STRINGS_attach[sizeof("attach")];
  const char FIELD_STRINGS_sasl_challenge[sizeof("sasl-challenge")];
  const char FIELD_STRINGS_rcv_settle_mode[sizeof("rcv-settle-mode")];
  const char FIELD_STRINGS_capabilities[sizeof("capabilities")];
  const char FIELD_STRINGS_global_id[sizeof("global-id")];
  const char FIELD_STRINGS_begin[sizeof("begin")];
  const char FIELD_STRINGS_delete_on_no_messages[sizeof("delete-on-no-messages")];
  const char FIELD_STRINGS_desired_capabilities[sizeof("desired-capabilities")];
  const char FIELD_STRINGS_dynamic_node_properties[sizeof("dynamic-node-properties")];
  const char FIELD_STRINGS_reply_to[sizeof("reply-to")];
  const char FIELD_STRINGS_unsettled[sizeof("unsettled")];
  const char FIELD_STRINGS_group_id[sizeof("group-id")];
  const char FIELD_STRINGS_footer[sizeof("footer")];
  const char FIELD_STRINGS_idle_time_out[sizeof("idle-time-out")];
  const char FIELD_STRINGS_reply_to_group_id[sizeof("reply-to-group-id")];
  const char FIELD_STRINGS_mechanism[sizeof("mechanism")];
  const char FIELD_STRINGS_delete_on_close[sizeof("delete-on-close")];
  const char FIELD_STRINGS_released[sizeof("released")];
  const char FIELD_STRINGS_transactional_state[sizeof("transactional-state")];
  const char FIELD_STRINGS_batchable[sizeof("batchable")];
  const char FIELD_STRINGS_filter[sizeof("filter")];
  const char FIELD_STRINGS_role[sizeof("role")];
  const char FIELD_STRINGS_remote_channel[sizeof("remote-channel")];
  const char FIELD_STRINGS_outgoing_locales[sizeof("outgoing-locales")];
  const char FIELD_STRINGS_group_sequence[sizeof("group-sequence")];
  const char FIELD_STRINGS_txn_id[sizeof("txn-id")];
  const char FIELD_STRINGS_last[sizeof("last")];
  const char FIELD_STRINGS_offered_capabilities[sizeof("offered-capabilities")];
  const char FIELD_STRINGS_undeliverable_here[sizeof("undeliverable-here")];
  const char FIELD_STRINGS_next_outgoing_id[sizeof("next-outgoing-id")];
  const char FIELD_STRINGS_more[sizeof("more")];
  const char FIELD_STRINGS_creation_time[sizeof("creation-time")];
  const char FIELD_STRINGS_target[sizeof("target")];
  const char FIELD_STRINGS_max_frame_size[sizeof("max-frame-size")];
  const char FIELD_STRINGS_end[sizeof("end")];
  const char FIELD_STRINGS_source[sizeof("source")];
  const char FIELD_STRINGS_incoming_window[sizeof("incoming-window")];
  const char FIELD_STRINGS_dynamic[sizeof("dynamic")];
  const char FIELD_STRINGS_first_acquirer[sizeof("first-acquirer")];
  const char FIELD_STRINGS_code[sizeof("code")];
  const char FIELD_STRINGS_aborted[sizeof("aborted")];
  const char FIELD_STRINGS_error[sizeof("error")];
  const char FIELD_STRINGS_info[sizeof("info")];
  const char FIELD_STRINGS_delete_on_no_links[sizeof("delete-on-no-links")];
  const char FIELD_STRINGS_resume[sizeof("resume")];
  const char FIELD_STRINGS_user_id[sizeof("user-id")];
  const char FIELD_STRINGS_data[sizeof("data")];
  const char FIELD_STRINGS_initial_response[sizeof("initial-response")];
  const char FIELD_STRINGS_delete_on_no_links_or_messages[sizeof("delete-on-no-links-or-messages")];
  const char FIELD_STRINGS_condition[sizeof("condition")];
  const char FIELD_STRINGS_additional_data[sizeof("additional-data")];
  const char FIELD_STRINGS_description[sizeof("description")];
  const char FIELD_STRINGS_default_outcome[sizeof("default-outcome")];
  const char FIELD_STRINGS_message_annotations[sizeof("message-annotations")];
  const char FIELD_STRINGS_next_incoming_id[sizeof("next-incoming-id")];
  const char FIELD_STRINGS_declared[sizeof("declared")];
  const char FIELD_STRINGS_container_id[sizeof("container-id")];
  const char FIELD_STRINGS_sasl_init[sizeof("sasl-init")];
  const char FIELD_STRINGS_correlation_id[sizeof("correlation-id")];
  const char FIELD_STRINGS_coordinator[sizeof("coordinator")];
  const char FIELD_STRINGS_sasl_mechanisms[sizeof("sasl-mechanisms")];
  const char FIELD_STRINGS_handle[sizeof("handle")];
  const char FIELD_STRINGS_timeout[sizeof("timeout")];
  const char FIELD_STRINGS_open[sizeof("open")];
  const char FIELD_STRINGS_available[sizeof("available")];
  const char FIELD_STRINGS_max_message_size[sizeof("max-message-size")];
  const char FIELD_STRINGS_section_number[sizeof("section-number")];
  const char FIELD_STRINGS_section_offset[sizeof("section-offset")];
  const char FIELD_STRINGS_message_format[sizeof("message-format")];
  const char FIELD_STRINGS_to[sizeof("to")];
  const char FIELD_STRINGS_delivery_id[sizeof("delivery-id")];
  const char FIELD_STRINGS_properties[sizeof("properties")];
  const char FIELD_STRINGS_accepted[sizeof("accepted")];
  const char FIELD_STRINGS_content_encoding[sizeof("content-encoding")];
  const char FIELD_STRINGS_name[sizeof("name")];
  const char FIELD_STRINGS_link_credit[sizeof("link-credit")];
  const char FIELD_STRINGS_amqp_value[sizeof("amqp-value")];
  const char FIELD_STRINGS_outcomes[sizeof("outcomes")];
  const char FIELD_STRINGS_incomplete_unsettled[sizeof("incomplete-unsettled")];
  const char FIELD_STRINGS_amqp_sequence[sizeof("amqp-sequence")];
  const char FIELD_STRINGS_challenge[sizeof("challenge")];
  const char FIELD_STRINGS_subject[sizeof("subject")];
  const char FIELD_STRINGS_hostname[sizeof("hostname")];
  const char FIELD_STRINGS_transfer[sizeof("transfer")];
  const char FIELD_STRINGS_rejected[sizeof("rejected")];
  const char FIELD_STRINGS_delivery_annotations[sizeof("delivery-annotations")];
  const char FIELD_STRINGS_channel_max[sizeof("channel-max")];
  const char FIELD_STRINGS_delivery_count[sizeof("delivery-count")];
  const char FIELD_STRINGS_snd_settle_mode[sizeof("snd-settle-mode")];
  const char FIELD_STRINGS_priority[sizeof("priority")];
  const char FIELD_STRINGS_fail[sizeof("fail")];
  const char FIELD_STRINGS_content_type[sizeof("content-type")];
  const char FIELD_STRINGS_declare[sizeof("declare")];
  const char FIELD_STRINGS_echo[sizeof("echo")];
  const char FIELD_STRINGS_message_id[sizeof("message-id")];
  const char FIELD_STRINGS_close[sizeof("close")];
  const char FIELD_STRINGS_incoming_locales[sizeof("incoming-locales")];
  const char FIELD_STRINGS_sasl_response[sizeof("sasl-response")];
};

extern const struct FIELD_STRINGS FIELD_STRINGPOOL;
#ifdef DEFINE_FIELDS

const struct FIELD_STRINGS FIELD_STRINGPOOL = {
  "",
  "application-properties",
  "handle-max",
  "header",
  "discharge",
  "received",
  "disposition",
  "distribution-mode",
  "initial-delivery-count",
  "settled",
  "sasl-outcome",
  "drain",
  "delivery-tag",
  "address",
  "state",
  "ttl",
  "sasl-server-mechanisms",
  "expiry-policy",
  "flow",
  "first",
  "absolute-expiry-time",
  "outcome",
  "closed",
  "response",
  "durable",
  "modified",
  "delivery-failed",
  "detach",
  "outgoing-window",
  "attach",
  "sasl-challenge",
  "rcv-settle-mode",
  "capabilities",
  "global-id",
  "begin",
  "delete-on-no-messages",
  "desired-capabilities",
  "dynamic-node-properties",
  "reply-to",
  "unsettled",
  "group-id",
  "footer",
  "idle-time-out",
  "reply-to-group-id",
  "mechanism",
  "delete-on-close",
  "released",
  "transactional-state",
  "batchable",
  "filter",
  "role",
  "remote-channel",
  "outgoing-locales",
  "group-sequence",
  "txn-id",
  "last",
  "offered-capabilities",
  "undeliverable-here",
  "next-outgoing-id",
  "more",
  "creation-time",
  "target",
  "max-frame-size",
  "end",
  "source",
  "incoming-window",
  "dynamic",
  "first-acquirer",
  "code",
  "aborted",
  "error",
  "info",
  "delete-on-no-links",
  "resume",
  "user-id",
  "data",
  "initial-response",
  "delete-on-no-links-or-messages",
  "condition",
  "additional-data",
  "description",
  "default-outcome",
  "message-annotations",
  "next-incoming-id",
  "declared",
  "container-id",
  "sasl-init",
  "correlation-id",
  "coordinator",
  "sasl-mechanisms",
  "handle",
  "timeout",
  "open",
  "available",
  "max-message-size",
  "section-number",
  "section-offset",
  "message-format",
  "to",
  "delivery-id",
  "properties",
  "accepted",
  "content-encoding",
  "name",
  "link-credit",
  "amqp-value",
  "outcomes",
  "incomplete-unsettled",
  "amqp-sequence",
  "challenge",
  "subject",
  "hostname",
  "transfer",
  "rejected",
  "delivery-annotations",
  "channel-max",
  "delivery-count",
  "snd-settle-mode",
  "priority",
  "fail",
  "content-type",
  "declare",
  "echo",
  "message-id",
  "close",
  "incoming-locales",
  "sasl-response",
};

/* This is an array of offsets into FIELD_STRINGPOOL */
const uint16_t FIELD_NAME[] = {
  offsetof(struct FIELD_STRINGS, STRING0),
  offsetof(struct FIELD_STRINGS, FIELD_STRINGS_open), /* 1 */
  offsetof(struct FIELD_STRINGS, FIELD_STRINGS_begin), /* 2 */
  offsetof(struct FIELD_STRINGS, FIELD_STRINGS_attach), /* 3 */
  offsetof(struct FIELD_STRINGS, FIELD_STRINGS_flow), /* 4 */
  offsetof(struct FIELD_STRINGS, FIELD_STRINGS_transfer), /* 5 */
  offsetof(struct FIELD_STRINGS, FIELD_STRINGS_disposition), /* 6 */
  offsetof(struct FIELD_STRINGS, FIELD_STRINGS_detach), /* 7 */
  offsetof(struct FIELD_STRINGS, FIELD_STRINGS_end), /* 8 */
  offsetof(struct FIELD_STRINGS, FIELD_STRINGS_close), /* 9 */
  offsetof(struct FIELD_STRINGS, FIELD_STRINGS_error), /* 10 */
  offsetof(struct FIELD_STRINGS, FIELD_STRINGS_received), /* 11 */
  offsetof(struct FIELD_STRINGS, FIELD_STRINGS_accepted), /* 12 */
  offsetof(struct FIELD_STRINGS, FIELD_STRINGS_rejected), /* 13 */
  offsetof(struct FIELD_STRINGS, FIELD_STRINGS_released), /* 14 */
  offsetof(struct FIELD_STRINGS, FIELD_STRINGS_modified), /* 15 */
  offsetof(struct FIELD_STRINGS, FIELD_STRINGS_source), /* 16 */
  offsetof(struct FIELD_STRINGS, FIELD_STRINGS_target), /* 17 */
  offsetof(struct FIELD_STRINGS, FIELD_STRINGS_delete_on_close), /* 18 */
  offsetof(struct FIELD_STRINGS, FIELD_STRINGS_delete_on_no_links), /* 19 */
  offsetof(struct FIELD_STRINGS, FIELD_STRINGS_delete_on_no_messages), /* 20 */
  offsetof(struct FIELD_STRINGS, FIELD_STRINGS_delete_on_no_links_or_messages), /* 21 */
  offsetof(struct FIELD_STRINGS, FIELD_STRINGS_coordinator), /* 22 */
  offsetof(struct FIELD_STRINGS, FIELD_STRINGS_declare), /* 23 */
  offsetof(struct FIELD_STRINGS, FIELD_STRINGS_discharge), /* 24 */
  offsetof(struct FIELD_STRINGS, FIELD_STRINGS_declared), /* 25 */
  offsetof(struct FIELD_STRINGS, FIELD_STRINGS_transactional_state), /* 26 */
  offsetof(struct FIELD_STRINGS, FIELD_STRINGS_sasl_mechanisms), /* 27 */
  offsetof(struct FIELD_STRINGS, FIELD_STRINGS_sasl_init), /* 28 */
  offsetof(struct FIELD_STRINGS, FIELD_STRINGS_sasl_challenge), /* 29 */
  offsetof(struct FIELD_STRINGS, FIELD_STRINGS_sasl_response), /* 30 */
  offsetof(struct FIELD_STRINGS, FIELD_STRINGS_sasl_outcome), /* 31 */
  offsetof(struct FIELD_STRINGS, FIELD_STRINGS_header), /* 32 */
  offsetof(struct FIELD_STRINGS, FIELD_STRINGS_delivery_annotations), /* 33 */
  offsetof(struct FIELD_STRINGS, FIELD_STRINGS_message_annotations), /* 34 */
  offsetof(struct FIELD_STRINGS, FIELD_STRINGS_properties), /* 35 */
  offsetof(struct FIELD_STRINGS, FIELD_STRINGS_application_properties), /* 36 */
  offsetof(struct FIELD_STRINGS, FIELD_STRINGS_data), /* 37 */
  offsetof(struct FIELD_STRINGS, FIELD_STRINGS_amqp_sequence), /* 38 */
  offsetof(struct FIELD_STRINGS, FIELD_STRINGS_amqp_value), /* 39 */
  offsetof(struct FIELD_STRINGS, FIELD_STRINGS_footer), /* 40 */
};
/* This is an array of offsets into FIELD_STRINGPOOL */
const uint16_t FIELD_FIELDS[] = {
  offsetof(struct FIELD_STRINGS, STRING0),
  offsetof(struct FIELD_STRINGS, FIELD_STRINGS_container_id), /* 1 (open) */
  offsetof(struct FIELD_STRINGS, FIELD_STRINGS_hostname), /* 2 (open) */
  offsetof(struct FIELD_STRINGS, FIELD_STRINGS_max_frame_size), /* 3 (open) */
  offsetof(struct FIELD_STRINGS, FIELD_STRINGS_channel_max), /* 4 (open) */
  offsetof(struct FIELD_STRINGS, FIELD_STRINGS_idle_time_out), /* 5 (open) */
  offsetof(struct FIELD_STRINGS, FIELD_STRINGS_outgoing_locales), /* 6 (open) */
  offsetof(struct FIELD_STRINGS, FIELD_STRINGS_incoming_locales), /* 7 (open) */
  offsetof(struct FIELD_STRINGS, FIELD_STRINGS_offered_capabilities), /* 8 (open) */
  offsetof(struct FIELD_STRINGS, FIELD_STRINGS_desired_capabilities), /* 9 (open) */
  offsetof(struct FIELD_STRINGS, FIELD_STRINGS_properties), /* 10 (open) */
  offsetof(struct FIELD_STRINGS, FIELD_STRINGS_remote_channel), /* 11 (begin) */
  offsetof(struct FIELD_STRINGS, FIELD_STRINGS_next_outgoing_id), /* 12 (begin) */
  offsetof(struct FIELD_STRINGS, FIELD_STRINGS_incoming_window), /* 13 (begin) */
  offsetof(struct FIELD_STRINGS, FIELD_STRINGS_outgoing_window), /* 14 (begin) */
  offsetof(struct FIELD_STRINGS, FIELD_STRINGS_handle_max), /* 15 (begin) */
  offsetof(struct FIELD_STRINGS, FIELD_STRINGS_offered_capabilities), /* 16 (begin) */
  offsetof(struct FIELD_STRINGS, FIELD_STRINGS_desired_capabilities), /* 17 (begin) */
  offsetof(struct FIELD_STRINGS, FIELD_STRINGS_properties), /* 18 (begin) */
  offsetof(struct FIELD_STRINGS, FIELD_STRINGS_name), /* 19 (attach) */
  offsetof(struct FIELD_STRINGS, FIELD_STRINGS_handle), /* 20 (attach) */
  offsetof(struct FIELD_STRINGS, FIELD_STRINGS_role), /* 21 (attach) */
  offsetof(struct FIELD_STRINGS, FIELD_STRINGS_snd_settle_mode), /* 22 (attach) */
  offsetof(struct FIELD_STRINGS, FIELD_STRINGS_rcv_settle_mode), /* 23 (attach) */
  offsetof(struct FIELD_STRINGS, FIELD_STRINGS_source), /* 24 (attach) */
  offsetof(struct FIELD_STRINGS, FIELD_STRINGS_target), /* 25 (attach) */
  offsetof(struct FIELD_STRINGS, FIELD_STRINGS_unsettled), /* 26 (attach) */
  offsetof(struct FIELD_STRINGS, FIELD_STRINGS_incomplete_unsettled), /* 27 (attach) */
  offsetof(struct FIELD_STRINGS, FIELD_STRINGS_initial_delivery_count), /* 28 (attach) */
  offsetof(struct FIELD_STRINGS, FIELD_STRINGS_max_message_size), /* 29 (attach) */
  offsetof(struct FIELD_STRINGS, FIELD_STRINGS_offered_capabilities), /* 30 (attach) */
  offsetof(struct FIELD_STRINGS, FIELD_STRINGS_desired_capabilities), /* 31 (attach) */
  offsetof(struct FIELD_STRINGS, FIELD_STRINGS_properties), /* 32 (attach) */
  offsetof(struct FIELD_STRINGS, FIELD_STRINGS_next_incoming_id), /* 33 (flow) */
  offsetof(struct FIELD_STRINGS, FIELD_STRINGS_incoming_window), /* 34 (flow) */
  offsetof(struct FIELD_STRINGS, FIELD_STRINGS_next_outgoing_id), /* 35 (flow) */
  offsetof(struct FIELD_STRINGS, FIELD_STRINGS_outgoing_window), /* 36 (flow) */
  offsetof(struct FIELD_STRINGS, FIELD_STRINGS_handle), /* 37 (flow) */
  offsetof(struct FIELD_STRINGS, FIELD_STRINGS_delivery_count), /* 38 (flow) */
  offsetof(struct FIELD_STRINGS, FIELD_STRINGS_link_credit), /* 39 (flow) */
  offsetof(struct FIELD_STRINGS, FIELD_STRINGS_available), /* 40 (flow) */
  offsetof(struct FIELD_STRINGS, FIELD_STRINGS_drain), /* 41 (flow) */
  offsetof(struct FIELD_STRINGS, FIELD_STRINGS_echo), /* 42 (flow) */
  offsetof(struct FIELD_STRINGS, FIELD_STRINGS_properties), /* 43 (flow) */
  offsetof(struct FIELD_STRINGS, FIELD_STRINGS_handle), /* 44 (transfer) */
  offsetof(struct FIELD_STRINGS, FIELD_STRINGS_delivery_id), /* 45 (transfer) */
  offsetof(struct FIELD_STRINGS, FIELD_STRINGS_delivery_tag), /* 46 (transfer) */
  offsetof(struct FIELD_STRINGS, FIELD_STRINGS_message_format), /* 47 (transfer) */
  offsetof(struct FIELD_STRINGS, FIELD_STRINGS_settled), /* 48 (transfer) */
  offsetof(struct FIELD_STRINGS, FIELD_STRINGS_more), /* 49 (transfer) */
  offsetof(struct FIELD_STRINGS, FIELD_STRINGS_rcv_settle_mode), /* 50 (transfer) */
  offsetof(struct FIELD_STRINGS, FIELD_STRINGS_state), /* 51 (transfer) */
  offsetof(struct FIELD_STRINGS, FIELD_STRINGS_resume), /* 52 (transfer) */
  offsetof(struct FIELD_STRINGS, FIELD_STRINGS_aborted), /* 53 (transfer) */
  offsetof(struct FIELD_STRINGS, FIELD_STRINGS_batchable), /* 54 (transfer) */
  offsetof(struct FIELD_STRINGS, FIELD_STRINGS_role), /* 55 (disposition) */
  offsetof(struct FIELD_STRINGS, FIELD_STRINGS_first), /* 56 (disposition) */
  offsetof(struct FIELD_STRINGS, FIELD_STRINGS_last), /* 57 (disposition) */
  offsetof(struct FIELD_STRINGS, FIELD_STRINGS_settled), /* 58 (disposition) */
  offsetof(struct FIELD_STRINGS, FIELD_STRINGS_state), /* 59 (disposition) */
  offsetof(struct FIELD_STRINGS, FIELD_STRINGS_batchable), /* 60 (disposition) */
  offsetof(struct FIELD_STRINGS, FIELD_STRINGS_handle), /* 61 (detach) */
  offsetof(struct FIELD_STRINGS, FIELD_STRINGS_closed), /* 62 (detach) */
  offsetof(struct FIELD_STRINGS, FIELD_STRINGS_error), /* 63 (detach) */
  offsetof(struct FIELD_STRINGS, FIELD_STRINGS_error), /* 64 (end) */
  offsetof(struct FIELD_STRINGS, FIELD_STRINGS_error), /* 65 (close) */
  offsetof(struct FIELD_STRINGS, FIELD_STRINGS_condition), /* 66 (error) */
  offsetof(struct FIELD_STRINGS, FIELD_STRINGS_description), /* 67 (error) */
  offsetof(struct FIELD_STRINGS, FIELD_STRINGS_info), /* 68 (error) */
  offsetof(struct FIELD_STRINGS, FIELD_STRINGS_section_number), /* 69 (received) */
  offsetof(struct FIELD_STRINGS, FIELD_STRINGS_section_offset), /* 70 (received) */
  offsetof(struct FIELD_STRINGS, FIELD_STRINGS_error), /* 71 (rejected) */
  offsetof(struct FIELD_STRINGS, FIELD_STRINGS_delivery_failed), /* 72 (modified) */
  offsetof(struct FIELD_STRINGS, FIELD_STRINGS_undeliverable_here), /* 73 (modified) */
  offsetof(struct FIELD_STRINGS, FIELD_STRINGS_message_annotations), /* 74 (modified) */
  offsetof(struct FIELD_STRINGS, FIELD_STRINGS_address), /* 75 (source) */
  offsetof(struct FIELD_STRINGS, FIELD_STRINGS_durable), /* 76 (source) */
  offsetof(struct FIELD_STRINGS, FIELD_STRINGS_expiry_policy), /* 77 (source) */
  offsetof(struct FIELD_STRINGS, FIELD_STRINGS_timeout), /* 78 (source) */
  offsetof(struct FIELD_STRINGS, FIELD_STRINGS_dynamic), /* 79 (source) */
  offsetof(struct FIELD_STRINGS, FIELD_STRINGS_dynamic_node_properties), /* 80 (source) */
  offsetof(struct FIELD_STRINGS, FIELD_STRINGS_distribution_mode), /* 81 (source) */
  offsetof(struct FIELD_STRINGS, FIELD_STRINGS_filter), /* 82 (source) */
  offsetof(struct FIELD_STRINGS, FIELD_STRINGS_default_outcome), /* 83 (source) */
  offsetof(struct FIELD_STRINGS, FIELD_STRINGS_outcomes), /* 84 (source) */
  offsetof(struct FIELD_STRINGS, FIELD_STRINGS_capabilities), /* 85 (source) */
  offsetof(struct FIELD_STRINGS, FIELD_STRINGS_address), /* 86 (target) */
  offsetof(struct FIELD_STRINGS, FIELD_STRINGS_durable), /* 87 (target) */
  offsetof(struct FIELD_STRINGS, FIELD_STRINGS_expiry_policy), /* 88 (target) */
  offsetof(struct FIELD_STRINGS, FIELD_STRINGS_timeout), /* 89 (target) */
  offsetof(struct FIELD_STRINGS, FIELD_STRINGS_dynamic), /* 90 (target) */
  offsetof(struct FIELD_STRINGS, FIELD_STRINGS_dynamic_node_properties), /* 91 (target) */
  offsetof(struct FIELD_STRINGS, FIELD_STRINGS_capabilities), /* 92 (target) */
  offsetof(struct FIELD_STRINGS, FIELD_STRINGS_capabilities), /* 93 (coordinator) */
  offsetof(struct FIELD_STRINGS, FIELD_STRINGS_global_id), /* 94 (declare) */
  offsetof(struct FIELD_STRINGS, FIELD_STRINGS_txn_id), /* 95 (discharge) */
  offsetof(struct FIELD_STRINGS, FIELD_STRINGS_fail), /* 96 (discharge) */
  offsetof(struct FIELD_STRINGS, FIELD_STRINGS_txn_id), /* 97 (declared) */
  offsetof(struct FIELD_STRINGS, FIELD_STRINGS_txn_id), /* 98 (transactional-state) */
  offsetof(struct FIELD_STRINGS, FIELD_STRINGS_outcome), /* 99 (transactional-state) */
  offsetof(struct FIELD_STRINGS, FIELD_STRINGS_sasl_server_mechanisms), /* 100 (sasl-mechanisms) */
  offsetof(struct FIELD_STRINGS, FIELD_STRINGS_mechanism), /* 101 (sasl-init) */
  offsetof(struct FIELD_STRINGS, FIELD_STRINGS_initial_response), /* 102 (sasl-init) */
  offsetof(struct FIELD_STRINGS, FIELD_STRINGS_hostname), /* 103 (sasl-init) */
  offsetof(struct FIELD_STRINGS, FIELD_STRINGS_challenge), /* 104 (sasl-challenge) */
  offsetof(struct FIELD_STRINGS, FIELD_STRINGS_response), /* 105 (sasl-response) */
  offsetof(struct FIELD_STRINGS, FIELD_STRINGS_code), /* 106 (sasl-outcome) */
  offsetof(struct FIELD_STRINGS, FIELD_STRINGS_additional_data), /* 107 (sasl-outcome) */
  offsetof(struct FIELD_STRINGS, FIELD_STRINGS_durable), /* 108 (header) */
  offsetof(struct FIELD_STRINGS, FIELD_STRINGS_priority), /* 109 (header) */
  offsetof(struct FIELD_STRINGS, FIELD_STRINGS_ttl), /* 110 (header) */
  offsetof(struct FIELD_STRINGS, FIELD_STRINGS_first_acquirer), /* 111 (header) */
  offsetof(struct FIELD_STRINGS, FIELD_STRINGS_delivery_count), /* 112 (header) */
  offsetof(struct FIELD_STRINGS, FIELD_STRINGS_message_id), /* 113 (properties) */
  offsetof(struct FIELD_STRINGS, FIELD_STRINGS_user_id), /* 114 (properties) */
  offsetof(struct FIELD_STRINGS, FIELD_STRINGS_to), /* 115 (properties) */
  offsetof(struct FIELD_STRINGS, FIELD_STRINGS_subject), /* 116 (properties) */
  offsetof(struct FIELD_STRINGS, FIELD_STRINGS_reply_to), /* 117 (properties) */
  offsetof(struct FIELD_STRINGS, FIELD_STRINGS_correlation_id), /* 118 (properties) */
  offsetof(struct FIELD_STRINGS, FIELD_STRINGS_content_type), /* 119 (properties) */
  offsetof(struct FIELD_STRINGS, FIELD_STRINGS_content_encoding), /* 120 (properties) */
  offsetof(struct FIELD_STRINGS, FIELD_STRINGS_absolute_expiry_time), /* 121 (properties) */
  offsetof(struct FIELD_STRINGS, FIELD_STRINGS_creation_time), /* 122 (properties) */
  offsetof(struct FIELD_STRINGS, FIELD_STRINGS_group_id), /* 123 (properties) */
  offsetof(struct FIELD_STRINGS, FIELD_STRINGS_group_sequence), /* 124 (properties) */
  offsetof(struct FIELD_STRINGS, FIELD_STRINGS_reply_to_group_id), /* 125 (properties) */
};
const pn_fields_t FIELDS[] = {
  {1, 1, 10}, /* 16 (open) */
  {2, 11, 8}, /* 17 (begin) */
  {3, 19, 14}, /* 18 (attach) */
  {4, 33, 11}, /* 19 (flow) */
  {5, 44, 11}, /* 20 (transfer) */
  {6, 55, 6}, /* 21 (disposition) */
  {7, 61, 3}, /* 22 (detach) */
  {8, 64, 1}, /* 23 (end) */
  {9, 65, 1}, /* 24 (close) */
  {0, 0, 0}, /* 25 */
  {0, 0, 0}, /* 26 */
  {0, 0, 0}, /* 27 */
  {0, 0, 0}, /* 28 */
  {10, 66, 3}, /* 29 (error) */
  {0, 0, 0}, /* 30 */
  {0, 0, 0}, /* 31 */
  {0, 0, 0}, /* 32 */
  {0, 0, 0}, /* 33 */
  {0, 0, 0}, /* 34 */
  {11, 69, 2}, /* 35 (received) */
  {12, 0, 0}, /* 36 (accepted) */
  {13, 71, 1}, /* 37 (rejected) */
  {14, 0, 0}, /* 38 (released) */
  {15, 72, 3}, /* 39 (modified) */
  {16, 75, 11}, /* 40 (source) */
  {17, 86, 7}, /* 41 (target) */
  {0, 0, 0}, /* 42 */
  {18, 0, 0}, /* 43 (delete-on-close) */
  {19, 0, 0}, /* 44 (delete-on-no-links) */
  {20, 0, 0}, /* 45 (delete-on-no-messages) */
  {21, 0, 0}, /* 46 (delete-on-no-links-or-messages) */
  {0, 0, 0}, /* 47 */
  {22, 93, 1}, /* 48 (coordinator) */
  {23, 94, 1}, /* 49 (declare) */
  {24, 95, 2}, /* 50 (discharge) */
  {25, 97, 1}, /* 51 (declared) */
  {26, 98, 2}, /* 52 (transactional-state) */
  {0, 0, 0}, /* 53 */
  {0, 0, 0}, /* 54 */
  {0, 0, 0}, /* 55 */
  {0, 0, 0}, /* 56 */
  {0, 0, 0}, /* 57 */
  {0, 0, 0}, /* 58 */
  {0, 0, 0}, /* 59 */
  {0, 0, 0}, /* 60 */
  {0, 0, 0}, /* 61 */
  {0, 0, 0}, /* 62 */
  {0, 0, 0}, /* 63 */
  {27, 100, 1}, /* 64 (sasl-mechanisms) */
  {28, 101, 3}, /* 65 (sasl-init) */
  {29, 104, 1}, /* 66 (sasl-challenge) */
  {30, 105, 1}, /* 67 (sasl-response) */
  {31, 106, 2}, /* 68 (sasl-outcome) */
  {0, 0, 0}, /* 69 */
  {0, 0, 0}, /* 70 */
  {0, 0, 0}, /* 71 */
  {0, 0, 0}, /* 72 */
  {0, 0, 0}, /* 73 */
  {0, 0, 0}, /* 74 */
  {0, 0, 0}, /* 75 */
  {0, 0, 0}, /* 76 */
  {0, 0, 0}, /* 77 */
  {0, 0, 0}, /* 78 */
  {0, 0, 0}, /* 79 */
  {0, 0, 0}, /* 80 */
  {0, 0, 0}, /* 81 */
  {0, 0, 0}, /* 82 */
  {0, 0, 0}, /* 83 */
  {0, 0, 0}, /* 84 */
  {0, 0, 0}, /* 85 */
  {0, 0, 0}, /* 86 */
  {0, 0, 0}, /* 87 */
  {0, 0, 0}, /* 88 */
  {0, 0, 0}, /* 89 */
  {0, 0, 0}, /* 90 */
  {0, 0, 0}, /* 91 */
  {0, 0, 0}, /* 92 */
  {0, 0, 0}, /* 93 */
  {0, 0, 0}, /* 94 */
  {0, 0, 0}, /* 95 */
  {0, 0, 0}, /* 96 */
  {0, 0, 0}, /* 97 */
  {0, 0, 0}, /* 98 */
  {0, 0, 0}, /* 99 */
  {0, 0, 0}, /* 100 */
  {0, 0, 0}, /* 101 */
  {0, 0, 0}, /* 102 */
  {0, 0, 0}, /* 103 */
  {0, 0, 0}, /* 104 */
  {0, 0, 0}, /* 105 */
  {0, 0, 0}, /* 106 */
  {0, 0, 0}, /* 107 */
  {0, 0, 0}, /* 108 */
  {0, 0, 0}, /* 109 */
  {0, 0, 0}, /* 110 */
  {0, 0, 0}, /* 111 */
  {32, 108, 5}, /* 112 (header) */
  {33, 0, 0}, /* 113 (delivery-annotations) */
  {34, 0, 0}, /* 114 (message-annotations) */
  {35, 113, 13}, /* 115 (properties) */
  {36, 0, 0}, /* 116 (application-properties) */
  {37, 0, 0}, /* 117 (data) */
  {38, 0, 0}, /* 118 (amqp-sequence) */
  {39, 0, 0}, /* 119 (amqp-value) */
  {40, 0, 0}, /* 120 (footer) */
};

#endif

enum {
  FIELD_MIN = 16,
  FIELD_MAX = 120
};

#endif /* protocol.h */
