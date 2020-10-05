from airflow.hooks.postgres_hook import PostgresHook
from airflow.models import BaseOperator
from airflow.utils.decorators import apply_defaults

class DataQualityOperator(BaseOperator):

    ui_color = '#89DA59'

    @apply_defaults
    def __init__(self,
                 redshift_conn_id="",
                 qry_template="",
                 threshold=1,
                 *args, **kwargs):

        super(DataQualityOperator, self).__init__(*args, **kwargs)
        self.redshift_conn_id = redshift_conn_id
        self.tables = kwargs["params"]["tables"]
        self.qry_template = qry_template
        self.threshold = threshold

    def execute(self, context):
        redshift = PostgresHook(postgres_conn_id=self.redshift_conn_id)

        self.log.info("Running quality checks")
        for t in tables:
            qry = self.qry_template.format(t)
            result = redshift.get_records(qry)

            if len(result) < self.threshold or len(result[0]) < self.threshold:
                raise ValueError(f"Table {t} has no records")

            num_records = result[0][0]
            if num_records < self.threshold:
                raise ValueError(f"Data quality check failed. {t} contained 0 rows")

        self.log.info(f"Quality check on table {t} passed with {num_records} records")
