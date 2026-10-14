/*!
 * Adapted from libtess.js: Copyright 2000, Silicon Graphics, Inc.
 * Copyright 2015, Google Inc. All Rights Reserved.
 * Distributed under the SGI Free Software License B, version 2.0:
 * http://oss.sgi.com/projects/FreeB/
 */
import libtess from "libtess/libtess.cat.js";
import type { HalfEdge } from "libtess/libtess.cat.js";
export declare function smaller_loop(a: HalfEdge, b: HalfEdge): HalfEdge;
/** Run a synchronous check against libtess's original mesh operations. */
export declare function with_upstream_mesh_operations<T>(fn: () => T): T;
export { libtess };
//# sourceMappingURL=tessellator.d.ts.map