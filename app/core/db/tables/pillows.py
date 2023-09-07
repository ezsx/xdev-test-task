from sqlalchemy import Table

from .meta import metadata

pillows_table = Table(
    'pillows',
    metadata,
)
