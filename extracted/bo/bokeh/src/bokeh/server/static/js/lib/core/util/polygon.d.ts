import type { Arrayable } from "../types";
/** Width of the anti-aliasing skirt in CSS pixels. Must match the
 *  `antialias` uniform passed to the polygon shader so that the
 *  smoothstep fade range equals the skirt geometry extent. */
export declare const POLYGON_AA_WIDTH = 0.75;
/** Split x/y coordinate arrays on non-finite values into rings (sub-paths).
 *  Each ring is a flat array of interleaved [x0, y0, x1, y1, ...] values. */
export declare function split_rings(sx: Arrayable<number>, sy: Arrayable<number>): number[][];
export type SkirtGeometry = {
    positions: Float32Array;
    edge_distance: Float32Array;
    indices: Uint32Array;
    nvertices: number;
    ntriangles: number;
};
/** Generate expanded geometry with an anti-aliasing skirt around polygon boundaries.
 *
 *  The skirt approach adds a thin fringe of extra triangles around each polygon
 *  boundary edge. Interior vertices get `edge_distance = antialias_width`
 *  (fully opaque). Skirt outer vertices get `edge_distance = 0.0` (fully
 *  transparent). The GPU linearly interpolates across the skirt, producing a
 *  smooth alpha gradient for anti-aliased polygon edges. Ordinarily the skirt
 *  straddles the mathematical boundary. Rings with subpixel segments instead
 *  keep their triangulated vertices fixed and place the entire fade outwards,
 *  because moving those vertices can invalidate skinny fill triangles.
 *
 *  @param flat_coords      Interleaved [x0,y0,...] screen-pixel coordinates.
 *  @param rings            Ring arrays as returned by {@link split_rings}.
 *  @param tri_indices      Fill triangle indices into flat_coords.
 *  @param antialias_width  Width of the AA skirt in CSS pixels.
 *  @param preserve_vertices Keep boundary vertices fixed when the tessellator
 *                           adds vertices shared by touching boundaries.
 *  @param canonical_orientation Every boundary has the filled region on its
 *                               left, regardless of whether it is an outer or hole.
 *  @returns SkirtGeometry with combined positions, edge distances, and indices.
 */
export declare function generate_skirt_geometry(flat_coords: ArrayLike<number>, rings: number[][], tri_indices: ArrayLike<number>, antialias_width: number, preserve_vertices?: boolean, canonical_orientation?: boolean): SkirtGeometry;
export type RingLineData = {
    points: Float32Array;
    show: Uint8Array;
    nline: number;
    length_so_far: Float32Array;
};
/** Build line rendering data from a flat ring [x0,y0,x1,y1,...].
 *  Produces points with guard vertices, show flags, and
 *  cumulative segment lengths (always computed so that any glyph view
 *  e.g. selection or hover can render dashed if needed). */
export declare function build_line_from_ring(ring: number[]): RingLineData;
//# sourceMappingURL=polygon.d.ts.map