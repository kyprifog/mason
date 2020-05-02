from engines import Engine, safe_interpolate_environment
from util.environment import MasonEnvironment
from engines.execution import ExecutionEngine
from engines.metastore import MetastoreEngine
from engines.storage import StorageEngine
from engines.scheduler import SchedulerEngine
from test.support import testing_base as base
from util.logger import logger
from util.yaml import parse_yaml
from definitions import from_root
from os import environ

class TestExecutionEngine:
    def before(self, config: str):
        base.set_log_level("error")
        config_home = from_root(config)
        env = MasonEnvironment(config_home=config_home)
        yaml_config_doc = parse_yaml(env.config_home)
        ee = ExecutionEngine(yaml_config_doc)
        return ee

    def test_configuration_exists(self):
        ee = self.before("/test/support/configs/test_config.yaml")
        assert(ee.client_name == "test2")
        assert(type(ee.client).__name__ == "EmptyExecutionClient")

    def test_configuration_dne(self):
        ee = self.before("/test/support/configs/test_partial_config.yaml")
        assert(ee.client_name == "")
        assert(type(ee.client).__name__ == "EmptyExecutionClient")

    def test_bad_config(self):
        ee = self.before("/test/support/configs/test_bad_config.yaml")
        assert(ee.client_name == "")
        assert(type(ee.client).__name__ == "EmptyExecutionClient")

class TestMetastoreEngine:
    def before(self, config: str):
        base.set_log_level("error")
        config_home = from_root(config)
        env = MasonEnvironment(config_home=config_home)
        yaml_config_doc = parse_yaml(env.config_home)
        me = MetastoreEngine(yaml_config_doc)
        return me

    def test_configuration_exists(self):
        me = self.before("/test/support/configs/test_config.yaml")
        assert(me.client_name == "test")
        assert(type(me.client).__name__ == "EmptyMetastoreClient")

    def test_configuration_dne(self):
        me = self.before("/test/support/configs/test_partial_config.yaml")
        assert(me.client_name == "")
        assert(type(me.client).__name__ == "EmptyMetastoreClient")



class TestStorageEngine:
    def before(self, config: str):
        base.set_log_level("error")
        config_home = from_root(config)
        env = MasonEnvironment(config_home=config_home)
        yaml_config_doc = parse_yaml(env.config_home)
        me = StorageEngine(yaml_config_doc)
        return me

    def test_configuration_exists(self):
        me = self.before("/test/support/configs/test_config.yaml")
        assert(me.client_name == "test")
        assert(type(me.client).__name__ == "EmptyStorageClient")

    def test_configuration_dne(self):
        me = self.before("/test/support/configs/test_partial_config_2.yaml")
        assert(me.client_name == "")
        assert(type(me.client).__name__ == "EmptyStorageClient")



class TestSchedulerEngine:
    def before(self, config: str):
        base.set_log_level("error")
        config_home = from_root(config)
        env = MasonEnvironment(config_home=config_home)
        yaml_config_doc = parse_yaml(env.config_home)
        me = SchedulerEngine(yaml_config_doc)
        return me

    def test_configuration_exists(self):
        me = self.before("/test/support/configs/test_config.yaml")
        assert(me.client_name == "test2")
        assert(type(me.client).__name__ == "EmptySchedulerClient")

    def test_configuration_dne(self):
        me = self.before("/test/support/configs/test_partial_config.yaml")
        assert(me.client_name == "")
        assert(type(me.client).__name__ == "EmptySchedulerClient")

class TestEnvironmentInterpolation:
    def test_interpolation(self):
        logger.set_level("fatal")
        # valid interpolation
        environ["AWS_REGION"] = "test"
        test_config = {"test": "{{AWS_REGION}}"}
        expect = {"test": "test"}
        d = safe_interpolate_environment(test_config)
        assert(d == expect)

        # unpermitted
        environ["SENSITIVE"] = "test"
        test_config = {"test": "{{SENSITIVE}}"}
        d = safe_interpolate_environment(test_config)
        assert(d == {"test": None})











