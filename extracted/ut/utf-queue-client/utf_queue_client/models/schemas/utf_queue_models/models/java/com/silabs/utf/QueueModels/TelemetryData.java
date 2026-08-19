
package com.silabs.utf.QueueModels;

import java.util.HashMap;
import java.util.Map;
import javax.annotation.processing.Generated;
import javax.validation.constraints.NotNull;
import com.fasterxml.jackson.annotation.JsonCreator;
import com.fasterxml.jackson.annotation.JsonInclude;
import com.fasterxml.jackson.annotation.JsonProperty;
import com.fasterxml.jackson.annotation.JsonPropertyOrder;
import com.fasterxml.jackson.annotation.JsonValue;

@JsonInclude(JsonInclude.Include.NON_NULL)
@JsonPropertyOrder({
    "dataType",
    "base64ProtobufData",
    "compression"
})
@Generated("jsonschema2pojo")
public class TelemetryData {

    /**
     * 
     * (Required)
     * 
     */
    @JsonProperty("dataType")
    @NotNull
    private TelemetryData.DataType dataType;
    /**
     * 
     * (Required)
     * 
     */
    @JsonProperty("base64ProtobufData")
    @NotNull
    private String base64ProtobufData;
    @JsonProperty("compression")
    private String compression;

    /**
     * 
     * (Required)
     * 
     */
    @JsonProperty("dataType")
    public TelemetryData.DataType getDataType() {
        return dataType;
    }

    /**
     * 
     * (Required)
     * 
     */
    @JsonProperty("dataType")
    public void setDataType(TelemetryData.DataType dataType) {
        this.dataType = dataType;
    }

    public TelemetryData withDataType(TelemetryData.DataType dataType) {
        this.dataType = dataType;
        return this;
    }

    /**
     * 
     * (Required)
     * 
     */
    @JsonProperty("base64ProtobufData")
    public String getBase64ProtobufData() {
        return base64ProtobufData;
    }

    /**
     * 
     * (Required)
     * 
     */
    @JsonProperty("base64ProtobufData")
    public void setBase64ProtobufData(String base64ProtobufData) {
        this.base64ProtobufData = base64ProtobufData;
    }

    public TelemetryData withBase64ProtobufData(String base64ProtobufData) {
        this.base64ProtobufData = base64ProtobufData;
        return this;
    }

    @JsonProperty("compression")
    public String getCompression() {
        return compression;
    }

    @JsonProperty("compression")
    public void setCompression(String compression) {
        this.compression = compression;
    }

    public TelemetryData withCompression(String compression) {
        this.compression = compression;
        return this;
    }

    @Override
    public String toString() {
        StringBuilder sb = new StringBuilder();
        sb.append(TelemetryData.class.getName()).append('@').append(Integer.toHexString(System.identityHashCode(this))).append('[');
        sb.append("dataType");
        sb.append('=');
        sb.append(((this.dataType == null)?"<null>":this.dataType));
        sb.append(',');
        sb.append("base64ProtobufData");
        sb.append('=');
        sb.append(((this.base64ProtobufData == null)?"<null>":this.base64ProtobufData));
        sb.append(',');
        sb.append("compression");
        sb.append('=');
        sb.append(((this.compression == null)?"<null>":this.compression));
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
        result = ((result* 31)+((this.compression == null)? 0 :this.compression.hashCode()));
        result = ((result* 31)+((this.base64ProtobufData == null)? 0 :this.base64ProtobufData.hashCode()));
        result = ((result* 31)+((this.dataType == null)? 0 :this.dataType.hashCode()));
        return result;
    }

    @Override
    public boolean equals(Object other) {
        if (other == this) {
            return true;
        }
        if ((other instanceof TelemetryData) == false) {
            return false;
        }
        TelemetryData rhs = ((TelemetryData) other);
        return ((((this.compression == rhs.compression)||((this.compression!= null)&&this.compression.equals(rhs.compression)))&&((this.base64ProtobufData == rhs.base64ProtobufData)||((this.base64ProtobufData!= null)&&this.base64ProtobufData.equals(rhs.base64ProtobufData))))&&((this.dataType == rhs.dataType)||((this.dataType!= null)&&this.dataType.equals(rhs.dataType))));
    }

    @Generated("jsonschema2pojo")
    public enum DataType {

        LOGS("LOGS"),
        METRICS("METRICS"),
        TRACES("TRACES");
        private final String value;
        private final static Map<String, TelemetryData.DataType> CONSTANTS = new HashMap<String, TelemetryData.DataType>();

        static {
            for (TelemetryData.DataType c: values()) {
                CONSTANTS.put(c.value, c);
            }
        }

        DataType(String value) {
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
        public static TelemetryData.DataType fromValue(String value) {
            TelemetryData.DataType constant = CONSTANTS.get(value);
            if (constant == null) {
                throw new IllegalArgumentException(value);
            } else {
                return constant;
            }
        }

    }

}
