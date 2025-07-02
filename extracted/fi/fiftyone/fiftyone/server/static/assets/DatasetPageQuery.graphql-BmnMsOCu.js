const X=function(){var S={defaultValue:null,kind:"LocalArgument",name:"count"},f={defaultValue:null,kind:"LocalArgument",name:"cursor"},K={defaultValue:null,kind:"LocalArgument",name:"extendedView"},v={defaultValue:null,kind:"LocalArgument",name:"name"},T={defaultValue:null,kind:"LocalArgument",name:"savedViewSlug"},b={defaultValue:"",kind:"LocalArgument",name:"search"},h={defaultValue:null,kind:"LocalArgument",name:"view"},u={alias:null,args:null,kind:"ScalarField",name:"colorBy",storageKey:null},d={alias:null,args:null,kind:"ScalarField",name:"colorPool",storageKey:null},n={alias:null,args:null,kind:"ScalarField",name:"colorscale",storageKey:null},o={alias:null,args:null,kind:"ScalarField",name:"multicolorKeypoints",storageKey:null},g={alias:null,args:null,kind:"ScalarField",name:"showSkeletons",storageKey:null},w=[{kind:"Variable",name:"name",variableName:"name"},{kind:"Variable",name:"savedViewSlug",variableName:"savedViewSlug"},{kind:"Variable",name:"view",variableName:"extendedView"}],e={alias:null,args:null,kind:"ScalarField",name:"name",storageKey:null},L={alias:null,args:null,kind:"ScalarField",name:"defaultGroupSlice",storageKey:null},a={alias:null,args:null,kind:"ScalarField",name:"id",storageKey:null},i={alias:null,args:null,kind:"ScalarField",name:"color",storageKey:null},C=[{alias:null,args:null,kind:"ScalarField",name:"intTarget",storageKey:null},i],m={alias:null,args:null,kind:"ScalarField",name:"value",storageKey:null},D={alias:null,args:null,concreteType:"ColorscaleList",kind:"LinkedField",name:"list",plural:!0,selections:[m,i],storageKey:null},V={alias:null,args:null,kind:"ScalarField",name:"rgb",storageKey:null},l={alias:null,args:null,kind:"ScalarField",name:"path",storageKey:null},A={alias:null,args:null,kind:"ScalarField",name:"fieldColor",storageKey:null},N={alias:null,args:null,concreteType:"ValueColor",kind:"LinkedField",name:"valueColors",plural:!0,selections:[i,m],storageKey:null},x={alias:null,args:null,concreteType:"ColorScheme",kind:"LinkedField",name:"colorScheme",plural:!1,selections:[a,u,d,o,{alias:null,args:null,kind:"ScalarField",name:"opacity",storageKey:null},g,{alias:null,args:null,concreteType:"MaskColor",kind:"LinkedField",name:"defaultMaskTargetsColors",plural:!0,selections:C,storageKey:null},{alias:null,args:null,concreteType:"DefaultColorscale",kind:"LinkedField",name:"defaultColorscale",plural:!1,selections:[e,D,V],storageKey:null},{alias:null,args:null,concreteType:"Colorscale",kind:"LinkedField",name:"colorscales",plural:!0,selections:[l,e,D,V],storageKey:null},{alias:null,args:null,concreteType:"CustomizeColor",kind:"LinkedField",name:"fields",plural:!0,selections:[{alias:null,args:null,kind:"ScalarField",name:"colorByAttribute",storageKey:null},A,l,N,{alias:null,args:null,concreteType:"MaskColor",kind:"LinkedField",name:"maskTargetsColors",plural:!0,selections:C,storageKey:null}],storageKey:null},{alias:null,args:null,concreteType:"LabelTagColor",kind:"LinkedField",name:"labelTags",plural:!1,selections:[A,N],storageKey:null}],storageKey:null},P={alias:null,args:null,kind:"ScalarField",name:"disableFrameFiltering",storageKey:null},M={alias:null,args:null,kind:"ScalarField",name:"mediaFallback",storageKey:null},I={alias:null,args:null,kind:"ScalarField",name:"plugins",storageKey:null},Q={alias:null,args:null,kind:"ScalarField",name:"paths",storageKey:null},$={alias:null,args:null,kind:"ScalarField",name:"createdAt",storageKey:null},B={alias:null,args:null,kind:"ScalarField",name:"datasetId",storageKey:null},s={alias:null,args:null,kind:"ScalarField",name:"info",storageKey:null},G={alias:null,args:null,kind:"ScalarField",name:"lastLoadedAt",storageKey:null},R={alias:null,args:null,kind:"ScalarField",name:"mediaType",storageKey:null},r={alias:null,args:null,kind:"ScalarField",name:"version",storageKey:null},q={alias:null,args:null,kind:"ScalarField",name:"key",storageKey:null},_={alias:null,args:null,kind:"ScalarField",name:"timestamp",storageKey:null},c={alias:null,args:null,kind:"ScalarField",name:"viewStages",storageKey:null},j={alias:null,args:null,kind:"ScalarField",name:"cls",storageKey:null},y={alias:null,args:null,kind:"ScalarField",name:"type",storageKey:null},z=[{alias:null,args:null,kind:"ScalarField",name:"target",storageKey:null},m],E={alias:null,args:null,kind:"ScalarField",name:"labels",storageKey:null},H={alias:null,args:null,kind:"ScalarField",name:"edges",storageKey:null},p={alias:null,args:null,kind:"ScalarField",name:"ftype",storageKey:null},F={alias:null,args:null,kind:"ScalarField",name:"subfield",storageKey:null},k={alias:null,args:null,kind:"ScalarField",name:"embeddedDocType",storageKey:null},O={alias:null,args:null,kind:"ScalarField",name:"dbField",storageKey:null},t={alias:null,args:null,kind:"ScalarField",name:"description",storageKey:null},Z=[e,{alias:null,args:null,kind:"ScalarField",name:"unique",storageKey:null},{alias:null,args:null,concreteType:"IndexFields",kind:"LinkedField",name:"key",plural:!0,selections:[{alias:null,args:null,kind:"ScalarField",name:"field",storageKey:null},y],storageKey:null},{alias:null,args:null,concreteType:"WildcardProjection",kind:"LinkedField",name:"wildcardProjection",plural:!1,selections:[{alias:null,args:null,kind:"ScalarField",name:"fields",storageKey:null},{alias:null,args:null,kind:"ScalarField",name:"inclusion",storageKey:null}],storageKey:null}],W=[{kind:"Variable",name:"after",variableName:"cursor"},{kind:"Variable",name:"first",variableName:"count"},{kind:"Variable",name:"search",variableName:"search"}],J={kind:"Variable",name:"datasetName",variableName:"name"},U=[l,p,F,k,s,t];return{fragment:{argumentDefinitions:[S,f,K,v,T,b,h],kind:"Fragment",metadata:null,name:"DatasetPageQuery",selections:[{alias:null,args:null,concreteType:"AppConfig",kind:"LinkedField",name:"config",plural:!1,selections:[u,d,n,o,g],storageKey:null},n,{alias:null,args:w,concreteType:"Dataset",kind:"LinkedField",name:"dataset",plural:!1,selections:[e,L,{alias:null,args:null,concreteType:"DatasetAppConfig",kind:"LinkedField",name:"appConfig",plural:!1,selections:[x],storageKey:null},{args:null,kind:"FragmentSpread",name:"datasetFragment"}],storageKey:null},{args:null,kind:"FragmentSpread",name:"NavFragment"},{args:null,kind:"FragmentSpread",name:"savedViewsFragment"},{args:null,kind:"FragmentSpread",name:"configFragment"},{args:null,kind:"FragmentSpread",name:"stageDefinitionsFragment"},{args:null,kind:"FragmentSpread",name:"viewSchemaFragment"}],type:"Query",abstractKey:null},kind:"Request",operation:{argumentDefinitions:[S,f,v,K,T,b,h],kind:"Operation",name:"DatasetPageQuery",selections:[{alias:null,args:null,concreteType:"AppConfig",kind:"LinkedField",name:"config",plural:!1,selections:[u,d,n,o,g,P,{alias:null,args:null,kind:"ScalarField",name:"gridZoom",storageKey:null},{alias:null,args:null,kind:"ScalarField",name:"enableQueryPerformance",storageKey:null},{alias:null,args:null,kind:"ScalarField",name:"defaultQueryPerformance",storageKey:null},{alias:null,args:null,kind:"ScalarField",name:"loopVideos",storageKey:null},M,{alias:null,args:null,kind:"ScalarField",name:"maxQueryTime",storageKey:null},{alias:null,args:null,kind:"ScalarField",name:"notebookHeight",storageKey:null},I,{alias:null,args:null,kind:"ScalarField",name:"showConfidence",storageKey:null},{alias:null,args:null,kind:"ScalarField",name:"showIndex",storageKey:null},{alias:null,args:null,kind:"ScalarField",name:"showLabel",storageKey:null},{alias:null,args:null,kind:"ScalarField",name:"showTooltip",storageKey:null},{alias:null,args:null,kind:"ScalarField",name:"theme",storageKey:null},{alias:null,args:null,kind:"ScalarField",name:"timezone",storageKey:null},{alias:null,args:null,kind:"ScalarField",name:"useFrameNumber",storageKey:null}],storageKey:null},n,{alias:null,args:w,concreteType:"Dataset",kind:"LinkedField",name:"dataset",plural:!1,selections:[e,L,{alias:null,args:null,concreteType:"DatasetAppConfig",kind:"LinkedField",name:"appConfig",plural:!1,selections:[x,{alias:null,args:null,concreteType:"ActiveFields",kind:"LinkedField",name:"activeFields",plural:!1,selections:[{alias:null,args:null,kind:"ScalarField",name:"exclude",storageKey:null},Q],storageKey:null},P,{alias:null,args:null,kind:"ScalarField",name:"dynamicGroupsTargetFrameRate",storageKey:null},{alias:null,args:null,kind:"ScalarField",name:"gridMediaField",storageKey:null},{alias:null,args:null,kind:"ScalarField",name:"mediaFields",storageKey:null},{alias:null,args:null,kind:"ScalarField",name:"modalMediaField",storageKey:null},M,I,{alias:null,args:null,concreteType:"SidebarGroup",kind:"LinkedField",name:"sidebarGroups",plural:!0,selections:[{alias:null,args:null,kind:"ScalarField",name:"expanded",storageKey:null},Q,e],storageKey:null}],storageKey:null},$,B,{alias:null,args:null,kind:"ScalarField",name:"groupField",storageKey:null},a,s,G,R,{alias:null,args:null,kind:"ScalarField",name:"parentMediaType",storageKey:null},r,{alias:null,args:null,concreteType:"BrainRun",kind:"LinkedField",name:"brainMethods",plural:!0,selections:[q,r,_,c,{alias:null,args:null,concreteType:"BrainRunConfig",kind:"LinkedField",name:"config",plural:!1,selections:[j,{alias:null,args:null,kind:"ScalarField",name:"embeddingsField",storageKey:null},{alias:null,args:null,kind:"ScalarField",name:"method",storageKey:null},{alias:null,args:null,kind:"ScalarField",name:"patchesField",storageKey:null},{alias:null,args:null,kind:"ScalarField",name:"supportsPrompts",storageKey:null},y,{alias:null,args:null,kind:"ScalarField",name:"maxK",storageKey:null},{alias:null,args:null,kind:"ScalarField",name:"supportsLeastSimilarity",storageKey:null}],storageKey:null}],storageKey:null},{alias:null,args:null,concreteType:"Target",kind:"LinkedField",name:"defaultMaskTargets",plural:!0,selections:z,storageKey:null},{alias:null,args:null,concreteType:"KeypointSkeleton",kind:"LinkedField",name:"defaultSkeleton",plural:!1,selections:[E,H],storageKey:null},{alias:null,args:null,concreteType:"EvaluationRun",kind:"LinkedField",name:"evaluations",plural:!0,selections:[q,r,_,c,{alias:null,args:null,concreteType:"EvaluationRunConfig",kind:"LinkedField",name:"config",plural:!1,selections:[j,{alias:null,args:null,kind:"ScalarField",name:"predField",storageKey:null},{alias:null,args:null,kind:"ScalarField",name:"gtField",storageKey:null}],storageKey:null}],storageKey:null},{alias:null,args:null,concreteType:"Group",kind:"LinkedField",name:"groupMediaTypes",plural:!0,selections:[e,R],storageKey:null},{alias:null,args:null,concreteType:"NamedTargets",kind:"LinkedField",name:"maskTargets",plural:!0,selections:[e,{alias:null,args:null,concreteType:"Target",kind:"LinkedField",name:"targets",plural:!0,selections:z,storageKey:null}],storageKey:null},{alias:null,args:null,concreteType:"NamedKeypointSkeleton",kind:"LinkedField",name:"skeletons",plural:!0,selections:[e,E,H],storageKey:null},{alias:null,args:null,kind:"ScalarField",name:"estimatedFrameCount",storageKey:null},{alias:null,args:null,kind:"ScalarField",name:"estimatedSampleCount",storageKey:null},{alias:null,args:null,concreteType:"SampleField",kind:"LinkedField",name:"frameFields",plural:!0,selections:[p,F,k,l,O,t,s],storageKey:null},{alias:null,args:null,concreteType:"Index",kind:"LinkedField",name:"frameIndexes",plural:!0,selections:Z,storageKey:null},{alias:null,args:null,concreteType:"Index",kind:"LinkedField",name:"sampleIndexes",plural:!0,selections:Z,storageKey:null},{alias:null,args:null,concreteType:"SampleField",kind:"LinkedField",name:"sampleFields",plural:!0,selections:[l,p,F,k,O,t,s],storageKey:null},{alias:null,args:[{kind:"Variable",name:"slug",variableName:"savedViewSlug"},{kind:"Variable",name:"view",variableName:"view"}],kind:"ScalarField",name:"stages",storageKey:null},{alias:null,args:null,kind:"ScalarField",name:"viewCls",storageKey:null},{alias:null,args:null,kind:"ScalarField",name:"viewName",storageKey:null}],storageKey:null},{alias:null,args:null,kind:"ScalarField",name:"context",storageKey:null},{alias:null,args:null,kind:"ScalarField",name:"dev",storageKey:null},{alias:null,args:null,kind:"ScalarField",name:"doNotTrack",storageKey:null},{alias:null,args:null,kind:"ScalarField",name:"uid",storageKey:null},r,{alias:null,args:W,concreteType:"DatasetStrConnection",kind:"LinkedField",name:"datasets",plural:!1,selections:[{alias:null,args:null,kind:"ScalarField",name:"total",storageKey:null},{alias:null,args:null,concreteType:"DatasetStrEdge",kind:"LinkedField",name:"edges",plural:!0,selections:[{alias:null,args:null,kind:"ScalarField",name:"cursor",storageKey:null},{alias:null,args:null,concreteType:"Dataset",kind:"LinkedField",name:"node",plural:!1,selections:[e,a,{alias:null,args:null,kind:"ScalarField",name:"__typename",storageKey:null}],storageKey:null}],storageKey:null},{alias:null,args:null,concreteType:"DatasetStrPageInfo",kind:"LinkedField",name:"pageInfo",plural:!1,selections:[{alias:null,args:null,kind:"ScalarField",name:"endCursor",storageKey:null},{alias:null,args:null,kind:"ScalarField",name:"hasNextPage",storageKey:null}],storageKey:null}],storageKey:null},{alias:null,args:W,filters:["search"],handle:"connection",key:"DatasetsList_query_datasets",kind:"LinkedHandle",name:"datasets"},{alias:null,args:[J],concreteType:"SavedView",kind:"LinkedField",name:"savedViews",plural:!0,selections:[a,B,e,{alias:null,args:null,kind:"ScalarField",name:"slug",storageKey:null},t,i,c,$,{alias:null,args:null,kind:"ScalarField",name:"lastModifiedAt",storageKey:null},G],storageKey:null},{alias:null,args:null,concreteType:"StageDefinition",kind:"LinkedField",name:"stageDefinitions",plural:!0,selections:[e,{alias:null,args:null,concreteType:"StageParameter",kind:"LinkedField",name:"params",plural:!0,selections:[e,y,{alias:null,args:null,kind:"ScalarField",name:"default",storageKey:null},{alias:null,args:null,kind:"ScalarField",name:"placeholder",storageKey:null}],storageKey:null}],storageKey:null},{alias:null,args:[J,{kind:"Variable",name:"viewStages",variableName:"view"}],concreteType:"SchemaResult",kind:"LinkedField",name:"schemaForViewStages",plural:!1,selections:[{alias:null,args:null,concreteType:"SampleField",kind:"LinkedField",name:"fieldSchema",plural:!0,selections:U,storageKey:null},{alias:null,args:null,concreteType:"SampleField",kind:"LinkedField",name:"frameFieldSchema",plural:!0,selections:U,storageKey:null}],storageKey:null}]},params:{cacheID:"376d1cbfca2288292579be904c7bea66",id:null,metadata:{},name:"DatasetPageQuery",operationKind:"query",text:`query DatasetPageQuery(
  $count: Int
  $cursor: String
  $name: String!
  $extendedView: BSONArray!
  $savedViewSlug: String
  $search: String = ""
  $view: BSONArray!
) {
  config {
    colorBy
    colorPool
    colorscale
    multicolorKeypoints
    showSkeletons
  }
  colorscale
  dataset(name: $name, view: $extendedView, savedViewSlug: $savedViewSlug) {
    name
    defaultGroupSlice
    appConfig {
      colorScheme {
        id
        colorBy
        colorPool
        multicolorKeypoints
        opacity
        showSkeletons
        defaultMaskTargetsColors {
          intTarget
          color
        }
        defaultColorscale {
          name
          list {
            value
            color
          }
          rgb
        }
        colorscales {
          path
          name
          list {
            value
            color
          }
          rgb
        }
        fields {
          colorByAttribute
          fieldColor
          path
          valueColors {
            color
            value
          }
          maskTargetsColors {
            intTarget
            color
          }
        }
        labelTags {
          fieldColor
          valueColors {
            color
            value
          }
        }
      }
    }
    ...datasetFragment
    id
  }
  ...NavFragment
  ...savedViewsFragment
  ...configFragment
  ...stageDefinitionsFragment
  ...viewSchemaFragment
}

fragment Analytics on Query {
  context
  dev
  doNotTrack
  uid
  version
}

fragment NavDatasets on Query {
  datasets(search: $search, first: $count, after: $cursor) {
    total
    edges {
      cursor
      node {
        name
        id
        __typename
      }
    }
    pageInfo {
      endCursor
      hasNextPage
    }
  }
}

fragment NavFragment on Query {
  ...Analytics
  ...NavDatasets
}

fragment colorSchemeFragment on ColorScheme {
  id
  colorBy
  colorPool
  multicolorKeypoints
  opacity
  showSkeletons
  labelTags {
    fieldColor
    valueColors {
      color
      value
    }
  }
  defaultMaskTargetsColors {
    intTarget
    color
  }
  defaultColorscale {
    name
    list {
      value
      color
    }
    rgb
  }
  colorscales {
    path
    name
    list {
      value
      color
    }
    rgb
  }
  fields {
    colorByAttribute
    fieldColor
    path
    valueColors {
      color
      value
    }
    maskTargetsColors {
      intTarget
      color
    }
  }
}

fragment configFragment on Query {
  config {
    colorBy
    colorPool
    colorscale
    disableFrameFiltering
    gridZoom
    enableQueryPerformance
    defaultQueryPerformance
    loopVideos
    mediaFallback
    maxQueryTime
    multicolorKeypoints
    notebookHeight
    plugins
    showConfidence
    showIndex
    showLabel
    showSkeletons
    showTooltip
    theme
    timezone
    useFrameNumber
  }
  colorscale
}

fragment datasetAppConfigFragment on DatasetAppConfig {
  activeFields {
    exclude
    paths
  }
  colorScheme {
    ...colorSchemeFragment
    id
  }
  disableFrameFiltering
  dynamicGroupsTargetFrameRate
  gridMediaField
  mediaFields
  modalMediaField
  mediaFallback
  plugins
}

fragment datasetFragment on Dataset {
  createdAt
  datasetId
  groupField
  id
  info
  lastLoadedAt
  mediaType
  name
  parentMediaType
  version
  appConfig {
    ...datasetAppConfigFragment
  }
  brainMethods {
    key
    version
    timestamp
    viewStages
    config {
      cls
      embeddingsField
      method
      patchesField
      supportsPrompts
      type
      maxK
      supportsLeastSimilarity
    }
  }
  defaultMaskTargets {
    target
    value
  }
  defaultSkeleton {
    labels
    edges
  }
  evaluations {
    key
    version
    timestamp
    viewStages
    config {
      cls
      predField
      gtField
    }
  }
  groupMediaTypes {
    name
    mediaType
  }
  maskTargets {
    name
    targets {
      target
      value
    }
  }
  skeletons {
    name
    labels
    edges
  }
  ...estimatedCountsFragment
  ...frameFieldsFragment
  ...groupSliceFragment
  ...indexesFragment
  ...mediaFieldsFragment
  ...mediaTypeFragment
  ...sampleFieldsFragment
  ...sidebarGroupsFragment
  ...viewFragment
}

fragment estimatedCountsFragment on Dataset {
  estimatedFrameCount
  estimatedSampleCount
}

fragment frameFieldsFragment on Dataset {
  frameFields {
    ftype
    subfield
    embeddedDocType
    path
    dbField
    description
    info
  }
}

fragment groupSliceFragment on Dataset {
  defaultGroupSlice
}

fragment indexesFragment on Dataset {
  frameIndexes {
    name
    unique
    key {
      field
      type
    }
    wildcardProjection {
      fields
      inclusion
    }
  }
  sampleIndexes {
    name
    unique
    key {
      field
      type
    }
    wildcardProjection {
      fields
      inclusion
    }
  }
}

fragment mediaFieldsFragment on Dataset {
  name
  appConfig {
    gridMediaField
    mediaFields
    modalMediaField
    mediaFallback
  }
  sampleFields {
    path
  }
}

fragment mediaTypeFragment on Dataset {
  mediaType
}

fragment sampleFieldsFragment on Dataset {
  sampleFields {
    ftype
    subfield
    embeddedDocType
    path
    dbField
    description
    info
  }
}

fragment savedViewsFragment on Query {
  savedViews(datasetName: $name) {
    id
    datasetId
    name
    slug
    description
    color
    viewStages
    createdAt
    lastModifiedAt
    lastLoadedAt
  }
}

fragment sidebarGroupsFragment on Dataset {
  datasetId
  appConfig {
    sidebarGroups {
      expanded
      paths
      name
    }
  }
  ...frameFieldsFragment
  ...sampleFieldsFragment
}

fragment stageDefinitionsFragment on Query {
  stageDefinitions {
    name
    params {
      name
      type
      default
      placeholder
    }
  }
}

fragment viewFragment on Dataset {
  stages(slug: $savedViewSlug, view: $view)
  viewCls
  viewName
}

fragment viewSchemaFragment on Query {
  schemaForViewStages(datasetName: $name, viewStages: $view) {
    fieldSchema {
      path
      ftype
      subfield
      embeddedDocType
      info
      description
    }
    frameFieldSchema {
      path
      ftype
      subfield
      embeddedDocType
      info
      description
    }
  }
}
`}}}();X.hash="ab62132aa2263272549c2597ae82996f";export{X as default};
