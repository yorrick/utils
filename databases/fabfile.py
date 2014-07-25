from datetime import datetime

from fabric.api import env, cd, hosts, settings, execute, local, task,\
    parallel, sudo
from fabric.contrib.console import confirm
import os
import psycopg2


user, password = 'dev', 'dev'
dbdump_dir = 'dbdump'


@task
def copy():
    with settings(warn_only=True):
        local('rm -rf ~/.Trash/{0}.old/'.format(dbdump_dir))
        local('mv -f ~/{0}.old ~/.Trash/; exit 0;'.format(dbdump_dir))
        local('mv ~/{0} ~/{0}.old; exit 0;'.format(dbdump_dir))
#        local('scp -r yorrick@vserver.auto:/srv/dbbackup/{0}/ ~'.format(dbdump_dir))
        local('rsync -d --progress --delete --include="*.backup" -e ssh "vserver.auto:/srv/dbbackup/dbdump/*" ~/{0}'.format(dbdump_dir))


RESTAURE_STRING = 'pg_restore --host localhost --port 5432 --username "dev" --dbname "{0}" --no-password  --no-owner --no-privileges --verbose {1} > /dev/null 2>&1'
DROP_STRING = 'dropdb --host=localhost --port=5432 --no-password --username=dev {0}'
CREATE_STRING = 'createdb --host=localhost --port=5432 --no-password --username=dev --owner=dev {0}'

databases = {
    'newcars': ('newcars.backup', ),
    'hellfire': ('hellfire.backup', ),
    'usedcars': ('usedcars.backup', ),
    'dealermaster': ('dealermaster.backup', ),
    'news': ('news.backup', ),
    'resolio': ('resolio.backup', ),
    'usedindex': ('usedindex.backup', ),
    'nciwork': ('nciwork.backup', ),
}

@task
def restore(db):
    if db not in databases:
        raise Exception('Unknow db {0}'.format(db))

    with settings(warn_only=True):
        local(DROP_STRING.format(db))

    local(CREATE_STRING.format(db))

    for path in databases[db]:
        file_path = os.path.join('~/{0}'.format(dbdump_dir), path)
        print 'Restauring dump {0}'.format(file_path)
        with settings(warn_only=True):
            local(RESTAURE_STRING.format(db, file_path), capture=False)


@task
def vacuum(db=None):
    if db and db not in databases:
        raise Exception('Unknow db {0}'.format(db))

    if not db:
        all_dbs = get_databases()
        if not confirm('Vacuum all DBs? ({0})'.format(', '.join(all_dbs)), default=False):
            return
    else:
        all_dbs = [db]

    for db in all_dbs:
        try:
            conn = psycopg2.connect(database=db, user=user, password=password)
            print 'Executing vacuum on DB {0}'.format(db)
            try:
                conn.set_isolation_level(0)
                cur = conn.cursor()
                cur.execute('vacuum full')
            finally:
                cur.close()

            conn.close()
        except Exception as e:
            pass


@task
def stop():
    local('sudo -u yorrick pg_ctl -D ~/postgres-data/ stop -m immediate')


@task
def start():
    local('sudo -u yorrick pg_ctl -D ~/postgres-data/ -l ~/postgres-data/server.log start')


def get_databases():
    conn = psycopg2.connect(database="postgres", user=user, password=password)
    try:
        cur = conn.cursor()
        cur.execute('select datname from pg_database')
        databases = [row[0] for row in cur.fetchall()]
    finally:
        cur.close()

    conn.close()
    return databases


ALL_COLUMNS = """
SELECT 
  tables.table_schema as schema,
  tables.table_name as table, 
  columns.column_name as column,
  columns.data_type as type
FROM 
  information_schema.tables
INNER JOIN information_schema.columns ON (tables.table_name = columns.table_name)
WHERE 
tables.table_schema <> 'information_schema' and tables.table_schema <> 'pg_catalog'
"""

COLUMN_LOOKUP = ALL_COLUMNS + """
and (lower(columns.column_name) LIKE lower(%(column)s))
ORDER BY tables.table_name, columns.column_name
"""


TABLE_LOOKUP = """
SELECT 
  tables.table_schema,
  tables.table_name
FROM 
  information_schema.tables
WHERE table_schema <> 'information_schema' and table_schema <> 'pg_catalog'
and (lower(table_name) LIKE lower(%(table)s))
order by table_name
"""

VALUE_LOOKUP = """
SELECT 
  tables.table_schema
  tables.table_name
FROM
  information_schema.tables
"""

def value_lookup(connection, value):
    # selects all columns for each table for each schema
    try:
        cur = connection.cursor()
        cur.execute(ALL_COLUMNS)

        # build a dict {schema: {table: [column]}}
        columns_by_table_by_schema = {}
        for row in cur.fetchall():
            schema = row[0]
            table = row[1]
            column = row[2]
            type = row[3]

            if not type == 'character varying':
                continue

            # workarround, TODO see why this column appears
            if column == 'fieldset':
                continue

            if schema not in columns_by_table_by_schema:
                tables = {}
                columns_by_table_by_schema[schema] = tables
            else:
                tables = columns_by_table_by_schema[schema]

            if table not in tables:
                columns = set()
                tables[table] = columns
            else:
                columns = tables[table]

            columns.add(column)
#        print 'columns_by_table_by_schema', columns_by_table_by_schema

        result = []
        for schema, tables in columns_by_table_by_schema.items():
            for table, columns in tables.items():
                for column in columns:
                    try:
                        table_cur = connection.cursor()
                        query = 'SELECT count(*) FROM %s.%s WHERE "%s" ILIKE ' % (schema, table, column) + '%s'
                        table_cur.execute(query, ('%%%s%%' % value.lower(), ))
                        count = table_cur.fetchone()[0]
                        if count > 0:
                            result.append((schema, table, column, '%d occurences' % count))
                    except Exception as e:
                        print '\t%s' % e
                    finally:
                        table_cur.close()

        return result
    finally:
        cur.close()

@task
def lookup(table='', column='', value='', database=''):
    if bool(table) == bool(column) == bool(value):
        raise Exception('Please specify one of "table" or "column" or "value"')

    databases = get_databases() if not database else [database]

    for db in databases:
        print db
        try:
            conn = psycopg2.connect(host='localhost', port='5432', database=db, user=user, password=password)
            try:
                cur = conn.cursor()
                if table:
                    cur.execute(TABLE_LOOKUP, {'table': '%%%s%%' % table})
                    result = cur.fetchall()
                elif column:
                    cur.execute(COLUMN_LOOKUP, {'column': '%%%s%%' % column})
                    result = cur.fetchall()
                elif value:
                    result = value_lookup(conn, value)
                else:
                    raise Exception()
                if result:
                    for row in result: print '\t', row
                else:
                    print '\tNothing'
            finally:
                cur.close()
        except Exception as e:
            print '\tException with DB %s' % db, e
    
        conn.close()



