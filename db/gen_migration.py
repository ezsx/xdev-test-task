from sqlalchemy import create_engine
from sqlalchemy import MetaData, Table, Index
from alembic import autogenerate
from alembic.operations import ops

#sqlacodegen postgresql+psycopg2://postgres:mysecretpassword@localhost:5432/postgres >33.txt

#e = create_engine("mysql://scott:tiger@localhost/test")
e = create_engine("postgresql+psycopg2://postgres:mysecretpassword@localhost:5432/postgres")

with e.connect() as conn:
    #cursor = conn._dbapi_connection.cursor()
    #cursor.execute("SET SESSION search_path='%s'" % 'mrp')
    m = MetaData()
    user_table = Table('pillows', m, autoload_with=conn)
    user_table = Table('pillows_history', m, autoload_with=conn)
    #Index('mms_action_curr_tbl_id_export_prcn_idx',m,autoload_with=conn)

print(autogenerate.render_python_code(
    ops.UpgradeOps(
        ops=[
            ops.CreateTableOp.from_table(table) for table in m.tables.values()
        ] + [
            ops.CreateIndexOp.from_index(idx) for table in m.tables.values()
            for idx in table.indexes
        ]
    ))
)

