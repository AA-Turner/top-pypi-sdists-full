def strip_shape_expr_id(shape_expr):
    if not hasattr(shape_expr, "id"):
        return shape_expr

    # only remove id, DO NOT reconstruct full object
    shape_expr.id = None
    return shape_expr

def rewrap_shape_decls(schema):
    from ShExJSG.ShExJ import ShapeDecl
    new_shapes = []

    for shape in schema.shapes:
        if isinstance(shape, ShapeDecl):
            new_shapes.append(shape)
            continue

        context = getattr(schema, "_context", None) or getattr(shape, "_context", None)

        shape_decl_id = shape.id
        shape_expr = shape
        shape_expr = strip_shape_expr_id(shape_expr)

        decl = ShapeDecl(
            id=shape_decl_id,
            abstract=getattr(shape, "abstract", None),
            restricts=getattr(shape, "restricts", None),
            shapeExpr=shape_expr,
            _context=context
        )

        new_shapes.append(decl)

    schema.shapes = new_shapes
    return schema