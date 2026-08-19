
package com.silabs.utf.QueueModels;

import java.util.ArrayList;
import java.util.List;
import javax.annotation.processing.Generated;
import javax.validation.Valid;
import javax.validation.constraints.NotNull;
import com.fasterxml.jackson.annotation.JsonInclude;
import com.fasterxml.jackson.annotation.JsonProperty;
import com.fasterxml.jackson.annotation.JsonPropertyDescription;
import com.fasterxml.jackson.annotation.JsonPropertyOrder;

@JsonInclude(JsonInclude.Include.NON_NULL)
@JsonPropertyOrder({
    "name",
    "id",
    "parameters",
    "status"
})
@Generated("jsonschema2pojo")
public class XrayIteration {

    @JsonProperty("name")
    private String name;
    @JsonProperty("id")
    private Integer id;
    /**
     * 
     * (Required)
     * 
     */
    @JsonProperty("parameters")
    @Valid
    @NotNull
    private List<XrayParameter> parameters = new ArrayList<XrayParameter>();
    /**
     * Status for the iteration (examples: PASS, FAIL, SKIP, BLOCK, BROKEN, REGRESSION)
     * (Required)
     * 
     */
    @JsonProperty("status")
    @JsonPropertyDescription("Status for the iteration (examples: PASS, FAIL, SKIP, BLOCK, BROKEN, REGRESSION)")
    @NotNull
    private String status;

    @JsonProperty("name")
    public String getName() {
        return name;
    }

    @JsonProperty("name")
    public void setName(String name) {
        this.name = name;
    }

    public XrayIteration withName(String name) {
        this.name = name;
        return this;
    }

    @JsonProperty("id")
    public Integer getId() {
        return id;
    }

    @JsonProperty("id")
    public void setId(Integer id) {
        this.id = id;
    }

    public XrayIteration withId(Integer id) {
        this.id = id;
        return this;
    }

    /**
     * 
     * (Required)
     * 
     */
    @JsonProperty("parameters")
    public List<XrayParameter> getParameters() {
        return parameters;
    }

    /**
     * 
     * (Required)
     * 
     */
    @JsonProperty("parameters")
    public void setParameters(List<XrayParameter> parameters) {
        this.parameters = parameters;
    }

    public XrayIteration withParameters(List<XrayParameter> parameters) {
        this.parameters = parameters;
        return this;
    }

    /**
     * Status for the iteration (examples: PASS, FAIL, SKIP, BLOCK, BROKEN, REGRESSION)
     * (Required)
     * 
     */
    @JsonProperty("status")
    public String getStatus() {
        return status;
    }

    /**
     * Status for the iteration (examples: PASS, FAIL, SKIP, BLOCK, BROKEN, REGRESSION)
     * (Required)
     * 
     */
    @JsonProperty("status")
    public void setStatus(String status) {
        this.status = status;
    }

    public XrayIteration withStatus(String status) {
        this.status = status;
        return this;
    }

    @Override
    public String toString() {
        StringBuilder sb = new StringBuilder();
        sb.append(XrayIteration.class.getName()).append('@').append(Integer.toHexString(System.identityHashCode(this))).append('[');
        sb.append("name");
        sb.append('=');
        sb.append(((this.name == null)?"<null>":this.name));
        sb.append(',');
        sb.append("id");
        sb.append('=');
        sb.append(((this.id == null)?"<null>":this.id));
        sb.append(',');
        sb.append("parameters");
        sb.append('=');
        sb.append(((this.parameters == null)?"<null>":this.parameters));
        sb.append(',');
        sb.append("status");
        sb.append('=');
        sb.append(((this.status == null)?"<null>":this.status));
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
        result = ((result* 31)+((this.name == null)? 0 :this.name.hashCode()));
        result = ((result* 31)+((this.id == null)? 0 :this.id.hashCode()));
        result = ((result* 31)+((this.parameters == null)? 0 :this.parameters.hashCode()));
        result = ((result* 31)+((this.status == null)? 0 :this.status.hashCode()));
        return result;
    }

    @Override
    public boolean equals(Object other) {
        if (other == this) {
            return true;
        }
        if ((other instanceof XrayIteration) == false) {
            return false;
        }
        XrayIteration rhs = ((XrayIteration) other);
        return (((((this.name == rhs.name)||((this.name!= null)&&this.name.equals(rhs.name)))&&((this.id == rhs.id)||((this.id!= null)&&this.id.equals(rhs.id))))&&((this.parameters == rhs.parameters)||((this.parameters!= null)&&this.parameters.equals(rhs.parameters))))&&((this.status == rhs.status)||((this.status!= null)&&this.status.equals(rhs.status))));
    }

}
