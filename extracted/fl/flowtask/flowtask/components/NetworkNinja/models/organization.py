from typing import List, Optional, Union, Any
from datetime import datetime
from datamodel import BaseModel, Field
from asyncdb import AsyncDB
from querysource.conf import default_dsn
from .abstract import AbstractPayload

class Organization(AbstractPayload):
    orgid: int = Field(required=False)
    organization_name: str
    program_slug: str
    program_id: int
    status: bool = Field(required=True, default=True)

    class Meta:
        name: str = 'organizations'
        schema: str = 'networkninja'
        strict: bool = True

    async def _sync_object(self, conn):
        """
        Sync the organization with the Database.
        """
        query = f"""
        select organization_name, company_slug as program_slug, p.program_id
        from troc.organizations o
        inner join auth.programs p on p.program_slug = o.company_slug
        where orgid = {self.orgid}
        """
        result = await conn.fetch_one(query)
        if result:
            self.organization_name = result['organization_name']
            self.program_id = result['program_id']
            self.program_slug = result['program_slug']
