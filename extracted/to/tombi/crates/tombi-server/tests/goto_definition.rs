use tombi_test_lib::project_root_path;

mod goto_definition_tests {
    use super::*;

    mod cargo_schema {
        use super::*;

        test_goto_definition!(
            #[tokio::test]
            async fn dependencies_serde_workspace(
                r#"
                [dependencies]
                serde = { workspace█ = true }
                "#,
                project_root_path().join("crates/test-crate/Cargo.toml"),
            ) -> Ok(project_root_path().join("Cargo.toml"));
        );

        test_goto_definition!(
            #[tokio::test]
            async fn dev_dependencies_rstest_workspace(
                r#"
                [dev-dependencies]
                rstest = { workspace█ = true }
                "#,
                project_root_path().join("crates/test-crate/Cargo.toml"),
            ) -> Ok(project_root_path().join("Cargo.toml"));
        );

        test_goto_definition!(
            #[tokio::test]
            async fn build_dependencies_rstest_workspace(
                r#"
                [build-dependencies]
                serde = { workspace█ = true }
                "#,
                project_root_path().join("crates/test-crate/Cargo.toml"),
            ) -> Ok(project_root_path().join("Cargo.toml"));
        );

        test_goto_definition!(
            #[tokio::test]
            async fn dependencies_tombi_ast_workspace(
                r#"
                [dependencies]
                tombi-ast = { workspace█ = true }
                "#,
                project_root_path().join("crates/test-crate/Cargo.toml"),
            ) -> Ok(project_root_path().join("crates/tombi-ast/Cargo.toml"));
        );

        test_goto_definition!(
            #[tokio::test]
            async fn dev_dependencies_tombi_ast_workspace(
                r#"
                [dev-dependencies]
                tombi-ast = { workspace█ = true }
                "#,
                project_root_path().join("crates/test-crate/Cargo.toml"),
            ) -> Ok(project_root_path().join("crates/tombi-ast/Cargo.toml"));
        );

        test_goto_definition!(
            #[tokio::test]
            async fn build_dependencies_tombi_ast_workspace(
                r#"
                [build-dependencies]
                tombi-ast = { workspace█ = true }
                "#,
                project_root_path().join("crates/test-crate/Cargo.toml"),
            ) -> Ok(project_root_path().join("crates/tombi-ast/Cargo.toml"));
        );

        test_goto_definition!(
            #[tokio::test]
            async fn dependencies_tombi_ast_path(
                r#"
                [workspace.dependencies]
                tombi-ast = { path█ = "crates/tombi-ast" }
                "#,
                project_root_path().join("Cargo.toml"),
            ) -> Ok(project_root_path().join("crates/tombi-ast/Cargo.toml"));
        );
    }

    mod pyproject_uv_schema {
        use super::*;

        test_goto_definition!(
            #[tokio::test]
            async fn tool_uv_sources_package_workspace(
                r#"
                [tool.uv.sources]
                tombi-beta = { workspace█ = true }
                "#,
                project_root_path().join("python
                /tombi-beta/pyproject.toml"),
            ) -> Ok(project_root_path().join("python/tombi-beta/pyproject.toml"));
        );
    }

    #[macro_export]
    macro_rules! test_goto_definition {
        (#[tokio::test] async fn $name:ident(
            $source:expr,
            $file_path:expr,
        ) -> Ok($expected_file_path:expr);) => {
            #[tokio::test]
            async fn $name() -> Result<(), Box<dyn std::error::Error>> {
                use tombi_server::handler::{handle_did_open, handle_goto_definition};
                use tombi_server::Backend;
                use tower_lsp::{
                    lsp_types::{
                        DidOpenTextDocumentParams, GotoDefinitionParams, GotoDefinitionResponse,
                        PartialResultParams, TextDocumentIdentifier, TextDocumentItem,
                        TextDocumentPositionParams, Url, WorkDoneProgressParams,
                    },
                    LspService,
                };

                tombi_test_lib::init_tracing();

                let (service, _) = LspService::new(|client| {
                    Backend::new(client, &tombi_server::backend::Options::default())
                });

                let backend = service.inner();

                let toml_file_url = Url::from_file_path($file_path).expect("failed to convert file path to URL");

                let mut toml_text = textwrap::dedent($source).trim().to_string();
                let Some(index) = toml_text.as_str().find("█") else {
                    return Err("failed to find position marker (█) in the test data".into());
                };
                toml_text.remove(index);

                handle_did_open(
                    backend,
                    DidOpenTextDocumentParams {
                        text_document: TextDocumentItem {
                            uri: toml_file_url.clone(),
                            language_id: "toml".to_string(),
                            version: 0,
                            text: toml_text.clone(),
                        },
                    },
                )
                .await;

                let params = GotoDefinitionParams {
                    text_document_position_params: TextDocumentPositionParams {
                        text_document: TextDocumentIdentifier { uri: toml_file_url },
                        position: (tombi_text::Position::default()
                            + tombi_text::RelativePosition::of(&toml_text[..index]))
                        .into(),
                    },
                    work_done_progress_params: WorkDoneProgressParams::default(),
                    partial_result_params: PartialResultParams::default(),
                };

                let Ok(result) = handle_goto_definition(&backend, params).await else {
                    return Err("failed to handle goto_definition".into());
                };

                tracing::debug!("goto_definition result: {:#?}", result);

                let expected_path = $expected_file_path.to_owned();

                match result {
                    Some(def_links) => {
                        // Handle different return types (single link or array)
                        match def_links {
                            GotoDefinitionResponse::Link(links) => {
                                assert!(!links.is_empty(), "Definition links were returned but empty");

                                let first_link = &links[0];
                                let target_url = first_link.target_uri.clone();
                                let target_path = target_url.to_file_path()
                                    .expect("Failed to convert URL to file path");

                                pretty_assertions::assert_eq!(
                                    target_path,
                                    expected_path,
                                    "Definition link points to an unexpected schema path\nExpected: {:?}\nActual: {:?}",
                                    expected_path,
                                    target_path
                                );
                            },
                            GotoDefinitionResponse::Scalar(location) => {
                                let target_url = location.uri.clone();
                                let target_path = target_url.to_file_path()
                                    .expect("Failed to convert URL to file path");

                                pretty_assertions::assert_eq!(
                                    target_path,
                                    expected_path,
                                    "Definition link points to an unexpected schema path\nExpected: {:?}\nActual: {:?}",
                                    expected_path,
                                    target_path
                                );
                            },
                            GotoDefinitionResponse::Array(locations) => {
                                assert!(!locations.is_empty(), "Definition locations were returned but empty");

                                let first_location = &locations[0];
                                let target_url = first_location.uri.clone();
                                let target_path = target_url.to_file_path()
                                    .expect("Failed to convert URL to file path");

                                pretty_assertions::assert_eq!(
                                    target_path,
                                    expected_path,
                                    "Definition link points to an unexpected schema path\nExpected: {:?}\nActual: {:?}",
                                    expected_path,
                                    target_path
                                );
                            }
                        }
                    },
                    None => {
                        panic!("No definition link was returned, but expected path: {:?}", expected_path);
                    }
                }

                Ok(())
            }
        };
    }
}
