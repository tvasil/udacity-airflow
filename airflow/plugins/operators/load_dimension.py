from airflow.hooks.postgres_hook import PostgresHook
from airflow.models import BaseOperator
from airflow.utils.decorators import apply_defaults

class LoadDimensionOperator(BaseOperator):

    ui_color = '#80BD9E'
    sql = """
        INSERT INTO {}
        {};
        """

    @apply_defaults
    def __init__(self,
                 redshift_conn_id="",
                 table="",
                 sql_template="",
                 truncate=False,
                 *args, **kwargs):

        super(LoadDimensionOperator, self).__init__(*args, **kwargs)
        self.table = table
        self.redshift_conn_id = redshift_conn_id
        self.truncate = truncate,
        self.sql_template = sql_template


    def execute(self, context):
        redshift = PostgresHook(postgres_conn_id=self.redshift_conn_id)

        if self.truncate:
            self.log.info(f"Truncating table {self.table}")
            redshift.run(f"DELETE FROM {self.table}")

        self.log.info(f"Loading data into dim table {self.table}")

        formatted_sql = LoadFactOperator.sql.format(
            self.table,
            self.sql_template
        )
        redshift.run(formatted_sql)
