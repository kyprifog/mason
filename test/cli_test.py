
from click.testing import CliRunner
from cli import config, operator, register
from definitions import from_root
import os
import pytest #type: ignore
import shutil
import re

#  TODO: Figure out how to remove references to /Users/kyle/dev from these tests for any user, remove basename from output

def ansi_escape(text):
    ansi_escape = re.compile(r'\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])')
    return ansi_escape.sub('', text)

def assert_multiline(s1: str, s2: str):
    e = re.compile(r"(\s|\n|\t)")
    f1 = e.sub('', ansi_escape(s1))
    f2 = e.sub('', s2)
    assert (f1 == f2)

def print_result(result):
    print(result.output)
    print(result.exception)

class TestCLI:

    @pytest.fixture(autouse=True)
    def run_around_tests(self):
        os.environ["MASON_HOME"] = ".tmp/"
        yield
        shutil.rmtree(".tmp/")

    def test_config_0(self):
        runner = CliRunner()
        self.test_valid_config()
        result = runner.invoke(config,
                               [from_root('/examples/operators/table/test_configs/config_0.yaml'), '-l', 'info'])
        print(result.output)
        expects = """
        Set log level to info
        +--------------------+
        | Config Validation  |
        +--------------------+

        Schema error /Users/kyle/dev/mason/configurations/schema.json: 'bad' is not one of ['glue', 's3']

        Invalid Config Schema: /Users/kyle/dev/mason/examples/operators/table/test_configs/config_0.yaml

        """
        assert_multiline(expects, result.output)

    def test_config_1(self):
      runner = CliRunner()
      result1 = runner.invoke(config, [from_root('/examples/operators/table/test_configs/config_1.yaml'), '-l', 'info'])
      expect1 = """
        Set log level to info
        +-------------------------------+
        | Creating MASON_HOME at .tmp/  |
        +-------------------------------+
        +-------------------------------------------------------+
        | Creating OPERATOR_HOME at .tmp/registered_operators/  |
        +-------------------------------------------------------+
        +-----------------------------------------------+
        | Creating CONFIG_HOME at .tmp/configurations/  |
        +-----------------------------------------------+
        +--------------------+
        | Config Validation  |
        +--------------------+

        Valid Configuration. Saving config /Users/kyle/dev/mason/examples/operators/table/test_configs/config_1.yaml to .tmp/configurations/

        +----------------+
        | Configuration  |
        +----------------+
        Configuration: {'metastore': {'client_name': 'glue', 'configuration': {'aws_role_arn': 'arn:aws:iam::062325279035:role/service-role/AWSGlueServiceRole-anduin-data-glue', 'region': 'us-east-1'}}, 'scheduler': {'client_name': 'glue', 'configuration': {'aws_role_arn': 'arn:aws:iam::062325279035:role/service-role/AWSGlueServiceRole-anduin-data-glue', 'region': 'us-east-1'}}, 'storage': {'client_name': 's3', 'configuration': {'region': 'us-east-1'}}, 'execution': {'client_name': '', 'configuration': {}}}
      """
      assert_multiline(expect1, result1.output)

    def test_config_2(self):
        runner = CliRunner()
        result1 = runner.invoke(config, [from_root('/examples/operators/table/test_configs/config_2.yaml'), '-l', 'info'])
        expects1 = """
        Set log level to info
        +-------------------------------+
        | Creating MASON_HOME at .tmp/  |
        +-------------------------------+
        +-------------------------------------------------------+
        | Creating OPERATOR_HOME at .tmp/registered_operators/  |
        +-------------------------------------------------------+
        +-----------------------------------------------+
        | Creating CONFIG_HOME at .tmp/configurations/  |
        +-----------------------------------------------+
        +--------------------+
        | Config Validation  |
        +--------------------+

        Valid Configuration. Saving config /Users/kyle/dev/mason/examples/operators/table/test_configs/config_2.yaml to .tmp/configurations/

        +----------------+
        | Configuration  |
        +----------------+
        Configuration: {'metastore': {'client_name': 's3', 'configuration': {'region': 'us-east-1'}}, 'scheduler': {'client_name': '', 'configuration': {}}, 'storage': {'client_name': '', 'configuration': {}}, 'execution': {'client_name': 'spark', 'configuration': {'threads': 3}}}
        """
        assert_multiline(result1.output, expects1)

        result2 = runner.invoke(register, [from_root('/examples/operators/table/')])
        expects2 = """
        Set log level to info
        Valid Operator Definition /Users/kyle/dev/mason/examples/operators/table/merge/operator.yaml
        Valid Operator Definition /Users/kyle/dev/mason/examples/operators/table/refresh/operator.yaml
        Valid Operator Definition /Users/kyle/dev/mason/examples/operators/table/get/operator.yaml
        Valid Operator Definition /Users/kyle/dev/mason/examples/operators/table/list/operator.yaml
        Valid Operator Definition /Users/kyle/dev/mason/examples/operators/table/infer/operator.yaml
        Registering operators at /Users/kyle/dev/mason/examples/operators/table/ to .tmp/registered_operators/table/
        """
        assert_multiline(result2.output, expects2)

        result3 = runner.invoke(operator, [])
        expects3 = """
        Set log level to info
        +----------------+
        | Configuration  |
        +----------------+
        Configuration: {'metastore': {'client_name': 's3', 'configuration': {'region': 'us-east-1'}}, 'scheduler': {'client_name': '', 'configuration': {}}, 'storage': {'client_name': '', 'configuration': {}}, 'execution': {'client_name': 'spark', 'configuration': {'threads': 3}}}
        Neither parameter string nor parameter path provided.

        +---------------------------------------------------------+
        | Available Operator Methods: .tmp/registered_operators/  |
        +---------------------------------------------------------+

        namespace    command    description                                                                               parameters
        -----------  ---------  ----------------------------------------------------------------------------------------  ----------------------------------------------------------------
        table        merge      Merge metastore tables                                                                    {'required': ['merge_strategy']}
        table        refresh    Refresh metastore tables                                                                  {'required': ['database_name', 'table_name']}
        table        get        Get metastore table contents                                                              {'required': ['database_name', 'table_name']}
        table        list       Get metastore tables                                                                      {'required': ['database_name']}
        table        infer      Registers a schedule for infering the table then does a one time trigger of the refresh.  {'required': ['database_name', 'storage_path', 'schedule_name']}
        """
        assert_multiline(result3.output, expects3)


        result4 = runner.invoke(operator, ["table", "merge"])
        expects4 = """
        Set log level to info
        +----------------+
        | Configuration  |
        +----------------+
        Configuration: {'metastore': {'client_name': 's3', 'configuration': {'region': 'us-east-1'}}, 'scheduler': {'client_name': '', 'configuration': {}}, 'storage': {'client_name': '', 'configuration': {}}, 'execution': {'client_name': 'spark', 'configuration': {'threads': 3}}}
        Neither parameter string nor parameter path provided.

        +-------------------------+
        | Parameters Validation:  |
        +-------------------------+
        Missing: ['merge_strategy']

        +--------------------+
        | Operator Response  |
        +--------------------+
        {
         "Errors": [
          "Missing required parameters: merge_strategy"
         ],
         "Info": [],
         "Warnings": []
        }
        """
        assert_multiline(result4.output, expects4)

        result5 = runner.invoke(operator, ["table", "merge", "-p", "merge_strategy:test"])
        print(result5.output)


