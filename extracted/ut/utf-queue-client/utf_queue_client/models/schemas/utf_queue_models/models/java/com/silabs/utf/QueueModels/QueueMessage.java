
package com.silabs.utf.QueueModels;

import java.util.HashMap;
import java.util.Map;
import javax.annotation.processing.Generated;
import javax.validation.Valid;
import javax.validation.constraints.NotNull;
import com.fasterxml.jackson.annotation.JsonCreator;
import com.fasterxml.jackson.annotation.JsonInclude;
import com.fasterxml.jackson.annotation.JsonProperty;
import com.fasterxml.jackson.annotation.JsonPropertyDescription;
import com.fasterxml.jackson.annotation.JsonPropertyOrder;
import com.fasterxml.jackson.annotation.JsonValue;

@JsonInclude(JsonInclude.Include.NON_NULL)
@JsonPropertyOrder({
    "recordType",
    "recordSubType",
    "tenantKey",
    "recordTimestamp",
    "payload",
    "messageId"
})
@Generated("jsonschema2pojo")
public class QueueMessage {

    /**
     * Type of record
     * (Required)
     * 
     */
    @JsonProperty("recordType")
    @JsonPropertyDescription("Type of record")
    @NotNull
    private QueueMessage.RecordType recordType;
    /**
     * Subtype of record. Not all types have a subtype, but it is required when they have one.
     * 
     */
    @JsonProperty("recordSubType")
    @JsonPropertyDescription("Subtype of record. Not all types have a subtype, but it is required when they have one.")
    private QueueMessage.RecordSubType recordSubType;
    /**
     * Unique string that identifies the app/group sending the message.
     * Forward looking to match the data lake infrastructure.
     * (Required)
     * 
     */
    @JsonProperty("tenantKey")
    @JsonPropertyDescription("Unique string that identifies the app/group sending the message.\nForward looking to match the data lake infrastructure.")
    @NotNull
    private String tenantKey;
    /**
     * UTC datetime.
     * Use ISO-8601 format with time zone
     *  2022-03-10T18:50:05Z
     * (Required)
     * 
     */
    @JsonProperty("recordTimestamp")
    @JsonPropertyDescription("UTC datetime.\nUse ISO-8601 format with time zone\n2022-03-10T18:50:05Z")
    @NotNull
    private String recordTimestamp;
    /**
     * 
     * (Required)
     * 
     */
    @JsonProperty("payload")
    @Valid
    @NotNull
    private QueueRecord payload;
    /**
     * Unique client-generated UUID
     * 
     */
    @JsonProperty("messageId")
    @JsonPropertyDescription("Unique client-generated UUID")
    private String messageId;

    /**
     * Type of record
     * (Required)
     * 
     */
    @JsonProperty("recordType")
    public QueueMessage.RecordType getRecordType() {
        return recordType;
    }

    /**
     * Type of record
     * (Required)
     * 
     */
    @JsonProperty("recordType")
    public void setRecordType(QueueMessage.RecordType recordType) {
        this.recordType = recordType;
    }

    public QueueMessage withRecordType(QueueMessage.RecordType recordType) {
        this.recordType = recordType;
        return this;
    }

    /**
     * Subtype of record. Not all types have a subtype, but it is required when they have one.
     * 
     */
    @JsonProperty("recordSubType")
    public QueueMessage.RecordSubType getRecordSubType() {
        return recordSubType;
    }

    /**
     * Subtype of record. Not all types have a subtype, but it is required when they have one.
     * 
     */
    @JsonProperty("recordSubType")
    public void setRecordSubType(QueueMessage.RecordSubType recordSubType) {
        this.recordSubType = recordSubType;
    }

    public QueueMessage withRecordSubType(QueueMessage.RecordSubType recordSubType) {
        this.recordSubType = recordSubType;
        return this;
    }

    /**
     * Unique string that identifies the app/group sending the message.
     * Forward looking to match the data lake infrastructure.
     * (Required)
     * 
     */
    @JsonProperty("tenantKey")
    public String getTenantKey() {
        return tenantKey;
    }

