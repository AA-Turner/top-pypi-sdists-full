"""Place a route pose (``RouteLanePose`` and its kin) on the map.

Each function takes the :class:`~.frame.RouteFrame` of the scenario's route
and, for a pose measured from the ego, the ego's route s when the action
starts; it returns a :class:`~autoware_carla_scenario.coordinate.poses.Lanelet2Pose`
for a pose on a lane, or a :class:`~autoware_carla_scenario.trajectory.MapPose`
for one off it (a crosswalk, the roadside).  A pose the map cannot give -- no
opposite lane there, no crosswalk on that leg -- raises a ``ValueError`` that
says which, so the action's error names the vertex and the reason.
"""

from __future__ import annotations

import math
from typing import TYPE_CHECKING, Optional, Union

# autoware_lanelet2_extension_python must be imported before lanelet2.
from autoware_lanelet2_extension_python.projection import MGRSProjector as _MGRS  # noqa: F401
import lanelet2.core
import lanelet2.geometry

from ..coordinate.poses import Lanelet2Pose
from ..kinematics.angle import normalize_angle_rad
from ..trajectory.model import (
    MapPose,
    RouteCrossingPose,
    RouteCrosswalkPose,
    RouteLanePose,
    RouteOppositePose,
    RouteRoadsidePose,
)
from ..trajectory.relative_lane import (
    _arc,
    _centreline,
    _heading_at,
    _point_at,
    advance_along_lane,
    shift_lanes,
)
from .frame import RouteFrame
from .geometry import BESIDE_MAX_TURN_DEG, _segment_intersection, paths_from_left

if TYPE_CHECKING:
    from lanelet2.core import ConstLanelet

__all__ = [
    "RoutePose",
    "junction_traffic_lights",
    "paths_from_left",
    "resolve_route_pose",
    "route_base_s",
]

RoutePose = Union[
    RouteLanePose,
    RouteOppositePose,
    RouteCrossingPose,
    RouteCrosswalkPose,
    RouteRoadsidePose,
]


def route_base_s(
    frame: RouteFrame, anchor: Optional[str], ego_s: Optional[float]
) -> float:
    """Route s a pose's ``ds`` counts from: its anchor's, else the ego's.

    Raises:
        ValueError: If there is no anchor and no ego position to count from.
    """
    if anchor:
        return frame.match.anchor_s(anchor)
    if ego_s is None:
        raise ValueError(
            "a route pose without an anchor is measured from the ego, and the "
            "ego's position on the route is not known"
        )
    return ego_s


def resolve_route_pose(
    pose: Union[
        RouteLanePose,
        RouteOppositePose,
        RouteCrossingPose,
        RouteCrosswalkPose,
        RouteRoadsidePose,
    ],
    frame: RouteFrame,
    ego_s: Optional[float] = None,
) -> Union[Lanelet2Pose, MapPose]:
    """Where *pose* is on *frame*'s map.

    *pose* is a :data:`RoutePose`, its union spelled out: the static check
    (docs/typecheck.md) compiles this once for each member.

    Raises:
        ValueError: When the map lacks what the pose names, saying what.
    """
    if isinstance(pose, RouteLanePose):
        return _lane(pose, frame, ego_s)
    if isinstance(pose, RouteOppositePose):
        return _opposite(pose, frame, ego_s)
    if isinstance(pose, RouteCrossingPose):
        return _crossing(pose, frame)
    if isinstance(pose, RouteCrosswalkPose):
        return _crosswalk(pose, frame)
    if isinstance(pose, RouteRoadsidePose):
        return _roadside(pose, frame, ego_s)
    raise TypeError(f"not a route pose: {type(pose).__name__}")


def _yaw(yaw: Optional[float]) -> float:
    return 0.0 if yaw is None else float(yaw)


def _lane(
    pose: RouteLanePose, frame: RouteFrame, ego_s: Optional[float]
) -> Lanelet2Pose:
    s = route_base_s(frame, pose.anchor, ego_s) + pose.ds
    lanelet_id, along = frame.locate(s)
    if pose.d_lane:
        lanelet_id, along = shift_lanes(
            frame.map, frame.graph, lanelet_id, along, pose.d_lane
        )
    return Lanelet2Pose(
        lanelet_id=lanelet_id, s=along, t=float(pose.offset), heading=_yaw(pose.yaw)
    )


