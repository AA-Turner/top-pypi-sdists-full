import asyncio
from typing import Any, Optional, List
from collections.abc import Awaitable
from abc import ABC
import pandas as pd
import pytest
from navconfig import BASE_DIR
from .components import getComponent
from .components.flow import FlowComponent


@pytest.fixture(autouse=True, scope="session")
def component():
    cp = "Dummy"
    yield cp


pytestmark = pytest.mark.asyncio


class BaseTestCase(ABC):
    """BaseTestCase.

    Args:
        BoilerPlate for Testing Dataintegration Components.
    """

    arguments: dict = {}
    component = None
    name: str = None
    expected_result: Any = None
    expected_result_type: type = None
    expected_exception_msg: str = None

    @pytest.fixture(autouse=True, scope="class")
    def setup_class(self, component):
        self.component = None
        error = None
        self.name = component
        try:
            obj = getComponent(component)
            self.component = obj(**self.arguments)
        except Exception as e:
            print(e)
            error = e
        assert not error
        yield f"Starting Component {self.name}"

    def teardown_class(self):
        try:
            asyncio.run_until_complete(self.component.close())
        except Exception:
            pass
        self.component = None

    @pytest.fixture(autouse=True)
    def setup_method(self, component):
        self.name = component
        error = None
        try:
            obj = getComponent(component)
            self.component = obj(**self.arguments)
        except Exception as e:
            print(e)
            error = e
        assert not error

    def teardown_method(self):
        try:
            asyncio.run_until_complete(self.component.close())
        except Exception:
            pass
        self.component = None

    async def test_initialize(self, component):
        assert self.name == component
        assert isinstance(self.component, FlowComponent) is True
        assert self.component.ComponentName() == component

    async def test_start(self):
        assert self.component is not None
        assert callable(self.component.start)
        if asyncio.iscoroutinefunction(self.component.start):
            start = await self.component.start()
        else:
            start = self.component.start()
        assert start is True
        if asyncio.iscoroutinefunction(self.component.close):
            await self.component.close()
        else:
            self.component.close()

    async def test_run(self):
        result = None
        error = None
        assert self.component is not None
        # start firsts:
        if asyncio.iscoroutinefunction(self.component.start):
            start = await self.component.start()
        else:
            start = self.component.start()
        try:
            if asyncio.iscoroutinefunction(self.component.run):
                result = await self.component.run()
            else:
                result = self.component.run()
            # print('RESULT : ', result)
            if self.expected_result is not None:
                assert self.expected_result == result
            if self.expected_result_type:
                assert isinstance(result, self.expected_result_type)
        except Exception as e:
            if self.expected_exception_msg:
                assert e, self.expected_exception_msg
                result = True

            else:
                error = e
        if error:
            print("Test ERROR >", error)
        assert result is not None
        assert error is None
        if asyncio.iscoroutinefunction(self.component.close):
            await self.component.close()
        else:
            self.component.close()

    async def test_close(self):
        error = None
        assert self.component is not None
        # starts first:
        if asyncio.iscoroutinefunction(self.component.start):
            start = await self.component.start()
        else:
            start = self.component.start()
        try:
            if asyncio.iscoroutinefunction(self.component.close):
                await self.component.close()
            else:
                self.component.close()
        except Exception as e:
            error = e
        assert error is None
        await asyncio.sleep(1.5)


class PandasTestCase(BaseTestCase):
    """PandasTestCase.

    Args:
        Test Case for components that requires a previous Pandas Dataframe.
    """

    file_test: str = None
    data: Optional[List[dict]] = None
    renamed_cols: list = []

    async def startup_function(self) -> Awaitable:
        return True

    async def ending_function(self) -> Awaitable:
        return True

    @pytest.fixture(scope='session', autouse=True)
    async def setup_and_teardown(self):
        """Setup and Teardown for creating and dropping the table."""
        # Create table at the beginning of the session
        # Ensure the setup function is called
        await self.startup_function()
        print(':: Calling Setup Function :: ')
        yield
        # Ensure the teardown function is called
        await self.ending_function()
        print(':: Calling Ending Function :: ')

    @pytest.fixture(scope='session')
    def return_pandas(self, request):
        df = None
        if self.file_test:
            filepath = BASE_DIR.joinpath("docs", self.file_test)
            assert filepath.exists()
            df = pd.read_csv(filepath)
        elif self.data:
            df = pd.DataFrame(self.data)
        else:
            # If file_test is None, look for the 'data_sample' fixture
            data_fixture = request.getfixturevalue('data_sample')
            assert data_fixture is not None, "No data provided and no file_test available"
            df = pd.DataFrame(data_fixture)
        assert df is not None
        return df

    @pytest.fixture(autouse=True)
    def setup_method(self, component, return_pandas):
        self.name = component
        error = None
        try:
            obj = getComponent(component)
            df = return_pandas
            self.arguments["input_result"] = df
            self.component = obj(**self.arguments)
        except Exception as e:
            print(e)
            error = e
        assert not error

    async def test_start(self):
        assert self.component is not None
        assert callable(self.component.start)
        error = None
        try:
            await self.component.start()
        except Exception as err:
            error = err
        assert error is None
        if asyncio.iscoroutinefunction(self.component.close):
            await self.component.close()
        else:
            self.component.close()

    async def test_run(self):
        result = None
        error = None
        assert self.component is not None
        # start firsts:
        if asyncio.iscoroutinefunction(self.component.start):
            start = await self.component.start()
        else:
            start = self.component.start()
        assert start is not False
        try:
            if asyncio.iscoroutinefunction(self.component.run):
                result = await self.component.run()
            else:
                result = self.component.run()
            assert isinstance(result, pd.DataFrame)
            if self.expected_result is not None:
                ## TODO: making proves of transformations
                assert self.expected_result == result
            if self.renamed_cols is not None:
                columns = result.columns.values.tolist()
                # check if those columns are present in Dataframe
                for col in self.renamed_cols:
                    assert col in columns
        except Exception as e:
            error = e
        print("ERROR :: ", error)
        assert result is not None
        assert error is None
        if asyncio.iscoroutinefunction(self.component.close):
            await self.component.close()
        else:
            self.component.close()


def pytest_sessionfinish(session, exitstatus):
    asyncio.get_event_loop().close()
