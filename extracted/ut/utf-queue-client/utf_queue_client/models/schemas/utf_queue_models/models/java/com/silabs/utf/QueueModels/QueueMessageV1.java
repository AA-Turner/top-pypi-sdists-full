
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
    "payload",
    "timestamp"
})
@Generated("jsonschema2pojo")
public class QueueMessageV1 {

    /**
     * Type of record
     * (Required)
     * 
     */
    @JsonProperty("recordType")
    @JsonPropertyDescription("Type of record")
    @NotNull
    private QueueMessageV1 .RecordType recordType;
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
     * UTC Timestamp
     * Given in seconds since epoch (unix time)
     * (Required)
     * 
     */
    @JsonProperty("timestamp")
    @JsonPropertyDescription("UTC Timestamp\nGiven in seconds since epoch (unix time)")
    @NotNull
    private Double timestamp;

    /**
     * Type of record
     * (Required)
     * 
     */
    @JsonProperty("recordType")
    public QueueMessageV1 .RecordType getRecordType() {
        return recordType;
    }

    /**
     * Type of record
     * (Required)
     * 
     */
    @JsonProperty("recordType")
    public void setRecordType(QueueMessageV1 .RecordType recordType) {
        this.recordType = recordType;
    }

    public QueueMessageV1 withRecordType(QueueMessageV1 .RecordType recordType) {
        this.recordType = recordType;
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

    public QueueMessageV1 withPayload(QueueRecord payload) {
        this.payload = payload;
        return this;
    }

    /**
     * UTC Timestamp
     * Given in seconds since epoch (unix time)
     * (Required)
     * 
     */
    @JsonProperty("timestamp")
    public Double getTimestamp() {
        return timestamp;
    }

    /**
     * UTC Timestamp
     * Given in seconds since epoch (unix time)
     * (Required)
     * 
     */
    @JsonProperty("timestamp")
    public void setTimestamp(Double timestamp) {
        this.timestamp = timestamp;
    }

    public QueueMessageV1 withTimestamp(Double timestamp) {
        this.timestamp = timestamp;
        return this;
    }

    @Override
    public String toString() {
        StringBuilder sb = new StringBuilder();
        sb.append(QueueMessageV1 .class.getName()).append('@').append(Integer.toHexString(System.identityHashCode(this))).append('[');
        sb.append("recordType");
        sb.append('=');
        sb.append(((this.recordType == null)?"<null>":this.recordType));
        sb.append(',');
        sb.append("payload");
        sb.append('=');
        sb.append(((this.payload == null)?"<null>":this.payload));
        sb.append(',');
        sb.append("timestamp");
        sb.append('=');
        sb.append(((this.timestamp == null)?"<null>":this.timestamp));
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
        result = ((result* 31)+((this.payload == null)? 0 :this.payload.hashCode()));
        result = ((result* 31)+((this.recordType == null)? 0 :this.recordType.hashCode()));
        result = ((result* 31)+((this.timestamp == null)? 0 :this.timestamp.hashCode()));
        return result;
    }

    @Override
    public boolean equals(Object other) {
        if (other == this) {
            return true;
        }
        if ((other instanceof QueueMessageV1) == false) {
            return false;
        }
        QueueMessageV1 rhs = ((QueueMessageV1) other);
        return ((((this.payload == rhs.payload)||((this.payload!= null)&&this.payload.equals(rhs.payload)))&&((this.recordType == rhs.recordType)||((this.recordType!= null)&&this.recordType.equals(rhs.recordType))))&&((this.timestamp == rhs.timestamp)||((this.timestamp!= null)&&this.timestamp.equals(rhs.timestamp))));
    }


    /**
     * Type of record
     * 
     */
    @Generated("jsonschema2pojo")
    public enum RecordType {

        ARTIFACT_UPLOAD_REQUEST("ARTIFACT_UPLOAD_REQUEST"),
        EXCEPTION_EVENT("EXCEPTION_EVENT"),
        LOG_EVENT("LOG_EVENT"),
        TEST_EVENT("TEST_EVENT"),
        UTF_TEST_EVENT("UTF_TEST_EVENT");
        private final String value;
        private final static Map<String, QueueMessageV1 .RecordType> CONSTANTS = new HashMap<String, QueueMessageV1 .RecordType>();

        static {
            for (QueueMessageV1 .RecordType c: values()) {
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
        public static QueueMessageV1 .RecordType fromValue(String value) {
            QueueMessageV1 .RecordType constant = CONSTANTS.get(value);
            if (constant == null) {
                throw new IllegalArgumentException(value);
            } else {
                return constant;
            }
        }

    }

}
