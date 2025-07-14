from airflow.hooks.postgres_hook import PostgresHook
from airflow.models import BaseOperator
# from airflow.utils.decorators import apply_defaults
from helpers.sql_queries import SqlQueries

class LoadFactOperator(BaseOperator):

    ui_color = '#F98866'

    # @apply_defaults
    def __init__(self,
                 redshift_conn_id="redshift",
                 table="",
                 select_sql = "",
                 **kwargs):

        super().__init__(**kwargs)
        self.redshift_conn_id = redshift_conn_id
        self.table = table
        self.select_sql = select_sql

    def execute(self, context):
        # self.log.info('LoadFactOperator not implemented yet')
        redshift = PostgresHook(postgres_conn_id=self.redshift_conn_id)

        try:
            exec_sql = f"INSERT INTO {self.table} {self.select_sql};"
            redshift.run(exec_sql)
        except Exception as e:
            self.log.error(f"'{self.table}' へのデータのロード中にエラーが発生しました: {e}")
            raise
