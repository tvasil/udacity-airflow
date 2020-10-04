from airflow.hooks.postgres_hook import PostgresHook
from airflow.models import BaseOperator
from airflow.utils.decorators import apply_defaults

class LoadFactOperator(BaseOperator):

    ui_color = '#F98866'

    sql = """
        INSERT INTO {}
        {};
        """

    @apply_defaults
    def __init__(self,
                 redshift_conn_id="",
                 table="",
                 sql_template="",
                 *args, **kwargs):

        super(LoadFactOperator, self).__init__(*args, **kwargs)
        self.table = table
        self.redshift_conn_id = redshift_conn_id
        self.sql_template = sql_template

    def execute(self, context):
        redshift = PostgresHook(postgres_conn_id=self.redshift_conn_id)

        self.log.info(f"Loading data into fact table {self.table}")

        formatted_sql = LoadFactOperator.sql.format(
            self.table,
            self.sql_template
        )
        redshift.run(formatted_sql)
