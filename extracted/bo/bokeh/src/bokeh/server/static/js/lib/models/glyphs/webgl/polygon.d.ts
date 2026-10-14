import type { SkirtGeometry } from "../../../core/util/polygon";
export declare function coordinates(indices: number[], coords: number[]): number[];
export declare function subdivide_contour(indices: number[]): Generator<number[]>;
/** Return source indices when a small ring is simple enough to triangulate directly. */
export declare function simple_ring_indices(ring: number[]): number[] | null;
export declare function is_affine_remap(source: number[], mapped: number[]): boolean;
/** Resolve an even-odd polygon into simple boundaries and cache its triangulation.
 *  Source vertex indices and intersection weights allow the same topology to be
 *  reused under affine screen mappings, including reversed axes. */
export declare class PolygonTopology {
    private readonly _ring_lengths;
    private readonly _source_coords;
    private readonly _combined;
    private readonly _groups;
    constructor(rings: number[][]);
    matches(rings: number[][]): boolean;
    geometries(rings: number[][], antialias_width?: number): SkirtGeometry[];
}
/** Construct polygon topology without allowing invalid geometry to abort a plot render. */
export declare function try_create_polygon_topology(rings: number[][]): PolygonTopology | null;
//# sourceMappingURL=polygon.d.ts.map