from airflow.hooks.postgres_hook import PostgresHook
from airflow.models import BaseOperator
from airflow.utils.decorators import apply_defaults
import logging
class LoadDimensionOperator(BaseOperator):

    ui_color = '#80BD9E'

    @apply_defaults
    def __init__(self,
                 redshift_conn_id="redshift",
                 table="",
                 select_sql = "",
                 truncate_table=False, # Not truncated by default
                 *args, **kwargs):

        super(LoadDimensionOperator, self).__init__(*args, **kwargs)
        self.redshift_conn_id = redshift_conn_id
        self.table = table
        self.select_sql = select_sql
        self.truncate_table = truncate_table

    def execute(self, context):
        # self.log.info('LoadDimensionOperator not implemented yet')
        redshift = PostgresHook(postgres_conn_id=self.redshift_conn_id)

        # truncate_table が True の場合、テーブルを切り捨てる
        if self.truncate_table:
            logging.info(f"テーブル '{self.table}' を切り捨てています。")
            truncate_sql = f"TRUNCATE TABLE {self.table};"
            try:
                redshift.run(truncate_sql)
            except Exception as e:
                self.log.error(f"テーブル '{self.table}' の切り捨て中にエラーが発生しました: {e}")
                raise

        logging.info(f"テーブル '{self.table}' へのデータロードを開始しています。")
        exec_sql = f"INSERT INTO {self.table} {self.select_sql};"

        try:
            redshift.run(exec_sql)
            logging.info(f"テーブル '{self.table}' へのデータロードが成功しました。")
        except Exception as e:
            self.log.error(f"'{self.table}' へのデータのロード中にエラーが発生しました: {e}")
            raise