def _opposite(
    pose: RouteOppositePose, frame: RouteFrame, ego_s: Optional[float]
) -> Lanelet2Pose:
    s = route_base_s(frame, pose.anchor, ego_s) + pose.ds
    lanelet_id, along = frame.locate(s)
    lanelet = frame.map.laneletLayer[lanelet_id]
    x, y = _point_at(_centreline(lanelet), along)
    found = frame.features.opposite_abreast(lanelet, x, y)
    if found is None:
        raise ValueError(
            f"there is no opposite-direction lane abreast of route s={s:.1f} m "
            f"(lanelet {lanelet_id})"
        )
    opposite: tuple[ConstLanelet, str] = found
    current, _side = opposite
    for step in range(1, pose.lane):
        outward = _outward(frame, current, x, y)
        if outward is None:
            raise ValueError(
                f"the opposite road abreast of route s={s:.1f} m has {step} "
                f"lane(s); there is no lane {pose.lane}"
            )
        farther: ConstLanelet = outward
        current = farther
    on, _t = _arc(current, x, y)
    return Lanelet2Pose(
        lanelet_id=int(current.id), s=on, t=float(pose.offset), heading=_yaw(pose.yaw)
    )


def _outward(
    frame: RouteFrame, lanelet: ConstLanelet, x: float, y: float
) -> Optional[ConstLanelet]:
    """*lanelet*'s same-direction neighbour farther from ``(x, y)``, or ``None``.

    The neighbour's lanelet abreast of the point, as *lanelet* is: its
    routing-graph neighbour, else the lane found beside it by where it is
    (:meth:`~.geometry.MapFeatures.beside`).
    """
    best: Optional[tuple[float, ConstLanelet]] = None
    for side in ("left", "right"):
        neighbour = frame.features.beside(lanelet, side, x, y)
        if neighbour is None:
            continue
        beside = frame.features.abreast(neighbour, x, y)
        s, _t = _arc(beside, x, y)
        bx, by = _point_at(_centreline(beside), s)
        own_s, _ = _arc(lanelet, x, y)
        ox, oy = _point_at(_centreline(lanelet), own_s)
        if math.hypot(bx - x, by - y) > math.hypot(ox - x, oy - y):
            gap = math.hypot(bx - x, by - y)
            if best is None or gap < best[0]:
                best = (gap, beside)
    if best is None:
        return None
    return best[1]


def _crossing(pose: RouteCrossingPose, frame: RouteFrame) -> Lanelet2Pose:
    way, _entry, _exit = frame.junction_way(pose.junction)
    members = [
        m
        for m in frame.features.junction_members(way)
        if m.approach == pose.approach and (pose.turn is None or m.turn == pose.turn)
    ]
    if not members:
        turning = "" if pose.turn is None else f" turning {pose.turn}"
        raise ValueError(
            f"junction {pose.junction} of the route has no lanelet entering it "
            f"from the {pose.approach}{turning}"
        )
    if pose.path is not None:
        ordered = paths_from_left(members)
        if pose.path > len(ordered):
            raise ValueError(
                f"junction {pose.junction} of the route has {len(ordered)} "
                f"path(s) from the {pose.approach} turning {pose.turn}; there "
                f"is no path {pose.path}"
            )
        chosen = ordered[pose.path - 1]
    else:
        # Traffic that actually crosses the ego's way first, then by id.
        chosen = min(members, key=lambda m: (not m.conflicts, int(m.lanelet.id)))
    lanelet_id, along = advance_along_lane(
        frame.map, frame.graph, int(chosen.lanelet.id), 0.0, float(pose.distance)
    )
    if pose.d_lane:
        lanelet_id, along = shift_lanes(
            frame.map, frame.graph, lanelet_id, along, pose.d_lane
        )
    return Lanelet2Pose(
        lanelet_id=lanelet_id, s=along, t=float(pose.offset), heading=_yaw(pose.yaw)
    )


