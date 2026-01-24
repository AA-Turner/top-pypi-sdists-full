from pyspark.sql.functions import col, explode_outer
from pyspark.sql.types import StringType, StructField, StructType

def flattenDF(nested_df):
    stack = [((), nested_df)]
    columns = []
    counter = 0

    while len(stack) > 0:
        counter+= 1
        parents, df = stack.pop()

        flat_cols = [
            col(".".join(parents + (c[0],))).alias("_".join(parents + (c[0],)))
            for c in df.dtypes
            if c[1][:6] != "struct"
        ]

        nested_cols = [
            c[0]
            for c in df.dtypes
            if c[1][:6] == "struct"
        ]

        columns.extend(flat_cols)
        for nested_col in nested_cols:
            print(f'flattening nested column {nested_col}')
            projected_df = df.select(nested_col + ".*")
            stack.append((parents + (nested_col,), projected_df))
   
    new_df = nested_df.select(columns)
    if len(_getArrayCols(new_df)) > 0:
        new_df = _explodeArrayCols(new_df)
    return new_df


def _getArrayCols(df):
    arrayCols = []
    for d in df.dtypes:
        if d[1][:5] == 'array':
            arrayCols.append(d[0])
    return arrayCols

   
def _explodeArrayCols(df):
    arrayColumns = _getArrayCols(df)
    for c in arrayColumns:
        # print('exploding column: {}'.format(c))
        df = df.select(explode_outer(c), '*').drop(c).withColumnRenamed("col", c) # .alias("{}_".format(c))
    df = flattenDF(df)
    return df