    /**
     * Unique string that identifies the app/group sending the message.
     * Forward looking to match the data lake infrastructure.
     * (Required)
     * 
     */
    @JsonProperty("tenantKey")
    public void setTenantKey(String tenantKey) {
        this.tenantKey = tenantKey;
    }

    public QueueMessage withTenantKey(String tenantKey) {
        this.tenantKey = tenantKey;
        return this;
    }

    /**
     * UTC datetime.
     * Use ISO-8601 format with time zone
     *  2022-03-10T18:50:05Z
     * (Required)
     * 
     */
    @JsonProperty("recordTimestamp")
    public String getRecordTimestamp() {
        return recordTimestamp;
    }

    /**
     * UTC datetime.
     * Use ISO-8601 format with time zone
     *  2022-03-10T18:50:05Z
     * (Required)
     * 
     */
    @JsonProperty("recordTimestamp")
    public void setRecordTimestamp(String recordTimestamp) {
        this.recordTimestamp = recordTimestamp;
    }

    public QueueMessage withRecordTimestamp(String recordTimestamp) {
        this.recordTimestamp = recordTimestamp;
        return this;
    }

    /**
     * 
     * (Required)
     * 
     */
    @JsonProperty("payload")
    public QueueRecord getPayload() {
        return payload;
    }

    /**
     * 
     * (Required)
     * 
     */
    @JsonProperty("payload")
    public void setPayload(QueueRecord payload) {
        this.payload = payload;
    }

    public QueueMessage withPayload(QueueRecord payload) {
        this.payload = payload;
        return this;
    }

    /**
     * Unique client-generated UUID
     * 
     */
    @JsonProperty("messageId")
    public String getMessageId() {
        return messageId;
    }

    /**
     * Unique client-generated UUID
     * 
     */
    @JsonProperty("messageId")
    public void setMessageId(String messageId) {
        this.messageId = messageId;
    }

    public QueueMessage withMessageId(String messageId) {
        this.messageId = messageId;
        return this;
    }

    @Override
    public String toString() {
        StringBuilder sb = new StringBuilder();
        sb.append(QueueMessage.class.getName()).append('@').append(Integer.toHexString(System.identityHashCode(this))).append('[');
        sb.append("recordType");
        sb.append('=');
        sb.append(((this.recordType == null)?"<null>":this.recordType));
        sb.append(',');
        sb.append("recordSubType");
        sb.append('=');
        sb.append(((this.recordSubType == null)?"<null>":this.recordSubType));
        sb.append(',');
        sb.append("tenantKey");
        sb.append('=');
        sb.append(((this.tenantKey == null)?"<null>":this.tenantKey));
        sb.append(',');
        sb.append("recordTimestamp");
        sb.append('=');
        sb.append(((this.recordTimestamp == null)?"<null>":this.recordTimestamp));
        sb.append(',');
        sb.append("payload");
        sb.append('=');
        sb.append(((this.payload == null)?"<null>":this.payload));
        sb.append(',');
        sb.append("messageId");
        sb.append('=');
        sb.append(((this.messageId == null)?"<null>":this.messageId));
        sb.append(',');
        if (sb.charAt((sb.length()- 1)) == ',') {
            sb.setCharAt((sb.length()- 1), ']');
        } else {
            sb.append(']');
        }
        return sb.toString();
    }

    @Override
    public int hashCode() {
        int result = 1;
        result = ((result* 31)+((this.recordSubType == null)? 0 :this.recordSubType.hashCode()));
        result = ((result* 31)+((this.messageId == null)? 0 :this.messageId.hashCode()));
        result = ((result* 31)+((this.tenantKey == null)? 0 :this.tenantKey.hashCode()));
        result = ((result* 31)+((this.payload == null)? 0 :this.payload.hashCode()));
        result = ((result* 31)+((this.recordType == null)? 0 :this.recordType.hashCode()));
        result = ((result* 31)+((this.recordTimestamp == null)? 0 :this.recordTimestamp.hashCode()));
        return result;
    }

