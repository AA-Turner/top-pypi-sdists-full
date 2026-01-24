# src/db.py

# src/db.py
from .imports import *
from sqlalchemy.exc import OperationalError

ENV_VARS = {
    "dbname": "abstract_base",
    "user": "admin",
}
def sanitize_output(record: dict) -> dict:
    if not record:
        return record
    if "audio" in record:
        record["audio"] = (
            f"<{len(record['audio'])} bytes>"
            if record["audio"]
            else None
        )
    return record
def sanitize_output(record: dict) -> dict:
    if "audio" in record:
        record["audio"] = f"<{len(record['audio'])} bytes>" if record["audio"] else None
    return record
class abstractHugpyDbManager(metaclass=SingletonMeta):
    def __init__(self,*args,**kwargs):
        if not hasattr(self,'initialized'):
            self.initialized = True
            self.metadata = MetaData()
            self.DATABASE_URL = self.get_database_url(**kwargs)
            self.VIDEOSTABLE = self.get_video_stable()
            
            self.engine = self.start_engine(self.DATABASE_URL,*args,**kwargs)
    def getEngine(self):
        return self.engine if self.engine is not None else None
    def getVideosTable(self):
        return self.VIDEOSTABLE if self.VIDEOSTABLE is not None else None
    def get_database_url(self,
                         **kwargs):
        ENV_VARS.update(**kwargs)
        env_js = get_db_vars(**ENV_VARS)
        return env_js.get("dburl")

    def start_engine(self,
                    url,*args,
                    future=None,
                    pool_size=None,
                    max_overflow=None,
                    **kwargs
        ):
        future= (False if (future == False) else True)
        pool_size=poolsize if is_number(pool_size) else 10
        max_overflow= max_overflow if is_number(max_overflow) else 20
        self.engine = None
        try:

            self.engine = create_engine(
                url,
                future=future,
                pool_size=pool_size,
                max_overflow=max_overflow,
            )
        except Exception as e:
            logger.info(f"{e}")
        return self.engine

    def get_video_stable(self):
        self.VIDEOSTABLE = None
        try:
            self.VIDEOSTABLE = Table(
                "videos",
                self.metadata,
                Column("id", Integer, primary_key=True),
                Column("video_id", String, unique=True, nullable=False),
                Column("info", JSONB),
                Column("extractfields", JSONB),
                Column("rawdata", JSONB),
                Column("metadata", JSONB),
                Column("whisper", JSONB),
                Column("captions", JSONB),
                Column("thumbnails", JSONB),
                Column("total_info", JSONB),
                Column("aggregated", JSONB),
                Column("seodata", JSONB),
                Column("audio_path", String),
                Column("audio_format", String),
                Column("metatags", JSONB),
                Column("pagedata", JSONB),
                Column("created_at", TIMESTAMP, server_default=text("NOW()")),
                Column("updated_at", TIMESTAMP, server_default=text("NOW()")),
            )
        except Exception as e:
            logger.info(f"{e}")
        return self.VIDEOSTABLE

    def init_db(self,**kwargs):

        if self.engine is not None:
            try:
                self.metadata.create_all(engine)
            except Exception as e:
                logger.info(f"{e}")
        return self.engine,self.VIDEOSTABLE



    def get_video_record(self,video_id, hide_audio: bool = True):
        video_id = normalize_video_id(video_id)

        with self.engine.begin() as conn:
            row = conn.execute(
                select(self.VIDEOSTABLE)
                .where(self.VIDEOSTABLE.c.video_id == video_id)
            ).first()

        if not row:
            return None

        record = dict(row._mapping)
        return sanitize_output(record) if hide_audio else record



    def upsert_video(self,video_id: str, **fields):
        """Insert or update a video record."""
        stmt = insert(self.VIDEOSTABLE).values(video_id=video_id, **fields)
        stmt = stmt.on_conflict_do_update(
            index_elements=["video_id"],
            set_={**fields, "updated_at": text("NOW()")}
        )
        with self.engine.begin() as conn:
            conn.execute(stmt)

    def get_video_record(self,video_id: str, hide_audio: bool = True):
        with self.engine.begin() as conn:
            row = conn.execute(select(self.VIDEOSTABLE).where(self.VIDEOSTABLE.c.video_id == video_id)).first()
            if not row:
                return None
            record = dict(row._mapping)
            if hide_audio and "audio" in record:
                # Replace huge binary blob with a short placeholder
                record["audio"] = f"<{len(record['audio'])} bytes>" if record["audio"] else None
            return record

def getHugpyDbManager(*args,**kwargs):
    return abstractHugpyDbManager(*args,**kwargs)
def getHugpyDbEngine(*args,**kwargs):     
    hugpyDb_mgr = getHugpyDbManager(*args,**kwargs)
    return hugpyDb_mgr.getEngine()
def getHugpyDbEVideosTable(*args,**kwargs):     
    hugpyDb_mgr = getHugpyDbManager(*args,**kwargs)
    return hugpyDb_mgr.getVideosTable()


def is_db_available(engine) -> bool:
    if engine is None:
        return False
    try:
        with engine.connect() as conn:
            return True
    except OperationalError:
        return False
        
        
    
