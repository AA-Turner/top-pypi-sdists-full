from chalk._gen.chalk.lsp.v1 import lsp_pb2 as pb
from chalk.parsed.duplicate_input_gql import (
    CodeActionGQL,
    CodeDescriptionGQL,
    DiagnosticGQL,
    DiagnosticRelatedInformationGQL,
    DiagnosticSeverityGQL,
    LocationGQL,
    LspGQL,
    PositionGQL,
    PublishDiagnosticsParams,
    RangeGQL,
    TextDocumentEditGQL,
    TextDocumentIdentifierGQL,
    TextEditGQL,
    WorkspaceEditGQL,
)

_severity_to_proto = {
    DiagnosticSeverityGQL.Error: pb.DIAGNOSTIC_SEVERITY_ERROR,
    DiagnosticSeverityGQL.Warning: pb.DIAGNOSTIC_SEVERITY_WARNING,
    DiagnosticSeverityGQL.Information: pb.DIAGNOSTIC_SEVERITY_INFORMATION,
    DiagnosticSeverityGQL.Hint: pb.DIAGNOSTIC_SEVERITY_HINT,
}


def convert_diagnostic_params(params: PublishDiagnosticsParams) -> pb.PublishDiagnosticsParams:
    return pb.PublishDiagnosticsParams(diagnostics=[convert_diagnostic(d) for d in params.diagnostics], uri=params.uri)


def convert_position(position: PositionGQL) -> pb.Position:
    return pb.Position(line=position.line, character=position.character)


def convert_range(range: RangeGQL) -> pb.Range:
    return pb.Range(start=convert_position(range.start), end=convert_position(range.end))


def convert_diagnostic_severity(severity: DiagnosticSeverityGQL) -> pb.DiagnosticSeverity:
    res = _severity_to_proto.get(severity)
    if res is None:
        raise ValueError(f"Unknown diagnostic severity: {severity}")
    return res


def convert_code_description(description: CodeDescriptionGQL) -> pb.CodeDescription:
    return pb.CodeDescription(href=description.href)


def convert_location(location: LocationGQL) -> pb.Location:
    return pb.Location(uri=location.uri, range=convert_range(location.range))


def convert_related_information(info: DiagnosticRelatedInformationGQL) -> pb.DiagnosticRelatedInformation:
    return pb.DiagnosticRelatedInformation(location=convert_location(info.location), message=info.message)


def convert_diagnostic(diagnostic: DiagnosticGQL) -> pb.Diagnostic:
    return pb.Diagnostic(
        range=convert_range(diagnostic.range),
        message=diagnostic.message,
        severity=convert_diagnostic_severity(diagnostic.severity) if diagnostic.severity is not None else None,
        code=diagnostic.code,
        code_description=convert_code_description(diagnostic.codeDescription)
        if diagnostic.codeDescription is not None
        else None,
        related_information=[convert_related_information(r) for r in diagnostic.relatedInformation or []],
    )


def convert_text_document(identifier: TextDocumentIdentifierGQL) -> pb.TextDocumentIdentifier:
    return pb.TextDocumentIdentifier(uri=identifier.uri)


def convert_text_edit(edit: TextEditGQL) -> pb.TextEdit:
    return pb.TextEdit(range=convert_range(edit.range), new_text=edit.newText)


def convert_document_edit(edit: TextDocumentEditGQL) -> pb.TextDocumentEdit:
    return pb.TextDocumentEdit(
        text_document=convert_text_document(edit.textDocument),
        edits=[convert_text_edit(e) for e in edit.edits],
    )


def convert_workspace_edit(edit: WorkspaceEditGQL) -> pb.WorkspaceEdit:
    return pb.WorkspaceEdit(
        document_changes=[convert_document_edit(c) for c in edit.documentChanges],
    )


def convert_code_action(action: CodeActionGQL) -> pb.CodeAction:
    return pb.CodeAction(
        title=action.title,
        diagnostics=[convert_diagnostic(d) for d in action.diagnostics or []],
        edit=convert_workspace_edit(action.edit),
    )


def convert_lsp_gql_to_proto(lsp: LspGQL) -> pb.LSP:
    return pb.LSP(
        diagnostics=[convert_diagnostic_params(p) for p in lsp.diagnostics],
        actions=[convert_code_action(a) for a in lsp.actions],
    )
