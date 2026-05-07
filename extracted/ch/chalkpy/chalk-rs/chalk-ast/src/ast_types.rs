use std::collections::HashMap;

use lsp_types::Location;

use crate::KwargLocationMap;

#[derive(Clone, Debug)]
pub struct FeatureFieldAST {
    pub field_name: String,
    pub field_name_location: Location,
    pub comment: Option<String>,
    pub description: Option<String>,
    pub owner: Option<String>,
    pub tags: Vec<String>,
    pub annotation: Option<Location>,
    pub feature_call: Option<Location>,
    pub kwarg_names: KwargLocationMap,
    pub kwargs: KwargLocationMap,
}

#[derive(Clone, Debug)]
pub struct FeatureClassAST {
    pub module: String,
    pub namespace: String,
    pub class_name: String,
    pub source: String,
    pub class_name_location: Location,
    pub class_definition_location: Location,
    pub decorator_location: Location,
    pub kwarg_names: KwargLocationMap,
    pub kwargs: KwargLocationMap,
    pub fields: HashMap<String, FeatureFieldAST>,
    pub annotations: Vec<FeatureFieldAST>,
}

#[derive(Clone, Debug)]
pub struct FunctionArgAST {
    pub arg_name: String,
    pub arg_location: Location,
    pub annotation: Option<Location>,
}

#[derive(Clone, Debug)]
pub struct ResolverAST {
    pub module: String,
    pub resolver_name: String,
    pub resolver_name_location: Location,
    pub decorator_location: Option<Location>,
    pub kwarg_names: KwargLocationMap,
    pub kwargs: KwargLocationMap,
    pub kwarg_dict_key_names: HashMap<String, KwargLocationMap>,
    pub kwarg_dict_values: HashMap<String, KwargLocationMap>,
    pub args_in_order: Vec<String>,
    pub args: HashMap<String, FunctionArgAST>,
    pub return_annotation: Option<Location>,
    pub missing_return_annotation: Option<Location>,
    pub return_statements: Vec<Location>,
    pub body: Option<Location>,
    pub return_arg: Option<Location>,
}

#[derive(Clone, Debug, Default)]
pub struct ParsedAstFile {
    pub feature_classes: Vec<FeatureClassAST>,
    pub functions: Vec<ResolverAST>,
    pub resolvers: Vec<ResolverAST>,
}