def junction_traffic_lights(
    frame: RouteFrame, junction: int, approach: str, turn: Optional[str]
) -> list[int]:
    """The traffic lights (regulatory element ids) of the paths through
    junction *junction* of the route that enter it from *approach* and turn
    *turn* (``None``: any way) -- on their first junction lanelet and on the
    lanelet entering it; for ``same``, the ego's own way too when it turns
    so.  In order found, each once.

    Raises:
        ValueError: If the route has no such junction.
    """
    from .geometry import MapFeatures  # noqa: PLC0415
    from .search import junction_turn  # noqa: PLC0415

    way, entry, _exit = frame.junction_way(junction)
    features = frame.features
    lanelets: list[ConstLanelet] = []
    if approach == "same" and (turn is None or junction_turn(features, way) == turn):
        for own in way:
            lanelets.append(own)
        if entry is not None:
            entering: ConstLanelet = entry
            lanelets.append(entering)
    for member in features.junction_members(way):
        if member.approach != approach:
            continue
        if turn is not None and member.turn != turn:
            continue
        lanelets.append(member.lanelet)
        before = features.straightest_previous(member.lanelet)
        if before is not None:
            previous: ConstLanelet = before
            lanelets.append(previous)
    ids: list[int] = []
    for lanelet in lanelets:
        for element in lanelet.regulatoryElements:
            key = int(element.id)
            if MapFeatures.is_traffic_light(element) and key not in ids:
                ids.append(key)
    return ids


def _crosswalk(pose: RouteCrosswalkPose, frame: RouteFrame) -> MapPose:
    way, entry, exit_ = frame.junction_way(pose.junction)
    crosswalks = [
        c
        for c in frame.features.junction_crosswalks(way, entry, exit_)
        if c.leg == pose.leg
    ]
    if not crosswalks:
        raise ValueError(
            f"junction {pose.junction} of the route has no crosswalk across its "
            f"{pose.leg} leg"
        )
    through = sum(frame.features.length(ll) for ll in way)
    # The one nearest the junction on that leg.
    boundary = 0.0 if pose.leg == "entry" else through
    crosswalk = min(crosswalks, key=lambda c: (abs(c.u - boundary), int(c.lanelet.id)))
    line = _centreline(crosswalk.lanelet)
    px, py = crosswalk.point
    hx, hy = math.cos(crosswalk.heading), math.sin(crosswalk.heading)

    def left_of_path(point: tuple[float, float]) -> bool:
        return hx * (point[1] - py) - hy * (point[0] - px) > 0.0

    first_left = left_of_path(line[0])
    if (pose.side == "left") != first_left:
        line = list(reversed(line))
    total = sum(math.hypot(b[0] - a[0], b[1] - a[1]) for a, b in zip(line, line[1:]))
    if pose.along >= 0.0:
        x, y = _point_at(line, min(pose.along, total))
        heading = _heading_at(line, min(pose.along, total))
        if pose.along > total:
            x += math.cos(heading) * (pose.along - total)
            y += math.sin(heading) * (pose.along - total)
    else:
        heading = _heading_at(line, 0.0)
        x = line[0][0] + math.cos(heading) * pose.along
        y = line[0][1] + math.sin(heading) * pose.along
    return MapPose(x, y, None if pose.yaw is None else heading + float(pose.yaw))


def _roadside(
    pose: RouteRoadsidePose, frame: RouteFrame, ego_s: Optional[float]
) -> MapPose:
    s = route_base_s(frame, pose.anchor, ego_s) + pose.ds
    lanelet_id, along = frame.locate(s)
    lanelet = frame.map.laneletLayer[lanelet_id]
    points = _centreline(lanelet)
    x, y = _point_at(points, along)
    heading = _heading_at(points, along)
    edge = frame.features.abreast(
        frame.features.outermost(lanelet, pose.side, x, y), x, y
    )
    opposite = frame.features.opposite_abreast(lanelet, x, y)
    if opposite is not None and opposite[1] == pose.side:
        # The opposite road is on this side: its outermost lane is the edge.
        edge = opposite[0]
        while True:
            outward = _outward(frame, edge, x, y)
            if outward is None:
                break
            edge = outward
    sign = 1.0 if pose.side == "left" else -1.0
    best = _outer_bound(frame, edge, x, y, heading, sign)
    if best is None:
        raise ValueError(
            f"no road edge found on the {pose.side} abreast of route s={s:.1f} m"
        )
    gap, (kx, ky) = best
    nx, ny = (kx - x) / gap, (ky - y) / gap
    # Still on a road lanelet just past that bound -- one the walks did not
    # reach, or the edge lanelet itself where it is not abreast of the point
    # -- the kerb is where the line out of the route point leaves it, until
    # it is on none.  Only a lanelet running along the road there is stepped
    # past: one running across it (a crossing road at a junction's mouth)
    # would carry the kerb along that road, far from the route.
    seen: set[int] = set()
    for _hop in range(_MAX_KERB_HOPS):
        px, py = kx + nx * _KERB_PROBE_M, ky + ny * _KERB_PROBE_M
        on = _road_at(frame, px, py, seen)
        if on is None:
            break
        road: ConstLanelet = on
        seen.add(int(road.id))
        road_s, _t = _arc(road, px, py)
        across = abs(math.sin(_heading_at(_centreline(road), road_s) - heading))
        if across > math.sin(math.radians(BESIDE_MAX_TURN_DEG)):
            break
        out = _exit_along(road, kx, ky, nx, ny)
        kx, ky = kx + nx * out, ky + ny * out
    distance = float(pose.kerb_distance)
    return MapPose(
        kx + nx * distance,
        ky + ny * distance,
        None if pose.yaw is None else heading + float(pose.yaw),
    )


