from mason.clients.response import Response
from mason.configurations.valid_config import ValidConfig
from mason.definitions import from_root
from mason.operators.operator import Operator
from mason.parameters.input_parameters import InputParameters
from mason.test.support.testing_base import run_tests
from mason.util.environment import MasonEnvironment
from dotenv import load_dotenv

load_dotenv(from_root('/.env.example'))

def test_get():

    def tests(env: MasonEnvironment, config: ValidConfig, op: Operator):
        # valid job_id
        params = InputParameters(parameter_string=f"job_id:good_job_id")
        # TODO: consolidate these
        expect = {
            'spark': {'Data': [{'Logs': ['<LOG_DATA>']}], 'Errors': [], 'Info': [], 'Warnings': []},
            'athena': {'Data': [{'ResultSetMetadata': {'ColumnInfo': [{'CaseSensitive': True, 'CatalogName': 'hive', 'Label': 'widget','Name': 'widget', 'Nullable': 'UNKNOWN','Precision': 2147483647, 'Scale': 0,'SchemaName': '','TableName': '','Type': 'varchar'}]},'Rows': [{'Data': [{'VarCharValue': 'widget'}]}]}],'Errors': [],'Info': ['Job Status: SUCCEEDED'], 'Warnings': []},
        }

        good = op.validate(config, params).run(env, Response())

        assert ((expect[config.execution.client_name], 200) == good.with_status())

        # invalid job_id
        params = InputParameters(parameter_string="job_id:bad_job_id")
        bad = op.validate(config, params).run(env, Response())


        expect = {
            'spark': {'Errors': ['Error from server (NotFound): pods "bad_job_id-driver" not found'], 'Info': [], 'Warnings': []},
            'athena': {'Errors': ['QueryExecution bad_job_id was not found', 'Invalid Job: QueryExecution bad_job_id was not found'], 'Info': [], 'Warnings': []}
        }

        assert (bad.with_status() == (expect[config.execution.client_name], 400))


    run_tests("job", "get", True, "fatal", ["config_3", "config_4"], tests)
