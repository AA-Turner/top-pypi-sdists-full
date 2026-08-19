
package com.silabs.utf.QueueModels;

import javax.annotation.processing.Generated;
import javax.validation.constraints.NotNull;
import com.fasterxml.jackson.annotation.JsonInclude;
import com.fasterxml.jackson.annotation.JsonProperty;
import com.fasterxml.jackson.annotation.JsonPropertyOrder;

@JsonInclude(JsonInclude.Include.NON_NULL)
@JsonPropertyOrder({
    "action",
    "data",
    "result"
})
@Generated("jsonschema2pojo")
public class XrayStep {

    /**
     * 
     * (Required)
     * 
     */
    @JsonProperty("action")
    @NotNull
    private String action;
    /**
     * 
     * (Required)
     * 
     */
    @JsonProperty("data")
    @NotNull
    private String data;
    /**
     * 
     * (Required)
     * 
     */
    @JsonProperty("result")
    @NotNull
    private String result;

    /**
     * 
     * (Required)
     * 
     */
    @JsonProperty("action")
    public String getAction() {
        return action;
    }

    /**
     * 
     * (Required)
     * 
     */
    @JsonProperty("action")
    public void setAction(String action) {
        this.action = action;
    }

    public XrayStep withAction(String action) {
        this.action = action;
        return this;
    }

    /**
     * 
     * (Required)
     * 
     */
    @JsonProperty("data")
    public String getData() {
        return data;
    }

    /**
     * 
     * (Required)
     * 
     */
    @JsonProperty("data")
    public void setData(String data) {
        this.data = data;
    }

    public XrayStep withData(String data) {
        this.data = data;
        return this;
    }

    /**
     * 
     * (Required)
     * 
     */
    @JsonProperty("result")
    public String getResult() {
        return result;
    }

    /**
     * 
     * (Required)
     * 
     */
    @JsonProperty("result")
    public void setResult(String result) {
        this.result = result;
    }

    public XrayStep withResult(String result) {
        this.result = result;
        return this;
    }

    @Override
    public String toString() {
        StringBuilder sb = new StringBuilder();
        sb.append(XrayStep.class.getName()).append('@').append(Integer.toHexString(System.identityHashCode(this))).append('[');
        sb.append("action");
        sb.append('=');
        sb.append(((this.action == null)?"<null>":this.action));
        sb.append(',');
        sb.append("data");
        sb.append('=');
        sb.append(((this.data == null)?"<null>":this.data));
        sb.append(',');
        sb.append("result");
        sb.append('=');
        sb.append(((this.result == null)?"<null>":this.result));
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
        result = ((result* 31)+((this.result == null)? 0 :this.result.hashCode()));
        result = ((result* 31)+((this.action == null)? 0 :this.action.hashCode()));
        return result;
    }

    @Override
    public boolean equals(Object other) {
        if (other == this) {
            return true;
        }
        if ((other instanceof XrayStep) == false) {
            return false;
        }
        XrayStep rhs = ((XrayStep) other);
        return ((((this.data == rhs.data)||((this.data!= null)&&this.data.equals(rhs.data)))&&((this.result == rhs.result)||((this.result!= null)&&this.result.equals(rhs.result))))&&((this.action == rhs.action)||((this.action!= null)&&this.action.equals(rhs.action))));
    }

}
