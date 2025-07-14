from airflow.hooks.postgres_hook import PostgresHook
from airflow.models import BaseOperator
# from airflow.utils.decorators import apply_defaults
from helpers.sql_queries import SqlQueries

class CreateTablesOperator(BaseOperator):

    ui_color = '#F98866'

    # @apply_defaults
    def __init__(self,
                 redshift_conn_id="redshift",
                 sql_lists = None,
                 **kwargs):

        super().__init__(**kwargs)
        self.redshift_conn_id = redshift_conn_id
        self.sql_lists = sql_lists if sql_lists is not None else []

    def execute(self, context):
        # self.log.info('LoadFactOperator not implemented yet')
        redshift = PostgresHook(postgres_conn_id=self.redshift_conn_id)

        try:
            for sql in self.sql_lists:
                exec_sql = sql
                redshift.run(exec_sql)
        except Exception as e:
            self.log.error(f"'{self.table}' へのデータのロード中にエラーが発生しました: {e}")
            raise
