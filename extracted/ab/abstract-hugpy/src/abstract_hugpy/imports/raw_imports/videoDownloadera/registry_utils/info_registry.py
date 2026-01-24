from .registry_functions import *

class infoRegistry(metaclass=SingletonMeta):
    def __init__(self, video_root=None, documents_root=None, flat_layout: bool = False, **kwargs):
        if not hasattr(self, "initialized"):
            self.initialized = True
            self.engine = engine
            self.videos_root = VIDEOS_ROOT_DEFAULT

    # ─────────────────────────────────────────────
    # Helper: make sure we always have a video_id
    # ─────────────────────────────────────────────
    def _normalize_video_id(self, video_id: Optional[str], data: Any) -> Optional[str]:
        """
        Ensure we end up with a non-empty video_id.

        Priority:
            1. explicit video_id argument
            2. data["video_id"]
            3. data["id"] (yt-dlp field)
        """
        if video_id:
            return str(video_id)

        if isinstance(data, dict):
            candidate = data.get("video_id") or data.get("id")
            if candidate:
                return str(candidate)

        return None

    def _upsert(self, video_id, data: dict):
        # 🔹 Derive a real id from the payload if needed
        video_id = self._normalize_video_id(video_id, data)

        # 🔹 Final guard: never write a NULL PK to the DB
        if not video_id:
            logger.warning(
                "infoRegistry._upsert called without a usable video_id; "
                "skipping upsert. data.id=%r",
                (data.get("id") if isinstance(data, dict) else None),
            )
            return

        # Also ensure the info blob itself carries the normalized id
        if isinstance(data, dict):
            data["video_id"] = video_id

        stmt = insert(VIDEOSTABLE).values(video_id=video_id, info=data)
        stmt = stmt.on_conflict_do_update(
            index_elements=["video_id"],
            set_={"info": data, "updated_at": text("NOW()")},
        )
        with self.engine.begin() as conn:
            conn.execute(stmt)

    def get_video_info(self, url=None, video_id=None, video_path=None, force_refresh=False):
        url = get_corrected_url(url)

        # ── 1) Try to derive video_id from url/path before DB / yt-dlp
        if not video_id:
            if url:
                video_id = get_video_id_from_url(url)
            elif video_path:
                video_id = generate_video_id(video_path)

        # ── 2) If we *do* know video_id, see if it's already in DB
        if video_id:
            with self.engine.begin() as conn:
                row = conn.execute(
                    VIDEOSTABLE.select().where(VIDEOSTABLE.c.video_id == video_id)
                ).first()
                if row and not force_refresh:
                    return dict(row._mapping)

        # ── 3) Hit yt-dlp
        info = get_yt_dlp_info(url) if url else {}
        # yt-dlp sometimes uses "id", sometimes "video_id"
        info_video_id = None
        if isinstance(info, dict):
            info_video_id = info.get("video_id") or info.get("id")

        # Prefer explicit, fall back to yt-dlp-derived
        video_id = video_id or info_video_id

        # If we *still* have nothing, bail out gracefully
        if not video_id:
            logger.warning(
                "get_video_info: could not determine video_id for url=%r, video_path=%r; "
                "skipping DB write.",
                url,
                video_path,
            )
            return None

        # Make sure the blob advertises the final id
        if isinstance(info, dict):
            info["video_id"] = video_id

        # Standardize paths before storage
        info = ensure_standard_paths(
            info,
            video_id=video_id,
            root_dir=self.videos_root,
            video_url=url,
            video_path=video_path,
        )

        if info:
            self._upsert(video_id, info)
            return {"video_id": video_id, "info": info}

        return None

    def edit_info(self, data, video_id=None, url=None, video_path=None):
        # Keep the same normalization logic here too
        if not video_id:
            if url:
                video_id = get_video_id_from_url(url)
            elif video_path:
                video_id = generate_video_id(video_path)

        video_id = self._normalize_video_id(video_id, data)
        if not video_id:
            logger.warning(
                "edit_info called without a usable video_id; skipping edit. url=%r video_path=%r",
                url,
                video_path,
            )
            return None

        self._upsert(video_id, data)
        return self.get_video_info(video_id=video_id, force_refresh=True)
