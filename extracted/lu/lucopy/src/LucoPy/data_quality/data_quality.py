import json

class CheckResult:

    def __init__(self, results):

        # Required - will throw exception if not present
        required_args = ['check', 'success']
        for k in required_args:
            if k not in results:
                raise Exception(f'Required arg not present: {k}')

        # Set required attributes
        self.check = results['check']
        self.success = results['success']

        # Set optional attributes
        self.__optional_attributes = [
            'checkArgs',
            'onFail',
            'referenceUrl',
            'tags',
            'observed',
            'metadata'
            ]

        for attr in self.__optional_attributes:
            setattr(self, attr, results.get(attr))

    def __str__(self):
        return json.dumps(self.to_dict(), indent=2, sort_keys=True)

    def to_dict(self):
        result_dict = {
            'check': self.check,
            'success' : self.success
        }

        for attr in self.__optional_attributes:
            if getattr(self, attr):
                result_dict[attr] = getattr(self, attr)

        return result_dict

    def to_json_dict(self):
        return self.to_dict()

    def is_exception_thrown(self):

        try:
            if not self.success and self.onFail['Action'].lower() == 'fail':
                return True
        except KeyError:
            pass

        return False

class CollectionResult:

    def __init__(self, results):

        # Set Collection attributes from results
        # Required - will throw exception if not present
        required_args = ['checks']
        for k in required_args:
            if k not in results:
                raise Exception(f'Required arg not present: {k}')

        # Extract recognised attributes
        # Set required attributes
        self.checks = self.__build_checks(results['checks'])

        # Set optional attributes
        self.__optional_attributes = [
            'success',
            'name',
            'start',
            'tool',
            'toolVersion',
            'referenceUrl',
            'tags',
            'dataSet',
            'metadata'
            ]

        for attr in self.__optional_attributes:
            setattr(self, attr, results.get(attr))

    def __str__(self):
        return json.dumps(self.to_dict(), indent=2, sort_keys=True)

    def __build_checks(self, checks):

        checks_objs = []

        for check_results in checks:
            checks_objs.append(CheckResult(check_results))

        return checks_objs        

    def to_dict(self):
        result_dict = {
            'checks': [check.to_dict() for check in self.checks]
        }

        for attr in self.__optional_attributes:
            # Only include in dict if not None
            if getattr(self, attr):
                result_dict[attr] = getattr(self, attr)

        return result_dict

    def to_json_dict(self):
        return self.to_dict()

    def is_exception_thrown(self, error_on_fail=True):
        """
        Checks the success of each check. Returns True if any checks fail and have 'Action': 'fail'
        in the onFail field. Always returns False if error_on_fail is False.
        """
        if error_on_fail:
            failed_checks = [check.is_exception_thrown() for check in self.checks]

            if True in failed_checks:
                return True

        return False