    @Override
    public boolean equals(Object other) {
        if (other == this) {
            return true;
        }
        if ((other instanceof QueueMessage) == false) {
            return false;
        }
        QueueMessage rhs = ((QueueMessage) other);
        return (((((((this.recordSubType == rhs.recordSubType)||((this.recordSubType!= null)&&this.recordSubType.equals(rhs.recordSubType)))&&((this.messageId == rhs.messageId)||((this.messageId!= null)&&this.messageId.equals(rhs.messageId))))&&((this.tenantKey == rhs.tenantKey)||((this.tenantKey!= null)&&this.tenantKey.equals(rhs.tenantKey))))&&((this.payload == rhs.payload)||((this.payload!= null)&&this.payload.equals(rhs.payload))))&&((this.recordType == rhs.recordType)||((this.recordType!= null)&&this.recordType.equals(rhs.recordType))))&&((this.recordTimestamp == rhs.recordTimestamp)||((this.recordTimestamp!= null)&&this.recordTimestamp.equals(rhs.recordTimestamp))));
    }


    /**
     * Subtype of record. Not all types have a subtype, but it is required when they have one.
     * 
     */
    @Generated("jsonschema2pojo")
    public enum RecordSubType {

        BUILD_RESULT("BUILD_RESULT"),
        IMPORT_TEST_EXECUTION("IMPORT_TEST_EXECUTION"),
        SESSION_START("SESSION_START"),
        SESSION_STOP("SESSION_STOP"),
        TEST_RESULT("TEST_RESULT"),
        TEST_RESULT_APP("TEST_RESULT_APP");
        private final String value;
        private final static Map<String, QueueMessage.RecordSubType> CONSTANTS = new HashMap<String, QueueMessage.RecordSubType>();

        static {
            for (QueueMessage.RecordSubType c: values()) {
                CONSTANTS.put(c.value, c);
            }
        }

        RecordSubType(String value) {
            this.value = value;
        }

        @Override
        public String toString() {
            return this.value;
        }

        @JsonValue
        public String value() {
            return this.value;
        }

        @JsonCreator
        public static QueueMessage.RecordSubType fromValue(String value) {
            QueueMessage.RecordSubType constant = CONSTANTS.get(value);
            if (constant == null) {
                throw new IllegalArgumentException(value);
            } else {
                return constant;
            }
        }

    }


    /**
     * Type of record
     * 
     */
    @Generated("jsonschema2pojo")
    public enum RecordType {

        ARTIFACT_UPLOAD_REQUEST("ARTIFACT_UPLOAD_REQUEST"),
        DATALAKE_DATA("DATALAKE_DATA"),
        EXCEPTION_EVENT("EXCEPTION_EVENT"),
        LOG_EVENT("LOG_EVENT"),
        OPENTELEMETRY_DATA("OPENTELEMETRY_DATA"),
        TEST_RAIL_EVENT("TEST_RAIL_EVENT"),
        UTF_TEST_EVENT("UTF_TEST_EVENT"),
        XRAY_EVENT("XRAY_EVENT");
        private final String value;
        private final static Map<String, QueueMessage.RecordType> CONSTANTS = new HashMap<String, QueueMessage.RecordType>();

        static {
            for (QueueMessage.RecordType c: values()) {
                CONSTANTS.put(c.value, c);
            }
        }

        RecordType(String value) {
            this.value = value;
        }

        @Override
        public String toString() {
            return this.value;
        }

        @JsonValue
        public String value() {
            return this.value;
        }

        @JsonCreator
        public static QueueMessage.RecordType fromValue(String value) {
            QueueMessage.RecordType constant = CONSTANTS.get(value);
            if (constant == null) {
                throw new IllegalArgumentException(value);
            } else {
                return constant;
            }
        }

    }

}
