use std::borrow::Cow;

use futures::{future::BoxFuture, FutureExt};
use itertools::Itertools;
use tombi_schema_store::{Accessor, ArraySchema, CurrentSchema, DocumentSchema, ValueSchema};

use crate::goto_type_definition::{
    all_of::get_all_of_type_definition, any_of::get_any_of_type_definition,
    one_of::get_one_of_type_definition, GetTypeDefinition, TypeDefinition,
};

impl GetTypeDefinition for tombi_document_tree::Array {
    fn get_type_definition<'a: 'b, 'b>(
        &'a self,
        position: tombi_text::Position,
        keys: &'a [tombi_document_tree::Key],
        accessors: &'a [Accessor],
        current_schema: Option<&'a CurrentSchema<'a>>,
        schema_context: &'a tombi_schema_store::SchemaContext,
    ) -> BoxFuture<'b, Option<TypeDefinition>> {
        tracing::trace!("self = {:?}", self);
        tracing::trace!("keys = {:?}", keys);
        tracing::trace!("accessors = {:?}", accessors);
        tracing::trace!("current_schema = {:?}", current_schema);

        async move {
            if let Some(Ok(DocumentSchema {
                value_schema,
                schema_url,
                definitions,
                ..
            })) = schema_context
                .get_subschema(accessors, current_schema)
                .await
            {
                let current_schema = value_schema.map(|value_schema| CurrentSchema {
                    value_schema: Cow::Owned(value_schema),
                    schema_url: Cow::Owned(schema_url),
                    definitions: Cow::Owned(definitions),
                });

                return self
                    .get_type_definition(
                        position,
                        keys,
                        accessors,
                        current_schema.as_ref(),
                        schema_context,
                    )
                    .await;
            }

            if let Some(current_schema) = current_schema {
                match current_schema.value_schema.as_ref() {
                    ValueSchema::Array(array_schema) => {
                        for (index, value) in self.values().iter().enumerate() {
                            if value.range().contains(position) {
                                let accessor = Accessor::Index(index);

                                if let Some(items) = &array_schema.items {
                                    let mut referable_schema = items.write().await;
                                    if let Ok(Some(current_schema)) = referable_schema
                                        .resolve(
                                            current_schema.schema_url.clone(),
                                            current_schema.definitions.clone(),
                                            schema_context.store,
                                        )
                                        .await
                                    {
                                        return value
                                            .get_type_definition(
                                                position,
                                                keys,
                                                &accessors
                                                    .iter()
                                                    .cloned()
                                                    .chain(std::iter::once(accessor.clone()))
                                                    .collect::<Vec<_>>(),
                                                Some(&current_schema),
                                                schema_context,
                                            )
                                            .await;
                                    }
                                }

                                return value
                                    .get_type_definition(
                                        position,
                                        keys,
                                        &accessors
                                            .iter()
                                            .cloned()
                                            .chain(std::iter::once(accessor))
                                            .collect::<Vec<_>>(),
                                        None,
                                        schema_context,
                                    )
                                    .await;
                            }
                        }
                        return array_schema
                            .get_type_definition(
                                position,
                                keys,
                                accessors,
                                Some(current_schema),
                                schema_context,
                            )
                            .await;
                    }
                    ValueSchema::OneOf(one_of_schema) => {
                        return get_one_of_type_definition(
                            self,
                            position,
                            keys,
                            accessors,
                            one_of_schema,
                            &current_schema.schema_url,
                            &current_schema.definitions,
                            schema_context,
                        )
                        .await
                    }
                    ValueSchema::AnyOf(any_of_schema) => {
                        return get_any_of_type_definition(
                            self,
                            position,
                            keys,
                            accessors,
                            any_of_schema,
                            &current_schema.schema_url,
                            &current_schema.definitions,
                            schema_context,
                        )
                        .await
                    }
                    ValueSchema::AllOf(all_of_schema) => {
                        return get_all_of_type_definition(
                            self,
                            position,
                            keys,
                            accessors,
                            all_of_schema,
                            &current_schema.schema_url,
                            &current_schema.definitions,
                            schema_context,
                        )
                        .await
                    }
                    _ => {}
                }
            }

            for (index, value) in self.values().iter().enumerate() {
                if value.range().contains(position) {
                    let accessor = Accessor::Index(index);
                    return value
                        .get_type_definition(
                            position,
                            keys,
                            &accessors
                                .iter()
                                .cloned()
                                .chain(std::iter::once(accessor))
                                .collect::<Vec<_>>(),
                            None,
                            schema_context,
                        )
                        .await;
                }
            }

            None
        }
        .boxed()
    }
}

impl GetTypeDefinition for ArraySchema {
    fn get_type_definition<'a: 'b, 'b>(
        &'a self,
        _position: tombi_text::Position,
        _keys: &'a [tombi_document_tree::Key],
        accessors: &'a [Accessor],
        current_schema: Option<&'a CurrentSchema<'a>>,
        _schema_context: &'a tombi_schema_store::SchemaContext,
    ) -> BoxFuture<'b, Option<TypeDefinition>> {
        async move {
            current_schema.map(|schema| {
                TypeDefinition::new(
                    schema.schema_url.as_ref().clone(),
                    accessors.iter().map(Into::into).collect_vec(),
                    schema.value_schema.range(),
                )
            })
        }
        .boxed()
    }
}
