import asyncio
import time
from fastapi import BackgroundTasks
from starlette.requests import Request
from app.main import create_lead
from app.schemas import LeadCreate
from app.models import AIAnalysis
from sqlalchemy import select

def test_inquiry_returns_before_slow_classification(crm, fake_provider, fake_email_provider):
    original = fake_provider.structured
    def slow(*args):
        time.sleep(0.3)
        return original(*args)
    fake_provider.structured = slow
    tasks = BackgroundTasks()
    with crm.session() as db:
        started = time.perf_counter()
        lead = create_lead(LeadCreate(**crm.inquiry()), Request({'type': 'http', 'client': ('test', 1), 'headers': []}), tasks, db, fake_provider, fake_email_provider)
        assert time.perf_counter() - started < 0.2
        assert not fake_provider.calls
        lead_id = lead.id
    asyncio.run(tasks())
    with crm.session() as db:
        assert db.scalar(select(AIAnalysis).where(AIAnalysis.lead_id == lead_id)) is not None
