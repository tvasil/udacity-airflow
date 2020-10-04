from airflow.hooks.postgres_hook import PostgresHook
from airflow.models import BaseOperator
from airflow.utils.decorators import apply_defaults

class DataQualityOperator(BaseOperator):

    ui_color = '#89DA59'

    @apply_defaults
    def __init__(self,
                 redshift_conn_id="",
                 *args, **kwargs):

        super(DataQualityOperator, self).__init__(*args, **kwargs)
        self.redshift_conn_id = redshift_conn_id
        self.tables = kwargs["params"]["tables"]

    def execute(self, context):
        redshift = PostgresHook(postgres_conn_id=self.redshift_conn_id)

        self.log.info("Running quality checks")
        for t in tables:
            result = redshift.get_records(f"SELECT COUNT(*) FROM {t}")
            if len(result) < 1 or len(result[0]) < 1:
                raise ValueError(f"Table {t} has no records")
            num_records = result[0][0]
            if num_records < 1:
                raise ValueError(f"Data quality check failed. {t} contained 0 rows")
        self.log.info(f"Quality check on table {t} passed with {num_records} records")