#: How far (m) past the kerb a roadside pose looks for a road lanelet it is
#: still on.
_KERB_PROBE_M = 0.05
#: The most road lanelets a roadside pose's kerb steps past so.
_MAX_KERB_HOPS = 12
#: How far (m) out from the kerb a road lanelet's outline is looked for.
_KERB_REACH_M = 50.0


def _outer_bound(
    frame: RouteFrame,
    lanelet: ConstLanelet,
    x: float,
    y: float,
    heading: float,
    sign: float,
) -> Optional[tuple[float, tuple[float, float]]]:
    """``(gap, point)`` of *lanelet*'s outer bound on the side *sign* picks
    (1 left, -1 right) of *heading* at ``(x, y)``: its point nearest
    ``(x, y)``, or ``None`` when neither bound is on that side.

    The outer bound is the one on that side of a lanelet running the route's
    way, the other of one running against it; where that one's nearest point
    is not on the side (a lanelet not abreast of the point), the bound
    farther from the point.
    """
    hx, hy = math.cos(heading), math.sin(heading)
    along, _t = _arc(lanelet, x, y)
    own = _heading_at(_centreline(lanelet), along)
    same = abs(normalize_angle_rad(own - heading)) < math.pi / 2.0
    outer = lanelet.leftBound if (sign > 0.0) == same else lanelet.rightBound
    ox, oy = frame.features.nearest_on(outer, x, y)
    if sign * (hx * (oy - y) - hy * (ox - x)) > 1e-6:
        return math.hypot(ox - x, oy - y), (ox, oy)
    best: Optional[tuple[float, tuple[float, float]]] = None
    for bound in (lanelet.leftBound, lanelet.rightBound):
        bx, by = frame.features.nearest_on(bound, x, y)
        if sign * (hx * (by - y) - hy * (bx - x)) <= 1e-6:
            continue
        gap = math.hypot(bx - x, by - y)
        if best is None or gap > best[0]:
            best = (gap, (bx, by))
    return best


def _road_at(
    frame: RouteFrame, x: float, y: float, seen: set[int]
) -> Optional[ConstLanelet]:
    """A road lanelet not in *seen* that ``(x, y)`` is on, or ``None``."""
    for distance, near in lanelet2.geometry.findNearest(
        frame.map.laneletLayer, lanelet2.core.BasicPoint2d(x, y), 4
    ):
        lanelet: ConstLanelet = near
        if float(distance) > 0.0:
            break
        if int(lanelet.id) not in seen and frame.features.is_road(lanelet):
            return lanelet
    return None


def _exit_along(
    lanelet: ConstLanelet, x: float, y: float, nx: float, ny: float
) -> float:
    """How far (m) from ``(x, y)`` along ``(nx, ny)`` the line leaves
    *lanelet*: its farthest crossing of the lanelet's outline (its bounds and
    ends), at least :data:`_KERB_PROBE_M`."""
    outline = [(float(p.x), float(p.y)) for p in lanelet.leftBound]
    outline += [(float(p.x), float(p.y)) for p in lanelet.rightBound][::-1]
    outline.append(outline[0])
    far = (x + nx * _KERB_REACH_M, y + ny * _KERB_REACH_M)
    out = _KERB_PROBE_M
    for a, b in zip(outline, outline[1:]):
        crossing = _segment_intersection((x, y), far, a, b)
        if crossing is not None:
            fractions: tuple[float, float] = crossing
            out = max(out, fractions[0] * _KERB_REACH_M)
    return out
