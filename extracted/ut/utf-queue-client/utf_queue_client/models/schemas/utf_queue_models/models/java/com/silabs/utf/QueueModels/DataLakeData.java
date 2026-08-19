
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
    "dataFormat",
    "object_id",
    "data",
    "compression"
})
@Generated("jsonschema2pojo")
public class DataLakeData {

    /**
     * 
     * (Required)
     * 
     */
    @JsonProperty("dataFormat")
    @NotNull
    private DataLakeData.DataFormat dataFormat;
    @JsonProperty("object_id")
    private String objectId;
    /**
     * 
     * (Required)
     * 
     */
    @JsonProperty("data")
    @NotNull
    private Object data;
    @JsonProperty("compression")
    private DataLakeData.Compression compression;

    /**
     * 
     * (Required)
     * 
     */
    @JsonProperty("dataFormat")
    public DataLakeData.DataFormat getDataFormat() {
        return dataFormat;
    }

    /**
     * 
     * (Required)
     * 
     */
    @JsonProperty("dataFormat")
    public void setDataFormat(DataLakeData.DataFormat dataFormat) {
        this.dataFormat = dataFormat;
    }

    public DataLakeData withDataFormat(DataLakeData.DataFormat dataFormat) {
        this.dataFormat = dataFormat;
        return this;
    }

    @JsonProperty("object_id")
    public String getObjectId() {
        return objectId;
    }

    @JsonProperty("object_id")
    public void setObjectId(String objectId) {
        this.objectId = objectId;
    }

    public DataLakeData withObjectId(String objectId) {
        this.objectId = objectId;
        return this;
    }

    /**
     * 
     * (Required)
     * 
     */
    @JsonProperty("data")
    public Object getData() {
        return data;
    }

    /**
     * 
     * (Required)
     * 
     */
    @JsonProperty("data")
    public void setData(Object data) {
        this.data = data;
    }

    public DataLakeData withData(Object data) {
        this.data = data;
        return this;
    }

    @JsonProperty("compression")
    public DataLakeData.Compression getCompression() {
        return compression;
    }

    @JsonProperty("compression")
    public void setCompression(DataLakeData.Compression compression) {
        this.compression = compression;
    }

    public DataLakeData withCompression(DataLakeData.Compression compression) {
        this.compression = compression;
        return this;
    }

    @Override
    public String toString() {
        StringBuilder sb = new StringBuilder();
        sb.append(DataLakeData.class.getName()).append('@').append(Integer.toHexString(System.identityHashCode(this))).append('[');
        sb.append("dataFormat");
        sb.append('=');
        sb.append(((this.dataFormat == null)?"<null>":this.dataFormat));
        sb.append(',');
        sb.append("objectId");
        sb.append('=');
        sb.append(((this.objectId == null)?"<null>":this.objectId));
        sb.append(',');
        sb.append("data");
        sb.append('=');
        sb.append(((this.data == null)?"<null>":this.data));
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
        result = ((result* 31)+((this.data == null)? 0 :this.data.hashCode()));
        result = ((result* 31)+((this.compression == null)? 0 :this.compression.hashCode()));
        result = ((result* 31)+((this.dataFormat == null)? 0 :this.dataFormat.hashCode()));
        result = ((result* 31)+((this.objectId == null)? 0 :this.objectId.hashCode()));
        return result;
    }

    @Override
    public boolean equals(Object other) {
        if (other == this) {
            return true;
        }
        if ((other instanceof DataLakeData) == false) {
            return false;
        }
        DataLakeData rhs = ((DataLakeData) other);
        return (((((this.data == rhs.data)||((this.data!= null)&&this.data.equals(rhs.data)))&&((this.compression == rhs.compression)||((this.compression!= null)&&this.compression.equals(rhs.compression))))&&((this.dataFormat == rhs.dataFormat)||((this.dataFormat!= null)&&this.dataFormat.equals(rhs.dataFormat))))&&((this.objectId == rhs.objectId)||((this.objectId!= null)&&this.objectId.equals(rhs.objectId))));
    }

    @Generated("jsonschema2pojo")
    public enum Compression {

        GZIP("GZIP"),
        NONE("NONE"),
        SNAPPY("SNAPPY");
        private final String value;
        private final static Map<String, DataLakeData.Compression> CONSTANTS = new HashMap<String, DataLakeData.Compression>();

        static {
            for (DataLakeData.Compression c: values()) {
                CONSTANTS.put(c.value, c);
            }
        }

        Compression(String value) {
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
        public static DataLakeData.Compression fromValue(String value) {
            DataLakeData.Compression constant = CONSTANTS.get(value);
            if (constant == null) {
                throw new IllegalArgumentException(value);
            } else {
                return constant;
            }
        }

    }

    @Generated("jsonschema2pojo")
    public enum DataFormat {

        CSV("CSV"),
        JSON("JSON"),
        JSONSTR("JSONSTR"),
        NDJSON("NDJSON"),
        PARQUET("PARQUET");
        private final String value;
        private final static Map<String, DataLakeData.DataFormat> CONSTANTS = new HashMap<String, DataLakeData.DataFormat>();

        static {
            for (DataLakeData.DataFormat c: values()) {
                CONSTANTS.put(c.value, c);
            }
        }

        DataFormat(String value) {
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
        public static DataLakeData.DataFormat fromValue(String value) {
            DataLakeData.DataFormat constant = CONSTANTS.get(value);
            if (constant == null) {
                throw new IllegalArgumentException(value);
            } else {
                return constant;
            }
        }

    }

}
