from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy import Column, String, Float, Integer, DateTime, Text
from datetime import datetime
from app.core.config import get_settings

settings = get_settings()

engine = create_async_engine(settings.database_url, echo=False)
AsyncSessionLocal = async_sessionmaker(engine, expire_on_commit=False)


class Base(DeclarativeBase):
    pass


class WalletScanCache(Base):
    __tablename__ = "wallet_scan_cache"

    wallet_address = Column(String, primary_key=True, index=True)
    chain = Column(String, default="ethereum")
    risk_score = Column(Integer)
    risk_level = Column(String)
    scan_result_json = Column(Text)
    scanned_at = Column(DateTime, default=datetime.utcnow)
    tx_count = Column(Integer, default=0)
    total_volume_usd = Column(Float, default=0.0)


class KnownBadActor(Base):
    __tablename__ = "known_bad_actors"

    address = Column(String, primary_key=True, index=True)
    label = Column(String)
    category = Column(String)
    source = Column(String)
    added_at = Column(DateTime, default=datetime.utcnow)


async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    await seed_blacklist()


async def seed_blacklist():
    known_bad = [
        {
            "address": "0x722122df12d4e14e13ac3b6895a86e84145b6967",
            "label": "Tornado Cash",
            "category": "mixer",
            "source": "OFAC"
        },
        {
            "address": "0x910cbd523d972eb0a6f4cae4618ad62622b39dbf",
            "label": "Tornado Cash",
            "category": "mixer",
            "source": "OFAC"
        },
        {
            "address": "0x3ad9db589d201a710ed237c829c7860ba404675d",
            "label": "Lazarus Group",
            "category": "sanctions",
            "source": "OFAC"
        },
        {
            "address": "0x098b716b8aaf21512996dc57eb0615e2383e2f96",
            "label": "Ronin Bridge Exploiter (Lazarus)",
            "category": "sanctions",
            "source": "OFAC"
        },
        {
            "address": "0x59abf3837fa962d6853b4cc0a19513aa031fd32b",
            "label": "FTX Exploiter",
            "category": "hack",
            "source": "Etherscan"
        },
    ]

    async with AsyncSessionLocal() as session:
        for actor in known_bad:
            existing = await session.get(KnownBadActor, actor["address"])
            if not existing:
                session.add(KnownBadActor(**actor))
        await session.commit()


async def get_db():
    async with AsyncSessionLocal() as session:
        yield session